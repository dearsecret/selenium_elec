import time
import os
import pandas as pd
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from spread import call_cust, call_spread, append_spread

load_dotenv()
HANJEON_ID = os.getenv("HANJEON_ID")
HANJEON_PW = os.getenv("HANJEON_PW")

# user_lst_path = os.path.abspath(os.path.join(os.getcwd(), "cust_lst.txt"))
# f = open(user_lst_path, "r", encoding="utf-8")
# lines = f.readlines()
# user_lst = [line.strip() for line in lines]

user_lst = call_cust()
db = call_spread().iloc[[-1], :]
# print(db)

browser = webdriver.Chrome()
browser.get(
    "https://cyber.kepco.co.kr/ckepco/front/jsp/ME/C/A/MECALP001_elec.jsp?login_type=1"
)


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


df = pd.DataFrame()
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
    cust = "".join(cust.split("-"))
    bill_date = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[3]/div'
    ).text
    kwh = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[4]/div'
    ).text
    price = browser.find_element(
        By.XPATH, '//*[@id="content"]/div[4]/div[1]/table/tbody/tr/td[6]/div'
    ).text
    df.loc[bill_date, cust] = price
    browser.find_element(By.XPATH, '//*[@id="searchCustNo"]/dd/input').clear()

time.sleep(1)


# print(pd.concat([db, df]))
if db.index != df.index:
    append_spread(df.reset_index().values.tolist()[0])
