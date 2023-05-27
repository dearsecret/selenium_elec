import os
from dotenv import load_dotenv
from scrapper.scrapper import billing_info
from scrapper.spread import call_cust, call_spread, append_spread

load_dotenv()
HANJEON_ID = os.getenv("HANJEON_ID")
HANJEON_PW = os.getenv("HANJEON_PW")


# google functions 사용시 하단으로 변경
# def main(request)
def main():
    user_lst = call_cust()
    db = call_spread().iloc[[-1], :]
    df = billing_info(HANJEON_ID, HANJEON_PW, user_lst)
    if db.index != df.index:
        append_spread(df.reset_index().values.tolist()[0])


if __name__ == "__main__":
    main()
