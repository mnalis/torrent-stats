#!/usr/bin/python2
# started Matija Nalis <mnalis-git@voyager.hr> GPLv3+ 2020-12-11

from old_scraper import scrape
print ("OSM bittorrent scrape test")

hashes=(
        'D84256FCBF807BA6B1257798176DF4CEB3056504',
        '049C08A4934C8A2EACE7E92A1F3F01F35B045660'
); 

# ex.scrape: {'D84256FCBF807BA6B1257798176DF4CEB3056504': {'peers': 25, 'seeds': 4, 'complete': 9}, '049C08A4934C8A2EACE7E92A1F3F01F35B045660': {'peers': 2, 'seeds': 13, 'complete': 31}}

def do_tracker (tracker):
    print "tracker:", tracker
    scr = scrape (tracker, hashes)
    print " scrape:", scr,"\n"

print ("IPv4/mixed UDP:")
#a1=do_tracker ('udp://tracker.opentrackr.org:1337/announce')
#a2=do_tracker ('udp://tracker-udp.gbitt.info:80/announce')
#a3=do_tracker ('udp://tracker.torrent.eu.org:451')

print ("IPv4/mixed TCP:");
a3=do_tracker('http://tracker.gbitt.info/announce');
#a4=do_tracker('https://tracker.gbitt.info/announce');

# FIXME - IPv6 does not work! check not only connceting, but different datasctructure, and share back via PR. Also fix to be python3 compatible
#print ("IPv6 only:")
#b=do_tracker ('udp://tracker.datacenterlight.ch:6969/announce')
