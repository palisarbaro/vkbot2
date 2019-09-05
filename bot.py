import vk
import connect
import datetime
import time
import json
import re

class Handler:
    def __init__(self):
        self.actions = []

    def add_action(self,reg_exp, func):
        self.actions.append((reg_exp,func))

    def handle(self, user_id, msg):
        db = connect.DB()
        msg = msg.lower()
        print(user_id, msg)
        for reg_exp,func in self.actions:
            match = re.fullmatch(reg_exp,msg)
            if match:
                print(user_id,msg,reg_exp)
                db.push_action(user_id,func(msg))
                break
        else:
            db.push_action(user_id, "help")


handler = Handler()
handler.add_action(r"get link[1234]",lambda x:x)
handler.add_action(r"get week",lambda x:"get week")
handler.add_action(r"get keyboard",lambda x:"get keyboard")

server = vk.get_long_poll_server()
while True:
    time.sleep(1)
    try:
        events = vk.get_new_messages(server)
    except (json.JSONDecodeError, KeyError):
        server = vk.get_long_poll_server()
        continue

    last_messages = events['updates']
    for msg_obj in last_messages:
        user_id = msg_obj['object']['user_id']
        handler.handle(user_id, msg_obj['object']['body'])