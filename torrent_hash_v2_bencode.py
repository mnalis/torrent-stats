#!/usr/bin/python2

from sys import argv
from sha import sha
from BitTorrent.bencode import bdecode, bencode

for metainfo_name in argv[1:]:
    metainfo_file = open(metainfo_name, 'rb')
    if metainfo_file.read(11) != 'd8:announce':
        print ('ERROR: %s is not a .torrent' % metainfo_name)
        continue
    metainfo_file.seek(0)
    metainfo = bdecode(metainfo_file.read())
    metainfo_file.close()
    info = metainfo['info']
    info_hash = sha(bencode(info))

    print (info_hash.hexdigest())
