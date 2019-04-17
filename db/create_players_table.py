#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 as sqlite

con = sqlite.connect('chess.db')

players = (
    (1, "Clem Aeppli", "", 1, 0),
    (2, "Sarah Betancourt", "", 2, 0),
    (3, "Will Brown", "", 5, 0),
    (4, "Evan Bruning", "", 2, 0),
    (5, "Jay Cincotti", "", 2, 0),
    (6, "Tracy Corley", "", 2, 0),
    (7, "Stefanie Coxe", "", 3, 0),
    (8, "Brendan Crighton", "", 3, 1),
    (9, "Josh Cutler", "", 2, 1),
    (10, "Rachel Dec", "", 4, 0),
    (11, "Mike Deehan", "", 2, 0),
    (12, "Joe Deering", "", 4, 0),
    (13, "Gintautas Dumcius", "", 2, 0),
    (14, "Preston Epps", "", 5, 0),
    (15, "Matt Giancola", "", 4, 0),
    (16, "Libby Gormley", "", 1, 0),
    (17, "Joe Gravellese", "", 3, 0),
    (18, "Christian Greve", "", 4, 0),
    (19, "Brian Jencunas", "", 3, 0),
    (20, "Maya Jonas-Silver", "", 5, 0),
    (21, "Steve Koczela", "", 5, 0),
    (22, "Ed Lyons", "", 5, 0),
    (23, "Juana Matias", "", 3, 0),
    (24, "Andy Metzger", "", 5, 0),
    (25, "Mike Morales", "", 4, 0),
    (26, "Ashira Morris", "", 3, 0),
    (27, "Stephanie Murray", "", 1, 0),
    (28, "Ben Muschol", "", 5, 0),
    (29, "Christine Prignano", "", 3, 0),
    (30, "Will Rasky", "", 3, 0),
    (31, "Becca Rausch", "", 3, 1),
    (32, "Jodi Reed", "", 1, 0),
    (33, "Hirak Shah", "", 4, 0),
    (34, "Aaron Van Leesten", "", 2, 0),
    (35, "Pete Wilson", "", 3, 0),
    (36, "Brad Wyatt", "", 5, 0),
    (37, "Neil Placeholder", "", 1, 0),
    (38, "Fred Phantom", "", 5, 0),
    (39, "Mark Wraith", "", 3, 0)
)

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS players")
    cur.execute("CREATE TABLE players(id INT, name TEXT, affiliation TEXT, level INT, vip INT)")

    cur.executemany("INSERT INTO players VALUES(?, ?, ?, ?, ?)", players)
