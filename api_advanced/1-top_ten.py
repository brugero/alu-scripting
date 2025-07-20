#!/usr/bin/python3
"""
Module for querying the Reddit API to get the titles of the first 10
hot posts for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Queries the Reddit API and prints the titles of the first 10 hot posts
    listed for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {
        "User-Agent": "MyCustomRedditApp/1.0"  
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            posts = data.get("data", {}).get("children", [])

            if not posts:
                print(None) 
                return

            for post in posts:
                title = post.get("data", {}).get("title")
                if title:
                    print(title)
        elif response.status_code == 404 or response.is_redirect:
            
            print(None)
        else:
            print(None)
    except requests.exceptions.RequestException:
        print(None)
    except ValueError: 
        print(None)