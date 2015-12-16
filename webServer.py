import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash

from flask.ext.script import Manager,Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.mail import Mail,Message


app=Flask(__name__)



"""Load default config  """
app.config.update(dict(
	DATABASE=os.path.join(app.root_path,'center.db'),
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))

manager=Manager(app)
moment=Moment(app)
bootstrap=Bootstrap(app)



def connect_db():
	"""Connects to the specific database."""
	rv=sqlite3.connect(app.config['DATABASE'])
	rv.row_factory=sqlite3.Row
	return rv


def get_db():
	if not hasattr(g,'sqlite_db'):
		g.sqlite_db=connect_db()
	return g.sqlite_db


@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username']!=app.config['USERNAME']:
			error='Invalid username'
		elif request.form['password']!=app.config['PASSWORD']:
			error='Invalid password'
		else:
			session['logged_in']=True
			flash('You were logged in')
			return redirect(url_for('home'))
	return render_template('login.html',error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('index'))


@app.route('/')
def index():
	if session.get('logged_in'):
		return redirect(url_for('home'))
	else:
		return render_template('cover.html')


@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/show')
def show_entries():
	db=get_db()
	cur=db.execute('select GATEID,CARID,DATA,STATE from DATABASE where STATE=1')
	entries=cur.fetchall()
	return render_template('show_entries.html',entries=entries)


@app.route('/show_legal')
def show_legal():
	db=get_db()
	cur=db.execute('select GATEID,CARID,DATA,STATE from DATABASE where STATE=1')
	entries=cur.fetchall()
	return render_template('show_legal.html',entries=entries)

@app.route('/show_illegal')
def show_illegal():
	db=get_db()
	cur=db.execute('select GATEID,CARID,DATA,STATE from DATABASE where STATE=0')
	entries=cur.fetchall()
	return render_template('show_illegal.html',entries=entries)





@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/setDistance',methods=['GET','POST'])
def set_dist():
	db=get_db()
	cur=db.execute('select GATEID,DIST from DISTTAB')
	entries=cur.fetchall()

	if request.method=='POST':
		if not session.get('logged_in'):
			abort(401)
		db=get_db()
		db.execute('UPDATE DISTTAB SET GATEID=?,DIST=?',
					[request.form['gateid'],request.form['dist']])
		db.commit()
		flash('New distance has been seted ')
		return redirect(url_for('show_legal'))
	return render_template('setDistance.html')


@app.route('/add_permission',methods=['GET','POST'])
def add_permission():
	db=get_db()
	cur=db.execute('select GATEID,CARID,CARSRC from PERMISSION')
	entries=cur.fetchall()

	if request.method=='POST':
		if not session.get('logged_in'):
			abort(401)
		db=get_db()
		db.execute('insert into PERMISSION (GATEID,CARID,CARSRC) values (?,?,?)',
					[request.form['GATEID'],request.form['CARID'],request.form['CARSRC']])
		db.commit()
		flash('New entry was successfully posted')
		return redirect(url_for('home'))
	return render_template('add_permission.html')


if __name__=='__main__':
	manager.run()
