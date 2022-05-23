import base64
import time
from urllib import parse
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

class person:
    def __init__(self, accountid, password,deviceModel,systemVersion,uuid,UA,token="", notifyType=1):
        self.accountid = accountid
        self.password = password
        self.token = token
        self.notifyType = notifyType
        self.deviceinfo={"deviceModel":deviceModel,"systemVersion":systemVersion,"uuid":uuid}
        self.UA = UA
        self.reoauth = False #是否需要重新授权
        self.log = '' #保存日志
        self.session = requests.Session()
        # 打卡
        self.res = self.daka()
        print(self.res)
        # 推送
        res2 = self.notifybyXtuis()
        print(res2)

    # 打卡主方法
    def daka(self):
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.log = '开始\n '

        self.log = self.log + '登录中\n'

        self.login()  # 登录

        if self.loginToken != None:
            output = self.post()
            self.log = self.log + date + output['msg'] + '\n'
            self.log = self.log + '结束\n\n'
            output['detail'] = self.log
            return output
        else:
            self.log = self.log + '登录失败\n结束\n'
            resp = {'code': 515, 'msg': '登录失败'}
            resp['detail'] = self.log
            return resp

    # 登录并提交打卡方法
    def post(self):
        AppVersion='5.0.9'
        for i in range(3):  # 尝试3此打卡
            time.sleep(0.5)
            date = time.strftime("%Y-%m-%d", time.localtime())
            

            # 第一次重定向
            # 从 http://f.yiban.cn/iapp378946 到 http://f.yiban.cn/iapp/index?act=iapp378946
            header1 = {
                'Host': 'f.yiban.cn',
                'Authorization': 'Bearer ' + self.loginToken,
                'AppVersion': AppVersion,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'loginToken': self.loginToken,
                'User-Agent': self.UA,
                'Connection': 'keep-alive'
            }
            url_1 = 'http://f.yiban.cn/iapp378946'
            try:
                a = self.session.get(url=url_1, headers=header1, allow_redirects=False)
                if "Location" not in a.headers:
                    self.log = self.log + '易班服务器异常\n'
                    yb_result = {'code': 404, 'msg': '易班服务器异常'}
                    return yb_result
            except Exception:
                self.log = self.log + '第一次重定向出错\n'
                continue

            # 第二次重定向
            # 从 http://f.yiban.cn/iapp/index?act=iapp378946 到 ygj判断授权界面
            url_2 = a.headers['Location']
            header2 = {
                'Host': 'f.yiban.cn',
                'AppVersion': AppVersion,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'loginToken': self.loginToken,
                'User-Agent': self.UA,
                'Connection': 'keep-alive'
            }
            try:
                b = self.session.get(url=url_2, headers=header2, allow_redirects=False)
                if "Location" not in b.headers:
                    self.log = self.log + 'loginToken错误\n'
                    yb_result = {'code': 555, 'msg': 'loginToken错误，请修改'}
                    return yb_result
            except Exception:
                self.log = self.log + '第二次重定向出错\n'
                continue

            # 跳转到易广金 得到cookie

            url_3 = b.headers['Location'] #ygj.gduf.edu.cn/index.aspx?verify_request-.......


            header3 = {
                'Host': 'ygj.gduf.edu.cn',
                'AppVersion': AppVersion,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'loginToken': self.loginToken,
                'User-Agent': self.UA,
                'Connection': 'keep-alive'
            }
            try:
                c = self.session.get(url=url_3, headers=header3, allow_redirects=False)
            except Exception:
                self.log = self.log + '第三次重定向出错\n'
                continue
                
            # 判断是否授权
            ygjhome=c.headers['Location']
            judge = self.oauth(ygjhome)
            if judge == 1:
                self.reoauth = True
                continue
            elif judge == 2:
                return {'code': 111, 'msg': "授权失败！"}
            
            # 拿到StudentID
            studentID = ygjhome.split('=')[1]
            
            #进入易广金首页
            self.session.get(url=ygjhome,headers=header3)
            
            #GetNotice
            header_api={
                'Host': 'ygj.gduf.edu.cn',
                'Accept': '*/*',
                "X-Requested-With": "XMLHttpRequest",
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://ygj.gduf.edu.cn",
                'User-Agent': self.UA,
                'Connection': 'keep-alive',
                "Referer":ygjhome
            }
            notice=self.session.post(url='https://ygj.gduf.edu.cn/Handler/device.ashx?flag=getNotice',headers=header_api,data={'studentID':studentID}).json()
            print(notice)
            
           

            # 检查绑定设备
            url_bind = "https://ygj.gduf.edu.cn/Handler/device.ashx?flag=checkBindDevice"
            
            #注意更换！！！！！！
            devicedata={
                "deviceData":'''{"appVersion":"5.0.9","deviceModel":'''+self.deviceinfo['deviceModel']+''',"systemVersion":'''+self.deviceinfo['systemVersion']+''',"uuid"'''+self.deviceinfo['uuid']+'''}''',
                "autoBind":"false"
            }
            print(self.session.post(url=url_bind, headers=header_api,data=devicedata).json())
            
            #进入健康打卡页面
            header_html={
                'Host': 'ygj.gduf.edu.cn',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': self.UA,
                'Connection': 'keep-alive',
                "Referer":ygjhome
            }
            url_health='https://ygj.gduf.edu.cn/ygj/health/student-index.aspx'
            self.session.get(url=url_health,headers=header_html)

            #GetStudentInfo
            header_api['Referer']=url_health
            self.session.post(url='https://ygj.gduf.edu.cn/Handler/health.ashx?flag=getStudentInfo',headers=header_api,data={"studentID":studentID})
            
             # 获取历史打卡地址
            #if self.address=='自动':
                # 失败
            if self.getHistoryData(studentID)==1:
                return {'code': 555, 'msg': "获取地址失败！"}
            
            #进入今日打卡界面
            url_today="https://ygj.gduf.edu.cn/ygj/health/student-add.aspx"
            header_html['Referer']=url_health
            self.session.get(url=url_today,headers=header_html)
            
            
            
            # 检查打卡记录 
            url_check='https://ygj.gduf.edu.cn/Handler/health.ashx?flag=getHealth'
            check_header={
             'Host': 'ygj.gduf.edu.cn' ,
             'Accept': '*/*' ,
             'X-Requested-With': 'XMLHttpRequest' ,
             'Accept-Language': 'zh-CN,zh-Hans;q=0.9' ,
             'Accept-Encoding': 'gzip, deflate, br' ,
             'Content-Type': 'application/x-www-form-urlencoded' ,
             'Origin': 'https://ygj.gduf.edu.cn' ,
             'User-Agent': self.UA,
             'Connection': 'keep-alive' ,
             "Referer":url_today
             }
            check_data={
                'studentID':studentID,
                'date':date
             }
            self.session.post(url=url_check,headers=check_header,data=check_data).json()
            



            # 判断今日是否已打卡
            if True:
                # 打卡
                url_save = "https://ygj.gduf.edu.cn/Handler/health.ashx?flag=save"
                save_headers = {
                    'Host': 'ygj.gduf.edu.cn',
                    'Accept': '*/*',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://ygj.gduf.edu.cn',
                    'User-Agent': self.UA,
                    'Connection': 'keep-alive',
                    "Referer":"https://ygj.gduf.edu.cn/ygj/health/student-add.aspx"
                }
                data_yb_save = {
                    "studentID": studentID,
                    "date": date,
                    "health": "体温37.3℃以下（正常）",
                    "address": self.addressinfo['address'],
                    "isTouch": "否",
                    "isPatient": "不是",
                    'latitude':self.addressinfo['latitude'],
                    'longitude':self.addressinfo['longitude'],
                    "autoAddress":'1'}
                try:
                    yb_result = self.session.post(url=url_save, headers=save_headers, data=data_yb_save).json()
                    if self.reoauth == True:
                        yb_result["code"] = 999
                    return yb_result
                except Exception:
                    self.log = self.log + '提交失败！\n'
                    yb_result = {'code': 411, 'msg': "提交失败"}
                    return yb_result
            # else:
            # yb_result = {'code': 0, 'msg': "今日已打卡"}
            # return yb_result
        return {'code': 404, 'msg': "打卡失败了"}

    # 登录接口方法
    def login(self):
        for i in range(3):
            try:
                LOGINURL = f'https://mobile.yiban.cn/api/v4/passport/login?mobile={self.accountid}&password={self.doCrypto()}&ct=2&identify=1'
                reqHeaders = {"Origin": "https://c.uyiban.com",
                              "User-Agent": "Yiban-Pro",
                              "AppVersion": "5.0"}
                loginRequest = self.session.post(LOGINURL, headers=reqHeaders).json()
                # 登录成功后获取
                if loginRequest is not None and str(loginRequest["response"]) == "100":
                    loginToken = loginRequest["data"]["access_token"]
                    name = loginRequest['data']['user']['name']
                    # print(name,'登录成功')
                    self.log = self.log + name + '登录成功\n'
                    self.loginToken = loginToken
                    return 0
                else:
                    # print('密码错误')
                    self.log = self.log + '密码错误\n'
            except Exception as e:
                print('出现异常'+repr(e))
                self.log = self.log + '登陆异常正在重试\n'
                time.sleep(0.5)

        # print('登录异常')
        self.log = self.log + '登录异常\n'
        self.loginToken = None
        return 1

    # 登录加密方法
    def doCrypto(self):
        """
            v4接口
            密码加密
            Rsa,base64
            """
        PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
            Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
            XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
            KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
            A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
            AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
            d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
            7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
            mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
            AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
            uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
            ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
            -----END PUBLIC KEY-----
            '''
        encrypt = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
        Sencrypt = base64.b64encode(encrypt.encrypt(bytes(self.password, encoding="utf8")))
        return parse.quote(Sencrypt.decode("utf-8"))

    # 判断授权并进行授权的方法
    def oauth(self, originUrl):
        "返回值为 0不需要授权 1授权成功 2授权失败"

        # 对重定向地址进行判断，如果地址为授权地址就需要授权，否则不需要
        oauthUrl = "https://oauth.yiban.cn/code/html?client_id=0b77c3ac53bd5c65&redirect_uri=http://f.yiban.cn/iapp378946"
        if originUrl == oauthUrl:
            print("授权失效")
            self.log += "授权失效\n"
            # 需要授权
            header1 = {
                "Host": "oauth.yiban.cn",
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "loginToken": self.loginToken,
                "User-Agent": self.UA,
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Accept-Encoding": "gzip, deflate, br"
            }
            self.session.get(url=oauthUrl, headers=header1)

            # 进行授权
            oauthUrl2 = 'https://oauth.yiban.cn/code/usersure'
            data1 = {
                'client_id': "0b77c3ac53bd5c65",
                'redirect_uri': "http://f.yiban.cn/iapp378946",
                'state': "",
                'display': "html",
                'scope': '1,2,3,4,'
            }
            headers2 = {
                "Host": "oauth.yiban.cn",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://oauth.yiban.cn",
                "User-Agent": self.UA,
                "Connection": "keep-alive",
                "Referer": "https://oauth.yiban.cn/code/html?client_id=0b77c3ac53bd5c65&redirect_uri=http://f.yiban.cn/iapp378946",
            }
            res = self.session.post(oauthUrl2, data=data1, headers=headers2).json()
            if res["code"] == "s200":
                print("重新授权成功")
                self.log += "重新授权成功\n"
                return 1
            else:
                return 2
        else:
            # 不需要授权
            self.log += "无需授权\n"
            return 0

    # 获取历史打卡信息
    def getHistoryData(self, studentID):
        headers = {
            "Host": "ygj.gduf.edu.cn",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://ygj.gduf.edu.cn",
            "User-Agent": self.UA,
            "Connection": "keep-alive",
        }
        data = {
            "studentID": studentID
        }
        res = self.session.post(url="https://ygj.gduf.edu.cn/Handler/health.ashx?flag=getHistoryList", data=data,
                                headers=headers).json()
        # 查询成功
        if res['code'] == 0:
            self.addressinfo = res['data'][0]
            self.log = self.log + "获取打卡地址成功\n打卡地址为:" + self.addressinfo['address'] + '\n'
            return 0
        else:
            self.log = self.log + "获取打卡地址失败"
            return 1

    def notifybyXtuis(self):
        # 微信提示方法
        """
        sendKey：虾推啥的token，具体在虾推啥获取 http://www.xtuis.cn/
        notifyType：提醒类型，0不提醒，1仅失败，2全部提醒
        code：打卡状态码，0为成功，其他为失败
        """
        code = self.res['code']
        desp = self.log
        if len(self.token) == 0 or self.notifyType == 0:
            return {"code": 1, "msg": "未输入key或无需提醒"}

        if code == 0 and self.notifyType == 2:
            mydata = {
                'text': '打卡成功!',
                'desp': desp
            }
            return requests.post('http://wx.xtuis.cn/' + self.token + '.send', data=mydata).json()

        elif code != 0:
            mydata = {
                'text': '打卡失败！',
                'desp': desp
            }
            return requests.post('http://wx.xtuis.cn/' + self.token + '.send', data=mydata).json()

# 通过sever酱来提醒（此方法已暂停维护）
# def notifybySeverJ(sendKey='', notifyType=0, code=0, desp=''):
#    """
#    sendKey：Sever酱的sendkey，具体在 Sever酱网站获取 https://sct.ftqq.com/sendkey
#    notifyType：提醒类型，0不提醒，1仅失败，2全部提醒
#    code：打卡状态码，0为成功，其他为失败
#   """
#   if len(sendKey) == 0 or notifyType == 0:
#        print("未输入key或无需提醒")
#        return 1
#
#    if code == 0 and notifyType == 2:
#        requests.get(url="https://sctapi.ftqq.com/" + sendKey + ".send?title=" + 'Clock%20success')
#    elif code != 0:
#        requests.get(url="https://sctapi.ftqq.com/" + sendKey + ".send?title=" + 'Clock%20failed')
#    return 0
