from __future__ import division
import sys, os
from flask import Flask
from flask import current_app
from rq import get_current_job
from speaking_time.config import *
from speaking_time.email import send_email
import glob
import shutil
import time

#OUT_DIR='/Users/rabbeh/Projects/ITU/flask_proj/mod_proj/app/out_dir'
def run_pipeline(data_filepath, emailID):
    job = get_current_job()
#    gender = {'male':'M', 'female':'F'}
    if emailID != "":
        MAIL_RECIPIENTS=[emailID]

    filename = data_filepath.rsplit('/')[-1].split('.')[0]
    job.meta['file_id'] = filename
    job.save_meta()
       
    
    time.sleep(5)
    job.meta['prog'] = 'Extracting audio (1/6)'
    job.save_meta()

    
    ## Create logmel feats
    time.sleep(5)
    job.meta['prog'] = 'Computing features for speech detection (2/6)'
    job.save_meta()

    ## Generate VAD labels; NOTE: not optimized for multiple-files, please see speaking_time_non_controlled.sh
    time.sleep(5)
    job.meta['prog'] = 'Detecting speech regions (3/6)'
    job.save_meta()

    ## Speaker segmentation
    time.sleep(5)
    job.meta['prog'] = 'Speaker segmentation (4/6)'
    job.save_meta()
    
    ## Extract vggish-embeddings
    time.sleep(5)
    job.meta['prog'] = 'Computing features for gender ID (5/6)'
    job.save_meta()

    ## Predict Gender
    time.sleep(5)
    job.meta['prog'] = 'Determining gender for speech segments (6/6)'
    job.save_meta()
    
    
    
    job.meta['prog'] = 'Done inference'
    job.save_meta()
    
    
    msg = 'Hi\nFile {} has been processed.'
    
    if emailID != '':
        send_email(subject = MAIL_SUBJECT, sender = MAIL_USERNAME, recipients = MAIL_RECIPIENTS, text_body=msg, html_body='', sync=True)

if __name__=='__main__':
    data_path = sys.argv[1]
    run_pipeline(data_path)
