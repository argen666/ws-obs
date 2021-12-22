import asyncio
import json
import os
import sys
import textwrap
import traceback
from io import BytesIO
from string import ascii_letters

import StarTSPImage
import nats
import numpy as np
import requests
import urllib3
from PIL import Image, ImageDraw, ImageFont
from nats.js.api import ReplayPolicy, ConsumerConfig, DeliverPolicy


async def test():
    json1 = ""
    # json1 = "[{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UC_K5OtuQ-4gXlhxRiAVp8vg\", \"channelUrl\": \"http://www.youtube.com/channel/UC_K5OtuQ-4gXlhxRiAVp8vg\", \"name\": \"McCallister\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLQnkSbkXKeD4-1lW1TyBV7BPpptJ1KzbK7fd530kQ=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNQREgwci1PMmZJQ0ZYc3FyUVlkOHNjTzJREidDUDIwNjhxTjJmSUNGVF8zT0FZZEc2NE92dzE2MzAzMzkyMzEzNzk%3D\", \"timestamp\": 1630339117392, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:37\", \"message\": \"@Unknown ok Medam :slightly_smiling_face:\"," \
    #             " \"messageEx\": [" \
    #             "{\"id\": \"🙂\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f642.svg\"}," \
    #             "{\"id\": \"🙂\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f642.svg\"}," \
    #             "\"@Unknown ok Medam \"," \
    #             " {\"id\": \"🙂\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f642.svg\"}," \
    #             " {\"id\": \"🙂\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f642.svg\"}," \
    #             " {\"id\": \"🙂\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f642.svg\"}," \
    #             "{\"id\": \"🙂\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f91f.svg\"}" \
    #             "], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCXTW0pjueft9RV1K_nW0Q0A\", \"channelUrl\": \"http://www.youtube.com/channel/UCXTW0pjueft9RV1K_nW0Q0A\", \"name\": \"jay ceasar\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLSlGdojtNacCTj1nwxy660AzVlqgzTcgJSRCw=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CjoKGkNMQ3E5Y0NPMmZJQ0ZVeUg1UWNkQWhnSkN3EhxDS0MtdklLTTJmSUNGZlFZclFZZENtd0xXQTE0\", \"timestamp\": 1630339120059, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:40\", \"message\": \"praise buddah\", \"messageEx\": [\"praise buddah\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCCEc-m0Gcn0Iorxs94O7ktQ\", \"channelUrl\": \"http://www.youtube.com/channel/UCCEc-m0Gcn0Iorxs94O7ktQ\", \"name\": \"Faith\", \"imageUrl\": \"https://yt4.ggpht.com/2miMrZAMpkbHm_rxA_Bb9aDG6YyBFLNa7ZfonV8MplgstQeR5jxbEzDDwavOrh1s4Iy8-209yA=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNKNzc2c0dPMmZJQ0ZSSzV3UW9kN3pVT2FBEidDTjJocWF1TzJmSUNGVWZBMVFvZGU1UUp3UTE2MzAzMzkxMjA5ODA%3D\", \"timestamp\": 1630339121987, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:41\", \"message\": \"Be Youself, Love Youself, Express yourself :love_you_gesture:\", \"messageEx\": [\"Be Youself, Love Youself, Express yourself \", {\"id\": \"🤟\", \"txt\": \":love_you_gesture:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f91f.svg\"}], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCpBMkvelkpAMr_KVGrwODDw\", \"channelUrl\": \"http://www.youtube.com/channel/UCpBMkvelkpAMr_KVGrwODDw\", \"name\": \"THREE\", \"imageUrl\": \"https://yt4.ggpht.com/vgpzgpp0bsNNs7Qorg-x8H8GQDirw1sWMxf9YTZz1qPdpLF_FtENQU6FpAQfmSoT0-IKSq7Tsos=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNNbXBrY0tPMmZJQ0ZWc2VyUVlkY0d3TTlBEidDSlMzbjdpTzJmSUNGVWJGb0FJZDFsb09YUTE2MzAzMzkxMjE4NTA%3D\", \"timestamp\": 1630339122615, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:42\", \"message\": \"hii lil\", \"messageEx\": [\"hii lil\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UC4AVGJfzti5a_92J0C_K7Wg\", \"channelUrl\": \"http://www.youtube.com/channel/UC4AVGJfzti5a_92J0C_K7Wg\", \"name\": \"Balram Kushwah\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLSCHcq6J6rbiO0reuKUEmd0xc6chl2PJilCX6wEMw=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNOYm0wc0tPMmZJQ0ZUTWI1d29kUGlVSmZREidDUGFxa3F1TjJmSUNGWW5GT0FZZG9oY0NhUTE2MzAzMzkxMjI4NTg%3D\", \"timestamp\": 1630339123688, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:43\", \"message\": \"suno mujhe msg..to dekh lene diya kro\", \"messageEx\": [\"suno mujhe msg..to dekh lene diya kro\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCCEc-m0Gcn0Iorxs94O7ktQ\", \"channelUrl\": \"http://www.youtube.com/channel/UCCEc-m0Gcn0Iorxs94O7ktQ\", \"name\": \"Faith\", \"imageUrl\": \"https://yt4.ggpht.com/2miMrZAMpkbHm_rxA_Bb9aDG6YyBFLNa7ZfonV8MplgstQeR5jxbEzDDwavOrh1s4Iy8-209yA=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNPajM3TWVPMmZJQ0ZRT293UW9keWRzSWV3EidDT1NpLXNLTzJmSUNGUXpXVVFvZFNRY0w2QTE2MzAzMzkxMzM0NjA%3D\", \"timestamp\": 1630339134602, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:54\", \"message\": \"Love Thy Neighbour as Thyself :red_heart:\", \"messageEx\": [\"Love Thy Neighbour as Thyself \", {\"id\": \"❤\", \"txt\": \":red_heart:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u2764.svg\"}], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UC_K5OtuQ-4gXlhxRiAVp8vg\", \"channelUrl\": \"http://www.youtube.com/channel/UC_K5OtuQ-4gXlhxRiAVp8vg\", \"name\": \"McCallister\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLQnkSbkXKeD4-1lW1TyBV7BPpptJ1KzbK7fd530kQ=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNKYUdfOGVPMmZJQ0ZSUU1yUVlkUzBBSHJBEidDUDIwNjhxTjJmSUNGVF8zT0FZZEc2NE92dzE2MzAzMzkyNDg4NDc%3D\", \"timestamp\": 1630339134899, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:54\", \"message\": \"@Ok bye people cya tc\", \"messageEx\": [\"@Ok bye people cya tc\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0}]"
    # json1 = "[{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UC_K5OtuQ-4gXlhxRiAVp8vg\", \"channelUrl\": \"http://www.youtube.com/channel/UC_K5OtuQ-4gXlhxRiAVp8vg\", \"name\": \"McCallister\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLQnkSbkXKeD4-1lW1TyBV7BPpptJ1KzbK7fd530kQ=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNQREgwci1PMmZJQ0ZYc3FyUVlkOHNjTzJREidDUDIwNjhxTjJmSUNGVF8zT0FZZEc2NE92dzE2MzAzMzkyMzEzNzk%3D\", \"timestamp\": 1630339117392, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:37\", \"message\": \"@Unknown ok Medam :slightly_smiling_face:\", \"messageEx\": [\"@Unknown ok Medam \", {\"id\": \"��\", \"txt\": \":slightly_smiling_face:\", \"url\": \"https://yt4.ggpht.com/ytc/AKedOLQnkSbkXKeD4-1lW1TyBV7BPpptJ1KzbK7fd530kQ=s64-c-k-c0x00ffffff-no-rj\"}], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCXTW0pjueft9RV1K_nW0Q0A\", \"channelUrl\": \"http://www.youtube.com/channel/UCXTW0pjueft9RV1K_nW0Q0A\", \"name\": \"jay ceasar\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLSlGdojtNacCTj1nwxy660AzVlqgzTcgJSRCw=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CjoKGkNMQ3E5Y0NPMmZJQ0ZVeUg1UWNkQWhnSkN3EhxDS0MtdklLTTJmSUNGZlFZclFZZENtd0xXQTE0\", \"timestamp\": 1630339120059, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:40\", \"message\": \"praise buddah\", \"messageEx\": [\"praise buddah\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCCEc-m0Gcn0Iorxs94O7ktQ\", \"channelUrl\": \"http://www.youtube.com/channel/UCCEc-m0Gcn0Iorxs94O7ktQ\", \"name\": \"Faith\", \"imageUrl\": \"https://yt4.ggpht.com/2miMrZAMpkbHm_rxA_Bb9aDG6YyBFLNa7ZfonV8MplgstQeR5jxbEzDDwavOrh1s4Iy8-209yA=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNKNzc2c0dPMmZJQ0ZSSzV3UW9kN3pVT2FBEidDTjJocWF1TzJmSUNGVWZBMVFvZGU1UUp3UTE2MzAzMzkxMjA5ODA%3D\", \"timestamp\": 1630339121987, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:41\", \"message\": \"Be Youself, Love Youself, Express yourself :love_you_gesture:\", \"messageEx\": [\"Be Youself, Love Youself, Express yourself \", {\"id\": \"��\", \"txt\": \":love_you_gesture:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u1f91f.svg\"}], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCpBMkvelkpAMr_KVGrwODDw\", \"channelUrl\": \"http://www.youtube.com/channel/UCpBMkvelkpAMr_KVGrwODDw\", \"name\": \"THREE\", \"imageUrl\": \"https://yt4.ggpht.com/vgpzgpp0bsNNs7Qorg-x8H8GQDirw1sWMxf9YTZz1qPdpLF_FtENQU6FpAQfmSoT0-IKSq7Tsos=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNNbXBrY0tPMmZJQ0ZWc2VyUVlkY0d3TTlBEidDSlMzbjdpTzJmSUNGVWJGb0FJZDFsb09YUTE2MzAzMzkxMjE4NTA%3D\", \"timestamp\": 1630339122615, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:42\", \"message\": \"hii lil\", \"messageEx\": [\"hii lil\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UC4AVGJfzti5a_92J0C_K7Wg\", \"channelUrl\": \"http://www.youtube.com/channel/UC4AVGJfzti5a_92J0C_K7Wg\", \"name\": \"Balram Kushwah\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLSCHcq6J6rbiO0reuKUEmd0xc6chl2PJilCX6wEMw=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNOYm0wc0tPMmZJQ0ZUTWI1d29kUGlVSmZREidDUGFxa3F1TjJmSUNGWW5GT0FZZG9oY0NhUTE2MzAzMzkxMjI4NTg%3D\", \"timestamp\": 1630339123688, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:43\", \"message\": \"suno mujhe msg..to dekh lene diya kro\", \"messageEx\": [\"suno mujhe msg..to dekh lene diya kro\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UCCEc-m0Gcn0Iorxs94O7ktQ\", \"channelUrl\": \"http://www.youtube.com/channel/UCCEc-m0Gcn0Iorxs94O7ktQ\", \"name\": \"Faith\", \"imageUrl\": \"https://yt4.ggpht.com/2miMrZAMpkbHm_rxA_Bb9aDG6YyBFLNa7ZfonV8MplgstQeR5jxbEzDDwavOrh1s4Iy8-209yA=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNPajM3TWVPMmZJQ0ZRT293UW9keWRzSWV3EidDT1NpLXNLTzJmSUNGUXpXVVFvZFNRY0w2QTE2MzAzMzkxMzM0NjA%3D\", \"timestamp\": 1630339134602, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:54\", \"message\": \"Love Thy Neighbour as Thyself :red_heart:\", \"messageEx\": [\"Love Thy Neighbour as Thyself \", {\"id\": \"❤\", \"txt\": \":red_heart:\", \"url\": \"https://www.youtube.com/s/gaming/emoji/7ff574f2/emoji_u2764.svg\"}], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0},{\"author\": {\"badgeUrl\": \"\", \"type\": \"\", \"isVerified\": false, \"isChatOwner\": false, \"isChatSponsor\": false, \"isChatModerator\": false, \"channelId\": \"UC_K5OtuQ-4gXlhxRiAVp8vg\", \"channelUrl\": \"http://www.youtube.com/channel/UC_K5OtuQ-4gXlhxRiAVp8vg\", \"name\": \"McCallister\", \"imageUrl\": \"https://yt4.ggpht.com/ytc/AKedOLQnkSbkXKeD4-1lW1TyBV7BPpptJ1KzbK7fd530kQ=s64-c-k-c0x00ffffff-no-rj\"}, \"type\": \"textMessage\", \"id\": \"CkUKGkNKYUdfOGVPMmZJQ0ZSUU1yUVlkUzBBSHJBEidDUDIwNjhxTjJmSUNGVF8zT0FZZEc2NE92dzE2MzAzMzkyNDg4NDc%3D\", \"timestamp\": 1630339134899, \"elapsedTime\": \"\", \"datetime\": \"2021-08-30 21:58:54\", \"message\": \"@Ok bye people cya tc\", \"messageEx\": [\"@Ok bye people cya tc\"], \"amountValue\": 0.0, \"amountString\": \"\", \"currency\": \"\", \"bgColor\": 0}]"
    jsondata = json.loads(json1)
    for j in jsondata:
        print(j['messageEx'])
        printMessage(j)
        await asyncio.sleep(3)


async def main(nats_host):
    nc = await nats.connect(nats_host)
    print(nc)
    js = nc.jetstream()
    sub = await js.subscribe(stream="youtube-stream", subject="comments", durable="printer",
                             config=ConsumerConfig(replay_policy=ReplayPolicy.instant,
                                                   deliver_policy=DeliverPolicy.all))
    while True:
        try:
            msg = await sub.next_msg()
            jsondata = json.loads(msg.data)
            if not 'messageEx' in jsondata or len(jsondata['messageEx']) == 0:
                continue
            # print(jsondata['author']['name'] + ": " + jsondata['message'])
            print(jsondata['messageEx'])
            printMessage(jsondata)
            await msg.ack()
            await asyncio.sleep(3)
        except Exception as ex:
            print(ex)
            traceback.print_stack()


def text2png(text, color="#000", bgcolor="#FFF", fontfullpath=None, fontsize=13, leftpadding=3, rightpadding=3,
             width=200):
    REPLACEMENT_CHARACTER = u'\uFFFD'
    NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '

    font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(
        fontfullpath, fontsize)
    text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

    lines = []
    line = u""

    for word in text.split():
        # print(word)
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
        lines.append(line[1:])  # add the last line

    line_height = font.getsize(text)[1]
    img_height = line_height * (len(lines) + 1)

    img = Image.new("RGBA", (width, img_height), bgcolor)
    draw = ImageDraw.Draw(img)

    y = 0
    for line in lines:
        draw.text((leftpadding, y), line, color, font=font)
        y += line_height

    # add linkback at the bottom
    # draw.text( (width - linkbackx, img_height - linkback_height), linkback, color, font=fontlinkback) 
    # img.save('test.png')
    return img


def url2png(url, bgcolor="#FFF", width=200, fit_to_width=True):
    try:
        path = str(urllib3.util.parse_url(url))
        ext = os.path.splitext(path)[1]
        if ext == ".svg":
            url = os.path.splitext(path)[0] + ".png"

        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((64, 64))
        if fit_to_width is False:
            return image
        img = Image.new("RGBA", (width, image.height), bgcolor)
        img.paste(image)
        return img
    except Exception:
        return None


def merge_images(images, bgcolor="#FFF", width=200):
    # min_shape = sorted([(np.sum(i.size), i.size) for i in images])[0][1]
    def range2(start, end):
        return range(start, end + 1)

    def zero_runs(a):
        try:
            iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
            absdiff = np.abs(np.diff(iszero))
            ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
            return ranges
        except Exception:
            return None

    shapes = list(map(lambda i: i.height, images))
    rrange = zero_runs(np.diff(shapes))
    if rrange is not None and rrange.size != 0:
        # склеить элементы по выбранному ренжу в один шириной 200, удалить их и созданный поставить по индексу min(range)
        for r in rrange:
            print(r, end=' ')
            ident_list = [images[i] for i in range2(np.amin(r), np.amax(r))]
            index = np.amin(r)
            height = ident_list[0].height
            n = int(width / height)
            idents_list = [ident_list[j:j + n] for j in range(0, len(ident_list), n)]
            idnt_lst_idx_min = np.amin(r)
            for idnt_lst in idents_list:
                img = Image.new("RGBA", (width, height), bgcolor)
                horizontal_image = np.hstack([np.asarray(i) for i in idnt_lst])
                horizontal_image = Image.fromarray(horizontal_image)
                img.paste(horizontal_image)

                for ii in range(idnt_lst_idx_min, idnt_lst_idx_min + len(idnt_lst)):
                    images[ii] = None
                idnt_lst_idx_min = idnt_lst_idx_min + len(idnt_lst)
                index += 1
                images[index] = img
        images = [x for x in images if x is not None]
    else:
        for i, im in enumerate(images):
            if (im.height == 64):
                img = Image.new("RGBA", (width, im.height), bgcolor)
                img.paste(im)
                images[i] = img

    final_image = np.vstack([np.asarray(i) for i in images])
    final_image = Image.fromarray(final_image)
    # final_image.save(str(time.time()) + 'final_image.png')
    return final_image


def printMessage(jsondata):
    try:
        # image = text2png(message, fontsize=25, fontfullpath=font)
        image = json2image(jsondata)
        star_print(image)
    except Exception as e:
        print(type(e), str(e))
        traceback.print_stack()


def json2image(jsondata):
    try:
        images = []
        font = os.path.dirname(os.path.abspath(__file__)) + "/Roboto-Regular.ttf"
        message = jsondata['messageEx']
        for msg in message:
            # print(type(msg))
            if (type(msg) == dict and msg is not None):
                # print(msg['url'])
                url = msg['url']
                image = url2png(url, fit_to_width=False)

                if image is not None:
                    images.append(image)
            elif (type(msg) == str):
                # print(msg)
                image = text2png(msg, fontsize=25, fontfullpath=font)
                if image is not None:
                    images.append(image)
            else:
                print("Unknown message type")

        # print(images)
        final_image = merge_images(images)
        return final_image
    except Exception as e:
        traceback.print_stack()
        print(type(e), str(e))


def star_print(image):
    raster = StarTSPImage.imageToRaster(image, cut=True)
    printer = open('/dev/usb/lp0', "wb")
    printer.write(raster)


async def shutdown(signal, loop):
    print(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks)
    loop.stop()


if __name__ == '__main__':
    nats_host = sys.argv[1]
    # loop = asyncio.get_event_loop()
    # signals = (signal.SIGTERM, signal.SIGINT)
    # for s in ('SIGINT','SIGTERM'):
    #     loop.add_signal_handler(getattr(signal, s), functools.partial(shutdown, loop))
    asyncio.run(main(nats_host))
    # asyncio.run(test())
