import json
# import os
from flask import (
    Flask, flash, get_flashed_messages, redirect,
    render_template, request, session, url_for
)
from validator import validate


app = Flask(__name__)
# users = []
# 'mike', 'mishel', 'adel', 'keks', 'kamila']
temp = 1


app.config['SECRET_KEY'] = 'popa'


@app.get('/users')
def users_get():
    users = json.loads(request.cookies.get('users', json.dumps({})))
    # filtered_users = users
    # pattern = request.args.get('username_pattern', '')
    # if pattern:
    # filtered_users = filter(lambda user: pattern in user, users)

    # with open('users_list.txt') as f:
    # for user in f.readlines():
    # users.append(json.loads(user))

    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'users/index.html',
        users=users,    # filtered_users,
        search='',    # pattern,
        messages=messages,
    )


# @app.post('/users')
# def users_post():
    # return 'Users', 302


@app.route('/users/new')
def users_new():
    user = {}
    errors = {}

    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


@app.post('/users')
def users_post():
    user = request.form.to_dict()
    errors = validate(user)

    if errors:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors,
        )

    global temp
    id = temp
    temp += 1

    user['id'] = id

    users = json.loads(request.cookies.get('users', json.dumps({})))
    users[id] = user

    resp = redirect(url_for('users_get'))
    resp.set_cookie('users', json.dumps(users))
    # with open('users_list.txt', 'w') as f:
    # f.write(json.dumps(user))

    flash('User was added successfully', 'success')

    return resp


@app.get('/users/<id>/edit')
def users_update(id):
    users = json.loads(request.cookies.get('users', json.dumps({})))
    # user = ''
    # with open('users_list.txt') as f:
    # user = json.loads(f.read())

    errors = {}

    return render_template(
        'users/edit.html',
        user=users[id],
        errors=errors,
    )


@app.post('/users/<id>/edit')
def users_update_post(id):
    # user = ''
    # with open('users_list.txt') as f:
    # user = json.loads(f.read())

    data = request.form.to_dict()
    errors = validate(data)

    if errors:
        return render_template(
            'users/edit.html',
            user=data,
            errors=errors,
        ), 422

    users = json.loads(request.cookies.get('users', json.dumps({})))

    users[id]['nickname'] = data['nickname']
    users[id]['email'] = data['email']

    resp = redirect(url_for('users_get'))
    resp.set_cookie('users', json.dumps(users))
    # with open('users_list.txt', 'w') as f:
    # f.write(json.dumps(user))
    flash('User has been successfully updated', 'success')

    return resp    # redirect(url_for('users_get'))


@app.post('/users/<id>/delete')
def users_delete(id):
    users = json.loads(request.cookies.get('users', json.dumps([])))

    for user_id, _ in users.items():
        if user_id == id:
            users.pop(user_id)
        break

    resp = redirect(url_for('users_get'))
    resp.set_cookie('users', json.dumps(users))
    # with open('users_list.txt', 'w') as f:
    # f.write('')

    flash('User has been successfully deleted', 'success')
    return resp


@app.get('/login')
def login():
    email = request.form.get('email', '')
    return render_template('/login.html', email=email)


@app.post('/login')
def login_post():
    session['email'] = request.form.get('email')

    return redirect(url_for('users_get'))


@app.post('/logout')
def logout():
    session.clear()

    return redirect(url_for('login'))


@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'
