import requests
import re
import time

files_path = '../files'
proxies = {
    'http': 'verenav.seio.club:21494'
}
patterns = [
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/animation/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/battle/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/collection/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/icon/([0-9a-f]*)\.png",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/icon/collection/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/list/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/mid/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/mypage/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/off/([0-9a-f]*)\.png",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/profile/([0-9a-f]*)\.jpg",
    r"c\.stat100\.ameba\.jp/vcard/ratio20/images/card/profile/off/([0-9a-f]*)\.png",
]
urls = [
    'stat100.ameba.jp/vcard/ratio20/images/card/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/animation/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/battle/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/collection/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/icon/{0}.png',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/icon/collection/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/list/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/mid/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/mypage/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/off/{0}.png',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/profile/{0}.jpg',
    'c.stat100.ameba.jp/vcard/ratio20/images/card/profile/off/{0}.png',
]

with open(files_path) as f:
    files = f.read()

hash_set = set()
for ptn in patterns:
    for match in re.finditer(ptn, files):
        hash_set.add(match.group(1))

i = 0
for hash in list(hash_set):
    print('[' + str(i) + '/' + str(len(hash_set)) + '] ' + hash)
    for url in urls:
        r = requests.get('http://' + url.format(hash), proxies=proxies)
#        if r.status_code != requests.codes.ok:
#            print(str(r.status_code) + ': ' + r.url)
    i += 1
#        time.sleep(0.1)
