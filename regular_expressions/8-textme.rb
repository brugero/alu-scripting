#!/usr/bin/env ruby

# This script extracts sender, receiver, and flags from a TextMe log line.
# It takes one command-line argument, which is the log string.
# The output format is: [SENDER],[RECEIVER],[FLAGS]

# Access the first command-line argument, which is the log string.
log_string = ARGV[0]

# Define the regular expression to capture the required information.
# Breakdown of the regex:
#   ^.*\[from:(.+?)\]:
#     ^.* - Matches any characters from the beginning of the string (non-greedy).
#     \[from:    - Matches the literal string "[from:".
#     (.+?)      - Capturing group 1: Matches one or more characters (non-greedy)
#                  until the next part of the regex. This captures the SENDER.
#     \]         - Matches the literal closing square bracket "]".
#   .*\[to:(.+?)\]:
#     .* - Matches any characters in between (non-greedy).
#     \[to:      - Matches the literal string "[to:".
#     (.+?)      - Capturing group 2: Captures the RECEIVER.
#     \]         - Matches the literal closing square bracket "]".
#   .*\[flags:(.+?)\]:
#     .* - Matches any characters in between (non-greedy).
#     \[flags:   - Matches the literal string "[flags:".
#     (.+?)      - Capturing group 3: Captures the FLAGS.
#     \]         - Matches the literal closing square bracket "]".
#   .*$          - Matches any remaining characters until the end of the string.
#
# The `?` after `.+` makes the matching non-greedy, ensuring it stops at the
# first `]` rather than consuming too much.
regex = /^.*\[from:(.+?)\](?:.*\[to:(.+?)\])?(?:.*\[flags:(.+?)\])?.*$/

# Attempt to match the regular expression against the log string.
# The `match` method returns a MatchData object if a match is found, otherwise nil.
match_data = log_string.match(regex)

# If a match is found, extract the captured groups and print them in the desired format.
if match_data
  sender = match_data[1] || "" # Sender is in the first capturing group
  receiver = match_data[2] || "" # Receiver is in the second capturing group
  flags = match_data[3] || "" # Flags are in the third capturing group

  # Print the extracted information, joined by commas.
  puts "#{sender},#{receiver},#{flags}"
end