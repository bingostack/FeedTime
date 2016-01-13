import sqlite3

def connect_to_db():
    return sqlite3.connect('/tmp/pin.db')

def get_access_token(username):
    db = connect_to_db();
    query = "select access_code from auth where username='{0}'".format(username)
    curs = db.cursor()
    curs.execute(query)
    return curs.fetchone()   

def get_all_access_tokens():
    db = connect_to_db();
    query = 'select * from auth'
    curs = db.cursor()
    curs.execute(query)
    return curs.fetchall()   

def update_access_token(username, code):
    query = ''
    if get_access_token(username) is not None:
       query = "update auth set access_code='{0}' where username='{1}'".format(code, username) 
    else:
        query = "insert into auth(username, access_code) values('{0}', '{1}')".format(username, code)
    db = connect_to_db()
    db.execute(query)
    db.commit()
    db.close()

def insert_pin(source, target, note, image_url, link, time, user, pin_id):
    query = 'insert into pins(sourceboard, targetboard, note, image_url, link, datetime, is_posted, pin_user, pin_id) '
    query += "values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '0', '{6}', '{7}')"
    query = query.format(source, target, note, image_url, link, time, user, pin_id)
    db = connect_to_db()
    db.execute(query)
    db.commit()
    db.close()

def update_posted_pins(posted):
    if len(posted) == 0:
        return
    query = 'update pins set is_posted=1 where id='    
    db = connect_to_db()
    for pid in posted:
        db.execute(query + str(pid))
    db.commit() 
    db.close()

def get_databased_pins(username):
    query = "select * from pins where pin_user = '{0}'".format(username)
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    entries = []
    for row in rows:
        entry = dict(id=row[0], 
						sourceboard = row[1], 
                        targetboard = row[2], 
                        board = row[2][row[2].find('/')+1:],
                        note = row[3], 
                        image_url = row[4], 
                        link = row[5], 
                        time = row[6], 
                        is_posted = row[7], 
                        user = row[8],
                        pin_id=row[9]) 
        entries.append(entry)
    db.close()
    return entries
        


