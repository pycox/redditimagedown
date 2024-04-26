from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# from bs4 import BeautifulSoup
# import requests
import time

import csv
import os

metadata_csv_path = "image_metadata.csv"


def add_data_row(row):
    if not os.path.exists(metadata_csv_path):
        with open(
            metadata_csv_path, mode="w", newline="", encoding="utf-8-sig"
        ) as metadata_file:
            metadata_writer = csv.writer(metadata_file)

            metadata_writer.writerow(
                [
                    "author",
                    "author_id",
                    "subreddit",
                    "content_id",
                    "title",
                    "href",
                    "comment",
                    "createAt",
                    "upvote",
                ]
            )

    with open(
        metadata_csv_path, mode="a", newline="", encoding="utf-8-sig"
    ) as metadata_file:
        metadata_writer = csv.writer(metadata_file)

        metadata_writer.writerow(row)


def main():
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.reddit.com/r/AbandonedPorn")

    last_height = 0
    last_len = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # for i in range(2000):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #     time.sleep(2)
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height

        items = driver.find_elements(By.CSS_SELECTOR, "article")

        for item in items[last_len:]:
            dom = item.find_element(By.CSS_SELECTOR, "shreddit-post")
            author = dom.get_attribute("author")
            author_id = dom.get_attribute("author-id")
            subreddit = dom.get_attribute("subreddit-prefixed-name")
            content_id = dom.get_attribute("id")
            href = dom.get_attribute("content-href")
            title = dom.get_attribute("post-title")
            comment = dom.get_attribute("comment-count")
            createAt = dom.get_attribute("created-timestamp")
            upvote = dom.get_attribute("score")

            add_data_row(
                [
                    author,
                    author_id,
                    subreddit,
                    content_id,
                    title,
                    href,
                    comment,
                    createAt,
                    upvote,
                ]
            )


        print(len(items))

        last_len = len(items)
    driver.quit()


main()
