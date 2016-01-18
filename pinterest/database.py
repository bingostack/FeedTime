import sqlite3
from contextlib import closing
from feedtime import app

class PinDb(object):
    
    def __init__(self, db='/tmp/pin.db'):
        self.db = db

    def connect_to_db():
        return sqlite3.connect(self.db)

    def init_db():
        with closing(connect_db) as db:
            with app.open_resource('pinterest/schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

