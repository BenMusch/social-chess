#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as sqlite

con = sqlite.connect('chess.db')

players = (
    (1,  'John Smith', 'Statehouse News', 3, 0),
    (2,  'Michael Newsome', 'State Senator', 2, 1),
    (3,  'Charlie Baker', 'Governor', 1, 1),
    (4,  'Terry McFeeney', 'Boston Globe', 2, 0),
    (5,  'Winnie McStooge', 'Activist', 1, 0),
    (6,  'Toady Longfellow', 'Boston Magazine', 1, 0),
    (7,  'Marcus More', 'SJC Judge', 3, 1),
    (8,  'Vernon Smithereens', 'WGBH', 1, 0),
    (9,  'Jodi Reinhardt', 'MassINC', 1, 0),
    (10, 'Maxine Vilamont', 'Activist', 1, 0),
    (11, 'Keefe Ochabi', 'Dorchester Reporter', 2, 0),
    (12, 'Tsunami Tanaka', 'Pretty Good Polling', 2, 0),
    (13, 'Radar O\'Relly', 'Boston Phoenix', 2, 0),
    (14, 'Manfred Jackson', 'WBUR', 2, 0),
)

with con:

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS players")
    cur.execute("CREATE TABLE players(id INT, name TEXT, affiliation TEXT, level INT, vip INT)")

    cur.executemany("INSERT INTO players VALUES(?, ?, ?, ?, ?)", players)
