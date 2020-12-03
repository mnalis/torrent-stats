#!/usr/bin/python2
import libtorrent as lt
import time
import sys
import pprint

ses = lt.session()
ses.listen_on(6881, 6891)

info = lt.torrent_info(sys.argv[1])

print "piece len=", info.piece_length(), " piece count=", info.num_pieces()
print "creator=", info.creator(), "comment=", info.comment()
print "name=", info.name(), "num_files=", info.num_files()
print "magnet=", lt.make_magnet_uri(info)

for tracker in info.trackers():
  print "  tracker=", tracker.tier, tracker.url
  #pprint.pprint (tracker.['endpoints'])

h = ses.add_torrent({'ti': info, 'save_path': './'})
print 'starting', h.name()

while (not h.is_seed()):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
      s.num_peers, state_str[s.state]),

   print 'peers: %d/(%d,%d) seeds: %d/(%d,%d) distributed copies: %d' % (s.num_peers, s.list_peers, s.num_incomplete, s.num_seeds, s.list_seeds, s.num_complete, s.distributed_copies)
   
   for peer in s.handle.get_peer_info():
        if peer.flags & lt.peer_info.handshake:
            id = 'waiting for handshake'
        elif peer.flags & lt.peer_info.connecting:
            id =  'connecting to peer'
        else:
            id = peer.client

        print ' peer ', id

   alerts = ses.pop_alerts()
   for a in alerts:
      #if a.category() & lt.alert.category_t.error_notification:
          print "alert:", a

   sys.stdout.flush()

   time.sleep(1)

print h.name(), 'complete'
