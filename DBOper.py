#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sqlite3
from player import Player, PLAYER_LIST
from Message import Message

conn = sqlite3.connect('playerInfo', check_same_thread=False)
c = conn.cursor()


def init():
    cursor = c.execute("SELECT * from playerInfo")
    for row in cursor:
        player_obj = Player(short_steamID=row[0],
                            long_steamID=row[1],
                            nickname=row[2],
                            last_DOTA2_match_ID=row[4])
        player_obj.DOTA2_score = row[4]
        PLAYER_LIST.append(player_obj)


def update_DOTA2_match_ID(short_steamID, last_DOTA2_match_ID):
    c.execute("UPDATE playerInfo SET last_DOTA2_match_ID='{}' "
              "WHERE short_steamID={}".format(last_DOTA2_match_ID, short_steamID))
    conn.commit()


def insert_info(short_steamID, long_steamID, nickname, last_DOTA2_match_ID):
    c.execute("INSERT INTO playerInfo (short_steamID, long_steamID, nickname, last_DOTA2_match_ID) "
              "VALUES ({}, {}, '{}', '{}')"
              .format(short_steamID, long_steamID, nickname, last_DOTA2_match_ID))
    conn.commit()


def get_player_by_short_id(short_steam_id: int) -> Player:
    c.execute("SELECT * FROM playerInfo WHERE short_steamID=={}".format(short_steam_id))
    row = c.fetchone()
    if row is None:
        return None
    return Player(short_steamID=row[0],
                  long_steamID=row[1],
                  nickname=row[2],
                  last_DOTA2_match_ID=row[4])


def get_playing_game(short_steamID):
    ret = c.execute(
        "SELECT gamename, last_update FROM playerInfo WHERE short_steamID=?",
        (short_steamID,)
    ).fetchone()
    return (ret[0], ret[1]) if ret else ('', 0)


def update_playing_game(short_steamID, gamename, timestamp):
    c.execute(
        "UPDATE playerInfo SET gamename=?, last_update=? WHERE short_steamID=?",
        (gamename, timestamp, short_steamID)
    )
    conn.commit()


def insert_message(message):
    c.execute('insert into message (message, send_succeed) values ({},0)'.format(message))
    conn.commit()


def get_no_succeed_one() -> Message:
    ret = c.execute('select * from message where send_succeed = 0 limit 1').fetchone()
    if ret is None:
        return None
    return Message(ret[0], ret[1], bool(ret[2]))


def send_success(id: int):
    c.execute('update message set send_succeed = 1 where id = {}'.format(id))
    conn.commit()


if __name__ == '__main__':
    send_success(1)
