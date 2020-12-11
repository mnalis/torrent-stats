#!/usr/bin/python2
# started Matija Nalis <mnalis-git@voyager.hr> GPLv3+ 2020-12-11

from scraper import scrape
print "OSM bittorrent scrape test"

hashes=(
        'D84256FCBF807BA6B1257798176DF4CEB3056504',
        '049C08A4934C8A2EACE7E92A1F3F01F35B045660'
); 

a1=scrape ('udp://tracker.opentrackr.org:1337/announce', hashes)
print "ipv4-1:", a1

a2=scrape ('udp://tracker-udp.gbitt.info:80/announce', hashes)
print "ipv4-2:", a2

a3=scrape ('udp://tracker.torrent.eu.org:451', hashes)
print "ipv4-3:", a3

# FIXME - IPv6 does not work! check not only connceting, but different datasctructure, and share back via PR. Also fix to be python3 compatibile
b=scrape ('udp://tracker.datacenterlight.ch:6969/announce', hashes)
print "ipv6:", b