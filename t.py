
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

load_dotenv()

max_length = 7
min_length = 5
target_submissions = 70000
metadata_csv_path = "image_metadata1.csv"


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
    hist_path = f"history1/{name}.csv"

    if not os.path.exists("history1"):
        os.makedirs("history1")

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
        hist_path = f"history1/{name}.csv"

        with open(hist_path, newline="", encoding="utf-8-sig") as hist_file:
            hist_reader = csv.reader(hist_file)
            return [row for row in hist_reader]
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

def exponential_backoff(retries):
    """Calculate wait time based on the number of retries."""
    return min(2 ** retries, 60)  # Cap the wait time at 60 seconds

last_post_name = None

for subreddit_name in subreddit_list:
    
    retries = 0

    # text = nltk.corpus.gutenberg.raw('shakespeare-hamlet.txt')
    # freq_dist = FreqDist(word.lower() for word in nltk.word_tokenize(text))
    # popular_words = freq_dist.most_common()
    # word_list = [word for word in words.words() if min_length <= len(word) <= max_length]

    print(f"======== <{subreddit_name}> ========")

    processed_submissions = set()
    [processed_submissions.add(row[1]) for row in read_hist_row(subreddit_name)]

    flag = True

    while len(processed_submissions) < target_submissions:
        try:
            subreddit = reddit.subreddit(subreddit_name)

            # keyword = random.choice(popular_words)[0]
            # keyword = random.choice(word_list)

            submissions = subreddit.new(limit=None, params={'after': last_post_name})
            
            print("--------", len(processed_submissions))

            for submission in submissions:
                last_post_name = submission.fullname
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
            print(f"Rate limit exceeded for subreddit <{subreddit_name}>: {e}")
            wait_time = exponential_backoff(retries)
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retries += 1  # Increment the retry counter
        except Exception as e:
            print(f"Error processing subreddit <{subreddit_name}>: {e}")
            time.sleep(20)
            continue
