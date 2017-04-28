# TTY-Countdown

![screenshot](http://i.imgur.com/lnRXPyZ.png)

A countdown timer that will live forever in the shadow of 
[tty-clock](https://github.com/xorg62/tty-clock).


## Usage
    usage: tty-countdown [-h] [-m MINUTES] [-s SECONDS] [-f FONT] [-n]
    
    Fancy countdown script
    
    optional arguments:
      -h, --help            show this help message and exit
      -m MINUTES, --minutes MINUTES
                            Number of minutes
      -s SECONDS, --seconds SECONDS
                            Number of seconds
      -f FONT, --font FONT  Custom font file
      -n, --nocenter        Do not center timer (more efficient)
    
## Installation
### Arch Linux
* [Install from the AUR](https://aur.archlinux.org/packages/tty-countdown-git)
* `pacaur -S tty-countdown-git`

### Other
    $ git clone https://github.com/veggiedefender/tty-countdown && cd tty-countdown
    $ sudo cp tty-countdown /usr/bin/ && chmod +x /usr/bin/tty-countdown
    $ sudo mkdir /usr/share/tty-countdown/ && cp font.txt /usr/share/tty-countdown/

### Windows
* Does this even work on Windows?
