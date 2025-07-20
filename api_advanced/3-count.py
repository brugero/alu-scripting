#!/usr/bin/python3
"""
Module for recursively querying the Reddit API to count occurrences of
given keywords in the titles of all hot articles for a subreddit.
"""

import requests
import re
from collections import defaultdict


def count_words(subreddit, word_list, after=None, counts=None, initial_call=True):
    """
    Recursively queries the Reddit API, parses the title of all hot articles,
    and prints a sorted count of given keywords (case-insensitive, delimited
    by spaces).

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): A list of keywords to count.
        after (str): The 'after' parameter for pagination (used internally).
        counts (defaultdict): Dictionary to store word counts (used internally).
        initial_call (bool): Flag to indicate the first call to the function.

    Returns:
        None: The function prints the results directly and does not return a value.
              Returns implicitly (None) if no posts match or subreddit is invalid.
    """
    if initial_call:
        normalized_word_set = {word.lower() for word in word_list}
        # Initialize counts using defaultdict for convenience
        counts = defaultdict(int)
    else:
        # For recursive calls, word_list is already the normalized set
        normalized_word_set = word_list

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "MyCustomRedditWordCounterApp/1.0"
    }
    params = {}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False)

        if response.status_code == 404 or response.is_redirect or \
           response.status_code != 200:
            return

        data = response.json()
        posts = data.get("data", {}).get("children", [])
        next_after = data.get("data", {}).get("after")

        if not posts and not next_after and initial_call:
            return

        for post in posts:
            title = post.get("data", {}).get("title", "")
            title_lower = title.lower()
            words_in_title = re.findall(r'[a-z]+', title_lower)

            for word_in_title in words_in_title:
                if word_in_title in normalized_word_set:
                    counts[word_in_title] += 1

        if next_after is None:
            # Base case: No more pages to fetch. Perform final printing.
            _print_sorted_counts(counts)
            return
        else:
            # Recursive step: Call for the next page
            return count_words(subreddit, normalized_word_set, next_after, counts, False)

    except requests.exceptions.RequestException:
        # Handle network errors. Print nothing if error on initial call.
        return
    except ValueError:  # Handles JSON decoding errors
        # Print nothing if error on initial call.
        return


def _print_sorted_counts(counts):
    """
    Helper function to sort and print the word counts.
    Prints words with count > 0, sorted by count descending, then alphabetically ascending.
    """
    filtered_counts = {word: count for word, count in counts.items() if count > 0}

    sorted_items = sorted(filtered_counts.items(), key=lambda item: (-item[1], item[0]))

    for word, count in sorted_items:
        print(f"{word}: {count}")