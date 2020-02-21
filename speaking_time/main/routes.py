import os, sys
import redis
from flask import current_app
from speaking_time.config import *
from flask import request, redirect, render_template, flash, Blueprint, g, url_for, jsonify
from werkzeug.utils import secure_filename
from speaking_time.main import bp
from rq import Queue, push_connection, pop_connection
from wtforms import Form, validators, TextField, FloatField, FileField
ALLOWED_EXTENSIONS = set(['mp4', 'mkv', 'wav'])


def get_redis_connection():
    redis_connection = getattr(g, '_redis_connection', None)
    if redis_connection is None:
        redis_url = current_app.config['REDIS_URL']
        redis_connection = g._redis_connection = redis.from_url(redis_url)
    return redis_connection


@bp.before_request
def push_rq_connection():
    push_connection(get_redis_connection())


@bp.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ReusableForm(Form):
    emailID = TextField('Email Address', validators=[validators.required()])
#    mod_gender = TextField('Moderator Gender (M/F)', validators=[validators.required()])
#    mod_start = FloatField('Moderator Start Time (s)', validators=[validators.required()])
#    mod_end = FloatField('Moderator Start Time (s)', validators=[validators.required()])
    ipfile = FileField('File', validators=[validators.required()])
    
@bp.route('/tasks/<job_id>')
def job_status(job_id):
    q = Queue()
    job = q.fetch_job(job_id)
    if job is None:
        response = {'status': 'no job found'}
    else:
        if 'file_id' in job.meta.keys():
            filename = job.meta['file_id']
        else:
            filename = '-'
        if 'per_fem' in job.meta.keys():
            per_fem = job.meta['per_fem']
        else:
            per_fem = '-'
        if 'prog' in job.meta.keys():
            prog = job.meta['prog']
        else:
            prog = '-'

        response = {'task_status': job.get_status(),
                    'prog': prog,
                    'per_fem': per_fem,
                    'file_id': filename,
                    'task_id': job.get_id()}
    return jsonify(response)

@bp.route('/_run_task', methods=['GET', 'POST'])
def run_task():
    print("In task")
    if request.method == 'POST':
        print("In post") 
        email = request.form['email'].lower()
#        if email == "":
            ## Do something
#            print("Email not registered")
#            return redirect(url_for('index'))
       
        if 'inputfile' in request.files: 
            print("File uploaded")
            ipfile = request.files['inputfile']
            filename = secure_filename(ipfile.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            ipfile.save(filepath)
            ### Next two lines need to be run on another server!!
            job_queue = Queue()
            job = job_queue.enqueue('speaking_time.process_files.run_pipeline', args=(filepath, email), timeout=current_app.config['JOB_TIMEOUT'])
            
            response = {'task_status': job.get_status(),
                        'file_id': filename,
                        'prog' : 'Beginning inference',
                        'per_fem': '-',
                        'task_id': job.get_id()}
            print(response)
            return jsonify(response), 202
#            return jsonify({}), 202, {'Location': url_for('main.job_status', job_id = job.get_id())}

@bp.route('/')
def index():
    form = ReusableForm(request.form)
    return render_template('index.html', form=form)

@bp.route('/task')
def progress():
    return render_template("progress.html")
