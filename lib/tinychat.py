import re

import requests

SESS = requests.session()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}
SESS.headers.update(HEADERS)


def getcsrf() -> str:
    g = SESS.get(url="https://tinychat.com/start?#signin")
    if g.status_code != 200:
        return None
    match = re.search("(?:csrf-token\" content=\")(\w+)", g.text)
    csrf = match[1]
    return csrf


def login(username: str, password: str, csrf: str):
    """POST to tinychat.com/login
    return None or str on error
    """
    formdata = {
        "login_username": username,
        "login_password": password,
        "remember": "1",
        "next": "https://tinychat.com/",
        "_token": csrf
    }
    a = SESS.post(url="https://tinychat.com/login", data=formdata, allow_redirects=True)
    if a.status_code == 200:
        if re.search("The password you specified is incorrect", a.text):
            return "Password is incorrect"
        elif re.search("That username is not registered", a.text):
            return "Username is incorrect"
        else:
            return None
    else:
        return "Error during login, got {} expected 200".format(a.status_code)


def rtcversion(room: str) -> str:
    req = SESS.get(url=f"https://tinychat.com/room/{room}")
    if req.status_code == 200:
        match = re.search("webrtc\/([0-9.-]+)\/", req.text)
        rtcversion = match[1]
        return rtcversion
    else:
        return None

# TODO -> typing.Dict
def token(room: str):
    req = SESS.get(url=f"https://tinychat.com/api/v1.0/room/token/{room}")
    if req.status_code == 200:
        return req.json()
    else:
        return None


class TokenException(Exception):
    pass


class RTCVersionException(Exception):
    pass


def payload(settings, req):
    t = token(settings.get("roomname", None))
    if t is None:
        raise TokenException

    version = rtcversion(settings.get("roomname", None))
    if rtcversion is None:
        raise RTCVersionException

    result = {
        "tc": "join",
        "req": req,
        "useragent": f"tinychat-client-webrtc-chrome_linux x86_64-{version}",
        "token": t.get("result", ""),
        "room": settings.get("roomname", "trash"),  # redirects idiots to tech.
        "nick": settings.get("nickname", "omega_reeeeeeee")}
    return result, t
