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
bootstrap=Bootstrap(app)
moment=Moment(app)




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
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))



@app.route('/')
def show_entries():
	db=get_db()
	cur=db.execute('select GATEID,CARID,DATA,STATE from DATABASE where STATE=1')
	entries=cur.fetchall()
	return render_template('show_entries.html',entries=entries)


@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db=get_db()
	db.execute('insert into DATABASE (GATEID,CARID,DATA,STATE) values (?,?,?,?)',
				[request.form['GATEID'],request.form['CARID'],request.form['DATA'],
				 request.form['STATE']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

if __name__=='__main__':
	manager.run()
