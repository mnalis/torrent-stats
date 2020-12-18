#!/usr/bin/python3

import libtorrent as lt
from sys import argv

for filename in argv[1:]:
  info = lt.torrent_info(filename)
  print (info.info_hash())
