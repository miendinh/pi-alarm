from flask import Flask, render_template, send_from_directory, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from firebase import firebase
from player import moc
import logging
import json

logging.basicConfig()
ERRORS = "Can not get Alarms info. Please check your Pi''s Configuration !"
ALARMS = []

app = Flask(__name__, static_url_path='')
scheduler = BackgroundScheduler()

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/')
def index():
  with open('config.js') as cf:
    config = json.load(cf)
    try:
      username = config['username']
      return render_template('admin.html',
        username = config['username'],
        password = config['password'],
        firebase_uri = config['firebase_uri'],
        music_folder = config['music_folder'])
    except:
      if config:
       return render_template('admin.html',
        username = config['username'],
        password = config['password'],
        firebase_uri = config['firebase_uri'],
        music_folder = config['music_folder'],
        errors = ERRORS)
      else:
        return render_template('admin.html', errors = ERRORS)

@app.route('/alarms', methods = ['GET'])
def alarms():
  global ALARMS
  return jsonify(ALARMS)

@app.route('/pi-config', methods = ['PUT'])
def update_pi_config():
  js = request.json
  config = {
    'username' : js['username'],
    'password' : js['password'],
    'firebase_uri' : js['firebase_uri'],
    'music_folder' : js['music_folder']
  }
  with open('config.js', 'w') as fp:
    json.dump(config, fp)

  return jsonify({'success': 'PI configuration is saved !'})

def syn_with_firebase():
  print 'sync with firebase \n'
  with open('config.js') as cf:
    global ALARMS
    config = json.load(cf)
    try:     
      fb = firebase.FirebaseApplication(config['firebase_uri'], None)
      result = fb.get('/users', config['username'])
      alarms = result['alarms']
      if ALARMS != alarms:
        print 'updated alarms !'
        ALARMS = alarms
        create_job_alarms() 
    except Exception, e:
     print str(e)
     print ERRORS

def create_job_alarms():
  global scheduler
  global ALARMS

  for job in scheduler.get_jobs():
    if job.name == 'alarms':
      scheduler.remove_job(job.id)

  for alarm in ALARMS:
    if (alarm['status'] == 'on'):
      hour, minute, second = alarm['time'].split(':')
      scheduler.add_job(play_music, trigger='cron', hour = hour, 
        minute = minute, second = second, name='alarms')
  
  scheduler.print_jobs();

def play_music():
  moc.play()

def run_schedular():
  global scheduler
  scheduler.add_job(syn_with_firebase, trigger='cron', month='*', 
    day='*', hour='*', 
    minute='*', second='15')
  scheduler.start()

if __name__ == "__main__":
  run_schedular()
  app.run(debug=True, host="192.168.16.134")