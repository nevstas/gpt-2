#!/usr/bin/env python3

import glob
import csv
import re
import urllib.request
import json

list_files = glob.glob("result/*")
posts = []

is_translate = True #True - enalbe translate, False - disable translate
translate_apikey = "4bd8ecae-24e7-4df9-8747-3230ce9abe6c"
translate_lang = "ru" #Supported: ar, bn, bg, zh-hans, hr, cs, da, nl, et, fi, fr, de, el, he, hi, is, id, it, ja, ko, lv, lt, ms, no, ps, fa, pl, pt, ro, ru, sk, sl, es, sv, th, tr, uk, ur, vi, cy

def translate(text, from_lang, to_lang):
    global translate_apikey
    #https://api-platform.systran.net/translation/text/translate?key=4bd8ecae-24e7-4df9-8747-3230ce9abe6c&source=en&target=ru&input=hello
    params = urllib.parse.urlencode({"key": translate_apikey, "source": from_lang, "target": to_lang, "input": text})
    request = urllib.request.Request("https://api-platform.systran.net/translation/text/translate?" + params)
    response = urllib.request.urlopen(request)
    response_json = response.read()
    response_obj = json.loads(response_json)
    return response_obj['outputs'][0]['output']


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

        if is_translate:
            post = translate(post, "en", translate_lang)
        post = post.replace("\n", "<br>")
        if not title:
            if is_translate:
                first_line = translate(first_line, "en", translate_lang)
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

