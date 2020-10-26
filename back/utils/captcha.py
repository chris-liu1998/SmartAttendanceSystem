import random
import string
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from flask import make_response
import matplotlib.font_manager as fm # to create font
# 验证码图片的大小
HEIGHT = 50
WIDTH = 120
# 验证码的个数
COUNT = 4
# 验证码字体大小
FONT_SIZE = 25


class Captcha():
    '''验证码'''
    def rndColor(self):
        # 随机颜色
        return (random.randint(32, 127), random.randint(32, 127),
                random.randint(32, 127))

    def genText(self):
        # 生成4位验证码
        # ascii_letters是生成所有字母 digits是生成所有数字0-9
        return ''.join(
            random.sample(string.ascii_letters + string.digits, COUNT))

    def drawLines(self, draw, num, width, height):
        # 划线
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def getVerifyCode(self):
        # 生成验证码图片
        # 生成4位验证码字符串
        code = self.genText()
        # 图片大小
        width, height = WIDTH, HEIGHT
        # 新图片对象
        im = Image.new('RGB', (width, height), 'white')
        # 字体
        font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), FONT_SIZE)
        # draw对象
        draw = ImageDraw.Draw(im)
        # 绘制字符串
        for item in range(COUNT):
            draw.text((5 + random.randint(-3, 3) + 23 * item,
                       5 + random.randint(-3, 3)),
                      text=code[item],
                      fill=self.rndColor(),
                      font=font)
        # 划线
        self.drawLines(draw, 2, width, height)
        return im, code

    def getCaptcha(self):
        image, code = self.getVerifyCode()
        # 图片以二进制形式写入
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        # 把buf_str作为response返回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/gif'
        return response, code
