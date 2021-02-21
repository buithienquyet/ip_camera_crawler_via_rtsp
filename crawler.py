import os
import json
import subprocess
import shlex


def load_config():
    with open("config.json") as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    config = load_config()
    for camera in config["cameras"]:
        try:
            if camera["protocal"] == "rtsp":
                rtsp_url = "{}://{}:{}@{}:{}{}".format(
                    camera["protocal"], camera["account"], camera["password"], camera["ip"], camera["port"], camera["sub_url"])
                video_path = os.path.join(config["data_path"], camera["name"])
                if not os.path.exists(video_path):
                    os.mkdir(video_path)
                cmd = "ffmpeg -i {} -c copy -f segment -reset_timestamps 1 -strftime 1 -segment_time {} \"{}/%Y_%m_%d_%H-%M-%S.mp4\"".format(
                    rtsp_url, config["video_duration"], video_path)
                subprocess.Popen(shlex.split(cmd))
        except Exception as ex:
            print("error when processing camera {}: {}".format(
                camera["name"], ex))
