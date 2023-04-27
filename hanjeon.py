import time
import os
import pandas as pd
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


load_dotenv()
HANJEON_ID = os.getenv("HANJEON_ID")
HANJEON_PW = os.getenv("HANJEON_PW")

user_lst_path = os.path.abspath(os.path.join(os.getcwd(), "cust_lst.txt"))
f = open(user_lst_path, "r", encoding="utf-8")
lines = f.readlines()
user_lst = [line.strip() for line in lines]


browser = webdriver.Chrome()
browser.get(
    "https://cyber.kepco.co.kr/ckepco/front/jsp/ME/C/A/MECALP001_elec.jsp?login_type=1"
)


# def wait_and_clear(driver, element, timeout=5, n=0):
#     """wait for the element and clear the content"""
#     try:
#         WebDriverWait(driver, timeout).until(
#             EC.presence_of_element_located((By.XPATH, element))
#         )
#     except:
#         wait_and_clear(driver, element, timeout)
#     finally:
#         n += 1
#         print(f"{n}번 시도")


# 로그인
login_id = browser.find_element(By.XPATH, '//*[@id="id_A"]')
password = browser.find_element(By.XPATH, '//*[@id="pw_A"]')

login_id.send_keys(HANJEON_ID)
password.send_keys(HANJEON_PW)

login_button = browser.find_element(
    By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/form/div/div/div/div[4]/a/span'
)
login_button.click()

try:
    WebDriverWait(browser, 3).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    # 취소하기(닫기)
    alert.dismiss()
    # 확인하기
    # alert.accept()
except Exception:
    print("no alert")

time.sleep(1)
browser.get("https://cyber.kepco.co.kr/ckepco/front/jsp/CY/E/A/CYEAPP008_esb1.jsp")


total = {}
for cust in user_lst:
    WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchCustNo"]/dd/input'))
    )
    select = Select(browser.find_element(By.XPATH, '//*[@id="sch"]'))
    select.select_by_visible_text("고객번호")

    cust_id = browser.find_element(By.XPATH, '//*[@id="searchCustNo"]/dd/input')
    cust_id.send_keys(cust)
    search_button = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[3]/form/fieldset/div[2]/a'
    )
    search_button.click()
    time.sleep(1)
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "td_cont"))
    )
    cust = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[2]/div'
    ).text
    bill_date = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[3]/div'
    ).text
    kwh = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[4]/div'
    ).text
    price = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[6]/div'
    ).text

    total[cust] = [bill_date, kwh, price]
    browser.find_element(By.XPATH, '//*[@id="searchCustNo"]/dd/input').clear()

time.sleep(1)
df = pd.DataFrame.from_dict(total, orient="index", columns=["날짜", "kwh", "청구요금"])
df.to_csv("result.csv")
print(df)
