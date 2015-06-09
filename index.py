# coding=utf8

"""
auth 	: luanhailiang
email	: hi@luanhailiang.cn
date 	: 2015-6-9
"""


from WxPayPubHelper.WxPayPubHelper import *
from flask import Flask, render_template, request, abort, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/js_api_call')
def js_api_call():
	#使用jsapi接口
	jsApi = JsApi_pub()
	#=========步骤1：网页授权获取用户openid============
	#通过code获得openid
	if not request.args.get('code') :
		#触发微信返回code码
		url = jsApi.createOauthUrlForCode(WxPayConf_pub.JS_API_CALL_URL)
		return redirect(url) 
		
	
	#获取code码，以获取openid
	code = request.args.get('code')
	jsApi.setCode(code)
	openid = jsApi.getOpenId()


	#=========步骤2：使用统一支付接口，获取prepay_id============
	#使用统一支付接口
	unifiedOrder = UnifiedOrder_pub()

	#设置统一支付接口参数
	#设置必填参数
	#appid已填,商户无需重复填写
	#mch_id已填,商户无需重复填写
	#noncestr已填,商户无需重复填写
	#spbill_create_ip已填,商户无需重复填写
	#sign已填,商户无需重复填写
	unifiedOrder.setParameter("openid","openid")#商品描述
	unifiedOrder.setParameter("body","贡献一分钱")#商品描述
	#自定义订单号，此处仅作举例
	timeStamp = time()
	out_trade_no = WxPayConf_pub.APPID+"timeStamp"
	unifiedOrder.setParameter("out_trade_no","out_trade_no")#商户订单号 
	unifiedOrder.setParameter("total_fee","1")#总金额
	unifiedOrder.setParameter("notify_url",WxPayConf_pub.NOTIFY_URL)#通知地址 
	unifiedOrder.setParameter("trade_type","JSAPI")#交易类型
	#非必填参数，商户可根据实际情况选填
	#unifiedOrder.setParameter("sub_mch_id","XXXX")#子商户号  
	#unifiedOrder.setParameter("device_info","XXXX")#设备号 
	#unifiedOrder.setParameter("attach","XXXX")#附加数据 
	#unifiedOrder.setParameter("time_start","XXXX")#交易起始时间
	#unifiedOrder.setParameter("time_expire","XXXX")#交易结束时间 
	#unifiedOrder.setParameter("goods_tag","XXXX")#商品标记 
	#unifiedOrder.setParameter("openid","XXXX")#用户标识
	#unifiedOrder.setParameter("product_id","XXXX")#商品ID

	prepay_id = unifiedOrder.getPrepayId()
	#=========步骤3：使用jsapi调起支付============
	jsApi.setPrepayId(prepay_id)

	jsApiParameters = jsApi.getParameters()
	#print jsApiParameters

	return render_template('js_api_call.html',jsApiParameters=jsApiParameters)


@app.route('/order_query')
def order_query():
	#退款的订单号
	order_data = ""
	if not request.form.get("out_trade_no"):
		out_trade_no = " "
		return render_template('order_query.html',out_trade_no=out_trade_no,order_data=order_data)
	
	out_trade_no = request.form.get("out_trade_no")

	#使用订单查询接口
	orderQuery = OrderQuery_pub()
	#设置必填参数
	#appid已填,商户无需重复填写
	#mch_id已填,商户无需重复填写
	#noncestr已填,商户无需重复填写
	#sign已填,商户无需重复填写
	orderQuery.setParameter("out_trade_no",out_trade_no)#商户订单号 
	#非必填参数，商户可根据实际情况选填
	#orderQuery.setParameter("sub_mch_id","XXXX")#子商户号  
	#orderQuery.setParameter("transaction_id","XXXX")#微信订单号

	#获取订单查询结果
	orderQueryResult = orderQuery.getResult()

	#商户根据实际情况设置相应的处理流程,此处仅作举例
	if orderQueryResult["return_code"] == "FAIL" :
		order_data += "通信出错："+orderQueryResult['return_msg']+"<br>"
	elif orderQueryResult["result_code"] == "FAIL":
		order_data += "错误代码："+orderQueryResult['err_code']+"<br>"
		order_data += "错误代码描述："+orderQueryResult['err_code_des']+"<br>"
	else:
		order_data += "交易状态："+orderQueryResult['trade_state']+"<br>"
		order_data += "设备号："+orderQueryResult['device_info']+"<br>"
		order_data += "用户标识："+orderQueryResult['openid']+"<br>"
		order_data += "是否关注公众账号："+orderQueryResult['is_subscribe']+"<br>"
		order_data += "交易类型："+orderQueryResult['trade_type']+"<br>"
		order_data += "付款银行："+orderQueryResult['bank_type']+"<br>"
		order_data += "总金额："+orderQueryResult['total_fee']+"<br>"
		order_data += "现金券金额："+orderQueryResult['coupon_fee']+"<br>"
		order_data += "货币种类："+orderQueryResult['fee_type']+"<br>"
		order_data += "微信支付订单号："+orderQueryResult['transaction_id']+"<br>"
		order_data += "商户订单号："+orderQueryResult['out_trade_no']+"<br>"
		order_data += "商家数据包："+orderQueryResult['attach']+"<br>"
		order_data += "支付完成时间："+orderQueryResult['time_end']+"<br>"
	return render_template('order_query.html',out_trade_no=out_trade_no,order_data=order_data)


@app.route('/notify_url')
def notify_url():
	#使用通用通知接口
	notify = Notify_pub()

	#存储微信的回调
	xml = request.data	
	notify.saveData(xml)
	
	#验证签名，并回应微信。
	#对后台通知交互时，如果微信收到商户的应答不是成功或超时，微信认为通知失败，
	#微信会通过一定的策略（如30分钟共8次）定期重新发起通知，
	#尽可能提高通知的成功率，但微信不保证通知最终能成功。
	if notify.checkSign() == FALSE:
		notify.setReturnParameter("return_code","FAIL")#返回状态码
		notify.setReturnParameter("return_msg","签名失败")#返回信息
	else:
		notify.setReturnParameter("return_code","SUCCESS")#设置返回码

	
	
	
	#==商户根据实际情况设置相应的处理流程，此处仅作举例=======
	
	#以log文件形式记录回调信息

	app.logger.info("【接收到的notify通知】:\n"+xml+"\n")
	if notify.checkSign() == TRUE:
		if notify.data["return_code"] == "FAIL":
			#此处应该更新一下订单状态，商户自行增删操作
			app.logger.info("【通信出错】:\n"+xml+"\n")
		
		elif notify.data["result_code"] == "FAIL":
			#此处应该更新一下订单状态，商户自行增删操作
			app.logger.info("【业务出错】:\n"+xml+"\n")
		else:
			#此处应该更新一下订单状态，商户自行增删操作
			app.logger.info("【支付成功】:\n"+xml+"\n")
		
		#商户自行增加处理流程,
		#例如：更新订单状态
		#例如：数据库操作
		#例如：推送支付完成信息
		

	returnXml = notify.returnXml()
	return returnXml

@app.route('/download_bill')
def download_bill():
	#对账单日期
	if not request.form.get("bill_date"):
		bill_date = "20140814"
		return render_template('download_bill.html',bill_date=bill_date,bill_list="")
	
	bill_date = request.form.get("bill_date")

	#使用对账单接口
	downloadBill = DownloadBill_pub()
	#设置对账单接口参数
	#设置必填参数
	#appid已填,商户无需重复填写
	#mch_id已填,商户无需重复填写
	#noncestr已填,商户无需重复填写
	#sign已填,商户无需重复填写
	downloadBill.setParameter("bill_date",bill_date)#对账单日期 
	downloadBill.setParameter("bill_type","ALL")#账单类型 
	#非必填参数，商户可根据实际情况选填
	#downloadBill.setParameter("device_info","XXXX")#设备号  

	#对账单接口结果
	downloadBillResult = downloadBill.getResult()

	bill_list = downloadBillResult['return_code']

	if downloadBillResult['return_code'] == "FAIL":
		bill_list += "通信出错："+downloadBillResult['return_msg']
	else:
		bill_list += '<pre>'
		bill_list += "【对账单详情】"+"</br>"
		bill_list += downloadBill.response
		bill_list += '</pre>'
	return render_template('download_bill.html',bill_date=bill_date,bill_list=bill_list)



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
