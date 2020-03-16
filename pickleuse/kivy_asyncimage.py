'''
Asynchronous image loading
==========================
Test of the widget AsyncImage.
We are just putting it in a CenteredAsyncImage for being able to center the
image on screen without doing upscale like the original AsyncImage.
'''

from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.lang import Builder




class TestAsyncApp(App):
    def build(self):
        url = ('https://cdn.profile-image.st-hatena.com/users/rkr0314/profile.png')
        return AsyncImage(source=url)


if __name__ == '__main__':
    TestAsyncApp().run()
