#!/bin/sh
BASE="https://planet.openstreetmap.org"
WGET_OPTS="-q --trust-server-names -N"
wget ${WGET_OPTS} ${BASE}/pbf/planet-latest.osm.pbf.torrent
wget ${WGET_OPTS} ${BASE}/pbf/full-history/history-latest.osm.pbf.torrent

wget ${WGET_OPTS} ${BASE}/planet/planet-latest.osm.bz2.torrent
wget ${WGET_OPTS} ${BASE}/planet/full-history/history-latest.osm.bz2.torrent

wget ${WGET_OPTS} ${BASE}/planet/changesets-latest.osm.bz2.torrent
wget ${WGET_OPTS} ${BASE}/planet/discussions-latest.osm.bz2.torrent

./osm_torrent_log.py *.torrent

find . -maxdepth 1 -name "*.osm.*.torrent" -mtime +16 -delete
