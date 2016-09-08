#!/usr/bin/python

# -*- coding: utf-8 -*-

from __future__ import print_function

import pytilia


consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

track = ['#detroittigers','#tigers','#dettigers','#whitesox']

stream_data = pytilia.Stream(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token_key=access_token_key,
    access_token_secret=access_token_secret,
    track=track)


f_p = open('2016-09-07_Tigers_WhiteSox.json','a')

for line in stream_data.get().iter_lines():
    if line:
        print('%s\n' % line)
        f_p.write(line)
        f_p.write('\n')

