import requests
# import random

stands_path = './log/stands'
not_stands_path = './log/not_stands'

urls = [
    'c.stat100.ameba.jp/vcard/ratio20/images/animation/mypage/loginbonus/girl_left/card_{0}.png',
    'c.stat100.ameba.jp/vcard/ratio20/images/animation/mypage/loginbonus/girl_right/card_{0}.png',
    'c.stat100.ameba.jp/vcard/ratio20/images/loginbonus/daily/common/animation/girl/left/card_{0}.png',
    'c.stat100.ameba.jp/vcard/ratio20/images/loginbonus/daily/common/animation/girl/right/card_{0}.png',
]

stands = open(stands_path, mode='w')
not_stands = open(not_stands_path, mode='w')

list = range(1, 12000)
# ramdom.shuffle(list)
for i in list:
    print('[' + str(i) + ']')
    for url in urls:
        tgt = url.format(str(i))
        r = requests.head('http://' + tgt)
        if r.status_code == requests.codes.ok:
            stands.write(tgt + '\n')
            stands.flush()
        else:
            print(str(r.status_code) + ': ' + tgt)
            not_stands.write(str(r.status_code) + ': ' + tgt + '\n')
            not_stands.flush()
stands.close()
not_stands.close()
