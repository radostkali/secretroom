from .. import socketio, redis
from flask_socketio import emit, join_room, leave_room
from flask import session


@socketio.on('disconnect')
def disconnect():
    try:
        room = session['room']
        user = session['user']
    except KeyError as e:
        print(e)
    leave_room(room)
    response = {
        'state': 'disconnected',
        'user': user
    }
    emit(
        'room',
        response,
        room=room
    )


@socketio.on('message')
def message(data):
    try:
        room = session['room']
    except KeyError as e:
        print(e)
    response = {
        'state': 'message',
        'message': str(data['encrypted']),
        'user': int(data['user']),
        'id': str(data['id'])
    }
    emit(
        'room',
        response,
        room=room
    )


@socketio.on('writing')
def writing(data):
    try:
        room = session['room']
        user = session['user']
    except KeyError as e:
        print(e)
    response = {
        'state': 'writing',
        'status': int(data['status']),
        'user': user
    }
    emit(
        'room',
        response,
        room=room
    )


@socketio.on('join')
def on_join(data):
    user = data['user']
    room = data['room']
    session['room'] = room
    session['user'] = user
    join_room(room)
    keys = redis.hgetall(room)
    response = {
        'state': 'connected',
        'user': user,
        'pubkey_1': keys['user_1'],
        'pubkey_2': keys['user_2']
    }
    emit(
        'room',
        response,
        room=room
    )


@socketio.on('leave')
def on_leave(data):
    command = data['command']
    user = session['user']
    room = session['room']
    leave_room(room)
    if command == 'reconnect':
        response = {
            'state': 'reconnecting',
            'user': user
        }
    elif command == 'leave':
        response = {
            'state': 'disconnected',
            'user': user
        }
    emit(
        'room',
        response,
        room=room
    )

