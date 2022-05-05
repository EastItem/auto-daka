import yiban
def main_handler(event, context):
	#支持多人打卡
	information=[
		#格式：账号,密码,打卡地址(输入具体打卡地址或输入自动，自动则默认根据昨天的地址打卡。）,【微信提醒token（可省略，获取方式见介绍文档）,提醒类型（可省略)，0不提醒，1仅失败，2全部提醒】
		#["账号","密码",'自动'] #不需要提醒者，建议这样写
		#["账号","密码",'自动','提醒token'，1] 需要失败提醒建议这样写（推荐！）
		#支持多人打卡
	]

	
	for i in range(len(information)):
		yiban.person(*information[i])
