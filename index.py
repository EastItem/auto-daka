import yiban
def main_handler(event, context):
	#支持多人打卡
	information=[
		#格式：账号,密码,deviceModel,systemVersion,uuid,UA,【微信提醒token（可省略，获取方式见介绍文档）,提醒类型（可省略)，0不提醒，1仅失败，2全部提醒】
		#支持多人打卡,打卡地址为昨天的地址
	]

	
	for i in range(len(information)):
		yiban.person(*information[i])
