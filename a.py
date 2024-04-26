import praw
import prawcore
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
import random
from nltk.probability import FreqDist
from nltk.corpus import words
import time
import nltk
import multiprocessing
import threading
import signal

load_dotenv()

max_length = 7
min_length = 5
target_submissions = 70000
metadata_csv_path = "image_metadata.csv"


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    # username=username,
    # password=password,
)

reddit.read_only = True


with open("sub_list.csv", newline="", encoding="utf-8-sig") as csvfile:
    csvreader = csv.reader(csvfile)
    subreddit_list = [row[0] for row in csvreader]


def add_hist_row(name, row):
    hist_path = f"history/{name}.csv"

    if not os.path.exists("history"):
        os.makedirs("history")

    if not os.path.exists(hist_path):
        with open(hist_path, mode="w", newline="", encoding="utf-8-sig") as hist_file:
            hist_writer = csv.writer(hist_file)
            hist_writer.writerow(row)
    else:
        with open(hist_path, mode="a", newline="", encoding="utf-8-sig") as hist_file:
            hist_writer = csv.writer(hist_file)
            hist_writer.writerow(row)


def read_hist_row(name):
    try:
        hist_path = f"history/{name}.csv"

        with open(hist_path, newline="", encoding="utf-8-sig") as hist_file:
            hist_reader = csv.reader(hist_file)
            return [row for row in hist_reader]
    except UnicodeDecodeError:
        encodings = ['utf-8', 'latin1', 'cp1252']  # Add more encodings if needed
        for encoding in encodings:
            try:
                with open(hist_path, newline="", encoding=encoding) as hist_file:
                    hist_reader = csv.reader(hist_file)
                    return [row for row in hist_reader]
            except UnicodeDecodeError:
                continue
    except:
        return []


def add_data_row(row):
    if not os.path.exists(metadata_csv_path):
        with open(
            metadata_csv_path, mode="w", newline="", encoding="utf-8-sig"
        ) as metadata_file:
            metadata_writer = csv.writer(metadata_file)

            metadata_writer.writerow(
                [
                    "subreddit",
                    "id",
                    "image_url",
                    "author",
                    "caption",
                    "up_votes",
                    "num_comments",
                    "time",
                ]
            )

    with open(
        metadata_csv_path, mode="a", newline="", encoding="utf-8-sig"
    ) as metadata_file:
        metadata_writer = csv.writer(metadata_file)

        metadata_writer.writerow(row)
        

def fetch_subreddit(subreddit_name):
    # text = nltk.corpus.gutenberg.raw('shakespeare-hamlet.txt')
    # freq_dist = FreqDist(word.lower() for word in nltk.word_tokenize(text))
    # popular_words = freq_dist.most_common()
    word_list = [
        word for word in words.words() if min_length <= len(word) <= max_length
    ]

    print(f"======== <{subreddit_name}> ========")

    processed_submissions = set()
    [processed_submissions.add(row[1]) for row in read_hist_row(subreddit_name)]

    flag = True

    while len(processed_submissions) < target_submissions:
        try:
            subreddit = reddit.subreddit(subreddit_name)

            # keyword = random.choice(popular_words)[0]
            keyword = random.choice(word_list)

            if flag:
                submissions = subreddit.hot(limit=1000)
                flag = False
            else:
                submissions = subreddit.search(keyword, limit=None)

            for submission in submissions:
                if (
                    "i.redd.it" in submission.url
                    and submission.id not in processed_submissions
                ):
                    created_at = datetime.utcfromtimestamp(
                        submission.created_utc
                    ).strftime("%Y-%m-%d %H:%M:%S")

                    row = [
                        subreddit_name,
                        submission.id,
                        submission.url,
                        submission.author,
                        submission.title,
                        submission.score,
                        submission.num_comments,
                        created_at,
                    ]

                    add_data_row(row)
                    add_hist_row(subreddit_name, row)

                    processed_submissions.add(submission.id)

            if len(processed_submissions) == 0:
                break

        except prawcore.exceptions.TooManyRequests as e:
            time.sleep(4)
        except Exception as e:
            print(f"Error processing subreddit <{subreddit_name}>: {e}")
            time.sleep(4)
            continue

def signal_handler(signal, frame):
    print('Stopping the script...')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
        
def main():
    threads = []
    for subreddit_name in subreddit_list:
        thread = threading.Thread(target=fetch_subreddit, args=(subreddit_name,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
