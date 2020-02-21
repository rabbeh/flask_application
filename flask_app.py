import redis
from flask_script import Server, Manager
from rq import Connection, Worker
#from uwsgi import app
from speaking_time import app

manager = Manager(app)
#context = ('/home/sail1/rajatheb/public_html/moderator_controlled_speaking_time/ssl/server.crt', '/home/sail1/rajatheb/public_html/moderator_controlled_speaking_time/ssl/server.key')
context = ('/home/sail3/web/security_certs/sail_usc_edu_cert.cer','/home/sail3/web/security_certs/sail.key')
manager.add_command(
    'runserver',
    Server(port=1030, use_debugger=True, use_reloader=True, ssl_crt=context[0], ssl_key=context[1], threaded=True))


@manager.command
def runworker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()

if __name__ == '__main__':
    manager.run()
