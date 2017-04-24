import sys
import re
import os

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <file> <columns>")
    sys.exit(1)

def print_row(text, time, label_size):
    print(text.ljust(label_size) + " {:02}:{:02}".format(int(time / 3600), int(time % 3600 / 60)))

def print_summary(filename):
    break_limit = 1200

    activity = {}

    group_start = None
    current_start = None

    lines = [line.rstrip('\n') for line in open(filename)]
    total = 0
    activity = {}
    groups = []

    matcher = re.compile('([0-9]{2}):([0-9]{2}):([0-9]{2})\s(.*)')
    for line in lines:
        match = matcher.match(line)

        if not match:
            print("Invalid file format")
            sys.exit(1)

        time = 3600 * int(match.group(1)) + 60 * int(match.group(2)) + int(match.group(3))
        application = match.group(4)

        if group_start:
            if time - current_start > break_limit or line == lines[-1]:
                groups.append([group_start, current_start])
                total = total + current_start - group_start
                group_start = time
            else:
                if application not in activity:
                    activity[application] = 0
                activity[application] = activity[application] + time - current_start
        else:
            group_start = time

        current_start = time

    label_size = len(max(activity, key=len))

    for group in groups:
        print_row("Start", group[0], label_size)
        print_row("End", group[1], label_size)
        print_row("Time", group[1] - group[0], label_size)
        print()

    for app_activity in activity:
        print_row(app_activity, activity[app_activity], label_size)

    print()
    print_row("Total", total, label_size)

print_summary(sys.argv[1])
