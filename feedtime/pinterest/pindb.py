import sqlite3

def connect_to_db():
    return sqlite3.connect('/tmp/pin.db')

def insert_pin(source, target, note, pin, link, time, user):
    query = 'insert into pins(sourceboard, targetboard, note, image_url, link, datetime, is_posted, pin_user) ' 
    query += "values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '0', '{6}')"
    query = query.format(source, target, note, pin, link, time, user)
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
                        note = row[3], 
                        image_url = row[4], 
                        link = row[5], 
                        time = row[6], 
                        is_posted = row[7], 
                        user = row[8]) 
        entries.append(entry)
    db.close()
    return entries
        


