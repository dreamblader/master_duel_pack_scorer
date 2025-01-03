import re
import datetime


def getDate(date_str:str):
    return datetime.datetime.strptime(date_str, "Released on %B %dth, %Y").date()


def clean_characters(s:str) -> str:
    conversion_list = [("“|”", "\""), ("–", "-")]
    for convert in conversion_list:
        s = re.sub(convert[0], convert[1], s)
    return s