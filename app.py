# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Program name: app.py                               
#-----------------------------------------------------------------------------
# https://peterberces.com                                                
# This is a Python Flask Project file called AggregatorSearch.com
#-----------------------------------------------------------------------------                                             
"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bcrypt import Bcrypt
import sqlite3 as sql
import datetime

#-----------------------------------------------------------------------------
# Variables
#-----------------------------------------------------------------------------
WEBSITE_NAME='AggregatorSearch.com'
WEBSITE_TAGLINE='The Ultimate Aggregator Search Engine - Result lists from: Bing, Swisscows, Yep, Wikipedia'
FLASK_APP_TEMPLATES = 'c:/AggregatorSearch/templates' # On Hosting Server when installing it, change the folder to: '/home3/username/projectname/templates'
UPLOAD_FOLDER = 'static/userdata'
SQLALCHEMY_DATABASE_URL_ROOT = 'sqlite:///database.db'
SECRET_KEY_CODE = 'secret_key_comes_here'
DEFAULT_PORT='http://127.0.0.1:5000/' # On Hosting Server when installing it, change the folder to: ''
SECURITY_REGISTERABLE_BOOLEAN = True
SECURITY_REGISTER_URL_ROOT = '/register'
LOGIN_MANAGER_LOGIN_VIEW = 'login'
# FETCH_RESULT_NUMBER=10
# RESULTS_PER_PAGE=5

#-----------------------------------------------------------------------------
# Color Design
#-----------------------------------------------------------------------------
highlighted_content_color='#000066'
warning_content_color='#800000'

#-----------------------------------------------------------------------------
# App init
#-----------------------------------------------------------------------------
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#-----------------------------------------------------------------------------
# Derived variables
#-----------------------------------------------------------------------------
TEMPLATES_FOLDER = FLASK_APP_TEMPLATES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL_ROOT
app.config['SECRET_KEY'] = SECRET_KEY_CODE
app.config['SECURITY_REGISTERABLE'] = SECURITY_REGISTERABLE_BOOLEAN
app.config['SECURITY_REGISTER_URL'] = SECURITY_REGISTER_URL_ROOT

#-----------------------------------------------------------------------------
# General Forms
#-----------------------------------------------------------------------------
class SearchForm(FlaskForm):
    contentsearch = StringField(validators=[DataRequired(), Length(min=1, max=512)], render_kw={"placeholder": "Content Search!"})
    submit = SubmitField('Search!')
    
#-----------------------------------------------------------------------------
# General page handler functions
#-----------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    webpage_title='General Error on '+WEBSITE_NAME
    msg = "System message: Ooops! We are sorry. General error on the site..."
    return render_template("404.html", website_name=WEBSITE_NAME, webpage_title=webpage_title, website_tagline=WEBSITE_TAGLINE, msg=msg, highlighted_content_color=highlighted_content_color, warning_content_color=warning_content_color), {"Refresh": "5; url="+DEFAULT_PORT}
   
#-----------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    webpage_title='Home of '+WEBSITE_NAME
    form = SearchForm()
    if form.is_submitted():
        now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        contentsearch_wikipedia=str(form.contentsearch.data).strip().replace(' ','_')
        contentsearch=str(form.contentsearch.data).strip().replace(' ','+')
        contentsearch_original=str(form.contentsearch.data).strip()
        #-----------------------------------------------------------------
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        
        l_sql='INSERT INTO searches VALUES ("'+contentsearch_original+'", "'+now+'"); '
        cur.execute(l_sql)
        con.commit()
        try:
            #-----------------------------------------------------------------
            msg = "System message: Operation successfull."
            webpage_title = 'Search Results Lists - '+contentsearch_original+' - '+WEBSITE_NAME
            #-----------------------------------------------------------------
            return render_template("layouts/results.html", website_name=WEBSITE_NAME, webpage_title=webpage_title, website_tagline=WEBSITE_TAGLINE, contentsearch=contentsearch, contentsearch_wikipedia=contentsearch_wikipedia, msg=msg, highlighted_content_color=highlighted_content_color, warning_content_color=warning_content_color)
    
        except Exception as e_all:
            webpage_title='Search Error on '+WEBSITE_NAME
            msg = "System message: Error in the operation: "+str(e_all)
            return render_template("404.html", website_name=WEBSITE_NAME, webpage_title=webpage_title, website_tagline=WEBSITE_TAGLINE, msg=msg, highlighted_content_color=highlighted_content_color, warning_content_color=warning_content_color)
                                
    return render_template('layouts/index.html', website_name=WEBSITE_NAME, webpage_title=webpage_title, website_tagline=WEBSITE_TAGLINE, highlighted_content_color=highlighted_content_color, warning_content_color=warning_content_color)

@app.route('/privacy_policy_and_terms_of_use', methods=['GET', 'POST'])
def privacy_policy_and_terms_of_use():
    webpage_title='Privacy policy and Terms of use - '+WEBSITE_NAME
    website_marketing_slogan='Remain anonymus while searching, we do not collect any personal data!'
    return render_template('layouts/privacy_policy_and_terms_of_use.html', website_name=WEBSITE_NAME, webpage_title=webpage_title, website_tagline=WEBSITE_TAGLINE, highlighted_content_color=highlighted_content_color, warning_content_color=warning_content_color, website_marketing_slogan=website_marketing_slogan)
#-----------------------------------------------------------------------------
# MAIN
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    
#-----------------------------------------------------------------------------
# Command line start
#-----------------------------------------------------------------------------
# On Windows System, from Anaconda (run as administrator) run the following commands:
# cd c:/projectname/
# set FLASK_ENV=development
# set FLASK_APP=app.py
# flask run
# 
#-----------------------------------------------------------------------------
# Web browser URL by default is http://127.0.0.1:5000/
#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------
# E. O. F.
#-----------------------------------------------------------------------------