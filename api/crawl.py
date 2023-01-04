import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'news.settings'
django.setup()

from api.models import CommentPost, NewsPost

def crawl_data():
    for i in range(1,30):
        print(f"Trang {i}")
        if i == 1:
            url = "https://vnexpress.net/giao-duc/tin-tuc"
        else:
            url = f"https://vnexpress.net/giao-duc/tin-tuc-p{i}"
        req = requests.get(url, 'html.parser')
        soup = BeautifulSoup(req.content, 'html.parser')
        contents = soup.findAll("article", {"class": "item-news"})
        for content in contents:
            content_div = content.find("h2", {"class": "title-news"})
            if content_div:
                content_a = content_div.find("a", href=True)
                detail_req = requests.get(content_a.get("href"), 'html.parser')
                detail_soup = BeautifulSoup(detail_req.content, 'html.parser')
                content_id =  detail_soup.find("section", {"class": "page-detail"}).attrs['data-component-config']
                article_id = json.loads(content_id).get("article_id",0)
                
                h1_title = detail_soup.find("h1", {"class": "title-detail"})
                description = detail_soup.find("article", {"class": "fck_detail"})
                if h1_title and description:
                    h1_title = h1_title.text
                    description = description.text
                    news_post = NewsPost.objects.create(
                        title=h1_title.strip(),
                        content=description.strip(),
                        article_id=article_id
                    )
                    if content_id:
                        get_comment(int(article_id), news_post)


def get_comment(article_id, news_post):
    try:
        req = requests.get(url=f"https://usi-saas.vnexpress.net/index/get?objectid={article_id}&objecttype=1&siteid=1000000&usertype=4")
        res = req.json()
        comments = res['data'].get("items")
        if comments:
            for comment in comments:
                CommentPost.objects.create(
                    post_id=news_post,
                    author=comment.get("full_name",""),
                    content=comment.get("content", ""),
                )
                # insert_comment(comment.get("full_name",""), comment.get("content", ""), article_id)
    except Exception as e:
        print(e)


def main():
    while True:
        try:
            crawl_data()
        except Exception as e:
            print(e)
        time.sleep(1)

main()