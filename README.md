# auto-daka GDUF/yiban/check
**调用daka()方法 即可使用** 

自用代码 代码粗糙 还请见谅

## daka()参数说明

daka(flag,accountid,password,address='广东省广州市天河区迎福路靠近广东金融学院(广州校区)')

|  参数   | 类型  |说明|
|  ----  | ----  | ---- |
| flag  | str |只是一个标记昵称，多人同时打卡时用作区分|
| accountid  | str |账户名|
| password  | str |密码|
| address  | str |打卡地址，默认广州校内|

## daka()方法返回值

返回的是一个字典值

|  参数   | 类型  |说明|
|  ----  | ----  | ---- |
| code  | int |打卡状态码，0是成功，其他都是失败|
| msg | str |code的说明|
|  detail   | str  |具体流程，操作日志信息|


还有很多错误码 都是我编的 为的是与原本的程序返回格式统一

detail返回的是具体的操作日志

**注：授权会过期，没有添加自动授权接口，授权失败时需要手动打卡。** 

**第一次授权失败后，大概半个月到一个月不会失效，即半个月到一个月需要手动打卡一次**

## 关于如何自动运行的方法

**推荐使用腾讯云免费的云函数**

[腾讯云,点这里](https://cloud.tencent.com/)

1.先注册腾讯云账号

2、进到云函数控制台界面

3、新建云函数

![image](https://user-images.githubusercontent.com/88192911/158826265-75603d6c-ffca-4107-9bbf-950105498250.png)
4、

从头开始 --> 选择python3.6 --> 本地上传文件夹 -->上传github下载的文件 -->（解压后） 提交 --> 完成
![image](https://user-images.githubusercontent.com/88192911/158829870-f069c5db-306c-4acd-b1b7-638af6742cf7.png)

5、

函数管理 --> 函数配置 --> 执行超过时间改成90秒
![image](https://user-images.githubusercontent.com/88192911/158827111-31e8e55b-65c3-48f1-8df8-78d61ee2bc2d.png)

6、打开在线编辑器终端

依次输入命令 安装依赖

**cd src**

**pip install -r requirements.txt -t ./**

![image](https://user-images.githubusercontent.com/88192911/158831942-88c8a487-3479-4639-9d5a-8feeb6fe5f42.png)

安装完成后 部署

7、设定自动启动时间

触发管理 --> 创建触发器

![image](https://user-images.githubusercontent.com/88192911/158832213-d3ad7a74-7bec-4efa-876b-c99f798e115b.png)

这个就是每天10点启动 （其他时间详见Cron相关文档）

**收工！**
