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
