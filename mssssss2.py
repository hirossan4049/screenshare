import pygame
from PIL.Image import Image
from mss import mss
from zlib import compress, decompress

WIDTH = 3840
HEIGHT = 2400
# WIDTH = 1920
# HEIGHT = 1080
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
watching = True



with mss() as sct:
    # Get rid of the first, as it represents the "All in One" monitor:
    while True:
        for num, monitor in enumerate(sct.monitors[1:], 1):
            # Get raw pixels from the screen
            sct_img = sct.grab(monitor)

            # Create the Image
            # img = Image.frombytes("RGB", sct_img.size, sct_img.bgra)
            img2 = pygame.image.fromstring(sct_img.rgb, sct_img.size, 'RGB')


            # Display the picture
            screen.blit(img2, (0, 0))
            pygame.display.flip()
            clock.tick(60)

        # print(img.rgb, 6)
        # conn.sendall(pixels)
