import os
import time
import json
import subprocess
import shlex
import threading

config = None

def load_config():
    with open("config.json") as f:
        data = json.load(f)
        return data


def crawl(camera):
    if camera["protocal"] == "rtsp":
        rtsp_url = "{}://{}:{}@{}:{}{}".format(
                    camera["protocal"], camera["account"], camera["password"], camera["ip"], camera["port"], camera["sub_url"])
        video_path = os.path.join(config["data_path"], camera["name"])
        if not os.path.exists(video_path):
            os.mkdir(video_path)
        cmd = "ffmpeg -i {} -c copy -f segment -reset_timestamps 1 -strftime 1 -segment_time {} \"{}/%Y_%m_%d_%H-%M-%S.mp4\"".format(
                    rtsp_url, config["video_duration"], video_path)
        print(cmd)
        process_result = subprocess.run(shlex.split(cmd), check=True)


def infinity_crawl(camera):
    while True:
        try:
            crawl(camera)
        except Exception as ex:
            print("error camera {}: {}, restarting".format(camera["name"], ex))
            time.sleep(config["retry_interval"])

def main():
    global config
    config = load_config()
    threads = []
    for camera in config["cameras"]:
        try:
           thread = threading.Thread(target=infinity_crawl, args=(camera,))
           thread.start()
        except Exception as ex:
            print("error when processing camera {}: {}".format(
                camera["name"], ex))


if __name__ == "__main__":
    main()

