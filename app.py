from flask import Flask, session, redirect, url_for, escape, request, render_template
import pymysql

app = Flask(__name__)
db = pymysql.connect("localhost", "root", "password", "fashionhub")
cur = db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('welcome.html', session_user_name=username_session)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        cur.execute("SELECT COUNT(1) FROM user WHERE username = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE username = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                raise SyntaxError('invalid password')
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/user', methods=['GET', 'POST'])
def user():
        username_session = escape(session['username']).capitalize()
        return render_template('user.html', session_user_name=username_session)

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        emploName_form = request.form['employeeName']
        password_form = request.form['password']
        departmentId_form = request.form['departmentId']
        designation_form = request.form['designation']
        emailId_form = request.form['emailId']
        phone_form = request.form['phone']
        sql = "INSERT INTO employee (empname,emppassword,deptid,designation,email,phone) values (%s,%s,%s,%s,%s,%s)"
        val = (emploName_form,password_form,departmentId_form,designation_form,emailId_form,phone_form)
        cur.execute(sql, val)
        db.commit()
        return render_template('welcome.html')



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)