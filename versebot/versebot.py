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
import os

import books
from regex import find_verses
from response import Response
from verse import Verse
from webparser import WebParser

TIMEOUT=3

class VerseBot:
    def __init__(self, token):
        logging.getLogger('requests').setLevel(logging.WARNING)
        self.log = logging.getLogger('versebot')
        self.log.addHandler(logging.FileHandler('versebot_log.txt'))
        self.parser = WebParser()
        self.slack = Slacker(token)
        self.next_id = 1
        
    async def connect(self):
        rtm_response = self.slack.rtm.start()

        if rtm_response.successful:
            url = rtm_response.body['url']

            await self.listen(url)

        else:
            self.log.error('Failed to connect to rtm')
            sys.exit(1)
            
    async def run(self):
        try:
            await self.connect()
        except websockets.ConnectionClosed:
            await self.connect()

    async def listen(self, url):
        async with websockets.connect(url) as websocket:
            while True:
                try: 
                    msg = await asyncio.wait_for(websocket.recv(), TIMEOUT)
                    msg = json.loads(msg)

                    if msg.get('type', '') == 'message':
                        if msg.get('text', '').find('@U15P6LAG5') != -1:
                            await self.send_verses_response(msg, websocket)
                            time.sleep(1)
                    elif msg.get('type', '') == 'error':
                        self.log.error('error message received',
                                       extra={'msg': msg})
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

                    await websocket.send(json.dumps(data))
                    response = await websocket.recv()

                    if not json.loads(response)['ok'] == 'true':
                        self.log.error('error response',
                                       extra={'response': response})
        else:
            self.log.info("No verses found in this message. Messaging admin")
            # TODO message admin

    async def ping(self, websocket):
        ping_message =  json.dumps({"id": self.next_id, "type": "ping", 
                "time": time.time()})
        self.next_id += 1
        await websocket.send(ping_message)
        pong = await websocket.recv()
        #eventually validate or something here


def handle_sigint(signal, frame):
    loop.stop()
    sys.exit(0)


loop = asyncio.get_event_loop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    token = os.environ['SLACK_TOKEN']
    bot = VerseBot(token)

    asyncio.ensure_future(bot.run())

    loop.run_forever()
