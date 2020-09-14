# gui.py
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'ina is dum'
import pygame
import logging

from session import Session
from cfg_dict import CfgDict

CLIENT_CFG_PATH = 'client.cfg'

def main():
    logging.info('gui starting')

    cfg = CfgDict(CLIENT_CFG_PATH)

    session = Session('moyalinka', 'Morsee6294')

    pygame.init()
    
    width = cfg['width']
    height = cfg['height']
    display = pygame.display.set_mode((width, height)) 
    pygame.display.set_caption('%s v%s' % (cfg['title'], cfg['version']))


    clock = pygame.time.Clock()
    closing = False

    while not closing: 
        time_delta = clock.tick(cfg['refresh'])/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing = True

        display.fill((0,0,22))
        pygame.draw.rect(display, (50, 50, 50), (20, 20, width-40, height-40))
        pygame.draw.rect(display, (255, 0, 0), (20, 20, width-40, height-40), 1)
        pygame.display.update()


    pygame.quit()
    cfg.export()
    logging.info('gui stopped')
