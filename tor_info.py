#!/usr/bin/python2
import libtorrent as lt
import time
import sys
import pprint
import datetime

settings = { 'user_agent': 'python_client/' + lt.__version__,
#        'download_rate_limit': int(options.max_download_rate),
#        'upload_rate_limit': int(options.max_upload_rate),
#        'listen_interfaces': '0.0.0.0:%d' % options.port,
#        'alert_mask': lt.alert.category_t.all_categories,
        'alert_mask': lt.alert.category_t.error_notification | lt.alert.category_t.tracker_notification | lt.alert.category_t.status_notification,
        'num_want': 1000,
        'enable_dht': 0,
}

ses = lt.session(settings)
ses.listen_on(6881, 6891)

info = lt.torrent_info(sys.argv[1])
print "piece len=", info.piece_length(), " piece count=", info.num_pieces()
print "creator=", info.creator(), "date=", datetime.datetime.fromtimestamp(info.creation_date())
print "comment=", info.comment()
print "name=", info.name(), "num_files=", info.num_files()
print "magnet=", lt.make_magnet_uri(info)

for webseed in info.web_seeds():
  print "webseed", webseed
  #info.remove_url_seed (webseed)

th = ses.add_torrent({'ti': info, 'save_path': './'})

print 'starting', th.name()
print "magnet2=", lt.make_magnet_uri(th)




while (not th.is_seed()):
   s = th.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
      s.num_peers, state_str[s.state]),

   print 'peers: %d/(%d,%d) seeds: %d/(%d,%d) distributed copies: %d' % (s.num_peers, s.list_peers, s.num_incomplete, s.num_seeds, s.list_seeds, s.num_complete, s.distributed_copies)

   for tracker in th.trackers():
     print "  tracker=", tracker#.tier, tracker.url
     #pprint.pprint (tracker.['endpoints'])
   
   for peer in s.handle.get_peer_info():
        if peer.flags & lt.peer_info.handshake:
            id = 'waiting for handshake'
        elif peer.flags & lt.peer_info.connecting:
            id =  'connecting to peer'
        else:
            id = peer.client

        if peer.flags & lt.peer_info.seed:
            print ' webseed '+id if peer.connection_type & lt.peer_info.web_seed else '    seed '+id
        else:
            print '    peer '+id

        print ' - peer source:', peer.source, ', addr=', peer.ip[0]

   alerts = ses.pop_alerts()
   for a in alerts:
      #if a.category() & lt.alert.category_t.error_notification:
          print "alert:", a

   sys.stdout.flush()

   time.sleep(1)

print th.name(), 'complete'
