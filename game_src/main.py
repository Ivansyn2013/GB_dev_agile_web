import sys

import pygame as pg
import os
from settings import *
from map import *
from player import *
import asyncio
import threading
from websocket_server import run_game
from threading import Thread
from queue import Queue
from multiprocessing import Process

from websocket2.server import WebsocketServer

import mss
import numpy as np
import cv2

class Game:
    def __init__(self, queue):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1 #ипользуется для вычесления скорости в зависимоти от фрейм рейта
        self.new_game()
        self.queue = queue

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)

    def update(self):
        self.player.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                self.queue.put('END')
                pg.quit()
                sys.exit()

    def get_screen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            raw = sct.grab(monitor)
        frame = np.array(raw, np.uint8)
        _, encoded_frame = cv2.imencode('.jpg', frame)
        return encoded_frame.tobytes()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
        try:
            self.queue.put(self.get_screen(), block=False)
        except Exception as error:
            print(error)



#запустить здесь, потом октрыть в браузере фаил websocket2/index.html
#должен быть стрим экрана
if __name__ == '__main__':
    my_queue = Queue()
    #game = Game(my_queue)

    #game.start()
    HOST = "localhost"

    PORT = 8766

    server = WebsocketServer(queue=my_queue, host=HOST, port=PORT)
    ser = Process(target=(lambda: asyncio.run(server.start())))

    #game = Process(target=(game.run))

    #game.start()
    ser.start()

    ser.join()
    #game.join()
