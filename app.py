import os
import json
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from firebase import firebase
from flask import Flask, render_template, send_from_directory, jsonify, request

from constant import *
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
  with open('config.js') as cf:
    config = json.load(cf)
    try:
      return render_template('admin.html',
                             username=config['username'],
                             password=config['password'],
                             firebase_uri=config['firebase_uri'])
    except:
      if config:
        return render_template('admin.html',
                               username=config['username'],
                               password=config['password'],
                               firebase_uri=config['firebase_uri'],
                               errors=ERRORS)
      else:
        return render_template('admin.html', errors=ERRORS)


@app.route('/alarms', methods=['GET'])
def alarms():
  global ALARMS
  return jsonify(ALARMS)


@app.route('/pi-config', methods=['PUT'])
def update_pi_config():
  js = request.json
  config = {
    'username': js['username'],
    'password': js['password'],
    'firebase_uri': js['firebase_uri']
  }
  with open('config.js', 'w') as fp:
    json.dump(config, fp)

  return jsonify({'success': 'PI configuration is saved !'})

@app.route('/player', methods=['PUT'])
def control_player():
  cmd = request.json['cmd']
  if cmd == 'play':
    moc.play()
  elif cmd == 'stop':
    moc.stop()
  elif cmd == 'pause':
    moc.pause()
  elif cmd == 'unpause':
    moc.unpause()
  elif cmd == 'next':
    moc.next_()
  elif cmd == 'prev':
    moc.prev()
  elif cmd == 'vol+':
    moc.volume('up')
  elif cmd == 'vol-':
    moc.volume('down')
  return jsonify({'success': cmd + ' done !'})

def syn_with_firebase():
  print 'sync with firebase...\n'
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