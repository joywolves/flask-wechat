# coding=utf8

"""
	auth 	: luanhailiang
	email	: hi@luanhailiang.cn
	date 	: 2015-6-9
"""

from fenghuang import app

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')