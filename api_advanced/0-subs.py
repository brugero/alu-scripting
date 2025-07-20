#!/usr/bin/python3
"""
Module for querying the Reddit API to get the number of subscribers
for a given subreddit.
"""

import requests


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of subscribers
    for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        int: The number of subscribers if the subreddit is valid,
             otherwise 0.
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        "User-Agent": "MyCustomUserAgent/1.0"  
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("subscribers", 0)
        elif response.status_code == 404 or response.is_redirect:
            return 0
        else:
            return 0
    except requests.exceptions.RequestException:
        return 0
    except ValueError:  
        return 0