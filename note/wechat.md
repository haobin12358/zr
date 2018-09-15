## 用户首次登录

### 开始登录

在用户使用需要登录的功能时会跳转到登录页面, 同时需要记录登录前的页面

- api:

```
{{api}}/user/login/
```

- method: POST

- body: 

```
{
    "phone": "13753392801",
    "code": "123456",
    "redirect": "http://www.oldurl.com/example"
}
```

#### 如果是新用户: 

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

前端对redirect_url执行跳转, 然后微信服务器执行302跳转到回调网址. 这时可以记录用户的基本信息, 包括唯一标志`oppenid`, 最后跳转到登录前的页面, 这次跳转可以由后端执行.


#### 如果是已经授权微信的用户:

如果是已经授权的用户则不会收到跳转链接, 不执行到微信服务器的跳转

```
{
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNzgwMzczOSwiaWF0IjoxNTM3MDA0NTM5fQ.eyJtb2RlbCI6IlVzZXIiLCJpZCI6IjI3YjQ0ZDViLThiZDMtNGE0Zi1hOWVhLTczNGI5MGVhNjE0MiIsImxldmVsIjowfQ.D_ndlAloGupoSz_VN1cZPxw4uKT_4zS3oDj8wCRD-NI"
    },
    "message": "获取token成功",
    "status": 200
}}


```


