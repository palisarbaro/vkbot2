import urllib.parse
import urllib.request
import top_secret
from math import ceil
import json


admin_id = 59544463
group_id = 152709221
send_url = "https://api.vk.com/method/messages.send"
token = top_secret.token
version = "5.0"
hello_msg = """get link3  - получить последнюю ссылку для 3 курса
get week - верхняя или нижняя неделя
"""



def debug(f):
    def g(*args,**kwargs):
        print(args,kwargs)
    return g if top_secret.debug else f


def create_url(**param):
    param['access_token'] = token
    param['v'] = version
    url = "?" + urllib.parse.urlencode(param)
    return url

def send_to_one(user_id, message):
    url = send_url + create_url(user_id=user_id,message=message)
    resp = urllib.request.urlopen(url)


def send_hello(user_id):
    send_to_one(user_id, hello_msg)


def send_to_admin(message):
    send_to_one(admin_id, message)


def send_to_admin2(message):
    send_to_one(108186884, message)

@debug
def send_to_many(user_ids, message):
    url = send_url + create_url(user_ids=user_ids,message=message)
    resp = urllib.request.urlopen(url)


def send_to_all(message):
    parts = get_users_by_parts(99)
    for hundredPart in parts:
        send_to_many(hundredPart, message)


def join_part(part):
    return ",".join(part)


def get_users_by_parts(N):
    result = []
    users = get_users()
    count_of_parts = ceil(len(users) / N)
    for i in range(count_of_parts):
        part = users[i * N:(i + 1) * N]
        result.append(join_part(part))
    return result

def get_last_msg(user_id):
    url = 'https://api.vk.com/method/messages.getHistory' + create_url(user_id=user_id,count=1)
    resp = urllib.request.urlopen(url)
    js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
    msg_obj = js['response']['items'][0]
    return msg_obj

def get_id_by_msg(msg):
    return msg["from_id"] if msg["out"]==0 else msg["peer_id"]

def get_users():
    messages = get_last_messages()
    list_of_users = []
    for msg in messages:
        user_id = get_id_by_msg(msg)
        check_url = 'https://api.vk.com/method/messages.isMessagesFromGroupAllowed' + create_url(user_id=user_id, group_id=152709221)
        check_resp = urllib.request.urlopen(check_url)
        check_js = json.loads(check_resp.fp.read(check_resp.length).decode("utf-8"))
        is_allowed = check_js['response']['is_allowed']
        if is_allowed == 1:
            list_of_users.append(str(user_id))
    return list_of_users

def get_last_messages():
    count = 10**10
    offset = 0
    dof = 150 # по сколько сообщений за раз. максимум 200(но лучше 199)
    list_of_messages = []
    while offset<count:
        url = 'https://api.vk.com/method/messages.getConversations' + create_url(offset=offset,count=dof)
        resp = urllib.request.urlopen(url)
        js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
        count = js["response"]["count"]
        dialogs = js['response']['items']
        for i in dialogs:
            list_of_messages.append(i["last_message"])
        offset+=dof
    return list_of_messages


def get_long_poll_server():
    url = 'https://api.vk.com/method/groups.getLongPollServer' + create_url(lp_version=3,group_id=group_id)
    resp = urllib.request.urlopen(url)
    js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
    return js['response']

def get_new_messages(server):
    url = str(server['server']) + create_url(act='a_check',key=server['key'],ts=server['ts'],wait=25)
    resp = urllib.request.urlopen(url)
    js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
    server['ts'] = js['ts']
    return js

if __name__ == "__main__":
    send_to_all("Бот пока не работает. Скорее всего заработает через пару дней. Не надо писать мне в личку.")