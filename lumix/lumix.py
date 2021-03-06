import sys
import signal
import time
import os
import subprocess
import psutil
import platform
import shlex
import configparser
from threading import Thread
from threading import current_thread
from time import sleep


class CameraThread(Thread):

    def __init__(self, camera_name, camera_ip, chunk_time, video_dir):
        Thread.__init__(self)
        self.camera_name = camera_name
        self.camera_ip = camera_ip
        self.ping_wait_time = 2
        self.video_chunk_time = chunk_time
        self.video_dir = video_dir

    def check_ping(self, isPingNeeded):
        if (isPingNeeded == False):
            return True
        response = os.system("ping -{} 1 {}".format(
            'n' if platform.system().lower() == "windows" else 'c', self.camera_ip))
        return response == 0

    def run(self):
        isPingNeeded = True
        counter = self.video_chunk_time
        log("Thread for camera " + self.camera_name + " running")
        while True:
            if (self.check_ping(isPingNeeded)):
                log("Ping camera " + self.camera_ip + " is OK")
                # cvlc rtsp://192.168.16.127/stream --sout=file/ts:camera_1_$(date +"%Y%m%d%H%M%S")_"$c".mp4 --stop-time=10 vlc://quit
                stream_url = "rtsp://" + self.camera_ip + "/stream"
                # self.captureCVLC(stream_url, counter)
                self.captureFFMPG(stream_url, counter)
                counter = counter + self.video_chunk_time
            else:
                log("Ping camera " + str(self.camera_ip) +
                    " FAILS, waiting " + str(self.ping_wait_time) + " sec")
                isPingNeeded = True
                sleep(self.ping_wait_time)

    def captureCVLC(self, stream_url, counter):
        file_name_template = self.camera_name + "_" + \
                             time.strftime("%Y%m%d-%H%M%S") + "_" + \
                             str(counter) + ".mp4"
        cmd = "cvlc " + stream_url + " --rtsp-frame-buffer-size=500000 -q --sout=file/ts:" + file_name_template + \
              " --stop-time=" + str(self.video_chunk_time) + " vlc://quit"
        cmd = shlex.split(cmd)
        # cmd = ["cvlc", stream_url, "--sout=file/ts:", file_name_template,
        #                      "--stop-time", str(self.video_chunk_time), "vlc://quit"]
        log(cmd)
        try:
            log("Chunk " + file_name_template + " saving in progress...")
            proc = subprocess.run(cmd, timeout=self.video_chunk_time + 5)
            log("Chunk " + file_name_template + " saved")
            if (os.stat(file_name_template).st_size == 0):
                log("ERROR! Chunk " + file_name_template +
                    " is ZERO size. Please Reboot camera!!!")
                isPingNeeded = True
            else:
                isPingNeeded = False
                # sleep(self.ping_wait_time+500)
        except (subprocess.TimeoutExpired):
            log("Capture for chunk " + file_name_template +
                " was stucked and terminated by timeout")
            isPingNeeded = True
        except:
            pass

    def captureFFMPG(self, stream_url, counter):
        stream_url = "rtsp://@" + self.camera_ip + "/stream"
        file_name_template = self.camera_name + "_" + \
                             time.strftime("%Y%m%d-%H%M%S")
        if not (self.video_chunk_time):
            self.video_chunk_time = 60
        if not (self.video_dir):
            save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
        else:
            save_dir = self.video_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_file = os.path.join(save_dir, file_name_template + "-%03d.ts")
        cmd = "ffmpeg -hide_banner -loglevel error -i " + stream_url + " -acodec copy -vcodec copy -f segment -segment_time " + str(
            self.video_chunk_time) + " \"" + save_file + "\""
        log(cmd)
        cmd = shlex.split(cmd)
        # log(cmd)
        try:
            log("Stream from " + self.camera_name + " saving in progress...")
            proc = subprocess.run(cmd)
            # log("Chunk "+file_name_template+" saved")
        except (subprocess.TimeoutExpired):
            log("Capture " + file_name_template +
                " was stucked and terminated by timeout")
            isPingNeeded = True
        except:
            log("FFMPG process was unexpexted ends, restarting...")
            isPingNeeded = True


class GetDict:

    def __init__(self, config):
        self.config = config

    def get_dict(self):
        config = configparser.ConfigParser()
        config.read(self.config)

        sections_dict = {}

        # get all defaults
        defaults = config.defaults()
        temp_dict = {}
        for key in defaults:
            temp_dict[key] = defaults[key]

        sections_dict['default'] = temp_dict

        # get sections and iterate over each
        sections = config.sections()

        for section in sections:
            options = config.options(section)
            temp_dict = {}
            for option in options:
                temp_dict[option] = config.get(section, option)

            sections_dict[section] = temp_dict

        return sections_dict


def log(*text):
    print(current_thread().name, text)


def kill_process(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            proc.kill()


def handler(signum, frame):
    log('Signal handler called with signal', signum)
    kill_process("vlc")
    kill_process("ffmpeg")
    exit(signum)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    kill_process("vlc")
try:

    if len(sys.argv) == 1:
        cfg = "lumix.conf"
    else:
        cfg = sys.argv[1]

    config = os.path.join(os.path.dirname(os.path.abspath(__file__)), cfg)
    log("Reading config file: " + config)
    getdict = GetDict(config)
    config_dict = getdict.get_dict()
    chunk_time = config_dict["SETTINGS"]["chunk_time"]
    video_dir = config_dict["SETTINGS"]["video_dir"]
    for key in config_dict["default"]:
        log(key, '->', config_dict["default"][key])
        camera_name = key
        camera_ip = config_dict["default"][key]
        cam_thread = CameraThread(camera_name, camera_ip, chunk_time, video_dir)
        cam_thread.setDaemon(True)
        cam_thread.setName("Thread-" + camera_name)
        cam_thread.start()

    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    handler(signal.SIGINT, None)
