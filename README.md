# Kanban
- A minimal kanban app built with Vue.js frontend and Flask backend. 
- Uses redis for caching and celery for handling batch jobs.
- Cron Jobs are scheduled for daily reminders and monthly reports through celery. 
- All reminders and reports are sent to the user via email.
- Default features like Card and List Management are implemented using CRUD APIs. 
- All the lists and cards can be exported and imported as CSV. 

> Language: Python, JavaScript \
> Backend: Flask \
> Framework: Vue.js, Bootstrap5 \
> Database: MySQL \
> Broker: Redis \
> Task Queue: Celery

## Local Setup:
You need to run 5 different servers to run it locally.

### Clone this repo

```
git clone https://github.com/aayushmahapatra/kanban_vue.git
```

### Client
Follow these steps for client setup:
- Go inside the `client` directory
- Run `npm i` to install dependencies
- Start the client:
```
npm run serve
```

### Redis
Start the redis server:
```
redis-server
```

### Server
Follow these steps for server setup:
- Go inside the `server` directory
- Run `pip3 install -r requirements.txt` to install dependencies
- Start the python server:
```
python3 app.py
```

### Celery Worker
Follow these steps to start celery worker:
- Go inside the `server` directory
- Start the celery worker:
```
celery -A app.py worker
```

### Celery Beat
Follow these steps to start celery beat:
- Go inside the `server` directory
- Start the celery beat:
```
celery -A app.py beat
```
