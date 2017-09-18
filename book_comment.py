import requests
from bs4 import BeautifulSoup
from wd_show import wd_show

def get_soup(url):
    headers = {
        'user_agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2595.400 QQBrowser/9.6.10872.400'}
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, 'lxml')
    return soup

def get_next_page(soup):
    comment_url = 'https://book.douban.com/subject/1002299/comments/'
    paras = soup.select('ul.comment-paginator > li.p > a.page-btn')
    if len(paras) == 1:
        para = paras[0]['href']
        next_page = comment_url + para
    else:
        para = paras[2]['href']
        next_page = comment_url + para
    return next_page

def parse_comment(soup):
    comments = ''
    ps = soup.select('li > div.comment > p')
    for p in ps:
        comment = p.get_text()
        comments += comment
    return comments

def main():
    url = 'https://book.douban.com/subject/1002299/'
    comment_url = 'https://book.douban.com/subject/1002299/comments/'
    comments = ''
    soup = get_soup(comment_url)
    comment = parse_comment(soup)
    comments += comment

    for i in range(20):
        next_page = get_next_page(soup)
        print(next_page)
        soup = get_soup(next_page)
        comment = parse_comment(soup)
        comments += comment

    # with open(r'./data/xajh.txt', 'w', encoding='gbk', errors='ignore') as f:
    #     f.write(comments)

    wd_show(comments)

if __name__ == '__main__':
    main()
