import requests
from apis.pastebin.constants import *
_url = "https://pastebin.com/api/api_post.php"


def create_log(key:      str,
               data:     str,
               title:    str,
               language: str = Format.LOGTALK,
               expires:  str = Expires.ONE_HOUR,
               private:  int = Privacy.PRIVATE):
    data = {
        "api_dev_key": key,
        "api_option": "paste",
        "api_paste_code": data,
        # optionals
        "api_paste_format": language,
        "api_paste_name": title,
        "api_paste_private": private,
        "api_paste_expire_date": expires
    }
    r = requests.post(url=_url, data=data)
    # url to the paste is returned
    return r.text
