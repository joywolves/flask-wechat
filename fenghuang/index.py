# coding=utf8

"""
	auth 	: luanhailiang
	email	: hi@luanhailiang.cn
	date 	: 2015-6-9
"""

from fenghuang import app

from flask import render_template

@app.route('/')
def index():
	return render_template('index.html')