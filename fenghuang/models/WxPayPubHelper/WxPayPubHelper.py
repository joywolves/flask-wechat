# coding=utf8

"""
update from php demo 

auth 	: luanhailiang
email	: hi@luanhailiang.cn
date 	: 2015-6-9
"""

"""
 * 微信支付帮助库
 * ====================================================
 * 接口分三种类型：
 * 【请求型接口】--Wxpay_client_
 * 		统一支付接口类--UnifiedOrder
 * 		订单查询接口--OrderQuery
 * 		退款申请接口--Refund
 * 		退款查询接口--RefundQuery
 * 		对账单接口--DownloadBill
 * 		短链接转换接口--ShortUrl
 * 【响应型接口】--Wxpay_server_
 * 		通用通知接口--Notify
 * 		Native支付——请求商家获取商品信息接口--NativeCall
 * 【其他】
 * 		静态链接二维码--NativeLink
 * 		JSAPI支付--JsApi
 * =====================================================
 * 【CommonUtil】常用工具：
 * 		trimString()，设置参数时需要用到的字符处理函数
 * 		createNoncestr()，产生随机字符串，不长于32位
 * 		formatBizQueryParaMap(),格式化参数，签名过程需要用到
 * 		getSign(),生成签名
 * 		arrayToXml(),array转xml
 * 		xmlToArray(),xml转 array
 * 		postXmlCurl(),以post方式提交xml到对应的接口url
 * 		postXmlSSLCurl(),使用证书，以post方式提交xml到对应的接口url
"""

import json
import urllib
import random
import pycurl
import hashlib
import cStringIO
import xmltodict

from WxPayConf_pub import WxPayConf_pub
from SDKRuntimeException import SDKRuntimeException


# 所有接口的基类
class Common_util_pub:

	def __init__(self):
		pass

	@staticmethod 
	def trimString(value):
		ret = None
		if None != value:
			ret = value
			if len(ret) == 0:
				ret = None
		return ret 

	# 	作用：产生随机字符串，不长于32位
	@staticmethod 
	def createNoncestr( length = 32 ) :
		chars = "abcdefghijklmnopqrstuvwxyz0123456789"
		str =""
		for i in range(length) :
			index = random.randint(0, len(chars)-1)
			str += chars[index:index+1] 
		return str

	# 	作用：格式化参数，签名过程需要使用
	@staticmethod 
	def formatBizQueryParaMap(paraMap, urlencode):
		buff = ""
		for k,v in sorted(paraMap.items(),key=lambda d: d[0]):
			if urlencode:
				v = urllib.urlencode(v)
			buff += k + "=" + v + "&"
			# buff += k.lower() + "=" + v + "&"
		reqPar = None
		if len(buff) > 0 :
			reqPar = buff[0:len(buff)-1]
		return reqPar

	# 	作用：生成签名
	@staticmethod 
	def getSign(Obj):
		Parameters = {}
		for k,v in Obj.items():
			Parameters[k] = v
		#签名步骤一：按字典序排序参数
		String = Common_util_pub.formatBizQueryParaMap(Parameters, False)
		# print String+"\n"
		#签名步骤二：在string后加入KEY
		String = String+"&key="+WxPayConf_pub.KEY
		# print String+"\n"
		#签名步骤三：MD5加密
		m = hashlib.md5()   
		m.update(String)
		String = m.hexdigest()
		#print "【string3】 "+String+"</br>"
		#签名步骤四：所有字符转为大写
		result_ = String.upper()
		#print "【result】 "+result_+"</br>"
		return result_
	
	# 	作用：array转xml
	@staticmethod 
	def arrayToXml(arr):
		xml = "<xml>"
		for key,val in arr.items():
			if val.isdigit():
				xml +="<"+key+">"+val+"</"+key+">" 
			else:
				xml +="<"+key+"><![CDATA["+val+"]]></"+key+">"  
		xml += "</xml>"
		return xml

	# 	作用：将xml转为array
	@staticmethod
	def xmlToArray(xml):
		#将XML转为array     
		array_data = xmltodict.parse(xml)   
		data = {}
		for k,v in array_data['xml'].items():
			data[k] = v
		return data

	# 	作用：以post方式提交xml到对应的接口url
	@staticmethod
	def postXmlCurl(xml,url,second=30):	
		print xml
		buf = cStringIO.StringIO()
		#初始化curl        
		ch = pycurl.Curl()
		ch.setopt(ch.WRITEFUNCTION, buf.write)
		#设置超时
		ch.setopt(ch.TIMEOUT, second)
		#这里设置代理，如果有的话
		#ch.setopt(ch.PROXY, '8.8.8.8')
		#ch.setopt(ch.PROXYPORT, 8080)
		ch.setopt(ch.URL, url)
		ch.setopt(ch.SSL_VERIFYPEER,False)
		ch.setopt(ch.SSL_VERIFYHOST,False)
		#设置header
		ch.setopt(ch.HEADER, False)
		#post提交方式
		ch.setopt(ch.POST, True)
		ch.setopt(ch.POSTFIELDS, xml)
		#运行curl
		ch.perform()
		data = buf.getvalue()
		buf.close()
		#返回结果
		if data:
			ch.close()
			return data
		else :
			error = ch.getinfo(ch.HTTP_CODE)
			print "curl出错，错误码:"+error+"<br>" 
			print "<a href='http://curl.haxx.se/libcurl/c/libcurl-errors.html'>错误原因查询</a></br>"
			ch.close()
			return False

	# 作用：使用证书，以post方式提交xml到对应的接口url
	@staticmethod
	def postXmlSSLCurl(xml,url,second=30):
		buf = cStringIO.StringIO()
		ch = pycurl.Curl()
		ch.setopt(ch.WRITEFUNCTION, buf.write)
		#超时时间
		ch.setopt(ch.TIMEOUT,second)
		#这里设置代理，如果有的话
		#ch.setopt(ch.PROXY, '8.8.8.8')
		#ch.setopt(ch.PROXYPORT, 8080)
		ch.setopt(ch.URL, url)
		ch.setopt(ch.SSL_VERIFYPEER,False)
		ch.setopt(ch.SSL_VERIFYHOST,False)
		#设置header
		ch.setopt(ch.HEADER,False)
		#设置证书
		#使用证书：cert 与 key 分别属于两个.pem文件
		#默认格式为PEM，可以注释
		ch.setopt(ch.SSLCERTTYPE,'PEM')
		ch.setopt(ch.SSLCERT, WxPayConf_pub.SSLCERT_PATH)
		#默认格式为PEM，可以注释
		ch.setopt(ch.SSLKEYTYPE,'PEM')
		ch.setopt(ch.SSLKEY, WxPayConf_pub.SSLKEY_PATH)
		#post提交方式
		ch.setopt(ch.POST, True)
		ch.setopt(ch.POSTFIELDS,xml)
		ch.perform()
		#返回结果
		data = buf.getvalue()
		buf.close()
		if data:
			ch.close()
			return data
		else :
			error = ch.getinfo(ch.HTTP_CODE)
			print "curl出错，错误码:"+error+"<br>" 
			print "<a href='http://curl.haxx.se/libcurl/c/libcurl-errors.html'>错误原因查询</a></br>"
			ch.close()
			return False

	# 	作用：打印数组
	@staticmethod
	def printErr(wording='',err=''):
		print '<pre>'
		print wording+"</br>"
		print vars(err)
		print '</pre>'


# 请求型接口的基类
class Wxpay_client_pub(Common_util_pub ):
	def __init__(self):
		self.parameters={}#请求参数，类型为关联数组
		# self.response=None#微信返回的响应
		# self.result=None#返回参数，类型为关联数组
		# self.url=None#接口链接
		# self.curl_timeout=None#curl超时时间
	
	# 	作用：设置请求参数
	def setParameter(self, parameter, parameterValue):
		self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)
	
	# 	作用：设置标配的请求参数，生成签名，生成接口参数xml
	def createXml(self):
		self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
		self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
		self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
		self.parameters["sign"] = self.getSign(self.parameters)#签名
		return  self.arrayToXml(self.parameters)
	
	# 	作用：post请求xml
	def postXml(self):
		xml = self.createXml()
		self.response = self.postXmlCurl(xml,self.url,self.curl_timeout)
		return self.response
	
	# 	作用：使用证书post请求xml
	def postXmlSSL(self):
		xml = self.createXml()
		self.response = self.postXmlSSLCurl(xml,self.url,self.curl_timeout)
		return self.response

	# 	作用：获取结果，默认不使用证书
	def getResult(self) :
		self.postXml()
		self.result = self.xmlToArray(self.response)
		return self.result


# 统一支付接口类
class UnifiedOrder_pub (Wxpay_client_pub) :

	def __init__(self) :
		Wxpay_client_pub.__init__(self)
		#设置接口链接
		self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT
	
	# 生成接口参数xml
	def createXml(self):
		try:
			#检测必填参数
			if self.parameters["out_trade_no"] == None :
				raise SDKRuntimeException("缺少统一支付接口必填参数out_trade_no！"+"<br>")
			elif  self.parameters["body"] == None :
				raise SDKRuntimeException("缺少统一支付接口必填参数body！"+"<br>")
			elif  self.parameters["total_fee"] == None :
				raise SDKRuntimeException("缺少统一支付接口必填参数total_fee！"+"<br>")
			elif  self.parameters["notify_url"] == None :
				raise SDKRuntimeException("缺少统一支付接口必填参数notify_url！"+"<br>")
			elif  self.parameters["trade_type"] == None :
				raise SDKRuntimeException("缺少统一支付接口必填参数trade_type！"+"<br>")
			elif  self.parameters["trade_type"] == "JSAPI" and parameters["openid"] == None :
				raise SDKRuntimeException("统一支付接口中，缺少必填参数openid！trade_type为JSAPI时，openid为必填参数！"+"<br>")
			
			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.parameters["spbill_create_ip"] = _SERVER['REMOTE_ADDR']#终端ip	    
			self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名
			return  self.arrayToXml(self.parameters)
		except SDKRuntimeException as e:
			raise e 

	# 获取prepay_id
	def getPrepayId(self):
		self.postXml()
		self.result = self.xmlToArray(self.response)
		prepay_id = self.result["prepay_id"]
		return prepay_id


 # 订单查询接口

class OrderQuery_pub (Wxpay_client_pub) :
	def __init__(self) :
		Wxpay_client_pub.__init__(self)
		#设置接口链接
		self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT		

	# 生成接口参数xml
	def createXml(self):
		try:
			#检测必填参数
			if self.parameters["out_trade_no"] == None and self.parameters["transaction_id"] == None :
				raise SDKRuntimeException("订单查询接口中，out_trade_no、transaction_id至少填一个！"+"<br>")
			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名
			return  self.arrayToXml(self.parameters)
		except SDKRuntimeException as e:
			raise e 

# 退款申请接口
class Refund_pub (Wxpay_client_pub) :
	def __init__(self) :
		Wxpay_client_pub.__init__(self)
		#设置接口链接
		self.url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT		
	
	# 生成接口参数xml
	def createXml(self):
		try:
			#检测必填参数
			if self.parameters["out_trade_no"] == None and parameters["transaction_id"] == None :
				raise SDKRuntimeException("退款申请接口中，out_trade_no、transaction_id至少填一个！"+"<br>")
			elif self.parameters["out_refund_no"] == None:
				raise SDKRuntimeException("退款申请接口中，缺少必填参数out_refund_no！"+"<br>")
			elif self.parameters["total_fee"] == None:
				raise SDKRuntimeException("退款申请接口中，缺少必填参数total_fee！"+"<br>")
			elif self.parameters["refund_fee"] == None:
				raise SDKRuntimeException("退款申请接口中，缺少必填参数refund_fee！"+"<br>")
			elif self.parameters["op_user_id"] == None:
				raise SDKRuntimeException("退款申请接口中，缺少必填参数op_user_id！"+"<br>")

			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名
			return  self.arrayToXml(self.parameters)
		except SDKRuntimeException as e:
			raise e 

	# 	作用：获取结果，使用证书通信
	def getResult(self) :	
		self.postXmlSSL()
		self.result = self.xmlToArray(self.response)
		return self.result


# 退款查询接口
class RefundQuery_pub (Wxpay_client_pub) :
	
	def __init__(self) :
		Wxpay_client_pub.__init__(self)
		#设置接口链接
		self.url = "https://api.mch.weixin.qq.com/pay/refundquery"
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT		

	# 生成接口参数xml
	def createXml(self):
		try :
			if self.parameters["out_refund_no"] == None and elf.parameters["out_trade_no"] == None and elf.parameters["transaction_id"] == None and elf.parameters["refund_id "] == None:
				raise SDKRuntimeException("退款查询接口中，out_refund_no、out_trade_no、transaction_id、refund_id四个参数必填一个！"+"<br>")
			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名
			return  self.arrayToXml(self.parameters)
		except SDKRuntimeException as e:
			raise e 

	# 	作用：获取结果，使用证书通信
	def getResult(self) :
		self.postXmlSSL()
		self.result = self.xmlToArray(self.response)
		return self.result


# 对账单接口
class DownloadBill_pub (Wxpay_client_pub) :

	def __init__(self) :
		Wxpay_client_pub.__init__(self)
		#设置接口链接
		self.url = "https://api.mch.weixin.qq.com/pay/downloadbill"
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT		

	# 生成接口参数xml
	def createXml(self):		
		try :
			if self.parameters["bill_date"] == None :
				raise SDKRuntimeException("对账单接口中，缺少必填参数bill_date！"+"<br>")
			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.parameters["nonce_str"] = "luanhailiang"#self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名
			return  self.arrayToXml(self.parameters)
		except SDKRuntimeException as e:
			raise e 
	
	# 	作用：获取结果，默认不使用证书
	def getResult(self) :
		self.postXml()
		self.result = self.xmlToArray(self.response)
		return self.result
	

# 短链接转换接口
class ShortUrl_pub (Wxpay_client_pub) :

	def __init__(self) :
		Wxpay_client_pub.__init__(self)
		#设置接口链接
		self.url = "https://api.mch.weixin.qq.com/tools/shorturl"
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT		
	
	# 生成接口参数xml
	def createXml(self):
		try :
			if self.parameters["long_url"] == None :
				raise SDKRuntimeException("短链接转换接口中，缺少必填参数long_url！"+"<br>")
			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名
			return  self.arrayToXml(self.parameters)
		except SDKRuntimeException as e:
			raise e 
	
	# 获取prepay_id
	def getShortUrl(self):
		self.postXml()
		prepay_id = self.result["short_url"]
		return prepay_id
	

# 响应型接口基类
class Wxpay_server_pub (Common_util_pub)  :

	def __init__(self) :
		self.data=None#接收到的数据，类型为关联数组
		self.returnParameters={}#返回参数，类型为关联数组
	
	# 将微信的请求xml转换成关联数组，以方便数据处理
	def saveData(self, xml):
		self.data = self.xmlToArray(xml)
	
	def checkSign(self):
		tmpData = self.data
		del tmpData['sign']
		sign = self.getSign(tmpData)#本地签名
		if self.data['sign'] == sign :
			return True
		return False

	# 获取微信的请求数据
	def getData(self):
		return self.data
	
	# 设置返回微信的xml数据
	def setReturnParameter(self, parameter, parameterValue):
		self.returnParameters[self.trimString(parameter)] = self.trimString(parameterValue)
	
	# 生成接口参数xml
	def createXml(self):
		return self.arrayToXml(self.returnParameters)
	
	# 将xml数据返回微信
	def returnXml(self):
		returnXml = self.createXml()
		return returnXml


#  通用通知接口
class Notify_pub (Wxpay_server_pub):
	pass


#请求商家获取商品信息接口
class NativeCall_pub (Wxpay_server_pub) :
	#生成接口参数xml
	def createXml(self):
		if self.returnParameters["return_code"] == "SUCCESS" :
			self.returnParameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.returnParameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			self.returnParameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.returnParameters["sign"] = self.getSign(self.returnParameters)#签名
		return self.arrayToXml(self.returnParameters)
	
	# 获取product_id
	def getProductId(self):
		product_id = self.data["product_id"]
		return product_id


# 静态链接二维码
class NativeLink_pub  (Common_util_pub) :

	def __init__(self) :
		self.parameters={}#静态链接参数
		self.url#静态链接
	
	# * 设置参数
	def setParameter(self, parameter, parameterValue) :
		self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)
		
	# * 生成Native支付链接二维码
	def createLink(self):
		try :
			if self.parameters["product_id"] == None: 
				raise SDKRuntimeException("缺少Native支付二维码链接必填参数product_id！"+"<br>")
			self.parameters["appid"] = WxPayConf_pub.APPID#公众账号ID
			self.parameters["mch_id"] = WxPayConf_pub.MCHID#商户号
			time_stamp = time()
			self.parameters["time_stamp"] = "time_stamp"#时间戳
			self.parameters["nonce_str"] = self.createNoncestr()#随机字符串
			self.parameters["sign"] = self.getSign(self.parameters)#签名    		
			bizString = self.formatBizQueryParaMap(self.parameters, False)
			self.url = "weixin://wxpay/bizpayurl?"+bizString
		except SDKRuntimeException as e:
			raise e 
	
	# * 返回链接
	def getUrl(self): 
		self.createLink()
		return self.url


#* JSAPI支付——H5网页端调起支付接口
class JsApi_pub (Common_util_pub) :

	def __init__(self) :
		self.code=None#code码，用以获取openid
		self.token=None
		self.userinfo=None
		self.parameters=None#jsapi参数，格式为json
		self.prepay_id=None#使用统一支付接口得到的预支付id
		#设置curl超时时间
		self.curl_timeout = WxPayConf_pub.CURL_TIMEOUT

	# * 作用：生成可以获得code的url
	def createOauthUrlForCode(self, redirectUrl, userInfo=False):
		urlObj = {}
		urlObj["appid"] = WxPayConf_pub.APPID
		urlObj["redirect_uri"] = redirectUrl
		urlObj["response_type"] = "code"
		if userInfo :
			urlObj["scope"] = "snsapi_userinfo"
		else:
			urlObj["scope"] = "snsapi_base"
		urlObj["state"] = "STATE"+"#wechat_redirect"
		bizString = self.formatBizQueryParaMap(urlObj, False)
		return "https://open.weixin.qq.com/connect/oauth2/authorize?"+bizString

	#* 	作用：生成可以获得openid的url	
	def createOauthUrlForAccessToken(self):
		urlObj = {}
		urlObj["appid"] = WxPayConf_pub.APPID
		urlObj["secret"] = WxPayConf_pub.APPSECRET
		urlObj["code"] = self.code
		urlObj["grant_type"] = "authorization_code"
		bizString = self.formatBizQueryParaMap(urlObj, False)
		return "https://api.weixin.qq.com/sns/oauth2/access_token?"+bizString
	
	#* 	作用：生成可以获得openid的url	
	def createOauthUrlForUserInfo(self):
		urlObj = {}
		urlObj["access_token"] = self.token['access_token']
		urlObj["openid"] = self.token['openid']
		urlObj["lang"] = "zh_CN"
		bizString = self.formatBizQueryParaMap(urlObj, False)
		return "https://api.weixin.qq.com/sns/userinfo?"+bizString

	def getDataByUrl(self,url):
		#初始化curl
		buf = cStringIO.StringIO()
		ch = pycurl.Curl()
		ch.setopt(ch.WRITEFUNCTION, buf.write)
		#设置超时
		ch.setopt(ch.TIMEOUT, self.curl_timeout)
		ch.setopt(ch.URL, url)
		ch.setopt(ch.SSL_VERIFYPEER,False)
		ch.setopt(ch.SSL_VERIFYHOST,False)
		ch.setopt(ch.HEADER, False)
		#运行curl，结果以jason形式返回
		ch.perform()
		res = buf.getvalue()
		buf.close()
		ch.close()
		#取出openid
		return json.loads(res)


	# * 	作用：通过curl向微信提交code，以获取openid
	def getAccessTokenByCode(self):
		url = self.createOauthUrlForAccessToken()
		data = self.getDataByUrl(url)
		self.token = data
		return data

	def getUserInfoByAccessToken(self):	
		url = self.createOauthUrlForUserInfo()
		data = self.getDataByUrl(url)
		self.userinfo = data
		return data

	def getOpenId(self):
		if not self.token:
			self.getAccessTokenByCode()
		return self.token['openid']

	def getToken(self):
		if not self.token:
			self.getAccessTokenByCode()
		return self.token

	def getUserInfo(self):
		if not self.token:
			self.getAccessTokenByCode()
		if not self.userinfo:
			self.getUserInfoByAccessToken()
		return self.userinfo

	# * 	作用：设置code
	def setCode(self, code_):
		self.code = code_

	# 	作用：设置prepay_id
	def setPrepayId(self, prepayId):
		self.prepay_id = prepayId

	# * 作用：设置jsapi的参数
	def getParameters(self):
		jsApiObj = {}
		jsApiObj["appId"] = WxPayConf_pub.APPID
		timeStamp = time()
		jsApiObj["timeStamp"] = "timeStamp"
		jsApiObj["nonceStr"] = self.createNoncestr()
		jsApiObj["package"] = "prepay_id="+self.prepay_id
		jsApiObj["signType"] = "MD5"
		jsApiObj["paySign"] = self.getSign(jsApiObj)
		self.parameters = json.dumps(jsApiObj)
		return self.parameters

