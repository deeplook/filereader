#!/usr/bin/env python

"""
A super-crude textfile reader using Apple's say tool on Mac OS X.

For further information please read the README.rst file.
"""

import re
import os
import sys
import json
import time
import subprocess


# some hardwired stuff, that might become more flexible later

VOICE = 'Bruce' # find all voices with 'say -v ?'
RATE = 210 # words per minute
BOOKMARKS_FILE = 'bookmarks.json' # e.g. {'ch00.txt': {'para_num': 23}}


def clean_para(para):
    "Clean Markdown-like format... only very basic stuff done."

    # comments
    m = re.search('^// ', para)
    if m:
        return ''

    # bookmarks (internal)
    m = re.search('^\.bookmark ', para)
    if m:
        return ''

    # headlines
    m = re.search('^\++', para)
    if m:
        time.sleep(1)
        return para[m.end():].strip()

    # full paragraph citations
    if para.startswith('> '):
        time.sleep(1)
        return para[1:].strip()

    # remove hyperlink targets, e.g. [target foo bar] -> foo bar
    link_pat = '\[(.*)\]'
    if re.search(link_pat, para):
        repl = lambda m: ' '.join(m.groups()[0].split()[1:])
        para = re.sub(link_pat, repl, para)

    return para


def read_paras(path):
    "Read paragraphs of a text file (using Apple's 'say' tool)."

    f = open(path)
    paras = f.read().split('\n')
    paras = [p for p in paras if p.strip()]
    f.close()

    # bookmarking
    try:
        js = json.load(open(BOOKMARKS_FILE))
    except IOError:
        js = {}
    base = os.path.basename(path)
    if not base in js:
        js[base] = {}
    if not 'para_num' in js[base]:
        js[base]['para_num'] = 0
    start = js[base]['para_num']

    # read paragraphs
    for i, p in enumerate(paras[start:]):
        # print('({}) {}'.format(start + i, p))
        p = clean_para(p)
        if not p:
            continue
        print('({}) {}'.format(start + i, p))
        print('')
        cmd = 'say -v {} -r {}'.format(VOICE, RATE)
        try:
            subprocess.check_output(cmd.split(' ') + ["%s" % p])
            time.sleep(0.4)
        except KeyboardInterrupt:
            # bookmarking
            js[base]['para_num'] = start + i
            json.dump(js, open(BOOKMARKS_FILE, 'w'), indent=4)
            msg = '\nCreated/updated bookmark to para #{} for file "{}" in {}.'
            print(msg.format(js[base]['para_num'], path, BOOKMARKS_FILE))
            break


def test():
    "Test this on the book 'Social Architecture' by Pieter Hintjens."

    url = 'https://github.com/hintjens/socialarchitecture/archive/master.zip'
    basename = os.path.basename(url)
    if not os.path.exists(basename):
        import requests
        data = requests.get(url).content
        open(basename, 'wb').write(data)
    root = 'socialarchitecture-master'
    if not os.path.exists(root):
        subprocess.check_output(['unzip', basename])
    for name in sorted(os.listdir(root)):
        if re.match('ch\d+\.txt', name):
            path = os.path.join(root, name)
            print(path)
            read_paras(path)


if __name__ == '__main__':
    try:
        path = sys.argv[1]
        if path == '-t':
            test()
        else:
            read_paras(path)
    except IndexError:
        print('Usage: filereader.py <textfile>')
        print('       filereader.py -t')
        print('Stop with ctrl-c.')
