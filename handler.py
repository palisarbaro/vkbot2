import connect
import vk
import datetime
import time
import re
from math import floor

def get_week():
    first_monday = datetime.date(2019,9,2)
    today = datetime.date.today()
    weeks_delta = (today - first_monday).days//7
    return weeks_delta%2==1


class Handler:
    def __init__(self):
        self.actions = {}

    def add_action(self,action, func):
        self.actions[action] = func

    def handle(self, user_id, action):
        db = connect.DB()
        for s_action in self.actions:
            if re.fullmatch(s_action,action):
                self.actions[s_action](user_id,action)


def action_help(user_id,real_msg):
    vk.send_hello(user_id)

def action_get_link(user_id,real_msg):
    n = real_msg[8]
    vk.send_to_one(user_id, db.get_link_and_date_str(n))

def action_get_week(user_id,real_msg):
    week = "верхняя" if get_week() else "нижняя"
    vk.send_to_one(user_id, week)

print(get_week())
exit(1)

handler = Handler()
handler.add_action(r"help",action_help)
handler.add_action(r"get week", action_get_week)
handler.add_action(r"get link[1234]", action_get_link)

while True:
    time.sleep(0.1)
    db = connect.DB()
    user_id,action = db.pop_action()
    if user_id and action:
        print(user_id,action)
        handler.handle(user_id,action)