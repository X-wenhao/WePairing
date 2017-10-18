# WeParing
*ming zhang*

# Android

# Back end
### 需要
- 框架: flask
- 数据库: sqlite
- 服务器软件： nginx

### 主要视图函数

| func name        | url           | note  |
|:-------------:|:-------------:|:-----:|
| register()      | app.route('/register/') | 需要返回表单，可以用jinja2模板渲染注册界面 |
|login() |app.route('/login/')| 需要返回表单，可以用jinja2模板渲染注册界面|
|getUserInfo()|app.route('/getuserinfo/') |注册后的资料填写,需要返回表单，可以用jinja2模板渲染注册界面|
|showInfo()|app.route('/showinfo/')| 后台数据库查询之后直接返回被渲染过的显示用户信息的界面 |
|studyPairing()| app.route('/studypairing/')| 自习匹配，获取用户名、自习的时间（下拉选择时间段）、想要一起自习的人数（设限）、自习地点。函数返回匹配的对象|
|otherParing()| app.route('/otherparing/')|其他匹配|

### 数据表

|手机号|用户名|学校（不同校区认为是不同学校）|年级|专业|性别|选填:擅长科目（下拉选择）|选填:个人信息|选填:头像|
|:-------------:|:-------------:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
|159xxxx6437|zhangming|hust|3|Computer Science & Technology|M||Computer System & DataStructrue|interested in CS|/image/avator/zhangming.jpg|

```sql
user.sql

drop table if exists user;
create table user (
  phoneNum integer primary key,
  userName string not null,
  school string not null,
  grade integer not null,
  major string not null,
  character not null,
  strength string,
  text selfInfo,
  avator string
);
```

### 一些细节
- showInfo()的返回
	return app.render_template('showinfo.html', userinfolist=userinfodic) # userinfodic是在showinfo.html中需要被渲染的部分，是一个字典
- 使用原生sql语句做数据库增删改查等事务
- 匹配池 paringPool（python dict），存储用户被匹配到的必要信息，用户登录进去即将该用户放入匹配池，登出即将该用户从匹配池删掉
