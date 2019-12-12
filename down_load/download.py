import requests
import time
import sys

from threading import Thread


def print_process(p_size, size, content_size, chunk_size):
    block_num = int(int(size / content_size * 100) * 0.8)
    persent = round(float((size / content_size) * 100), 2)
    speed = round(float((size - p_size) / chunk_size ** 2), 2)
    process_bar = '█' * block_num + f' {persent}%, {speed}MB/s' + '\r'
    sys.stdout.write(process_bar)
    sys.stdout.flush()
    if int(persent) == 100:
        sys.stdout.write(process_bar)
        sys.stdout.flush()
        print()


def get_vedio():
    start = time.time()
    url = 'https://rbv01.ku6.com/wifi/o_1cv2emaj71icj1g0270jq8oqfp13kvs'
    try:
        size = 0
        response = requests.get(url, stream=True)
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        print(f'文件大小{round(float(content_size / chunk_size ** 2), 2)}MB')
        with open('v1.mp3', 'wb') as f:
            s_time = time.time()
            p_size = 0
            for data in response.iter_content(chunk_size):
                f.write(data)
                size += len(data)
                if (time.time() - s_time >= 1):
                    print_process(p_size, size, content_size, chunk_size)
                    s_time = time.time()
                    p_size = size
        print_process(p_size, size, content_size, chunk_size)
        download_time = round(time.time() - start, 2)
        print(f'下载完成，耗时{download_time}秒, 平均速度为:{round(float(content_size / download_time / chunk_size ** 2), 2)}MB/s')
    except Exception as e:
        print(e.args)

    
if __name__ == "__main__":
    get_vedio()
