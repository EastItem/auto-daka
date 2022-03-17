import yiban
def main_handler(event, context):
	res=yiban.daka(flag='1',accountid='1',password='1',address='广东省广州市天河区迎福路靠近广东金融学院(广州校区)') 
	#分别填写昵称、账号、密码（易班）、打卡地址等信息
	print(res)
	