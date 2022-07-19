from flask import Flask, render_template, url_for, request, flash,current_app, redirect
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import os
import datetime


app = Flask(__name__)

app.secret_key = ''
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

def add_logo(update):

    if update :
        image = update.filename
        image_folder = 'static/images/{0}'.format(image)
        filepath = os.path.join(current_app.root_path, image_folder)
        
        update.save(filepath)
        flash('success')
    else:
        flash('Error')

@app.route('/')
def index():
    
    return render_template("index.html", )


@app.route('/portal')
def portal():

    return render_template('portal.html')

@app.route('/submitform', methods= ['GET', 'POST'])
def submitform():
    if request.method == 'POST':
        upload = request.files['upload']
        image = upload.filename
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        email = request.form['email']
        gender = request.form['gender']
        dob = request.form['dob']
        sog = request.form['sog']
        log = request.form['log']
        nok = request.form['nok']
        address = request.form['address']
        jscore = request.form['jscore']
        pnumber = request.form['pnumber']
        add_logo(upload)    
        conn = mysql.get_db()
        cur = conn.cursor()
        cur.execute('insert into studentportal.list(imagename, lastname, firstname, middlename, gender, email, jambscore, phonenumber, address, dateofbirth, stateoforigin, localgovernment, nextofkin) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (image, lname, fname, mname, gender, email, jscore, pnumber, address, dob, sog, log, nok))
        conn.commit()
        cur.close()

        return redirect('/pdisplay')
        


@app.route('/pdisplay')
def pdisplay():
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from list ')
    rv = cur.fetchall()
    
    return render_template("pdisplay.html", words=rv)

@app.route('/searchword', methods=['POST'])
def search_word():
    req = request.get_json()
    sname = req['sname']
    sstatus = req['sstatus']
    sgender= req['sgender']
    sscore = req['sscore']
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from studentportal.list where lastname=%s or middlename=%s or firstname=%s or admissionstatus=%s or gender=%s or jambscore=%s', (sname, sname, sname, sstatus, sgender, sscore))
    conn.commit()
    cur.close()
    
    return 'success'

@app.route('/information/<id>')
def information(id):
    word_id = id
    conn = mysql.get_db()
    cur = conn.cursor()
    cur.execute('select * from studentportal.list where id=%s',(word_id))
    rv = cur.fetchall()

    return render_template('information.html', words= rv)

@app.route('/changestatus', methods = ['POST','GOT'])
def change_status():
    if request.method == 'POST': 
        if request.form['sstatus'] == "":

            return redirect('/pdisplay')

        else:
            sid = request.form['sid']
            sstatus = request.form['sstatus']
            conn = mysql.get_db()
            cur = conn.cursor()
            cur.execute('update studentportal.list set admissionstatus = %s where id = %s', (sstatus, sid))
            conn.commit()
            cur.close()

            return redirect('/pdisplay')



if __name__ == "__main__":
    app.run(debug=True)