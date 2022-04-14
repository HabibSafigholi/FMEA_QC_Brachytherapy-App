import sqlite3
import uuid
import hashlib
import getpass

database_filename = "tasker.db"

def database_write(sql, data=None):
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
  # rows_affected =0
    if data:
        rows_affected = db.execute(sql, data).rowcount
    else:
        rows_affected = db.execute(sql).rowcount
    connection.commit()
    db.close()
    connection.close()
    return rows_affected

def database_read(sql, data=None):
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
    if data:
        db.execute(sql, data) 
    else:
        db.execute(sql)
    records =db.fetchall() 
    rows = [dict(record) for record in records]	
    db.close()
    connection.close()
    return rows

def registeration_page():
    userid = input("userid: ")
    email = input("email: ")
    name = input("name: ")
    password = getpass.getpass("Password:")
#   salt = str(uuid.uuid1())
#   key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 10000).hex()
    sql = f"INSERT INTO accounts (userid, password, email, name) VALUES (:userid,  :password, :email, :name); "
    record ={
        "userid": userid,
#       "salt": salt,
        "password": password,
        "email" : email,
        "name": name
    }
    ok = database_write(sql, record)
    print (ok)

registeration_page()
