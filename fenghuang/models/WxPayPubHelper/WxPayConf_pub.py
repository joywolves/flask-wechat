# coding=utf8


#配置账号信息
class WxPayConf_pub:
	#=======【基本信息设置】=====================================
	#微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
	APPID = 'wx8888888888888888'
	#受理商ID，身份标识
	MCHID = '18888887'
	#商户支付密钥Key。审核通过后，在微信发送的邮件中查看
	KEY = '48888888888888888888888888888886'
	#JSAPI接口中获取openid，审核后在公众平台开启开发模式后可查看
	APPSECRET = '48888888888888888888888888888887'
	
	#=======【JSAPI路径设置】===================================
	#获取access_token过程中的跳转uri，通过跳转将code传入jsapi支付页面
	JS_API_CALL_URL = 'http://fhzb.luanhailiang.cn:5000/js_api_call'
	
	#=======【证书路径设置】=====================================
	#证书路径,注意应该填写绝对路径
	SSLCERT_PATH = '/xxx/xxx/xxxx/WxPayPubHelper/cacert/apiclient_cert.pem'
	SSLKEY_PATH = '/xxx/xxx/xxxx/WxPayPubHelper/cacert/apiclient_key.pem'
	
	#=======【异步通知url设置】===================================
	#异步通知url，商户根据实际开发过程设定
	NOTIFY_URL = 'http://fhzb.luanhailiang.cn:5000/notify_url'

	#=======【curl超时设置】===================================
	#本例程通过curl使用HTTP POST方法，此处可修改其超时时间，默认为30秒
	CURL_TIMEOUT = 30
