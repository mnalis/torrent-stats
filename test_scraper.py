#!/usr/bin/python2

from scraper import scrape
print "hello world"

hashes=(
        'D84256FCBF807BA6B1257798176DF4CEB3056504',
        '049C08A4934C8A2EACE7E92A1F3F01F35B045660'
); 
a=scrape ('udp://tracker.opentrackr.org:1337/announce', hashes)
print "ipv4:", a
b=scrape
b=scrape ('udp://tracker.datacenterlight.ch:6969/announce', hashes)
print "ipv6:", b