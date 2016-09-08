#!/usr/bin/python

# -*- coding: utf-8 -*-

from __future__ import print_function

import requests
from requests_oauthlib import OAuth1

from urlparse import urlparse, urlunparse
from urllib import urlencode
from urllib import __version__ as urllib_version

try:
    import simplejson as json
except ImportError:
    import json








class Stream(object):
    """
    Class to query Twitter's streaming API.
    """
    def __init__(
            self,
            consumer_key,
            consumer_secret,
            access_token_key,
            access_token_secret,
            follow=None,
            track=None):
        """
        Form a request to Twitter's streaming API.

        INPUT:
            consumer_key :: str (required)
                The consumer key component of an API key.

            consumer_secret :: str (required)
                The consumer secret compoent of an API key.

            access_token_key :: str (required)
                The access token key component of an API key.

            access_token_secret :: str (required)
                The access token secret component of an API key.

            follow :: int, long, str, or list
                A user ID or list of user IDs, indicating the users whose Tweets should be delivered
                on the stream. Following protected users is not supported. For each user specified,
                the stream will contain:
                    * Tweets created by the user.
                    * Tweets which are retweeted by the user.
                    * Replies to any Tweet created by the user.
                    * Retweets to any Tweet created by the user.
                    * Manual replies to Tweets by the user.
                The stream will not contain:
                    * Tweets mentioning the user.
                    * Manual Retweets.
                    * Tweets by protected users.

            track :: str or list of str
                A phrase or list of phrases which will be used to determine which Tweets will be
                delivered on the stream. A phrase may be one or more terms separated by spaces, and
                a phrase will match if all of the terms in the phrase are present in the Tweet,
                regardless of order and ignoring case. By this model, you can think of commas as
                logical ORs, while spaces are equivalent to logical ANDs (e.g. 'the twitter' is the
                AND twitter, and 'the,twitter' is the OR twitter).

                The text of the Tweet and some entity fields are considered for matches.
                Specifically, the text attribute of the Tweet, expanded_url and display_url for
                links and media, text for hashtags, and screen_name for user mentions are checked
                for matches.

                Each phrase must be between 1 and 60 bytes, inclusive.

                Exact matching of phrases (equivalent to quoted phrases in most search engines) is
                not supported.

                Punctuation and special characters will be considered part of the term they are
                adjacent to. In this sense, "hello." is a different track term than "hello".
                However, matches will ignore punctuation present in the Tweet. So "hello" will match
                both "hello world" and "my brother says hello." Note that punctuation is not
                considered to be part of a #hashtag or @mention, so a track term containing
                punctuation will not match either #hashtags or @mentions.

                UTF-8 characters will match exactly, even in cases where an "equivalent" ASCII
                character exists.

                Non-space separated languages, such as CJK are currently unsupported.

                URLs are considered words for the purposes of matches which means that the entire
                domain and path must be included in the track query for a Tweet containing an URL to
                match. Note that display_url does not contain a protocol, so this is not required to
                perform a match.

                Twitter currently canonicalizes the domain "www.example.com" to "example.com" before
                the match is performed, so omit the "www" from URL track terms.

                Finally, to address a common use case where you may want to track all mentions of a
                particular domain name (i.e., regardless of subdomain or path), you should use
                "example com" as the track parameter for "example.com" (notice the lack of period
                between "example" and "com" in the track parameter). This will be over-inclusive,
                so make sure to do additional pattern-matching in your code. See the table below
                for more examples related to this issue.

                See https://dev.twitter.com/streaming/overview/request-parameters for examples.
        """
        # Parse input options
        if follow is None and track is None:
            raise ValueError({'message': "follow or track filter must be specified."})
        # Get config
        self._user_agent = 'Python-urllib/%s' % urllib_version
        self._url = 'https://stream.twitter.com/1.1/statuses/filter.json'
        self._oauth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
        self._parameters = {'stall_warnings': str(True)}
        if follow:
            if not isinstance(follow, list):
                follow = [follow]
            if not all(isinstance(u, (int, long, str)) for u in follow):
                raise TypeError("follow can contain only ints, strs, and longs")
            follow = [str(u) for u in follow]
            self._parameters['follow'] = ','.join(follow)
        if track:
            if not isinstance(track, list):
                track = [track]
            if not all(isinstance(u, str) for u in track):
                raise TypeError("tracl can contain only strs")
            self._parameters['track'] = ','.join(track)
    
    def get(self):
        try:
            return requests.post(self._url, data=self._parameters, stream=True, auth=self._oauth, timeout=60)
        except Exception as e:
            print("exception: %s" % str(e))
