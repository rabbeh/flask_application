# flask_application

# Instructions to use
1. Install redis-server:
```bash
    $ wget http://download.redis.io/releases/redis-4.0.11.tar.gz
    $ tar xzf redis-4.0.11.tar.gz
    $ cd redis-4.0.11
    $ make
```
2. Start redis-server: ```src/redis-server```
3. Install python dependencies: 
```bash 
   $ virtualenv -p python2 venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt
```
4. In a new window/tab, start rq-worker: ``` python flask_app.py runworker```
5. Run flask application!: ``` python flask_app.py runserver --host 0.0.0.0 --port 1234
6. View the application at ```localhost:1234```

