import time
import datetime
import os
import json

sleep_time = 60*60


def load_config():
    with open("config.json") as f:
        data = json.load(f)
        return data


def clear():
    config = load_config()
    now = datetime.datetime.now()
    now_timestamp = datetime.datetime.timestamp(now)
    clean_cnt = 0

    print('processing at '+ now)
    for camera in config["cameras"]:
        try:
            video_path = os.path.join(config["data_path"], camera["name"])
            for filename in os.listdir(video_path):
                file_path = os.path.join(video_path, filename)
                stat = os.stat(file_path)
                diff_time = now_timestamp - stat.st_ctime
                if (diff_time > config["store_time"]):
                    clean_cnt += 1
                    print('cleaning' + filename)
                    os.remove(file_path)
        except Exception as ex:
            print("error when processing camera {}: {}".format(
                camera["name"], ex))
    if clean_cnt>0:
        print('total clean: '+ clean_cnt)
    else:
        print('no files to clean')


if __name__ == "__main__":
    while True:
        clear()
        time.sleep(sleep_time)
