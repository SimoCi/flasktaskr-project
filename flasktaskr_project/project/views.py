# project/views.py

#################
#### imports ####
#################

from project import app, db
from project.models import Task
from flask import flash, redirect, session, url_for, \
render_template, request, jsonify, make_response
from functools import wraps
import logging as log
import datetime
# import json


##########################
#### helper functions ####
##########################

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


################
#### routes ####
################

@app.route('/', defaults={'page': 'index'})
def index(page):
    return redirect(url_for('tasks.tasks'))


########################
#### error handlers ####
########################

# catches the 404 error, replaces the default template with 404.html
@app.errorhandler(404)
def page_not_found(error):
    print app.debug
    if app.debug is not True:
        print app.debug
        now = datetime.datetime.now()
        r = request.url
        # with open('error.log', 'a') as f:
        #     current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
        #     f.write("\n404 error at {}: {}".format(
        #         current_timestamp, 
        #         r
        #         )
        #     )
        current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
        log.basicConfig(filename='error.log', level=log.DEBUG)
        log.debug("\n404 error at {}: {}".format(
                current_timestamp, 
                r
                )
        )
    else:
         print "app.debug: {}, manjime el kool".format(app.debug)
    return render_template('404.html'), 404

# catches the 500 error, replaces the default template with 500.html
@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        # with open('error.log', 'a') as f:
        #     current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
        #     f.write("\n500 error at {}: {}".format(
        #         current_timestamp, 
        #         r
        #         )
        #     )
        current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
        log.basicConfig(filename='error.log', level=log.DEBUG)
        log.debug("\n500 error at {}: {}".format(
                current_timestamp, 
                r
                )
        )
    return render_template('500.html'), 500


# REST API

# collection
@app.route('/api/tasks/', methods=['GET'])
def tasks():
    if request.method == 'GET':
        results = db.session.query(Task).limit(10).offset(0).all()
        json_results = []
        for result in results:
            data = {
                'task_id': result.task_id,
                'task name': result.name,
                'due date': str(result.due_date),
                'priority': result.priority,
                'posted date': str(result.posted_date),
                'status': result.status,
                'user id': result.user_id
            }
            json_results.append(data)

    # return json.dumps(data), 200, { "Content-Type" :"application/json"}
    return jsonify(items=json_results)

# specific item in collection
@app.route('/api/tasks/<int:task_id>')
def task(task_id):
    if request.method == 'GET':
        result = db.session.query(Task).filter_by(task_id=task_id).first()

        if result:
            result = {
                    'task_id': result.task_id,
                    'task name': result.name,
                    'due date': str(result.due_date),
                    'priority': result.priority,
                    'posted date': str(result.posted_date),
                    'status': result.status,
                    'user id': result.user_id
                }
            code = 200

            # return json.dumps(data), 200, { "Content-Type" :"application/json"}
            # return jsonify(items=json_result, code)
        else:
            result = {"sorry": "Element does not exist"}
            code = 404
        return make_response(jsonify(result), code)

