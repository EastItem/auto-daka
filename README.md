# auto-daka GDUF/yiban/check
## 调用daka()方法 即可使用 
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
|  code   | msg  |detail|
|  ----  | ----  | ---- |
| 0  | 打卡成功 |‘log’|
| 1  | 打卡失败 |‘log’|

还有很多错误码 都是我编的 为的是与原本的程序返回格式统一

detail返回的是具体的操作日志
