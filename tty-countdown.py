import subprocess
import argparse
import time

#Default terminal width just in case
DEFAULT_WIDTH = 90

#Arguments
parser = argparse.ArgumentParser(description = "Fancy countdown script")

parser.add_argument("-m", "--minutes", action="store",
                    type=int, help="Number of minutes",
                    default=0)
parser.add_argument("-s", "--seconds", action="store",
                    type=int, help="Number of seconds",
                    default=0)
parser.add_argument("-L", "--left", action="store_true",
                    help="Align left (faster)")

args = parser.parse_args()

centered = not args.left
seconds = args.seconds
minutes = args.minutes

seconds = minutes * 60 + seconds


#Turn string into blocky ascii representation
#Supports 0-9, colon
def asciiFormat(string, font):
    #enumerate numbers and colons
    string = list(map(int, [ c.replace(":", "10") for c in list(string) ]))
    height = len(font[0])
    
    frame = ""
    #fill frame top to bottom
    for i in range(height):
        #loop through string
        for char in string[:-1]:
            frame += font[char][i] + " "
        #dirty hack to have no space at the end
        frame += font[string[-1]][i]

        frame += "\n"
    return frame[:-1]

#Pad left and right side with spaces to center
def centered(frame, termWidth):
    if centered:
        frame = frame.split("\n")
        frameWidth = max(map(len, frame))
        pad = " " * int((termWidth - frameWidth)/2)
        frame = "\n".join([ (pad + line + pad) for line in frame ])
    clear()
    return frame

#Clear screen
def clear():
    #no idea how this works
    print("\033c")

def getTermWidth():
    try:
        columns = subprocess.check_output(['stty', 'size']).split()[1]
        return int(columns)
    except subprocess.CalledProcessError:
        return DEFAULT_WIDTH

#Load font file
with open("font.txt", "r") as f:
    font = f.read().split("\n<---->\n")
    font = [ symbol.split("\n") for symbol in font ]

#Countdown
while seconds >= 0:
    t = "%s:%02d" % divmod(seconds, 60)
    print(centered(asciiFormat(t, font), getTermWidth()), end="")

    seconds -= 1
    time.sleep(1)