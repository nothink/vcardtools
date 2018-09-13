import requests
import re

files_path = '../files'
targets_path = './log/targets'
ignores_path = './log/ignores'
proxies = {
    'http': 'verenav.seio.club:21494'
}
patterns = [
    r"^stat100\.ameba\.jp/vcard/ratio20/images/card/([0-9a-f]*)\.jpg",
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

targets = open(targets_path, mode='w')
ignores = open(ignores_path, mode='w')

hash_set = set()
for ptn in patterns:
    for match in re.finditer(ptn, files):
        hash_set.add(match.group(1))

for hash in list(hash_set):
    idx = list(hash_set).index(hash) + 1
    print('[' + str(idx) + '/' + str(len(hash_set)) + '] ' + hash)
    for url in urls:
        tgt = url.format(hash)
        r = requests.head('http://' + tgt)
        if r.status_code == requests.codes.ok:
            targets.write(tgt + '\n')
            targets.flush()
        else:
            print(str(r.status_code) + ': ' + tgt)
            ignores.write(str(r.status_code) + ': ' + tgt + '\n')
            ignores.flush()
targets.close()
ignores.close()
