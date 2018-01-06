# -*- coding: utf-8 -*-

import random
from PIL import Image, ImageDraw, ImageFont
import StringIO

class RandomChar(object):
    @staticmethod
    def Unicode():
        #val = random.randint(0x4E00, 0x9FBB)
        val = random.randint(65, 90)
        return unichr(val)


class ImageChar():
    def __init__(self, fontColor = (0, 0, 0),
                     size = (100, 40),
                     fontPath = 'app/static/OpenSans-Bold.ttf',
                     bgColor = (255, 255, 255, 255),
                     fontSize = 20):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGBA', size, bgColor)

    def rotate(self):
        img1 = self.image.rotate(random.randint(-5, 5), expand=0)
        img = Image.new('RGBA',img1.size,(255,)*4)
        self.image = Image.composite(img1,img,img1)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw

    def randRGB(self):
        return (random.randint(0, 255),
               random.randint(0, 255),
               random.randint(0, 255))
    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB())
        del draw

    def randCode(self, num):
        gap = 0
        start = 0
        strRes = ''
        for i in range(0, num):
            char = RandomChar().Unicode()
            strRes += char
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.drawText((x, random.randint(-5, 5)), char, (0,0,0))
            self.rotate()
        self.randLine(8)
        return strRes,self.image
