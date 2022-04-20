# auto-daka yiban/check
**调用daka()方法 即可使用** 

**温馨提示： 请如实打卡，按时打卡。本代码只是代替每日重复的工作，如有异常请及时上报！**

~~**注：授权会过期，没有添加自动授权接口，授权失败时需要手动打卡。** ~~（已更新）

~~**第一次授权失败后，大概半个月到一个月不会失效，即半个月到一个月需要手动打卡一次**~~（已更新）

## 关于如何自动运行的方法

**推荐使用[腾讯云](https://cloud.tencent.com/)免费的云函数**

**1、先注册腾讯云账号**

**2、进到云函数控制台界面**

**3、新建云函数**

![image](https://user-images.githubusercontent.com/88192911/158826265-75603d6c-ffca-4107-9bbf-950105498250.png)

4、从头开始 --> 选择python3.6 --> 本地上传文件夹 -->上传github下载的文件 -->（解压后） 提交 --> 完成

![image](https://user-images.githubusercontent.com/88192911/158829870-f069c5db-306c-4acd-b1b7-638af6742cf7.png)

5、函数管理 --> 函数配置 --> 执行超过时间改成90秒

![image](https://user-images.githubusercontent.com/88192911/158827111-31e8e55b-65c3-48f1-8df8-78d61ee2bc2d.png)

6、打开在线编辑器终端（**新建终端**）

依次输入命令 安装依赖

**cd src**

**pip install -r requirements.txt -t ./**

![image](https://user-images.githubusercontent.com/88192911/158831942-88c8a487-3479-4639-9d5a-8feeb6fe5f42.png)

安装完成后 部署

7、设定自动启动时间

触发管理 --> 创建触发器

![image](https://user-images.githubusercontent.com/88192911/158832213-d3ad7a74-7bec-4efa-876b-c99f798e115b.png)

这个就是每天10点启动 （其他时间详见Cron相关文档） 

**注意事项：请把时间设置到8点以后，以避免不必要的错误。因为云函数的时间是UTC+0.**

**收工！**

## 常见问题

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

## daka()参数说明

daka(flag,accountid,password,address='')

|  参数   | 类型  |说明|
|  ----  | ----  | ---- |
| flag  | str |只是一个标记昵称，多人同时打卡时用作区分|
| accountid  | str |账户名|
| password  | str |密码|
| address  | str |打卡地址，默认广州校内|

**返回值**

|  参数   | 类型  |说明|
|  ----  | ----  | ---- |
| code  | int |打卡状态码，0是成功，其他都是失败|
| msg | str |code的说明|
|  detail   | str  |具体流程，操作日志信息|
