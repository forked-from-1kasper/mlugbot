#! /usr/bin/env python3
import requests
from sys import argv, exit
from constants import *
from prepare_arguments import get_argument

place = "/id/login"

def login(name, password, token="False"):
    headers = {"Conetent-type": "application/x-www-form-urlencoded", \
               "Accept": "text/plain", \
               "Referer": "https://beta.mlug.ru"}

    data = {"csrfmiddlewaretoken": token, \
            "username": name, \
            "password": password}

    jar = requests.cookies.RequestsCookieJar()
    jar.set("csrftoken", token, domain="beta.mlug.ru", path="/")

    r = requests.post(dest + place, data=data, headers=headers, cookies=jar, allow_redirects=False)
    return dict(r.cookies)["sessionid"]

if __name__ == "__main__":
    name = get_argument(argv, '--username')
    password = get_argument(argv, '--password')
    if (not name) or (not password) or get_bool_argument(argv, '--help'):
        print('Usage: login --username [username] --password [password]')
        exit(1)

    id = login(name, password)

    print(id)

