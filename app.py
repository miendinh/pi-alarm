import json
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from firebase import firebase
from flask import Flask, render_template, send_from_directory, jsonify, request

from config import *
from player import moc

logging.basicConfig()
app = Flask(__name__, static_url_path='')
scheduler = BackgroundScheduler()
ALARMS = []


@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('static/js', path)


@app.route('/')
def index():
  return render_template('admin.html', running_mode = STANDALONE,
                                       firebase_uri = FIREBASE_URI, 
                                       username = FIREBASE_AUTH_USERNAME)

@app.route('/alarms', methods=['GET'])
def alarms():
  global ALARMS
  return jsonify(ALARMS)

@app.route('/player', methods=['PUT'])
def control_player():
  cmd = request.json['cmd']
  if cmd in ['play', 'stop', 'pause', 'unpause', 'next_', 'prev']:
    getattr(moc, cmd)()
  elif cmd in ['up', 'down']:
    moc.volume(cmd)
    
  return jsonify({'success': cmd + ' done !'})


def syn_with_firebase():
  print 'sync with firebase...\n'
  global ALARMS
  try:
    fb = firebase.FirebaseApplication(FIREBASE_URI, None)
    result = fb.get('/users', FIREBASE_AUTH_USERNAME)
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
      scheduler.add_job(play_music, trigger='cron', hour=hour,
                        minute=minute, second=second, name='alarms')

  scheduler.print_jobs();


def play_music():
  moc.play()


def run_schedular():
  global scheduler
  scheduler.add_job(syn_with_firebase, 'interval', seconds=TIME_PERIOR_SYNC_FIREBASE)
  scheduler.start()


if __name__ == "__main__":
  moc.mocp('-a', os.path.dirname(os.path.abspath(__file__)) + '/' + MUSIC_FOLDER)
  run_schedular()
  app.run(debug=DEBUG, host=HOST, port=PORT)