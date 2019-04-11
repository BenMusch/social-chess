#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as sqlite

con = sqlite.connect('chess.db')

with con:

    cur = con.cursor()

    cur.execute("CREATE TABLE players(id INT, name TEXT, level INT, vip INT)")

    # This will be dummy data
    cur.execute("INSERT INTO players VALUES(1,'John Smith',3,0)")

