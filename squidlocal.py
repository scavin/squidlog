#!/usr/bin/env python

import sys
import argparse

parser = argparse.ArgumentParser(description='Analyze squid log by user and display usage.')
parser.add_argument('logfile_path', help='logfile to analyze')
parser.add_argument('--exclude-pattern', help='skipped if username contains this regexp', default='')
args = parser.parse_args()

logfile = open(args.logfile_path)
print logfile

sys.stdout.write("Analyzing...\n")

sum_bytes = {}
for i, line in enumerate(logfile):

    _, _, _, _, num_bytes, _, _, rfc931, _, _ = line.split()[:10]
  
    if rfc931 == '-': continue
  
    try:
        sum_bytes[rfc931] = sum_bytes[rfc931] + int(num_bytes)
    except KeyError:
        sum_bytes[rfc931] = int(num_bytes)

if args.exclude_pattern:
    print "Exclusion check has been enabled."
    exclude_pattern = re.compile(args.exclude_pattern)

def format(size):
    if size < 1024:
        fmt = str(size) + 'B'
    elif size < (1024 * 1024):
        fmt = str(size / 1024) + 'KB'
    elif size < (1024 * 1024 * 1024):
        fmt = str(size / 1024 /1024) + 'MB'
    elif size < (1024 * 1024 * 1024 * 1024):
        fmt = str(size / 1024 /1024 / 1024) + 'GB'
    elif size < (1024 * 1024 * 1024 * 1024 * 1024):
        fmt = str(size / 1024 /1024 / 1024 / 1024) + 'GB'
    else:
        fmt = str(size / 1024 /1024 / 1024 / 1024 / 1024) + 'PB'

    return fmt

for username, total_bytes in sum_bytes.iteritems():
    sys.stdout.write(username + ' ' + '<' + format(total_bytes) + '>')
    sys.stdout.write("\n")
    sys.stdout.flush()
  
    if args.exclude_pattern and exclude_pattern.search(username):
        sys.stdout.write("..skipped!\n")
        sys.stdout.flush()
        continue

sys.stdout.write("Done.\n")
