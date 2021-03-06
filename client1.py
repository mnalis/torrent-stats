#!/usr/bin/python2
import libtorrent as lt
import time
import sys

ses = lt.session()
ses.listen_on(6881, 6891)

info = lt.torrent_info(sys.argv[1])
h = ses.add_torrent({'ti': info, 'save_path': './'})
print 'starting', h.name()

while (not h.is_seed()):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
      s.num_peers, state_str[s.state]),

   alerts = ses.pop_alerts()
   for a in alerts:
      if a.category() & lt.alert.category_t.error_notification:
         print(a)


   sys.stdout.flush()

   time.sleep(1)

print h.name(), 'complete'
