import yiban
import requests
def main_handler(event, context):
	res=yiban.daka(flag='1',accountid='1',password='1',address='广东省广州市天河区迎福路靠近广东金融学院(广州校区)') 
	#分别填写昵称、账号、密码（易班）、打卡地址等信息
	print(res)
	notifybyXtuis(sendKey='',notifyType=1,code=res["code"],desp=res['detail'])
	#具体参数信息，请看下面方法 提供两种平台可自行选择，推荐使用notifybyXtuis，公众号提醒时更加清晰。

def notifybySeverJ(sendKey='',notifyType=0,code=0,desp=''):
	"""  
	sendKey：Sever酱的sendkey，具体在 Sever酱网站获取 https://sct.ftqq.com/sendkey
	notifyType：提醒类型，0不提醒，1仅失败，2全部提醒
	code：打卡状态码，0为成功，其他为失败
	"""
	if len(sendKey)==0 or notifyType==0:
		print("未输入key或无需提醒")
		return 1

	if code==0 and notifyType==2:
		requests.get(url="https://sctapi.ftqq.com/"+sendKey+".send?title="+'Clock%20success')
	elif code!=0:
		requests.get(url="https://sctapi.ftqq.com/"+sendKey+".send?title="+'Clock%20failed')
	return 0
	       
def notifybyXtuis(sendKey='',notifyType=0,code=0,desp=''):
	"""  
	sendKey：虾推啥的token，具体在虾推啥获取 http://www.xtuis.cn/
	notifyType：提醒类型，0不提醒，1仅失败，2全部提醒
	code：打卡状态码，0为成功，其他为失败
	"""
	if len(sendKey)==0 or notifyType==0:
		print("未输入key或无需提醒")
		return 1

	if code==0 and notifyType==2:
		mydata={
			'text':'打卡成功' ,
			'desp':desp
		    }
		requests.post('http://wx.xtuis.cn/'+sendKey+'.send', data=mydata) 
		
	elif code!=0:
		mydata={
			'text':'打卡失败！',
			'desp':desp
		    }
		requests.post('http://wx.xtuis.cn/'+sendKey+'.send', data=mydata) 
	return 0
