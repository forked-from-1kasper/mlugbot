#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv, exit, stdin
from uuid import uuid1
import mlugbot.constants as constants
from mlugbot.prepare_arguments import get_bool_argument, get_argument
import requests

place = "/chat/%s/message" % constants.room


def send_message(msg, token, sessionid=False):
    data = {"csrfmiddlewaretoken": token,
            "message": msg}
    headers = {"Conetent-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain",
               "Referer": "https://beta.mlug.ru/chat/tsmr"}

    jar = requests.cookies.RequestsCookieJar()
    jar.set("csrftoken", token, domain=constants.domain, path="/")
    if sessionid:
        jar.set("sessionid", sessionid, domain=constants.domain, path="/")

    return requests.post(constants.dest + place,
                         data=data,
                         headers=headers,
                         cookies=jar,
                         allow_redirects=False)

usage = ('say --token [token] --sessionid (sessionid) '
         '[--without-uuid] [--print-request]')
if __name__ == "__main__":
    without_uuid = get_bool_argument('--without-uuid')
    print_request = get_bool_argument('--print-request')
    sessionid = get_argument('--sessionid')
    token = get_argument('--token')

    if (token is None) or get_bool_argument('--help'):
        print(usage)
        exit(1)

    message = stdin.read()

    if not without_uuid:
        msg = "%s :: %s" % (message, str(uuid1()))
    else:
        msg = message

    req = send_message(msg, token, sessionid=sessionid)
    if print_request:
        print(req.text)
