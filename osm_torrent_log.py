#!/usr/bin/python3
# started Matija Nalis <mnalis-git@voyager.hr> GPLv3+ 2020-12-11
# logs OpenStreetMap bittorrent statistics to sqlite3 DB

from scraper import scrape
import time
import apsw

DBFILE='osm-torrent-stats.sqlite'

print ('OSM bittorrent scrape test')

connection=apsw.Connection(DBFILE)
sql=connection.cursor()

sql.execute ('PRAGMA foreign_keys = ON')

sql.execute("""
  CREATE TABLE IF NOT EXISTS trackers (
    id integer PRIMARY KEY AUTOINCREMENT,
    announce_url varchar(255),
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (announce_url) )
""")

sql.execute('INSERT OR IGNORE INTO trackers (announce_url) VALUES (?)', ('udp://tracker.opentrackr.org:1337/announce',))
sql.execute('INSERT OR IGNORE INTO trackers (announce_url) VALUES (?)', ('udp://tracker-udp.gbitt.info:80/announce',))
sql.execute('INSERT OR IGNORE INTO trackers (announce_url) VALUES (?)', ('udp://tracker.torrent.eu.org:451',))

sql.execute(""" 
  CREATE TABLE IF NOT EXISTS torrent_stats (
    tracker_id integer NOT NULL,
    hash char(40) NOT NULL,
    timestamp int NOT NULL,
    peers int,
    seeds int,
    complete int,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hash, timestamp, tracker_id),
    FOREIGN KEY (tracker_id) REFERENCES trackers (id) )
""")

hashes = (
        'D84256FCBF807BA6B1257798176DF4CEB3056504',
        '049C08A4934C8A2EACE7E92A1F3F01F35B045660'
) 

_now = int(time.time())


# ex.scrape: {'D84256FCBF807BA6B1257798176DF4CEB3056504': {'peers': 25, 'seeds': 4, 'complete': 9}, '049C08A4934C8A2EACE7E92A1F3F01F35B045660': {'peers': 2, 'seeds': 13, 'complete': 31}}

def do_tracker (tracker_id, announce_url):
    print ('tracker:', announce_url)
    scr = scrape (announce_url, hashes)
    #print (' scrape:', scr,"\n")
    for hash in scr:
        stats = scr[hash]
        print ('  hash=',hash, ' --- stats=',stats)
        sql.execute ('INSERT INTO torrent_stats (tracker_id, hash, timestamp, peers, seeds, complete) VALUES (?, ?, ?, ?, ?, ?)', (tracker_id, hash, _now, stats['peers'], stats['seeds'], stats['complete']))
    
def do_all_trackers():
    tr_sql = connection.cursor()
    for tracker_id, announce_url in tr_sql.execute ('SELECT id, announce_url FROM trackers'):
        do_tracker (tracker_id, announce_url)
    

print ('IPv4/mixed:')
do_all_trackers()

# FIXME - IPv6 does not work! check not only connceting, but different datasctructure, and share back via PR. Also fix to be python3 compatible
#print ('IPv6 only:')
#b = do_tracker ('udp://tracker.datacenterlight.ch:6969/announce')
