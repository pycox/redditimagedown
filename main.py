# import praw
# import requests
# import os
# from urllib.parse import urlparse
# from dotenv import load_dotenv
# import csv
# from datetime import datetime


# load_dotenv()


# # CLIENT_ID="ro0H6KXI4gxylTBx_gHfAA"
# # CLIENT_SECRET="N4dyKgZS7o0WQXR1c2vopKB_1iwRlw"
# # USER_AGENT="img_download"
# # USERNAME="MatterOk9891"
# # PASSWORD="hyesongwking"


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


# def download_image(image_url, image_dir):
#     try:
#         parsed_url = urlparse(image_url)
#         file_name = os.path.basename(parsed_url.path)
#         file_path = os.path.join(image_dir, file_name)
#         response = requests.get(image_url)
#         if response.status_code == 200:
#             with open(file_path, "wb") as file:
#                 file.write(response.content)
#             print(f"Downloaded {file_name}")
#             return file_name, image_url  # Return the file name and image URL
#         else:
#             return None, None
#     except Exception as e:
#         print(f"Error downloading image: {e}")
#         return None, None


# # Open the CSV file for writing metadata
# metadata_csv_path = "image_metadata.csv"
# with open(metadata_csv_path, mode="w", newline="") as metadata_file:
#     metadata_writer = csv.writer(metadata_file)
#     # Write the header row
#     metadata_writer.writerow(
#         ["subreddit", "image_file_name", "image_url", "caption", "up_votes", "time"]
#     )

#     # Open the CSV file with subreddit list
#     with open("sub_list.csv", newline="") as csvfile:
#         csvreader = csv.reader(csvfile)
#         subreddit_list = [row[0] for row in csvreader]

#     for subreddit_name in subreddit_list:
#         try:
#             subreddit = reddit.subreddit(subreddit_name)
#             print(f"======== Starting <{subreddit_name}> ========")
#             image_dir = f"downloads/{subreddit_name}"
#             if not os.path.exists(image_dir):
#                 os.makedirs(image_dir)

#             for submission in subreddit.hot():  # Adjust the limit as needed
#                 try:
#                     if "i.redd.it" in submission.url:
#                         file_name, image_url = download_image(submission.url, image_dir)
#                         if file_name:
#                             # Convert time from UTC to a readable format
#                             time = datetime.utcfromtimestamp(
#                                 submission.created_utc
#                             ).strftime("%Y-%m-%d %H:%M:%S")
#                             # Write metadata to the CSV file
#                             metadata_writer.writerow(
#                                 [
#                                     subreddit_name,
#                                     file_name,
#                                     image_url,
#                                     submission.title,  # Assuming the title is the caption
#                                     submission.score,  # The number of upvotes
#                                     time,
#                                 ]
#                             )
#                 except Exception as e1:
#                     print(f"Error processing submission <{submission}>: {e1}")
#         except Exception as e:
#             print(f"Error processing subreddit <{subreddit_name}>: {e}")


import praw
import os
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Set up PRAW with your credentials
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    # username=username,
    # password=password,
)

reddit.read_only = True

# Open the CSV file for writing metadata
metadata_csv_path = "image_metadata.csv"
with open(metadata_csv_path, mode="w", newline="") as metadata_file:
    metadata_writer = csv.writer(metadata_file)
    # Write the header row
    metadata_writer.writerow(
        ["subreddit", "id", "image_url", "caption", "up_votes", "time"]
    )

    # Open the CSV file with subreddit list
    with open("sub_list.csv", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        subreddit_list = [row[0] for row in csvreader]

    for subreddit_name in subreddit_list:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"======== Starting <{subreddit_name}> ========")

            for submission in subreddit.hot():  # Adjust the limit as needed
                try:
                    if "i.redd.it" in submission.url:
                        # Convert time from UTC to a readable format
                        time = datetime.utcfromtimestamp(
                            submission.created_utc
                        ).strftime("%Y-%m-%d %H:%M:%S")
                        # Write metadata to the CSV file
                        row = [
                            subreddit_name,
                            submission.id,
                            submission.url,
                            submission.title,  # Assuming the title is the caption
                            submission.score,  # The number of upvotes
                            time,
                        ]
                        metadata_writer.writerow(row)
                        print(row)
                except Exception as e1:
                    print(f"Error processing submission <{submission}>: {e1}")
        except Exception as e:
            print(f"Error processing subreddit <{subreddit_name}>: {e}")
