from PIL import Image
import pygame
from mss import mss
import time


WIDTH = 1920
HEIGHT = 1080

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Hello!')

with mss() as sct:
    while 1:
        pygame.time.Clock().tick(60)
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        sct_img = sct.grab(rect)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img_byte = img.tobytes("raw", 'RGB')
        pygame_surface = pygame.image.fromstring(img_byte, img.size, 'RGB')
        screen.blit(pygame_surface, (0, 0))
        pygame.display.flip()
        # clock.tick(60)
        # time.sleep(1)