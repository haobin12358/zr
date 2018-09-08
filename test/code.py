import requests

headers = {
    'Authorization': 'APPCODE a1ead5dd338d44c7ac4caa083a13278e'
}
url = 'http://mobai.market.alicloudapi.com/mobai_sms?param=code%3A9999&phone=18753391801&templateId=tp18090816'
content = requests.get(url, )