#!/usr/bin/env python

import subprocess
import argparse
import time
import dateutil.parser as dateParser
import datetime
import cursor

# Default dimensions just in case
DEFAULT_HEIGHT = 24
DEFAULT_WIDTH = 80

# Arguments
parser = argparse.ArgumentParser(description="Fancy countdown script")

parser.add_argument("-d", "--date", action="store", help="Date to countdown to", default="")
parser.add_argument("-m", "--minutes", action="store",
                    type=int, help="Number of minutes",
                    default=0)
parser.add_argument("-s", "--seconds", action="store",
                    type=int, help="Number of seconds",
                    default=0)
parser.add_argument("-f", "--font", action="store",
                    help="Custom font file",
                    default="/usr/share/tty-countdown/font.txt")
parser.add_argument("-n", "--nocenter", action="store_true",
                    help="Do not center timer (more efficient)")

args = parser.parse_args()

centered = not args.nocenter
seconds = args.seconds
minutes = args.minutes
fontFile = args.font
date = args.date

seconds = minutes * 60 + seconds


# Turn string into blocky ascii representation
# Supports 0-9, colon
def asciiFormat(string, font):
    # enumerate numbers and colons
    string = list(map(int, [c.replace(":", "10") for c in list(string)]))
    height = len(font[0])

    frame = ""
    # fill frame top to bottom
    for i in range(height):
        for char in string[:-1]:
            frame += font[char][i] + " "
        # dirty hack to have no space at the end
        frame += font[string[-1]][i]

        frame += "\n"
    return frame[:-1]


# Pad with spaces and newlines to center
def center(frame, termDimensions):
    if centered:
        termHeight = termDimensions[0]
        termWidth = termDimensions[1]
        frame = frame.split("\n")
        frameWidth = max(map(len, frame))
        frameHeight = len(frame)
        # pad horizontally
        pad = " " * int((termWidth - frameWidth) / 2)
        frame = "\n".join([(pad + line + pad) for line in frame])

        # pad vertically
        pad = "\n" * int((termHeight - frameHeight) / 2)
        frame = pad + frame + pad
    clear()
    return frame


# Clear screen
def clear():
    # no idea how this works but it does
    print("\033c")
    cursor.hide()


# Terminal dimensions [height, width]
def getTermDimensions():
    try:
        dimensions = subprocess.check_output(['stty', 'size']).split()
        return list(map(int, dimensions))
    except subprocess.CalledProcessError:
        return [DEFAULT_HEIGHT, DEFAULT_WIDTH]

def getTime(seconds):
    d = datetime.datetime(1,1,1) + datetime.timedelta(seconds=seconds)
    if d.day > 1:
        return "%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)
    elif d.hour > 0:
        return "%d:%d:%d" % (d.hour, d.minute, d.second)
    elif d.minute > 0:
        return "%d:%d" % (d.minute, d.second)
    return "%d" % d.second

if __name__ == '__main__':
    # Load font file
    with open(fontFile, "r") as f:
        font = f.read().split("\n<---->\n")
        font = [symbol.split("\n") for symbol in font]

    if date != "":
        parsedDate = dateParser.parse(date, dayfirst=True)
        now = datetime.datetime.now()
        timeDiff = parsedDate - now
        seconds = round(timeDiff.total_seconds())
        if seconds < 0:
            seconds = 0

    # Countdown
    while seconds >= 0:
        print(center(asciiFormat(getTime(seconds), font), getTermDimensions()), end="")
        seconds -= 1
        time.sleep(1)
        
    cursor.show()
