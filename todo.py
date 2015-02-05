from flask import Flask, request , url_for,redirect
import sqlite3
dbFile='db1.db'
conn=None
def get_conn():
    global conn
    if conn is None :
        conn=sqlite3.connect(dbFile)
        conn.row_factory=sqlite3.Row
    return conn
def close_conn():
    global conn
    if conn is not None :
        conn.close()
        conn= None
    return conn
def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    r = cur.fetchall()
    cur.close()
    return (r[0] if r else None) if one else r
def add_task(category):
    query_db('insert into tasks(category) values(?)', [category], one = True)
    get_conn().commit()
def print_tasks():
    tasks = query_db('select * from tasks')
    for task in tasks:
        print("Task(category): %s " %task['category'])
        print ("%d tasks in total." %len(tasks))
        app = Flask(__name__)
        tasks= []
@app.route('/')
def welcome():
    return '<h1>Welcome to flask</h1>'

@app.route('/task1',methods=['GET','POST'])

def task():
#POST
    if request.method=='POST':
        category = request.form['category']
        tasks.append({'category':category})
        #return redirect('/task1')
        return redirect(url_for('task'))
    
    resp='''
    <form action ="" method=post>
    <p>Category <input type =text name = category ></p>
    <p><input type = submit value = Add ></p>
    </form>
    '''
     # show the table
    resp = resp + '''
    <table border="1" cellpadding="3">
    <tbody>
    <tr>
    <th>Category</th>
    </tr>
    '''
    for task in tasks:
        resp = resp + "<tr><td>%s</td></tr>" %(task['category'])
    resp = resp + '</tbody></table>'
    return resp
      

if __name__ == '__main__':
    app.debug=True
    app.run()