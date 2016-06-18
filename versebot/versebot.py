"""
VerseBot for Slack
By Matt Arnold
Adapted from VerseBot for Reddit by Matthieu Grieger
Copyright (c) 2016 Matt Arnold (MIT License)

"""
import asyncio
import websockets
import json
import signal
import logging
import time
from slacker import Slacker

import sys
import threading

import books
from regex import find_verses
from response import Response
from verse import Verse
from webparser import WebParser

# Time (seconds) to wait between receiving message before sending a ping
TIMEOUT = 3


class VerseBot(threading.Thread):
    def __init__(self, token):
        super(VerseBot, self).__init__()
        logging.getLogger('requests').setLevel(logging.WARNING)
        self.log = logging.getLogger('versebot')
        self.log.addHandler(logging.FileHandler('versebot_log.txt'))
        self.parser = WebParser()
        self.slack = Slacker(token)
        self.next_id = 1
        self.unacked_messages = set()

        self.user_id = self._get_user_id()

    def _get_user_id(self):
        data = self.slack.auth.test()

        if data.successful:
            return data.body['user_id']
        else:
            raise Exception

    async def connect(self):
        rtm_response = self.slack.rtm.start()

        if rtm_response.successful:
            url = rtm_response.body['url']

            while True:
                try:
                    await self.listen(url)
                except websockets.ConnectionClosed:
                    pass
                except Exception as e:
                    self.log.error(str(e))
                    pass

        else:
            self.log.error('Failed to connect to rtm')

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        asyncio.ensure_future(self.connect())
        loop.run_forever()

    async def listen(self, url):
        async with websockets.connect(url) as websocket:
            while True:
                try:
                    msg = await asyncio.wait_for(websocket.recv(), TIMEOUT)
                    msg = json.loads(msg)

                    if msg.get('type', '') == 'message' and \
                                    msg.get('subtype', '') != 'bot_message':
                        if msg.get('text', '').find('@' + self.user_id) != -1:
                            await self.send_verses_response(msg, websocket)
                            time.sleep(1)
                    elif msg.get('type', '') == 'error':
                        self.log.error('error message received',
                                       extra={'msg': msg})
                    # TODO handle rtm response. check if ok
                    else:
                        pass
                except asyncio.TimeoutError:
                    await self.ping(websocket)

    async def send_verses_response(self, msg, websocket):
        user = msg['user']
        channel = msg['channel']

        body = msg['text']

        verses = find_verses(body)
        if verses is not None:
            response = Response(body, self.parser)
            for verse in verses:
                book_name = books.get_book(verse[0])
                if book_name is not None:
                    v = Verse(book_name,
                              verse[1],
                              verse[3],
                              user,
                              channel,
                              verse[2])
                    if not response.is_duplicate_verse(v):
                        response.add_verse(v)
            if len(response.verse_list) != 0:
                message_response = response.construct_message()
                if message_response is not None:
                    data = {'id': self.next_id, 'type': 'message',
                            'channel': channel, 'text': message_response}

                    self.next_id += 1
                    self.unacked_messages.add(self.next_id)

                    await websocket.send(json.dumps(data))
        else:
            pass

    async def ping(self, websocket):
        ping_message = json.dumps({"id": self.next_id, "type": "ping",
                                   "time": time.time()})
        self.next_id += 1
        await websocket.send(ping_message)
        pong = await websocket.recv()
        # eventually validate or something here


def handle_sigint(sig, frame):
    for thread in threads:
        signal.pthread_kill(thread.ident, signal.SIGINT)

    sys.exit(0)


threads = []
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)

    with open('tokens.dat') as tokens:
        for token in tokens.readlines():
            token = token.strip()
            vb = VerseBot(token)
            vb.start()
            threads.append(vb)

    for t in threads:
        t.join()
