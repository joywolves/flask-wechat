"""
	auth 	: luanhailiang
	email	: hi@luanhailiang.cn
	date 	: 2015-6-9
"""

from fenghuang import app

import logging

setting = {
	"log.debug":logging.DEBUG,
	"log.info":logging.INFO,
	"log.warning":logging.WARNING,
	"log.error":logging.ERROR,
}

for k,v in setting.items():
	file_handler = logging.FileHandler(k);
	file_handler.setLevel(v)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s:\n %(message)s \n'
		'[in %(pathname)s:%(lineno)d]\n\n'
	))
	app.logger.addHandler(file_handler)

