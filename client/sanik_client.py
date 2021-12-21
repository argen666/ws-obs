import asyncio
import socketio
import StarTSPImage
import os,sys, urllib, signal
import textwrap
from string import ascii_letters
from PIL import Image, ImageDraw, ImageFont

sio = socketio.AsyncClient()

def text2png(text, fullpath, color="#000", bgcolor="#FFF", fontfullpath=None, fontsize=13, leftpadding=3, rightpadding=3, width=200):
    REPLACEMENT_CHARACTER = u'\uFFFD'
    NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '

    font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(
        fontfullpath, fontsize)
    text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

    lines = []
    line = u""

    for word in text.split():
        print(word)
        if word == REPLACEMENT_CHARACTER:  # give a blank line
            lines.append(line[1:])  # slice the white space in the begining of the line
            line = u""
            # lines.append(u"")  # the blank line
        elif font.getsize(line + ' ' + word)[0] <= (width - rightpadding - leftpadding):
            line += ' ' + word
        else:  # start a new line
            lines.append(line[1:])  # slice the white space in the begining of the line
            line = u""

            avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((width * .95) / avg_char_width)
            lines.extend(textwrap.wrap(word, max_char_count))
            

    if len(line) != 0:
        lines.append( line[1:] ) #add the last line

    line_height = font.getsize(text)[1]
    img_height = line_height * (len(lines) + 1)

    img = Image.new("RGBA", (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)
    
    y = 0
    for line in lines:
        draw.text( (leftpadding, y), line, color, font=font)
        y += line_height

    # add linkback at the bottom
    # draw.text( (width - linkbackx, img_height - linkback_height), linkback, color, font=fontlinkback) 
    # img.save(fullpath)
    return img

@sio.event
async def connect():
    global url
    print('connected to server ')
    print('Reading stream url: ' + url)
    json = {'stream_url': urllib.parse.quote_plus(url)}
    print(json)
    await sio.emit('ws_connect', json)


@sio.event
async def disconnect():
    print('disconnected from server')
    await sio.emit('ws_disconnect', {})


def printMessage(message):
    try:
        font = os.path.dirname(os.path.abspath(__file__)) + "/Roboto-Regular.ttf"
        image = text2png(message, 'test.png', fontsize=25, fontfullpath=font)
        raster = StarTSPImage.imageToRaster(image, cut=True)
        printer = open('/dev/usb/lp0', "wb")
        printer.write(raster)
    except Exception as e:
        print(type(e), str(e))


@sio.event
def message(msg):
    message = msg['message']
    print(message)
    printMessage(message)
    # message = json.loads(str(msg))
    # print(message.message)


async def start_server(host):
    # await sio.connect('http://localhost:80')
    await sio.connect("http://"+host)
    await sio.wait()

async def handler(signum, frame):
    print('Signal handler called with signal', signum)
    await sio.emit('ws_disconnect', {})
    # os.read()
    exit(signum)
    
if __name__ == '__main__':
    # signal.signal(signal.SIGINT, handler)
    host = sys.argv[1]
    global url
    url = sys.argv[2]
    print("Connecting to " + host)
    asyncio.run(start_server(host))
