#!/usr/bin/env python3

import glob
import csv
import re

list_files = glob.glob("result/*")
posts = []

for f in list_files:
    with open(f,'r', encoding='utf-8') as file:
        category = ''
        title = ''
        post = file.read()
        first_line = post.split('\n', 1)[0]
        m = re.search('^param=(.*?)$', first_line)    
        if m:
            params = m.group(1).split('|')
            for param in params:
                param_arr = param.split(':')
                param_name = param_arr[0]
                param_value = param_arr[1]
                if param_name == 'category':
                    category = param_value
                elif param_name == 'title':
                    title = param_value

            post = 'n'.join(post.split('n')[1:])
            first_line = post.split('\n', 1)[0]

        post = post.replace("\n", "<br>")
        if not title:
            m = re.search('^(.{60}.*?)(\s|$)', first_line)        
            if m:
                title = m.group(1) + "..."
            else:
                title = first_line
        posts.append([title, post, category])
  

with open('export.csv','w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    csv_writer.writerow(['title', 'post', 'category'])
    for p in posts:
        csv_writer.writerow(p)

