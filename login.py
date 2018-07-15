#! /usr/bin/env python3
import requests
from sys import argv, exit
from uuid import uuid1
import mlugbot.constants as constants
from mlugbot.prepare_arguments import get_argument, get_bool_argument

place = "/id/login"


def login(name, password, token):
    headers = {"Conetent-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain",
               "Referer": "https://beta.mlug.ru"}

    data = {"csrfmiddlewaretoken": token,
            "username": name,
            "password": password}

    jar = requests.cookies.RequestsCookieJar()
    jar.set("csrftoken", token, domain=constants.domain, path="/")

    r = requests.post(constants.dest + place,
                      data=data,
                      headers=headers,
                      cookies=jar,
                      allow_redirects=False)
    return dict(r.cookies)["sessionid"]

if __name__ == "__main__":
    name = get_argument('--username')
    password = get_argument('--password')
    if (name is None) or (password is None) or get_bool_argument('--help'):
        print('Usage: login --username [username] --password [password]')
        exit(1)

    print(login(name, password, "AnalGay"))
