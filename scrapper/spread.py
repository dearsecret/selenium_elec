import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def call_spread():
    """건물 총합 스프레드 불러오기"""

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    json_file_name = "gspread-384908-7f214dba2b69.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file_name, scope
    )
    gc = gspread.authorize(credentials)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1cFqs8KcvMDMd17kcqqNZqzmNpvGK4P5o6yT7QmhLr7U/edit#gid=0x"

    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet("건물 총합")
    db = pd.DataFrame(
        worksheet.get_all_values()[2:],
        columns=worksheet.get_all_values()[1],
        index=worksheet.col_values(1)[2:],
    ).iloc[:, 1:]
    return db


def call_cust():
    """고객번호 목록 불러오기"""
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    json_file_name = "gspread-384908-7f214dba2b69.json"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file_name, scope
    )
    gc = gspread.authorize(credentials)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1cFqs8KcvMDMd17kcqqNZqzmNpvGK4P5o6yT7QmhLr7U/edit#gid=1781087906"
    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet("고객번호")
    cust = worksheet.col_values(1)[1:]
    return cust


def append_spread(new_data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    json_file_name = "gspread-384908-7f214dba2b69.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file_name, scope
    )
    gc = gspread.authorize(credentials)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1cFqs8KcvMDMd17kcqqNZqzmNpvGK4P5o6yT7QmhLr7U/edit#gid=0x"

    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet("건물 총합")
    worksheet.append_row(new_data)
    return print("confirm your database")
