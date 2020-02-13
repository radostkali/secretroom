from flask import jsonify, session, request
from shortuuid import ShortUUID
from . import main
from secret_room import redis
from datetime import timedelta


api_messages = {
    'no_room': {'status': 'error', 'message': 'No room with this id'},
    'error': {'status': 'error', 'message': 'Something went wrong'},
    'key_error': {'status': 'error', 'message': 'Key error'},

    'room_ready': {'status': 'success', 'message': 'Room is ready'},
    'key_received': {'status': 'success', 'message': 'Key received'},
    'key_verified': {'status': 'success', 'message': 'Key verified'},
    'reconnected': {'status': 'reconnected', 'message': 'Reconnected'},
}


@main.route('/api/create_room', methods=['POST'])
def create_room():
    room_id = ShortUUID().random(length=8)
    while redis.exists(room_id):
        room_id = ShortUUID().random(length=8)
    session['room'] = room_id
    session['user'] = None
    redis.hmset(room_id, {'user_1': '', 'user_2': ''})
    redis.expire(room_id, timedelta(days=1))
    return jsonify({'room_id': room_id})


@main.route('/api/check_room', methods=['GET'])
def check_room():
    print('check_room_func')
    room_id = request.args.get('room_id')
    if room_id is None:
        return jsonify(api_messages['error'])
    else:
        key_1 = redis.hget(room_id, 'user_1')
    if key_1 is None:
        return jsonify(api_messages['no_room'])
    elif key_1 == '':
        if 'room' not in session:
            return jsonify(api_messages['no_room'])
        elif session['room'] != room_id:
            return jsonify(api_messages['no_room'])
        else:
            user = 1
            session['user'] = user
            return jsonify({**api_messages['room_ready'], 'user': user})
    else:
        key_2 = redis.hget(room_id, 'user_2')
        if 'user' in session:
            if room_id == session['room'] and session['user'] == 1:
                return jsonify({**api_messages['reconnected'], 'user': 1})
        if key_2 == '':
            session['room'] = room_id
            user = 2
            session['user'] = user
            return jsonify({**api_messages['room_ready'], 'user': user})
        else:
            if 'user' in session:
                if room_id == session['room'] and session['user'] == 2:
                    return jsonify({**api_messages['reconnected'], 'user': 2})
            return jsonify(api_messages['no_room'])


@main.route('/api/send_pubkey', methods=['POST'])
def send_pubkey():
    print('send_pubkey_func')
    try:
        room_id = session['room']
        user = int(session['user'])
        pubkey = request.json['pubkey']
    except KeyError as e:
        print(e)
        return jsonify(api_messages['error'])
    redis_key = redis.hget(room_id, f'user_{ user }')
    if pubkey is None or pubkey == '':
        return jsonify(api_messages['error'])
    elif redis_key is None:
        return jsonify(api_messages['no_room'])
    elif redis_key != '':
        return jsonify(api_messages['no_room'])
    else:
        redis.hset(room_id, f'user_{ user }', pubkey)
        return jsonify(api_messages['key_received'])


@main.route('/api/verify_pubkey', methods=['POST'])
def verify_pubkey():
    print('verify_pubkey')
    try:
        room_id = session['room']
        user = int(session['user'])
        pubkey = request.json['pubkey']
    except KeyError as e:
        print(e)
        return jsonify(api_messages['error'])
    redis_key = redis.hget(room_id, f'user_{user}')
    if redis_key == pubkey:
        return jsonify(api_messages['key_verified'])
    else:
        return jsonify(api_messages['key_error'])
