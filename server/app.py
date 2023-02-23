from flask import Flask, jsonify, request, render_template
from celery import Celery
from celery.schedules import crontab
from flask_cors import CORS
from flaskext.mysql import MySQL
from flask_mail import Mail, Message
from flask_caching import Cache
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
import re

# config
DEBUG = True

# app initialisation
app = Flask(__name__)
app.config.from_object(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gr00t##00'
app.config['MYSQL_DATABASE_DB'] = 'kanban'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '21f2000846@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'mokktrrvnsdvajvs'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_KEY_PREFIX'] = 'fcache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = '6379'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379'
app.config['SECRET_KEY'] = "004f2af45d3a4e161a7dd2d17fzcx47f"

# MySQL Integration
mysql = MySQL()
mysql.init_app(app)

# Flask-Mail Integration
mail = Mail(app)

# Celery Integration
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"], timezone="Asia/Calcutta", enable_utc = False)
celery.conf.update(app.config)

# Flask-Cache Integration
cache = Cache(app)

# CORS
CORS(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  sender.add_periodic_task(
    crontab(hour=18, minute=00, day_of_week='0-6'),
    daily_reminder.s(),
    name = "daily reminder"
  )
  sender.add_periodic_task(
    crontab(hour=12, minute=00, day_of_month=1, month_of_year='1-12'),
    monthly_report.s(),
    name = "monthly report"
  )

# Initialize Tables
with app.app_context():
  cursor = mysql.get_db().cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS users (\
    id INTEGER PRIMARY KEY AUTO_INCREMENT, \
    name TEXT NOT NULL, \
    email TEXT NOT NULL, \
    password TEXT NOT NULL)')
  cursor.execute('CREATE TABLE IF NOT EXISTS lists (\
    id INTEGER PRIMARY KEY AUTO_INCREMENT, \
    userid INTEGER NOT NULL, \
    title TEXT NOT NULL, \
    FOREIGN KEY(userid) REFERENCES users(id) ON DELETE CASCADE)')
  cursor.execute('CREATE TABLE IF NOT EXISTS cards (\
    id INTEGER PRIMARY KEY AUTO_INCREMENT, \
    userid INTEGER NOT NULL, \
    listid INTEGER NOT NULL, \
    list TEXT NOT NULL, \
    title TEXT NOT NULL, \
    content TEXT NOT NULL, \
    deadline DATETIME NOT NULL, \
    completed INTEGER NOT NULL, \
    created_at DATETIME NOT NULL, \
    last_modified DATETIME NOT NULL, \
    completed_at DATETIME, \
    FOREIGN KEY(listid) REFERENCES lists(id) ON DELETE CASCADE)')
  cursor.close()

# Middleware
def is_authenticated(f):
  @wraps(f)
  def authorize(*args, **kwargs):
    token = None
    bearer_token = request.headers.get('Authorization', '').split()
    if bearer_token:
      token = bearer_token[1]
    if not token:
      return jsonify({'error': 'Session timed out'})
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
      cursor = mysql.get_db().cursor()
      cursor.execute('SELECT id, name, email FROM users WHERE id=%s', (
        data['user_id']
      ))
      user = cursor.fetchall()
      cursor.close()
    except:
      return jsonify({'error': 'Invalid token'})
    return f(user, *args, **kwargs)
  return authorize

# Celery Tasks
@celery.task()
def daily_reminder():
  print('added to queue...')
  with app.app_context():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM cards')
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    for user in users:
      pending_tasks = []
      for card in cards:
        if card[1] == user[0]:
          if card[6] < datetime.datetime.now() and card[7] == 0:
            pending_tasks.append(card[4])

      msg = Message(subject="Daily Reminder",
        sender="admin.kanban",
        recipients=[user[2]])
      msg.html = render_template('daily_reminder.html', data=user, tasks=pending_tasks)
      mail.send(msg)

@celery.task()
def monthly_report():
  print('added to queue...')
  with app.app_context():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM cards')
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    for user in users:
      total_tasks = 0
      total_completed = 0
      total_missed = 0
      current_month = datetime.datetime.now().date().month
      previous_month = 12 if current_month - 1 == 0 else current_month - 1
      for card in cards:
        if card[1] == user[0]:
          if card[8].date().month == previous_month:
            total_tasks += 1
          if card[10] and card[10].date().month == previous_month:
            total_completed += 1
          if card[6].date().month == previous_month and card[7] == 0:
            total_missed += 1
      
      msg = Message(subject="Monthly Report",
        sender="admin.kanban",
        recipients=[user[2]])
      msg.html = render_template('monthly_report.html', data=user, tasks=total_tasks, completed=total_completed, missed=total_missed)
      mail.send(msg)

@celery.task()
def export_mail(data):
  print('added to queue...')
  with app.app_context():
    msg = Message(subject=data['subject'],
      sender="admin.kanban",
      recipients=[data['email']])
    msg.html = render_template('export_alert.html', data=data)
    mail.send(msg)

@celery.task()
def import_csv(data):
  print('added to queue...')
  with app.app_context():
    for file in data:
      cursor = mysql.get_db().cursor()
      cursor.execute('INSERT INTO cards (userid, listid, list, title, content, deadline, completed, created_at, last_modified, completed_at) \
      SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \
      WHERE NOT EXISTS ( \
        SELECT id FROM cards WHERE id=%s \
      )', (
        file[1],
        file[2],
        file[3],
        file[4],
        file[5],
        datetime.datetime.strptime(file[6], "%d/%m/%Y, %H:%M:%S"),
        file[7],
        datetime.datetime.strptime(file[8], "%d/%m/%Y, %H:%M:%S"),
        datetime.datetime.strptime(file[9], "%d/%m/%Y, %H:%M:%S"),
        datetime.datetime.strptime(file[10], "%d/%m/%Y, %H:%M:%S") if file[10] else None,
        file[0],
      ))

    cursor.execute('SELECT * FROM cards WHERE userid=%s', 2)
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    print(cards)

# APIs
@app.route('/format_mail', methods = ['GET'])
@is_authenticated
def format_mail(user):
  data = {}
  data['subject'] = "Export Successful"
  data['email'] = user[0][2]
  data['name'] = user[0][1]
  duration = int(60)
  print('Connecting to celery')
  export_mail.apply_async(args=[data], countdown=duration)
  print('Email will be sent in 1 minute')
  return jsonify('Email job scheduled!')

@app.route('/importcsv', methods = ['POST'])
@is_authenticated
def importcsv(user):
  import_csv.apply_async(args=[request.get_json()["csv"]])
  return jsonify('Importing...')

# test route
@app.route('/ping', methods=['GET'])
def ping_pong():
  return jsonify('pong!')

@app.route('/signup', methods = ['POST'])
def signup():
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    name = request.get_json()['name']
    email = request.get_json()['email']
    password = request.get_json()['password']
    confirm_password = request.get_json()['confirm_password']
    hashed_password = generate_password_hash(password, method='sha256')
    
    result = re.match('^[A-Za-z0-9]$', password)    
    if not email:
      print("Username can not be empty.")
    else:
      if len(password) < 8 and not result:
        print("Your password must be atleast 8 characters long and contain letters & numbers.")
      else:
        if password == confirm_password:
          cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (
            name,
            email,
            hashed_password,
          ))
          mysql.get_db().commit()
          cursor.close()
          print("Account Created Successfully")
          return jsonify('Success')
        else:
          print("Passwords do not match. Try Again!")
    return jsonify('Failed')

@app.route('/signin', methods = ['POST'])
def signin():
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    given_password = request.get_json()['password']
    cursor.execute('SELECT id, password FROM users WHERE email=%s', (
      request.get_json()['email'],
    ))
    user = cursor.fetchall()
    cursor.close()
    userid = user[0][0]
    password = user[0][1]
    if check_password_hash(password, given_password):
      print("Login Successful")
      token = jwt.encode({'user_id' : userid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'], "HS256")
      return jsonify({'token' : token})
    else:
      print("Username or Password is Incorrect")
      return jsonify('Login Failed')

@app.route('/addlist', methods = ['POST'])
@is_authenticated
def addlist(user):
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    cursor.execute('INSERT INTO lists (userid, title) VALUES (%s, %s)', (
      user[0][0],
      request.get_json()['title'],
    ))

    cursor.execute('SELECT * FROM lists WHERE userid=%s', user[0][0])
    lists = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    return jsonify(lists)

@app.route('/editlist/<id>', methods = ['POST'])
@is_authenticated
def editlist(user, id):
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    cursor.execute('UPDATE lists SET title=%s WHERE id=%s', (
      request.get_json()['title'],
      id,
    ))
    cursor.execute('SELECT * FROM lists WHERE userid=%s', user[0][0])
    lists = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    return jsonify(lists)


@app.route('/deletelist/<id>', methods = ['DELETE'])
@is_authenticated
def deletelist(user, id):
  cursor = mysql.get_db().cursor()
  cursor.execute('DELETE FROM lists WHERE ID=%s', (
    id,
  ))
  cursor.execute('SELECT * FROM lists WHERE userid=%s', user[0][0])
  lists = cursor.fetchall()
  mysql.get_db().commit()
  cursor.close()
  return jsonify(lists)

@app.route('/addcard', methods = ['POST'])
@is_authenticated
def addcard(user):
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    cursor.execute('INSERT INTO cards (userid, listid, list, title, content, deadline, completed, created_at, last_modified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (
      user[0][0],
      request.get_json()['listid'],
      request.get_json()['list'],
      request.get_json()['title'],
      request.get_json()['content'],
      request.get_json()['deadline'],
      0,
      datetime.datetime.now(),
      datetime.datetime.now(),
    ))
    
    cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    return jsonify(cards)

@app.route('/editcard/<id>', methods = ['POST'])
@is_authenticated
def editcard(user, id):
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    cursor.execute('UPDATE cards SET title=%s, content=%s, deadline=%s, last_modified=%s WHERE id=%s', (
      request.get_json()['title'],
      request.get_json()['content'],
      request.get_json()['deadline'],
      datetime.datetime.now(),
      id,
    ))
    cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    return jsonify(cards)

@app.route('/movecard/<id>', methods = ['POST'])
@is_authenticated
def movecard(user, id):
  if request.method == 'POST':
    cursor = mysql.get_db().cursor()
    cursor.execute('UPDATE cards SET listid=%s, list=%s, last_modified=%s WHERE id=%s', (
      request.get_json()['listid'],
      request.get_json()['list'],
      datetime.datetime.now(),
      id,
    ))
    cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    return jsonify(cards)

@app.route('/completed/<id>', methods = ['POST'])
@is_authenticated
def completed(user, id):
  if request.method == 'POST':
    completed = request.get_json()['completed']
    cursor = mysql.get_db().cursor()
    if completed:
      cursor.execute('UPDATE cards SET completed=%s, last_modified=%s, completed_at=%s WHERE id=%s', (
        completed,
        datetime.datetime.now(),
        datetime.datetime.now(),
        id,
      ))
    else:
      cursor.execute('UPDATE cards SET completed=%s, last_modified=%s, completed_at=%s WHERE id=%s', (
        completed,
        datetime.datetime.now(),
        None,
        id,
      ))
    cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
    cards = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    return jsonify(cards)

@app.route('/deletecard/<id>', methods = ['DELETE'])
@is_authenticated
def deletecard(user, id):
  cursor = mysql.get_db().cursor()
  cursor.execute('DELETE FROM cards WHERE id=%s', (
    id,
  ))
  cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
  cards = cursor.fetchall()
  mysql.get_db().commit()
  cursor.close()
  return jsonify(cards)

@app.route('/getdata', methods = ['GET'])
@is_authenticated
@cache.cached(timeout=30)
def getdata(user):
  cursor = mysql.get_db().cursor()
  cursor.execute('SELECT * FROM lists WHERE userid=%s', user[0][0])
  lists = cursor.fetchall()
  cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
  cards = cursor.fetchall()
  mysql.get_db().commit()
  cursor.close()
  return jsonify(lists, cards)

@app.route('/stats', methods = ['GET'])
@is_authenticated
@cache.cached(timeout=30)
def stats(user):
  cursor = mysql.get_db().cursor()
  cursor.execute('SELECT * FROM cards WHERE userid=%s', user[0][0])
  cards = cursor.fetchall()
  mysql.get_db().commit()
  cursor.close()

  total_tasks = 0
  total_completed = 0
  total_missed = 0
  tasks_dict = {}
  completed_dict = {}
  missed_dict = {}
  for i in range(9,-1,-1):
    tasks_dict[str(datetime.datetime.now().date() - datetime.timedelta(i))] = 0
    completed_dict[str(datetime.datetime.now().date() - datetime.timedelta(i))] = 0
    missed_dict[str(datetime.datetime.now().date() - datetime.timedelta(i))] = 0

  for card in cards:
    total_tasks += 1
    if card[8] > datetime.datetime.now() - datetime.timedelta(9):
      if tasks_dict[str(card[8].date())]:
        tasks_dict[str(card[8].date())] += 1
      else:
        tasks_dict[str(card[8].date())] = 1
    if card[10]:
      total_completed += 1
      if card[10] > datetime.datetime.now() - datetime.timedelta(9):
        if completed_dict[str(card[10].date())]:
          completed_dict[str(card[10].date())] += 1
        else:
          completed_dict[str(card[10].date())] = 1
    if card[6] < datetime.datetime.now() and card[7] == 0:
      total_missed += 1
      if card[6] > datetime.datetime.now() - datetime.timedelta(9):
        if missed_dict[str(card[6].date())]:
          missed_dict[str(card[6].date())] += 1
        else:
          missed_dict[str(card[6].date())] = 1

  return jsonify(total_tasks, total_completed, total_missed ,tasks_dict, completed_dict, missed_dict)

if __name__ == '__main__':
    app.run()