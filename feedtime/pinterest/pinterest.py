from datetime import datetime
import pindb
import requests
from flask import request, session, redirect, render_template, Markup, Blueprint, Flask, jsonify
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
    url += '&redirect_uri=https://stormgiant.net/pinterest/connect'
    url += '&scope=read_public,write_public'
    return redirect(url, code=302)

@pinterest.route('/pinterest/connect')
def pinterest_connect():
    code =  request.args.get('code','')
    session['access_token'] = get_access_token(code) 
    session['username'] = get_username()
    return redirect('https://stormgiant.net/pinterest', code=302)

@pinterest.route('/pinterest/addpin', methods=['POST'])
def submit_pin():
    if 'access_token' not in session:
        return redirect('http://stormgiant.net/pinterest', code=400)
    pindb.insert_pin(request.form['source_board'],
                     request.form['target_board'],
                     request.form['note'],
                     request.form['pin'],
                     request.form['link'],
                     request.form['time'],
                     user = session['username'])
    return redirect('http://stormgiant.net/pinterest', code=302)

@pinterest.route('/pinterest/pins')
def request_pins():
    board = request.args.get('board', '')
    pins = get_pins_for_board(board)
    return jsonify(result=pins)

@pinterest.route('/pinterest/pinit')
def process_pending_pins():
    entries = pindb.get_databased_pins(session['username'])
    to_post = []
    posted = []
    url = '{0}/pins/'.format(_url)
    for entry in entries:
        if entry['is_posted'] == 0 and datetime.strptime(entry['time'],'%Y-%m-%dT%H:%M') < datetime.now():
            to_post.append(entry)
    for post in to_post:
        pin = '' 
        pins = get_pins_for_board(post['sourceboard'])
        for p in pins:
            if p['id'] == post['image_url']:
                pin = p['image']['original']['url']
                break
        if pin == '':
            continue
        payload = { 
               'access_token':session['access_token'],
               'board': post['targetboard'],
               'note': post['note'],
               'link': post['link'],
               'image_url': pin }
        r = requests.post(url,payload)
        if r.status_code == 200 or r.status_code == 201:
            posted.append(post['id'])
    
	pindb.update_posted_pins(posted)
    return redirect('/pinterest', code=302)

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

def get_username():
    url = '{0}/me/'.format(_url)
    payload = {'access_token': session['access_token'], 'fields': 'username,first_name,last_name'}
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

        


