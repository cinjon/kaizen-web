from app import db

def add(transaction):
    #Will be queue later on
    db.session.add(transaction)
    commit()

def commit():
    db.session.commit()
