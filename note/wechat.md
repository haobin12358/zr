### 用户首次登录

#### 开始登录

在用户使用登录的功能时会跳转到登录页面, 同时需要记录登录前的页面

链接:

```
{{api}}/user/login/
```

参数:
```
{
    "phone": "13753392801",
    "code": "123456",
    "redirect": "http://www"
}
```

如果用户是首次使用手机号码登录, 则会收到token和跳转链接, 格式为:

```
{
"data": {
    "redirect_url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa7109d8534a2d837&redirect_uri=http://l.wkt.ooo:7443/user/weixin_callback/&response_type=code&scope=snsapi_base&state=25c479b7-08c9-4d94-b1c6-10d74e59af4d#wechat_redirect",
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNzY5MDkyMSwiaWF0IjoxNTM2ODkxNzIxfQ.eyJtb2RlbCI6IlVzZXIiLCJpZCI6IjI1YzQ3OWI3LTA4YzktNGQ5NC1iMWM2LTEwZDc0ZTU5YWY0ZCIsImxldmVsIjowfQ.9YV-i7ECp4ZvSAzZROm_m7rKRtXEphUVwiYJTokiZOo"
   },
"message": "注册成功",
"status": 302
}

```


#### 跳转

前端使用跳转链接做跳转, 这时后端会将用户的资料存下, 跳转到之前的页面

