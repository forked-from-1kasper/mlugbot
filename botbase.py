#! /usr/bin/env python3
import mlugbot.say as say
import mlugbot.readmessages as readmessages
from mlugbot.readmessages import Message

from dataclasses import dataclass
from time import sleep
from html.parser import HTMLParser
from typing import Optional, List, Callable
from uuid import UUID

SLEEP_TIME = 2


@dataclass
class Bot:
    sessionid: str
    token: str
    uuid: Optional[UUID]
    functions: List[Callable[[Message], List[str]]]
    read_from_anon: bool

    def __post_init__(self):
        if self.uuid is None:
            if self.read_from_anon:
                self.last_uuid = readmessages.get_last_uuid(None, None)
            else:
                self.last_uuid = \
                    readmessages.get_last_uuid(self.token, self.sessionid)

        self.ignore = []
        self.HTMLParser = HTMLParser()

    def run(self):
        current_uuid = self.last_uuid

        while True:
            print("[read thread] try to grab messages")
            if self.read_from_anon:
                posts = readmessages.get_last_messages(current_uuid,
                                                       None, None)
            else:
                posts = readmessages.get_last_messages(current_uuid,
                                                       self.token,
                                                       self.sessionid)
            print("[read thread] done")

            if len(posts) > 0:
                current_uuid = posts[-1].uuid

            for msg in posts:
                unescaped = self.HTMLParser.unescape(msg.text)
                if unescaped in self.ignore:
                    self.ignore.remove(unescaped)
                    print("[write thread] skipped")
                    continue
                for func in self.functions:
                    buff = func(msg)
                    for text in buff:
                        say.send_message(text, self.token,
                                         sessionid=self.sessionid)
                        self.ignore.append(text)

            print("[read thread] sleep")
            sleep(SLEEP_TIME)
            print("[read thread] done")
