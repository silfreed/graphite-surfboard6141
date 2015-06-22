#!/bin/env python

import os
import re
import subprocess
import sys
import time
import requests

hostname = os.environ.get('COLLECTD_HOSTNAME', subprocess.check_output(['hostname', '-f']).strip())
interval = float(os.environ.get('COLLECTD_INTERVAL', '10'))

def surfboard6141_signaldata():
  ret = {
    'downstream': {},
    'upstream': {},
  }

  r = requests.get("http://192.168.100.1/cmSignalData.htm")

  # Pull apart and put back together the ugly HTML output from the SB6141
  content = r.text
  content = re.sub('\n','', content)
  content = re.sub('&nbsp; ', ' ', content)
  content = re.sub('&nbsp;', ' ', content)
  content = re.sub(r'<.*?>', '', content)
  content = " ".join(content.split())

  ret['downstream']['channel_id'] = re.findall(r'\d+', re.search(r'Downstream.+?Channel ID(.*?)Frequency', content).group(1))
  ret['downstream']['frequency_Hz'] = re.findall(r'\d+', re.search(r'Downstream.+?Frequency(.*?)Signal to Noise Ratio', content).group(1))
  ret['downstream']['SNR_dB'] = re.findall(r'\d+', re.search(r'Downstream.+?Signal to Noise Ratio(.*?)Downstream Modulation', content).group(1))
  ret['downstream']['power_level_dBmV'] = re.findall(r'\d+', re.search(r'Downstream.+?new reading(.*?)Upstream', content).group(1))
  ret['downstream']['CodewordsUnerrored'] = re.findall(r'\d+', re.search(r'Signal Stats.+?Total Unerrored Codewords(.*?)Total Correctable Codewords', content).group(1))
  ret['downstream']['CodewordsCorrectable'] = re.findall(r'\d+', re.search(r'Signal Stats.+?Total Correctable Codewords(.*?)Total Uncorrectable Codewords', content).group(1))
  ret['downstream']['CodewordsUncorrectable'] = re.findall(r'\d+', re.search(r'Signal Stats.+?Total Uncorrectable Codewords(.*?)document', content).group(1))
  ret['upstream']['channel_id'] = re.findall(r'\d+', re.search(r'Upstream.+?Channel ID(.*?)Frequency', content).group(1))
  ret['upstream']['frequency_Hz'] = re.findall(r'\d+', re.search(r'Upstream.+?Frequency(.*?)Ranging', content).group(1))
  ret['upstream']['power_level_dBmV'] = re.findall(r'\d+', re.search(r'Upstream.+?Power Level(.*?)Upstream', content).group(1))
  return ret

while True:
  signaldata = surfboard6141_signaldata()

  for direction, stats in signaldata.iteritems():
    for key, values in stats.iteritems():
      if key == 'channel_id':
        print "PUTVAL %s/surfboard6141/%s-%s interval=%s %s:%s" % (hostname, "bonded_channels", direction, interval, int(time.time()), len(values))
        continue

      for channelid, value in zip(signaldata[direction]['channel_id'], values):
        print "PUTVAL %s/surfboard6141/%s/%s-%s interval=%s %s:%s" % (hostname, direction, key, channelid, interval, int(time.time()), value)
  sys.stdout.flush()

  time.sleep(interval)

# vim: ts=2:sw=2:sts=2:et
