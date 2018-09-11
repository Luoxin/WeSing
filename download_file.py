from contextlib import closing
import requests
from tqdm import tqdm

def download_file(self, url, fileName):
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        # content_size = int(response.headers['content-length'])  # 内容体总大小
        with open(fileName, "wb") as file:
            for data in tqdm(response.iter_content(chunk_size=chunk_size)):
                file.write(data)
    print(f"{fileName}下载完成")