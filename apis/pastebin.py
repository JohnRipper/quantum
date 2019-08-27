import requests

_url = "https://pastebin.com/api/api_post.php"

NEVER = "N"
TEN_MIN = "10M"
ONE_HOUR = "1H"
ONE_DAY = "1D"
ONE_WEEK = "1W"
TWO_WEEKS = "2W"
ONE_MONTH = "1M"
SIX_MONTHS = "6M"
ONE_YEAR = "1Y"


def paste(key: str, data, title: str, expires: str = ONE_HOUR, private: bool = True):
    data = {
        "api_dev_key": key,
        "api_option": "paste",
        "api_paste_code": data,
        # optionals
        "api_paste_format": "logtalk",
        "api_paste_name": title,
        "api_paste_private": private,
        "api_paste_expire_date": expires
    }
    r = requests.post(url=_url, data=data)
    return r.text
