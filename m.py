# import praw
# import os
# from dotenv import load_dotenv
# import csv
# from datetime import datetime
# import random
# from nltk.corpus import words

# load_dotenv()

# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# user_agent = os.getenv("USER_AGENT")
# username = os.getenv("USERNAME")
# password = os.getenv("PASSWORD")

# # Set up PRAW with your credentials
# reddit = praw.Reddit(
#     client_id=client_id,
#     client_secret=client_secret,
#     user_agent=user_agent,
#     # username=username,
#     # password=password,
# )

# reddit.read_only = True

# # Open the CSV file for writing metadata
# metadata_csv_path = "image_metadata.csv"
# with open(metadata_csv_path, mode="w", newline="") as metadata_file:
#     metadata_writer = csv.writer(metadata_file)
#     # Write the header row
#     metadata_writer.writerow(
#         ["subreddit", "id", "image_url", "caption", "up_votes", "time"]
#     )

#     # Open the CSV file with subreddit list
#     with open("sub_list.csv", newline="") as csvfile:
#         csvreader = csv.reader(csvfile)
#         subreddit_list = [row[0] for row in csvreader]

#     for subreddit_name in subreddit_list:
#         try:
#             subreddit = reddit.subreddit(subreddit_name)
#             print(f"======== Starting <{subreddit_name}> ========")

#             # Get a list of 5-character English words
#             word_list = [word for word in words.words() if len(word) == 5]

#             # Retrieve up to 10,000 submissions
#             submission_count = 0
#             after = None
#             while submission_count < 10000:
#                 # Search for submissions containing a random word
#                 random_word = random.choice(word_list)
#                 search_results = subreddit.search(random_word, limit=1000, after=after)

#                 # Process the search results and write to the CSV file
#                 for submission in search_results:
#                     try:
#                         # Convert time from UTC to a readable format
#                         time = datetime.utcfromtimestamp(
#                             submission.created_utc
#                         ).strftime("%Y-%m-%d %H:%M:%S")
#                         # Write metadata to the CSV file
#                         row = [
#                             subreddit_name,
#                             submission.id,
#                             submission.url,
#                             submission.title,  # Assuming the title is the caption
#                             submission.score,  # The number of upvotes
#                             time,
#                         ]
#                         metadata_writer.writerow(row)
#                         print(row)
#                         submission_count += 1
#                     except Exception as e1:
#                         print(f"Error processing submission <{submission}>: {e1}")

#                 # Get the last submission's ID to use as the `after` parameter
#                 after = search_results[-1].id if search_results else None

#                 if not search_results or submission_count >= 10000:
#                     break
#         except Exception as e:
#             print(f"Error processing subreddit <{subreddit_name}>: {e}")


# import praw
# import os
# from dotenv import load_dotenv
# import csv
# from datetime import datetime
# import random
# from nltk.corpus import words
# import time

# load_dotenv()

# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# user_agent = os.getenv("USER_AGENT")
# username = os.getenv("USERNAME")
# password = os.getenv("PASSWORD")

# # Set up PRAW with your credentials
# reddit = praw.Reddit(
#     client_id=client_id,
#     client_secret=client_secret,
#     user_agent=user_agent,
#     # username=username,
#     # password=password,
# )

# reddit.read_only = True


# def get_random_word(length=6):
#     # Get a list of all English words
#     word_list = [word for word in words.words() if len(word) == length]

#     # Choose a random word from the list
#     random_word = random.choice(word_list)

#     return random_word


# # Open the CSV file for writing metadata
# metadata_csv_path = "image_metadata.csv"
# with open(metadata_csv_path, mode="w", newline='', encoding='utf-8-sig') as metadata_file:
#     metadata_writer = csv.writer(metadata_file)
#     # Write the header row
#     metadata_writer.writerow(
#         ["subreddit", "id", "image_url", "caption", "up_votes", "time"]
#     )

#     # Open the CSV file with subreddit list
#     with open("sub_list.csv", newline='', encoding='utf-8-sig') as csvfile:
#         csvreader = csv.reader(csvfile)
#         subreddit_list = [row[0] for row in csvreader]

#     for subreddit_name in subreddit_list:
#         try:
#             subreddit = reddit.subreddit(subreddit_name)
#             print(f"======== Starting <{subreddit_name}> ========")

#             # Retrieve up to 10,000 submissions
#             submission_count = 0
#             search_results = None
#             # Set the target number of submissions to retrieve
#             target_submissions = 10000

#             # Keep track of the processed submission IDs to avoid duplicates
#             processed_submissions = set()

#             while len(processed_submissions) < target_submissions:

#                 # Search for submissions using the random search term
#                 keyword = get_random_word()
#                 submissions = subreddit.search(keyword, limit=None)
#                 print("--------", keyword, len(processed_submissions))
#                 for submission in submissions:
#                     try:
#                         if (
#                             "i.redd.it" in submission.url
#                             and submission.id not in processed_submissions
#                         ):
#                             # Convert time from UTC to a readable format
#                             time = datetime.utcfromtimestamp(
#                                 submission.created_utc
#                             ).strftime("%Y-%m-%d %H:%M:%S")

#                             # Write metadata to the CSV file
#                             row = [
#                                 subreddit_name,
#                                 submission.id,
#                                 submission.url,
#                                 submission.title,  # Assuming the title is the caption
#                                 submission.score,  # The number of upvotes
#                                 time,
#                             ]
#                             metadata_writer.writerow(row)

#                             # Add the processed submission ID to the set
#                             processed_submissions.add(submission.id)
#                     except praw.exceptions.APIException as e:
#                         if e.error_type == "RATELIMIT":
#                             # Extract delay time from the error message
#                             delay = float(e.message.split(" ")[-1])
#                             print(f"Rate limit exceeded. Sleeping for {delay} seconds.")
#                             time.sleep(delay)
#                         else:
#                             raise  # Re-raise the exception if it's not a RateLimit exception

#         except Exception as e:
#             print(f"Error processing subreddit <{subreddit_name}>: {e}")


import praw
import prawcore
import os
from dotenv import load_dotenv
import csv
from datetime import datetime
import random
from nltk.corpus import words
import time

load_dotenv()

max_length = 7
min_length = 5
target_submissions = 10000
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

for subreddit_name in subreddit_list:
    
    retries = 0

    word_list = [word for word in words.words() if min_length <= len(word) <= max_length]

    print(f"======== <{subreddit_name}> ========")

    processed_submissions = set()
    [processed_submissions.add(row[1]) for row in read_hist_row(subreddit_name)]

    flag = True

    while len(processed_submissions) < target_submissions:
        try:
            subreddit = reddit.subreddit(subreddit_name)

            keyword = random.choice(word_list)

            if flag:
                submissions = subreddit.hot(limit=1000)
                flag = False
            else:
                submissions = subreddit.search(keyword, limit=None)

            print("--------", keyword, len(processed_submissions))

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
            print(f"Rate limit exceeded for subreddit <{subreddit_name}>: {e}")
            wait_time = exponential_backoff(retries)
            print(f"Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retries += 1  # Increment the retry counter
        except Exception as e:
            print(f"Error processing subreddit <{subreddit_name}>: {e}")
            time.sleep(20)
            continue
