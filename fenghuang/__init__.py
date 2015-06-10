from flask import Flask
app = Flask(__name__)


import fenghuang.index
import fenghuang.wechat_api

import fenghuang.logger_setting