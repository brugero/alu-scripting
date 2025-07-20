#!/usr/bin/python3
"""
Module for recursively querying the Reddit API to get all hot article titles
for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): A list to accumulate the titles (initialized to None).
        after (str): The 'after' parameter for pagination (initialized to None).

    Returns:
        list: A list of hot article titles, or None if no results are found
              or the subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "MyRecursiveRedditCrawler/1.0"
    }
    params = {}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        if response.status_code == 404 or response.is_redirect:
            return None
        elif response.status_code != 200:
            return None

        data = response.json()
        posts = data.get("data", {}).get("children", [])
        next_after = data.get("data", {}).get("after")

        if not posts and not next_after and not hot_list:
            return None

        for post in posts:
            title = post.get("data", {}).get("title")
            if title:
                hot_list.append(title)

        if next_after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, next_after)

    except requests.exceptions.RequestException:
        
        return None
    except ValueError:  
        return None