import requests
import lxml.html
import datetime
from natsort import natsorted, ns
import MySQLdb
import re

def main():
    '''
    メイン処理
    '''
    session = requests.Session()
    res = session.get('http://gfkari.gamedbs.jp/')
    urls = get_girl_urls(res)
    nat_urls = natsorted(urls)
    for url in nat_urls:
        print(url)
        res = session.get(url)
        print(get_girl(res))
        break

def get_girl_urls(res):
    '''
    個別ページのURLを取得する
    '''
    root = lxml.html.fromstring(res.content)
    root.make_links_absolute(res.url)
    urls = []
    for anker in root.cssselect('#girls li a[class="girl-link"]'):
        url = anker.get('href')
        if '9999' in url:
            continue
        urls.append(url)
    return urls

def get_girl(res):
    '''
    個別ページからガール情報をDictionaryで取得する
    '''
    root = lxml.html.fromstring(res.content)

    title_name = root.cssselect('#bside div.gf_headline')[0].text.strip()
    school = get_girl_info_text(root, 3, '学園')
    grade = get_girl_info_text(root, 4, '学年')
    classroom = get_girl_info_text(root, 5, 'クラス')
    club = get_girl_info_text(root, 6, '部活')
    age = get_girl_info_text(root, 7, '年齢')
    birthday = get_girl_info_text(root, 8, '誕生日')
    star_sign = get_girl_info_text(root, 9, '星座')
    blood_type = get_girl_info_text(root, 10, '血液型')
    height = get_girl_info_text(root, 11, '身長')
    weight = get_girl_info_text(root, 12, '体重')
    three_size = get_girl_info_text(root, 13, '3サイズ')
    bust = three_size.split('/')[0][1:] if three_size else None
    waist = three_size.split('/')[1][1:] if three_size else None
    hip = three_size.split('/')[2][1:] if three_size else None
    hobby = get_girl_info_text(root, 14, '趣味')
    favorite_food = get_girl_info_text(root, 15, '好きな食べ物')
    hated_food = get_girl_info_text(root, 16, '嫌いな食べ物')
    favorite_subject = get_girl_info_text(root, 17, '得意科目')
    voice_actor = get_girl_info_text(root, 18, 'CV')
    hitokoto_id = get_girl_info_text(root, 19, 'ツイート名')
    introduction = get_girl_introduction(root)

    dic = {
        'girl_number': int(res.url[res.url.rfind('/')+1:]),
        'name': title_name[:title_name.find('(')-1].strip(),
        'kana': title_name[title_name.find('(')+1:title_name.find(')')].strip(),
        'school': school,
        'grade': int(re.compile(r'[1-3]').search(grade).group(0))
                        if grade and re.compile(r'[1-3]').search(grade) is not None else None,
        'grade_txt': grade,
        'classroom': classroom,
        'club': club,
        'age': int(age[:2]) if age and age[2:3] in ['才', '歳'] else None,
        'birthday': datetime.date(2012,
                        int(birthday[:birthday.find('月')].strip()),
                        int(birthday[birthday.find('月')+1:birthday.find('日')].strip()))
                            if birthday and birthday[2:3] == '月' else None,
        'star_sign': star_sign if star_sign and star_sign[-1:] == '座' else None,
        'blood_type': blood_type[:-1] if blood_type and blood_type[-1:] == '型' else None,
        'height': int(height[:3]) if height and height[3:5] == 'cm' else None,
        'weight': int(weight[:2]) if weight and weight[2:4] == 'kg' else None,
        'bust': int(bust) if bust and bust.isdigit() else None,
        'waist': int(waist) if waist and waist.isdigit() else None,
        'hip': int(hip) if hip and hip.isdigit() else None,
        'hobby': hobby,
        'favorite_food': favorite_food,
        'hated_food': hated_food,
        'favorite_subject': favorite_subject,
        'voice_actor': voice_actor,
        'hitokoto_id': hitokoto_id,
        'introduction': introduction,
    }

    return dic

# テキスト抜き出し
def get_girl_info_text(root, cell_no, heading):
    '''
    gfkari.gamedbs.jpの個別ページにあるガールのテーブル内部テキストを抜き出す
    '''
    ths = root.cssselect('#bside div.profile-dat table.bcinf tr:nth-child(' + str(cell_no) + ') th')
    if ths[0].text.strip() != heading:
        raise Exception('unknow header: ' + heading)
    tds = root.cssselect('#bside div.profile-dat table.bcinf tr:nth-child(' + str(cell_no) + ') td')

    if len(tds) > 1:
        raise Exception('unknown string: ' + str(tds))
    elif len(tds) == 0:
        return None
    elif len(tds[0].getchildren()) == 0:
        last_text = tds[0].text.strip()
    elif len(tds[0].getchildren()) == 1 and tds[0].getchildren()[0].tag == 'a':
        last_text = tds[0].getchildren()[0].text.strip()
    elif len(tds[0].getchildren()) > 0 and tds[0].getchildren()[0].tag == 'br':
        for br in tds[0].cssselect('br'):
            br.tail = '\n' + br.tail if br.tail else '\n'
        last_text = tds[0].text_content().strip()
    elif len(tds[0].getchildren()) == 1 and tds[0].getchildren()[0].tag == 'img':
        last_text = tds[0].text_content().strip()
    else:
        raise Exception('unknown string: ' + str(tds[0].getchildren()))

    return None if last_text == '???' else last_text

def get_girl_introduction(root):
    '''
    gfkari.gamedbs.jpの個別ページにあるガールの説明テキストを抜き出す
    '''
    tr20_child = root.cssselect('#bside div.profile-dat table.bcinf tr:nth-child(20)')[0].getchildren()[0]
    tr21_child = root.cssselect('#bside div.profile-dat table.bcinf tr:nth-child(21)')[0].getchildren()[0]
    tr22_child = root.cssselect('#bside div.profile-dat table.bcinf tr:nth-child(22)')[0].getchildren()[0]
    if tr20_child.tag == 'th' and tr20_child.text.strip() == '紹介文' and tr21_child.tag == 'td':
        td = tr21_child
    elif tr21_child.tag == 'th' and tr21_child.text.strip() == '紹介文' and tr22_child.tag == 'td':
        td = tr22_child

    if len(td.getchildren()) > 0 and td.getchildren()[0].tag == 'br':
        for br in td.cssselect('br'):
            br.tail = '\n' + br.tail if br.tail else '\n'
        last_text = td.text_content().strip()

    return last_text

# main呼び出し
if __name__ == '__main__':
    main()
