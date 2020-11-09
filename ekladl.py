# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib3.request
import certifi
import sys
import os
import re


def download_file(url, path):
    chunk_size = 4096
    r = http.request('GET', url, preload_content=False)

    with open(path, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)

    r.release_conn()

url = sys.argv[1]

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

source = BeautifulSoup(http.request("GET", url).data, "html.parser")

title = source.find("title").text
print(title)
title = re.sub(r'[\\/\:*"<>\|\.%\$\^&£]', '', title)

if not os.path.exists(path):
    os.makedirs(path)

article = source.find("div", {"class": "article_text"})

links = article.find_all("a")

i = 0

print("Found " + str(len(links)))
sys.stdout.flush()

for link in links:
    img = link.find("img")
    if img is not None:
        print("Downloading " + str(i).zfill(3)+".jpg")
        sys.stdout.flush()
        download_file(link["href"], title+"/"+str(i).zfill(3)+".jpg")
        i+=1
