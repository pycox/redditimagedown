import requests
from bs4 import BeautifulSoup


def main():
    key = 52

    id = "dDNfMWM5bml2YQ"

    response = requests.get(
        f"https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after={id}%3D%3D&t=DAY&name=AbandonedPorn&feedLength=5"
    )

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("div.posting")

    data = []

    for item in items:
        link = item.find("a").get("href").strip()
        title = item.find("h5").text.strip()
        location = item.find_all("span")[-1].text.strip()

        data.append([title, com, location, link])

    updateDB(key, data)


if __name__ == "__main__":
    main()
