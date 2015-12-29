import sqlite3
import requests
from flask import request, session, redirect, render_template, flash, Markup, Blueprint, Flask
from . import pinterest

__client_id = '4807395013948353036'
__client_secret = '5d620491b5d91462cc2c945db562bc40a1c02c57840a554c7e1cde025ded513f'
_url = 'https://api.pinterest.com/v1'

@pinterest.route('/pinterest')
def pinterest_home():
    if 'access_token' in session:
        boards = get_boards()
        pins = get_pins_for_board(boards[0]['name'], session['username'])
        return render_template('pinterest.html', boards=boards, pins=pins)
    else:
        return render_template('pinterest.html')

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

@pinterest.route('/pinterest/schedule', methods=['POST'])
def submit_pin():
    board = request.form['board']
    pin = request.form['pin']
    pins = get_pins_for_board(board)
    selected_pin = None
    for p in pins:
	    if p['note'] == pin:
	        selected_pin = p
            break
    if selected_pin is None:
         return Markup('Pinning failed')
    payload = {'board': 'danbusha/'+board,
               'note': p['note'], 
               'image_url': p['image']['original']['url'],
               'access_token':session['access_token']}
    url = '{0}/pins'.format(_url)
    r = requests.post(url, payload)
    return Markup(r.text)

def get_boards():
    payload = { 'access_token':session['access_token'], 'fields':'id,name'}
    r = requests.get(_url + '/me/boards/', params=payload)
    return r.json()['data']

def get_pins_for_board(board, user):
    payload = { 'access_token':session['access_token'], 'fields':'note,id,link,url,board,image'}
    r = requests.get(_url + '/boards/{0}/{1}/pins/'.format(session['username'], board), params=payload)
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
