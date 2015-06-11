# coding=utf8

"""
auth 	: luanhailiang
email	: hi@luanhailiang.cn
date 	: 2015-6-9
"""

import httplib  
from urllib import quote
from SendSMSConf import SendSMSConf

class Singleton(type):  
	def __init__(cls, name, bases, dict):  
		super(Singleton, cls).__init__(name, bases, dict)  
		cls.instance = None  

	def __call__(cls, *args, **kw):  
		if cls.instance is None:  
			cls.instance = super(Singleton, cls).__call__(*args, **kw)  
		return cls.instance  


class SendSMS(object):  
	__metaclass__ = Singleton  

	def __init__(self):
		self.cpId = SendSMSConf.CPID
		self.cpPwd = SendSMSConf.CPPWD
		self.server = SendSMSConf.SERVER

	def send(self, phone, msg):
		# msg = "您本次验证码为：%s【七星集团】" % msg
		msg = msg.decode("UTF-8").encode("GBK")
		msg = quote(msg)
		conn = httplib.HTTPConnection(self.server)  
		url = "/sms/mt.jsp?cpName=%s&cpPwd=%s&phones=%s&msg=%s"%(self.cpId,self.cpPwd,phone,msg)
		conn.request("GET", url)  
		r = conn.getresponse()  
		data = r.read() 
		conn.close()
		return data 



