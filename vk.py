import urllib.parse
import urllib.request
import top_secret
from math import ceil
import json
import keyboard

admin_id = 59544463
group_id = 152709221
send_url = "https://api.vk.com/method/messages.send"
token = top_secret.token
version = "5.0"
hello_msg = """get link3  - получить последнюю ссылку для 3 курса
get week - верхняя или нижняя неделя
get keyboard - получить кнопки
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

def get_keyboard():
    return keyboard.keyboard.replace("\n","")

def send_keyboard(user_id):
    url = send_url + create_url(user_id=user_id,message="...",keyboard=get_keyboard())
    resp = urllib.request.urlopen(url)

def send_to_admin(message):
    send_to_one(admin_id, message)


def send_to_admin2(message):
    send_to_one(108186884, message)

@debug
def send_to_many(user_ids, message):
    url = send_url + create_url(user_ids=join_part(user_ids),message=message)
    resp = urllib.request.urlopen(url)
    js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
    if "error" in js:
        n = len(user_ids)
        print(user_ids)
        if n == 0 or n == 1:
            return
        u_ids1 = user_ids[0:n//2]
        u_ids2 = user_ids[n//2:]
        send_to_many(u_ids1,message)
        send_to_many(u_ids2,message)



def send_to_all(message):
    users = get_actual_users()
    parts = split_users_by_N(users,99)
    for hundredPart in parts:
        send_to_many(hundredPart, message)


def join_part(part):
    return ",".join(str(i) for i in part)


def split_users_by_N(users,N):
    result = []
    count_of_parts = ceil(len(users) / N)
    for i in range(count_of_parts):
        part = users[i * N:(i + 1) * N]
        result.append(part)
    return result

def get_last_msg(user_id):
    url = 'https://api.vk.com/method/messages.getHistory' + create_url(user_id=user_id,count=1)
    resp = urllib.request.urlopen(url)
    js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
    msg_obj = js['response']['items'][0]
    return msg_obj

def get_id_by_msg(msg):
    return msg["from_id"] if msg["out"]==0 else msg["peer_id"]

def get_actual_users():
    count = 10**10
    offset = 0
    dof = 150 # по сколько сообщений за раз. максимум 200(но лучше 199)
    actual_users = []
    while offset<count:
        url = 'https://api.vk.com/method/messages.getConversations' + create_url(offset=offset,count=dof)
        resp = urllib.request.urlopen(url)
        js = json.loads(resp.fp.read(resp.length).decode("utf-8"))
        #print(js["response"]["items"])
        count = js["response"]["count"]
        items = js['response']['items']
        for item in items:
            item = item["conversation"]
            try:
                if item["can_write"]["allowed"]:
                    actual_users.append(item["peer"]["id"])
            except KeyError as e:
                print(item,"has no ",e)
        offset+=dof
    return actual_users


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
    print(get_keyboard())
#send_to_all("Бот пока не работает. Скорее всего заработает через пару дней. Не надо писать мне в личку.")