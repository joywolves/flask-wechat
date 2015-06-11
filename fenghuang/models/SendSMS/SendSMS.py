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

	def send_change_pwd(phone):
		msg = "您的交易密码已成功设置，请注意保管！【凤金所】"
		return self.send(phone,msg)

	def send_check_card(phone,name):
		msg = "[%s]会员您好！您的银行卡审核已经通过。凤金所欢迎您的访问【凤金所】" % (name)
		return self.send(phone,msg)
	
	def send_check_require(phone,num,name,bank,account):
		msg = "请您向以下帐号打款[%s]元钱，以完成银行卡的认证，收款方：[%s]，开户行：[%s]，帐号：[%s]【凤金所】" % (num,name,bank,account)
	
	def send_sign_notify(phone,name):
		msg = "您的注册已成功，恭喜您成为凤金所会员，用户名是[*]，继续认证流程可获的凤凰币哦！【凤金所】" % (name)

	def send_check_code(phone,code):
		msg = "您好，您的注册验证码为：[%s]，请不要把验证码泄露给其他人。如非本人操作，可不用理会！【凤金所】" % (code)
	
