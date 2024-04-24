from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# from bs4 import BeautifulSoup
# import requests
import time

# import csv
# import os


def main():
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.reddit.com/r/AbandonedPorn")

    last_height = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # for i in range(5):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, "article")

    for item in items:
        dom = item.find_element(By.CSS_SELECTOR, "shreddit-post")
        author = dom.get_attribute("author")
        author_id = dom.get_attribute("author-id")
        subreddit = dom.get_attribute("subreddit-prefixed-name")
        subreddit_id = dom.get_attribute("subreddit-id")
        href = dom.get_attribute("content-href")
        title = dom.get_attribute("post-title")
        comment = dom.get_attribute("comment-count")
        createAt = dom.get_attribute("created-timestamp")
        upvote = dom.get_attribute("score")

        print(
            [
                author,
                author_id,
                subreddit,
                subreddit_id,
                title,
                href,
                comment,
                createAt,
                upvote,
            ]
        )
        
        
    print(len(items))

    driver.quit()


main()
