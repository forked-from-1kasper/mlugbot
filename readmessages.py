#! /usr/bin/env python3
import requests
import datetime
from uuid import UUID
from dataclasses import dataclass
from typing import List, Optional
from sys import argv, exit
from time import sleep

import mlugbot.constants as constants
from prepare_arguments import get_argument, get_bool_argument

req_url = constants.dest + ("/chat/%s/poll" % constants.room)
usage = 'Usage: readmessages.py --uuid [uuid] --token [token] --sessionid [sessionid] [--get-last-uuid]'


@dataclass
class Message:
    uuid: UUID
    time: datetime.time
    name: str
    text: str


def get_last_messages(uuid: Optional[UUID], token: Optional[str], sessionid: Optional[str]) -> List[Message]:
    def json_to_message(json) -> Message:
        uuid_str, time_str, name, text = json

        # 00:00:00 time format
        hour_str, minute_str, second_str = time_str.split(":")
        time = datetime.time(hour=int(hour_str),
                             minute=int(minute_str),
                             second=int(second_str))

        return Message(UUID(uuid_str), time, name, text)

    #if uuid is None:
    #    uuid_str = ''
    #else:
    #    uuid_str = str(uuid)
    uuid_str = constants.option_default(constants.option_map(uuid, str), '')

    jar = requests.cookies.RequestsCookieJar()

    if token is not None:
        jar.set("csrftoken", token, domain=constants.domain, path="/")
    if sessionid is not None:
        jar.set("sessionid", sessionid, domain=constants.domain, path="/")

    r = requests.get(req_url + ('?uuid=%s' % uuid_str), cookies=jar)

    if r.status_code == 200:
        data = r.json()
    else:
        # TODO: replace IndexError
        raise IndexError("Bad status code: %i" % r.status_code)

    return [json_to_message(s) for s in data['messages']]


def get_last_uuid(token, sessionid) -> Optional[UUID]:
    posts = get_last_messages(None, token, sessionid)
    try:
        last = posts[-1]
        return last.uuid
    except IndexError:
        return None

if __name__ == "__main__":
    uuid = get_argument('--uuid')
    token = get_argument('--token')
    sessionid = get_argument('--sessionid')
    if get_bool_argument('--help'):
        print(usage)
        exit(1)
    elif get_bool_argument('--get-last-uuid') or not token:
        print(get_last_uuid(token, sessionid))
    else:
        print(get_last_messages(UUID(uuid), token, sessionid))
