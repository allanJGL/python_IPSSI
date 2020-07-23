#!/usr/bin/env python3

from string import ascii_letters, digits
from itertools import chain
from random import choice
import sqlite3
import os


def create_uid(n=9):
    '''Génère une chaîne de caractères alétoires de longueur n
    en évitant 0, O, I, l pour être sympa.'''
    chrs = [c for c in chain(ascii_letters, digits)
            if c not in '0OIl']
    return ''.join((choice(chrs) for i in range(n)))


def save_info(uid=None, code=None, lang=None):
    '''
    Crée le document en base.
    Return the file name.
    '''

    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()

    if uid is None:
        uid = create_uid()
        code = '# Write your code here...'
        lang = ''
    curs.execute("INSERT INTO info(uid, code, lang) VALUES(?, ?, ?)", (uid, code, lang))
    conn.commit()
    return uid


def edit_info(uid=None, code=None, lang=None):
    '''
    Enregistre le document en base.
    Return the file name.
    '''

    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()
        if uid is None:
            uid = create_uid()
            code = '# Write your code here...'
            lang = ''
        curs.execute("UPDATE info SET code = ?, lang = ? WHERE uid = ?", (code, lang, uid))
        conn.commit()
        return uid


def read_code(uid):
    '''récupère le code en base'''

    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()
        curs.execute("SELECT code FROM info WHERE uid = ?", (uid,))
        code = curs.fetchone()
        return code[0]


def read_lang(uid):
    '''récupère le langage en base'''

    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()
        curs.execute("SELECT lang from info WHERE uid = ?", (uid,))
        lang = curs.fetchone()
        return lang[0]


def save_user_info(ip, user_agent, date, uid):
    '''
    Enregistre les infos sur la dernière modif en base
    '''
    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()
        curs.execute("INSERT INTO user_info(ip_adr, user_agent, date_modif, uid) VALUES(?, ?, ?, ?)",
                     (ip, user_agent, date, uid))


def get_last_modifs():
    '''
    Récupère les infos sur les dernières modifs
    '''
    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()
        curs.execute("SELECT ui.*, i.code from user_info ui INNER JOIN info i ON ui.uid = i.uid LIMIT 10")
        modifs = curs.fetchall()
        d = []
        for i, e in enumerate(modifs):
            print(e)
            if i >= 10:
                break
            d.append({'ip': e[1], 'user_agent': e[2], 'date': e[3], 'uid': e[4], 'code': e[5]})
        return d


def get_last_entries_from_files(n=10, nlines=10):
    with sqlite3.connect('sharecode.sqlite3') as conn:
        curs = conn.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS info (uid text not null primary key, code text, lang text)")
        curs.execute(
            "CREATE TABLE IF NOT EXISTS user_info (id integer not null primary key autoincrement, ip_adr text, user_agent text, date_modif datetime, uid text)")
        curs.execute("SELECT * from info")
        entries = curs.fetchall()
        d = []
        for i, e in enumerate(entries):
            if i >= n:
                break
            d.append({'uid': e[0], 'code': e[1], 'lang': e[2]})
        return d
