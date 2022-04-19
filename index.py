import yiban
def main_handler(event, context):
	#支持多人打卡
	information=[
		#信息格式：账号,密码,打卡地址(默认为校本部）,微信提醒token（可省略，获取方式见介绍文档）,提醒类型（可省略)，0不提醒，1仅失败，2全部提醒
		["myaccount","mypassword"],#第一个人信息
		["myaccount","mypassword","我的地址","token",1],#第二个人信息（推荐需要微信提醒者）
		["myaccount","mypassword","我的地址"]#第三个人信息（推荐不需要微信提醒者），以此类推
		#注：仅建议这三种写法
	]

	for i in range(len(information)):
		yiban.person(*information[i])