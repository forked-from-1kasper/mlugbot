#! /usr/bin/env python3
import requests
from sys import argv, exit
from time import sleep
from constants import *
from prepare_arguments import get_argument, get_bool_argument

req_url = dest + ("/chat/%s/poll" % room)
usage = 'Usage: readmessages.py --uuid [uuid] --token [token] --sessionid [sessionid] [--get-last-uuid]'


def get_last_messages(uuid, token, sessionid):
    if not uuid:
        uuid = ''

    jar = requests.cookies.RequestsCookieJar()

    if token:
        jar.set("csrftoken", token, domain="beta.mlug.ru", path="/")
    if sessionid:
        jar.set("sessionid", sessionid, domain="beta.mlug.ru", path="/")

    r = requests.get(req_url + ('?uuid=%s' % (uuid)), cookies=jar)

    if r.status_code == 200:
        data = r.json()
    else:
        # TODO: replace IndexError
        raise IndexError("Bad status code: %i" % r.status_code)

    return data


def get_last_uuid(token, sessionid):
    posts = get_last_messages('', token, sessionid)
    try:
        last = posts['messages'][-1]
        return last[0]
    except IndexError:
        return False

if __name__ == "__main__":
    uuid = get_argument(argv, '--uuid')
    token = get_argument(argv, '--token')
    sessionid = get_argument(argv, '--sessionid')
    if get_bool_argument(argv, '--help'):
        print(usage)
        exit(1)
    elif get_bool_argument(argv,  '--get-last-uuid') or not token:
        print(get_last_uuid(token, sessionid))
    else:
        print(get_last_messages(uuid, token, sessionid))
