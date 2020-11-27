#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import requests
import config
import threading
import time
from DBOper import get_no_succeed_one, send_success
import Message

url = config.MIRAI_URL
# 群号
target = config.QQ_GROUP_ID
# bot的QQ号
bot_qq = config.BOT_QQ
# mirai http的auth key
authKey = config.MIRAI_AUTH_KEY
fragment_message = config.FRAGMENT_MESSAGE


def message(m: str):
    # Authorize
    auth_key = {"authKey": authKey}
    r = requests.post(url + "/auth", json.dumps(auth_key))
    if json.loads(r.text).get('code') != 0:
        print("ERROR@auth")
        print(r.text)
        exit(1)
    # Verify
    session_key = json.loads(r.text).get('session')
    session = {"sessionKey": session_key, "qq": bot_qq}
    r = requests.post(url + "/verify", json.dumps(session))
    if json.loads(r.text).get('code') != 0:
        print("ERROR@verify")
        print(r.text)
        exit(2)
    data = {
        "sessionKey": session_key,
        "target": target,
        "messageChain": [
            {"type": "Plain", "text": m}
        ]
    }
    send_result = requests.post(url + "/sendGroupMessage", json.dumps(data))
    send_result.json()
    # release
    data = {
        "sessionKey": session_key,
        "qq": bot_qq
    }
    r = requests.post(url + "/release", json.dumps(data))
    # print(r.text)
    return send_result


def send_message():
    while True:
        msg = get_no_succeed_one()
        if msg is None:
            time.sleep(60)
            continue

        if fragment_message:
            succeed = send_fragment(msg.message)
        else:
            succeed = do_send(msg.message)

        if succeed:
            send_success(msg.id)
        else:
            send_error(msg)


def do_send(msg) -> bool:
    try:
        ret = message(msg)
        if ret is None:
            return False
    except BaseException:
        return False
    json_ret = ret.json()
    return json_ret['code'] == 0 and json_ret['msg'] == 'success'


def send_fragment(msg) -> bool:
    # 按行发送
    lines = msg.split('\n')
    for line in lines:
        succeed = do_send(line)
        if not succeed:
            return False
    return True


def send_error(msg: Message):
    print('消息发送失败，消息id： %d' % msg.id)
    time.sleep(60)


def start_send():
    t1 = threading.Thread(target=send_message)
    t1.start()
