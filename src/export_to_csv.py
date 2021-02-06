#!/usr/bin/env python3

import glob
import csv
import re

list_files = glob.glob("result/*")
posts = []

for f in list_files:
    with open(f,'r') as file:
        post = file.read()
        first_line = post.split('\n', 1)[0]
        post = post.replace("\n", "<br>")
        m = re.search('^(.{60}.*?)(\s|$)', first_line)		
        if m:
            title = m.group(1) + "..."
        else:
            title = first_line
        posts.append([title, post])
  

with open('export.csv','w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    csv_writer.writerow(['title', 'post'])
    for p in posts:
        csv_writer.writerow(p)

