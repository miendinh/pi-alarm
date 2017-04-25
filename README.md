# Pi-Alarm
A tiny & cool application for Raspberry Pi 3 to alarm by playing music.
Pi-Alarm is controlled by [Hi-Morning](https://github.com/hi-morning/HiMorning) (a mobile app) that uses google firebase to sync scheduler alarms between Pi & mobile.

[Hi-Morning](https://github.com/hi-morning/HiMorning) is contributed by **@thoqbk**

Special thanks to **@nghnam** [https://github.com/nghnam/music-aekt](https://github.com/nghnam/music-aekt) for supporting a nice and concise Python Mocp Wrapper Utils, which uses to play music in Linux Terminal Command Line.

# Requirements & Setup.
## Hardware
Pi - 3 with Wi-Fi & audio support

## Setup Environment
```
sudo pip install Flask
sudo pip install requests
sudo pip install python-firebase
sudo pip install apscheduler
sudo apt-get install moc
```

## Integrate with Hi-Morning
* You can use [Hi-Morning](https://github.com/hi-morning/HiMorning) as a mobile controller app. Let's follow introduction of @thoqbk at [https://github.com/hi-morning/HiMorning](https://github.com/hi-morning/HiMorning)

* Pi-Alarm can run standalone as well through browser.

## Run
```
$ export FLASK_APP=app.py
$ flask run -h 127.0.0.1 -p 5000
```
Open browser and go to: http://127.0.0.1:5000

### Run with debug mode
```
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ flask run -h 127.0.0.1 -p 5000
```

#### Reference
1. http://apscheduler.readthedocs.io/en/3.0/userguide.html
2. https://moc.daper.net/