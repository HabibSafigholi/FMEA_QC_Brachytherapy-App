from flask import Flask , render_template, request, redirect 
import flask_login
import csv
import sqlite3
from datetime import datetime
import uuid
from flask_login import  logout_user

app = Flask(__name__)
database_filename = "tasker.db"
app.config['SECRET_KEY'] = 'sdsd dfd ewer qwqfdlk'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, userid, email, name):
        self.id = userid
        self.email = email
        self.name = name
 
    def get_dict(self):
        return {'userid': self.id, 'email': self.email, 'name': self.name}

@login_manager.user_loader
def load_user(userid):
    users = database_read(f"SELECT * FROM accounts WHERE userid = '{userid}';")
    if len(users) !=1:
        return  None
    user = User(users[0]['userid'],users[0]['email'], users[0]['name'])
    user.id = userid
    return user

def database_write(sql, data=None):
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
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

	
@app.route("/")
def index_page():
    if  flask_login.current_user.is_authenticated:
	    return redirect ("/main")
    else:
        return redirect ("/login")		
	
@app.route("/register")
def registeration_page():
#    return "Registration page"
    return render_template ("register.html")
	
	
		
@app.route("/login", methods = ['GET'])
def login_page():

    return render_template ("login.html" , alert = "")
	
	
	
@app.route("/login", methods = ['POST'])
def login_request():
    #return "received a form"
    form = dict(request.values)
    users = database_read("SELECT * FROM accounts WHERE userid=:userid AND password=:password", form)
    if len(users) == 1:
        user = load_user (form['userid'])
        flask_login.login_user(user)
        return redirect ("/main")
    else:
        return render_template("login.html", alert= "Invalid user/password. please try again.")		

@app.route("/logout")	
@flask_login.login_required
def logout_page():
    flask_login.logout_user()
 #   logout_user()
    return redirect ("/")



@app.route("/main")	
@flask_login.login_required
def main_page():
    folderid="0"
    if 'folderid' in request.values:
        folderid = request.values['folderid']
    id ='1'
    if 'id' in request.values:
        id  = request.values ['id']
    user = {
        'name':'Mark ',
        'userid': 'HS125'
           }
    folders = database_read("SELECT * FROM folders ORDER BY name;")
    items = database_read(f"SELECT * FROM tasks WHERE folderid='{folderid}' AND status != 'Completed';")
	# items = database_read(f"SELECT * FROM tasks WHERE folderid='{folderid}' AND status != 'Completed';")
    maintask = database_read(f"SELECT * FROM tasks WHERE id='{id}';")
    if len(maintask)==1:
        maintask = maintask[0]
    else:
        maintask = {}
    return render_template("main.html", user=user, folders=folders, tasks=items, maintask=maintask, folderid=folderid, id=id)


@app.route("/save_task", methods =["POST"])
@flask_login.login_required
def task_update():
    form = dict(request.values)
    id = form['id']
    folderid = form['folderid']
    print("Form info received", form)
    if "submit-close" in form:
	    form['status'] = "Completed"
    if "submit-delete" in form:
        database_write(f"DELETE FROM tasks WHERE id={id};")
        return redirect(f"/main?folderid={folderid}")
    if id == "": # New task
        id = str(uuid.uuid1())
        form['id']=id
        form['link']= ""
        form['created'] = datetime.now().strftime("%Y-%m-%d")
        sql ="""INSERT INTO tasks
			(userid, folderid, id, title, due, category, Potentail_failure_mode,  Potentail_cause_failure, Potentail_effects_failure, Occurrence, Severity, Detect, RPN, status, notes, link) VALUES
            (:userid, :folderid, :id, :title, :due, :category, :Potentail_failure_mode, :Potentail_cause_failure,  :Potentail_effects_failure, :Occurrence, :Severity, :Detect, :RPN, :status, :notes, :link);"""
        ok = database_write (sql, form)
        if ok == 1:
            return redirect(f"/main?folderid={folderid}&id={id}")
        else:
            return redirect(f"/error?folderid={folderid}&id={id}")

    else: # Existing task
        form ['link']= ""
        sql ="UPDATE tasks SET title=:title, due=:due, category=:category, Potentail_failure_mode=:Potentail_failure_mode, Potentail_cause_failure=:Potentail_cause_failure, Potentail_effects_failure=:Potentail_effects_failure, Occurrence=:Occurrence, Severity=:Severity, Detect=:Detect,RPN=:RPN, status=:status, notes=:notes, link=:link WHERE id=:id;"
        ok = database_write (sql, form)
        if ok == 1:
            return redirect(f"/main?folderid={folderid}&id={id}")
        else:
            return redirect(f"/error?folderid={folderid}&id={id}")
        return("ok")
	
@app.route("/new_folder", methods=["POST"])
@flask_login.login_required
def creat_new_folder():
    form = dict(request.values)
    id = str(uuid.uuid1())
    form['id'] = id
    sql = f"INSERT INTO folders (userid, id, name) VALUES (:userid, '{id}', :name);"
    ok = database_write (sql, form)
    if ok == 1:
        return "ok"
    else:
        return "ERR"

@app.route("/error")
def error_page():
    return "THERE WAS AN ERROR!!!"
	
app.run(debug=True)
