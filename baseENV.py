import requests

#finmind登入資料
login_url = "https://api.finmindtrade.com/api/v4/login"
data_url = "https://api.finmindtrade.com/api/v4/data"
payload = {
    #登入帳號
    "user_id": "",
    #登入密碼
    "password": "",
}
login_data = requests.post(login_url, data=payload)
login_data = login_data.json()

#USPTO_Patentsview_key
patentkey = ''

#google API key
googleapikey = ''