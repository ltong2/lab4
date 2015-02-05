from flask import Flask, request , url_for,redirect
import sqlite3
app =Flask (__name__)
dbFile='db1.db'
conn=None

def get_conn():
    global conn
    if conn is None :
        conn=sqlite3.connect(dbFile)
        conn.row_factory=sqlite3.Row
    return conn

@app.teardown_appcontext
def close_conn(a):
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

def add_task(category,priority, description):
    tasks= query_db('insert into tasks(category,priority, description) values(?,?,?) ', (category,priority,description), one = True)
        
    get_conn().commit()
    
@app.route('/')
def welcome():
    return '<h1>Welcome to Flask lab</h1>'

def print_tasks():
    tasks = query_db('select * from tasks')
    for task in tasks:
        print("Task(category): %s " %task['category'])
    print ("%d tasks in total." %len(tasks))

@app.route('/task', methods = ['GET', 'POST'])
def task():
    #POST:
    if request.method == 'POST':
            get_conn()
            category = request.form['category']
            priority = request.form['priority']
            description = request.form['description']
            add_task(category, priority, description)
            return redirect(url_for('task'))        
        
    #GET:
    resp =  '''
           <form action ="" method =post>
               <p>Category <input type=text name=category></p>
               <p>Priority <input type=text name=priority></p>
               <p>Description <input type=text name=description></p>
               <p><input type=submit value=Add></p>
           </form>
           '''
           
    #Show table
    resp = resp + '''
           <table border="1" cellpadding="3">
                <tbody>
                    <tr>
                        <th>Category</th>
                        <th>Priority</th>
                        <th>Description</th>
                    </tr>
            '''                   
                   
    for task in query_db('select * from tasks'):
            resp = resp + "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" %(task['category'], task['priority'], task['description'])
    resp = resp + '</tbody></table>'
    return resp                            


      

if __name__ == '__main__':
    app.debug=True
    app.run()