import sqlite3
from flask import Flask,redirect,request,session,render_template
app=Flask(__name__)
app.secret_key = "secret123"
def createdb():
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("""create table if not exists users(
    id integer primary key autoincrement,
    username text,
    password text)""")
    cursor.execute("""create table if not exists tasks(
    id integer primary key autoincrement,
    title text,
    description text,
    status text)""")
    conn.commit()
    conn.close()
createdb()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        try:
            u=request.form["username"]
            p=request.form["password"]
            conn=sqlite3.connect("database.db")
            cursor=conn.cursor()
            cursor.execute("insert into users(username,password)values(?,?)",(u,p))
            cursor.execute("select * from users where username=? and password=?",(u,p))
            user=cursor.fetchone()
            conn.close()
            if user:
                session["user"]=u
                return redirect("/dashboard")
            else:
                 return "Invalid login"
        except Exception:
            return "Login Error"
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
     conn=sqlite3.connect("database.db")
     cursor=conn.cursor()
     search=request.args.get("search")
     if search:
        cursor.execute("select * from tasks where title like ?",('%'+search+'%',))
     else:
        cursor.execute("select * from tasks")
     tasks=cursor.fetchall()
     conn.close()
     return render_template('dashboard.html',tasks=tasks)

@app.route('/add',methods=["POST"])
def add():
    try:
        t=request.form["title"]
        d=request.form["description"]
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()
        cursor.execute("insert into tasks(title,description,status) values(?,?,?)",(t,d,"Pending"))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    except Exception:
        return "Error adding task"

@app.route('/delete/<int:id>',methods=["POST"])
def delete(id):
    try:
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()
        cursor.execute("delete from tasks where id=?",(id,))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    except Exception:
        return "Error deleting task"

@app.route('/update/<int:id>')
def update(id):
    try:
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()
        cursor.execute("update tasks set status='Done' where id=?",(id,))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    except Exception:
        return "Error updating tasks"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)


