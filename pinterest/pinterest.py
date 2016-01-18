from datetime import datetime
import pindb
import requests
from flask import request, session, redirect, render_template, Markup, Blueprint, Flask, jsonify, url_for
from . import pinterest
from contextlib import closing

__client_id = '4807395013948353036'
__client_secret = '5d620491b5d91462cc2c945db562bc40a1c02c57840a554c7e1cde025ded513f'
_url = 'https://api.pinterest.com/v1'

@pinterest.route('/pinterest')
def pinterest_home():
    if 'access_token' in session:
        boards = get_boards()
        entries = pindb.get_databased_pins(session['username'])
        return render_template('pinterest.html', boards=boards, entries=entries) 
    else:
        return render_template('welcome.html')

@pinterest.route('/pinterest/login')
def pinterest_login():
    url = 'https://api.pinterest.com/oauth/'
    url += '?response_type=code'
    url += '&client_id=' + __client_id
    url += '&state=tw399afd'
    url += '&redirect_uri=https://stormgiant.net'+url_for('pinterest.pinterest_connect')
    url += '&scope=read_public,write_public,read_relationships,write_relationships'
    return redirect(url, code=302)

@pinterest.route('/pinterest/connect')
def pinterest_connect():
    code =  request.args.get('code','')
    token = get_access_token(code)
    session['access_token'] = token 
    username = get_username()
    session['username'] = username
    pindb.update_access_token(username, token)
    return redirect(url_for('pinterest.pinterest_home'), code=302)

@pinterest.route('/pinterest/addpin', methods=['POST'])
def submit_pin():
    if 'access_token' not in session:
        return redirect(url_for('pinterest.pinterest_home'), code=302)
    source = request.form['source_board']
    pin_id = request.form['pin_id']
    url = get_url_for_pin(source, pin_id)
    pindb.insert_pin(source,
                     request.form['target_board'],
                     request.form['note'],
                     url,
                     request.form['link'],
                     request.form['time'],
                     session['username'],
                     pin_id)
    return redirect(url_for('pinterest.pinterest_home'), code=302)

@pinterest.route('/pinterest/pins')
def request_pins():
    board = request.args.get('board', '')
    pins = get_pins_for_board(board)
    return jsonify(result=pins)

@pinterest.route('/pinterest/pinit')
def process_pending_pins():
    tokens = pindb.get_all_access_tokens()
    to_post = []
    posted = []
    result = ''
    for token in tokens:
        entries = pindb.get_databased_pins(token[1])
        post_url = '{0}/pins/'.format(_url)
        for entry in entries:
            if entry['is_posted'] == 0 and datetime.strptime(entry['time'],'%Y-%m-%dT%H:%M') < datetime.now():
                to_post.append([entry, token[2]])
    for post_pair in to_post:
        post = post_pair[0]
        token = post_pair[1]
        session['access_token'] = token
        pin_url = get_url_for_pin(post['sourceboard'], post['pin_id'])
        if pin_url is None:
            continue
        payload = { 
               'access_token': token,
               'board': post['targetboard'],
               'note': post['note'],
               'link': post['link'],
               'image_url': pin_url }
        r = requests.post(post_url, payload)
        result += r.text
        if r.status_code == 200 or r.status_code == 201:
            posted.append(post['id'])
    pindb.update_posted_pins(posted)
    return result

def get_boards():
    payload = { 'access_token':session['access_token'], 'fields':'id,name,url'}
    r = requests.get(_url + '/me/boards/', params=payload)
    boards = []
    for b in r.json()['data']:
        arr = b['url'].split('/')
        boards.append([arr[3], arr[4]])
    return boards

def get_pins_for_board(board):
    payload = { 'access_token':session['access_token'], 'fields':'note,id,link,url,board,image'}
    r = requests.get(_url + '/boards/{0}/pins/'.format(board), params=payload)
    return r.json()['data']

def get_url_for_pin(board, pin_id):
    pins = get_pins_for_board(board)
    for p in pins:
        if p['id'] == pin_id:
            return p['image']['original']['url']
    return None

def get_username():
    url = '{0}/me/'.format(_url)
    token = session['access_token']
    payload = {'access_token': token, 'fields': 'username,first_name,last_name'}
    r = requests.get(url, params=payload)
    return r.json()['data']['username']

def get_access_token(code):
    url = '{0}/oauth/token'.format(_url)
    payload = {'grant_type': 'authorization_code', 
               'client_id': __client_id,
               'client_secret': __client_secret,
               'code': request.args.get('code', '')}
    r = requests.post(url, payload)
    return r.json()['access_token']

