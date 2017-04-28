# flask server
DEBUG = True
HOST = "0.0.0.0"
PORT = 8080

# play list folder 
MUSIC_FOLDER = 'musics'

# running mode 
## Note : unsupport Standalone mode yet !
STANDALONE = False

# firebase authentication
FIREBASE_URI = "https://hi-morning.firebaseio.com"
FIREBASE_AUTH_USERNAME = "pi-alarm"
FIREBASE_AUTH_PASSWORD = "pi-alarm"

## time to sync with firebase ( seconds )
TIME_PERIOR_SYNC_FIREBASE = 15

# message
ERRORS = "Can not get Alarms info. Please check your Pi''s Configuration !"