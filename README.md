# auto-daka yiban/check
**调用index.py下的主方法 即可使用** 

**温馨提示： 请如实打卡，按时打卡。本代码只是代替每日重复的工作，如有异常请及时上报！**

## 关于如何获取deviceData、UA信息
 deviceData一定为
 
 '''
 
 '{"appVersion":"5.0.9","deviceModel":"iPhone+X","systemVersion":"15.4.1","uuid":"123F123123D-6CE2-4035-BD75-D081231231"}'
 
 '''
 
 **注意：单双引号不能弄反**
 
 字典字符串

 建议抓包获取！记得安装https证书。
 
 抓取的接口为： **https://ygj.gduf.edu.cn/Handler/device.ashx?flag=checkBindDevice**
 
 获取请求头的UA以及提交的data表单信息。
 
 若不想抓包，也可以自行百度如何获取uuid，然后自行构造deviceData以及UA等信息

 **ps：可能可以缩减某些参数，例如UA，像上个版本一样，可能可以使用统一的UA，具体暂未尝试**
 
 
## 历史重大版本

   **v1.0 完成自动打卡**
   
   **v1.5 增加微信提醒**
     
   **v2.0 增加自动授权**
   
   **v3.0 增加自动获取打卡地址（根据上次打卡地址进行打卡）**
   
   **v3.1 修复可能导致授权失败从而获取地址失败的问题**
   
   **v3.2 修复打卡失败**


## 一、关于如何自动运行的方法

**下面是[腾讯云](https://cloud.tencent.com/)云函数的例子，其他云函数大同小异，其他函数要更改入口程序。**

**（注：腾讯云函数从2022/05开始，不再提供最低免费额度。建议使用其他云函数方法，例如 github action、阿里云等，改一下入口程序就可以使用）**

**1、先注册腾讯云账号**

**2、进到云函数控制台界面**

**3、新建云函数**

![image](https://user-images.githubusercontent.com/88192911/158826265-75603d6c-ffca-4107-9bbf-950105498250.png)

4、从头开始 --> 选择python3.6 -->空白函数 --> 本地上传文件夹 -->上传github下载的文件 -->（解压后） 提交 --> 完成

![image](https://user-images.githubusercontent.com/88192911/158829870-f069c5db-306c-4acd-b1b7-638af6742cf7.png)

5、函数管理 --> 函数配置 --> 执行超过时间改成90秒

![image](https://user-images.githubusercontent.com/88192911/158827111-31e8e55b-65c3-48f1-8df8-78d61ee2bc2d.png)

6、打开在线编辑器终端（**新建终端**）

依次输入命令 安装依赖

```
cd src

pip install -r requirements.txt -t ./

```

![image](https://user-images.githubusercontent.com/88192911/158831942-88c8a487-3479-4639-9d5a-8feeb6fe5f42.png)

安装完成后 部署 

7、在index.py中填写相关打卡信息.

  支持多人打卡。
  
  **格式：账号,密码,打卡地址(输入具体打卡地址或输入"自动"，自动则默认根据昨天的地址打卡。），微信提醒token（可省略，获取方式见常见问题）,提醒类型（可省略)，0不提醒，1仅失败，2全部提醒**
  
  例如：
  
  ```
  information=[["137123123","password","自动",'ASDASDAS123123','1'],
                         
                         ["121233","ASDWD123","具体地址"]]
                         
   ```
 
上文即是两人打卡的例子，第一个人自动获取地址且需要失败提醒，第二个人固定打卡地址且不需要提醒 **(具体地址建议填写打卡记录中的地址)**。

8、设定自动启动时间

触发管理 --> 创建触发器

![image](https://user-images.githubusercontent.com/88192911/158832213-d3ad7a74-7bec-4efa-876b-c99f798e115b.png)

这个就是每天10点启动 （其他时间详见Cron相关文档） 

**注意事项：请把时间设置到8点以后，以避免不必要的错误。因为云函数的时间是UTC+0.**

**收工！**

## 二、常见问题

**1、关于如何随机时间执行**

答：关于取随机时间进行打卡。这里建议更改触发器的设定。如果在代码里增加随机延迟的话，延迟短了没什么用，延迟长了浪费云函数的资源使用量。

解决方法： 设定多个触发器，设置7个，每周执行不一样的。或者设置3个，循环使用。

**2、关于虾推啥Token获取**

![image](https://user-images.githubusercontent.com/88192911/163210690-1e54b806-b0c3-4da5-b74d-f83f016148db.png)

关注公众号，即可获取！


**~~3、关于Server酱微信提醒功能的key值获取~~（已弃用）**

~~答：[Sever酱地址](https://sct.ftqq.com/upgrade?fr=sc)，进入页面后，微信登录并关注公众号。再按**Key&API选项**，复制SendKey，即可获取。~~

**4、如何更新**

  答：在腾讯云云函数中覆盖 yiban.py index.py 两个文件，并重新在index中填写信息，部署即可。
