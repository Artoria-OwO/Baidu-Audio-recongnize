# coding: utf-8
import urllib2
import json
import base64
import os

#设置应用信息
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "kd3E8Lg13fdG4zd4LBLUXrbC" #填写API Key
client_secret = "KiC7tTg97dQAWFXeuvGBx13yvAP6tS78" #填写Secret Key

#合成请求token的URL
url = baidu_server+"grant_type="+grant_type+"&client_id="+client_id+"&client_secret="+client_secret

#获取token
res = urllib2.urlopen(url).read()
data = json.loads(res)
token = data["access_token"]
print token

path = "./record/"                           # 设置路径
dirs = os.listdir(path)                    # 获取指定路径下的文件
for i in dirs:                             # 循环读取路径下的文件并筛选输出
    if os.path.splitext(i)[1] == ".pcm":   # 筛选pcm文件
        print i                            # 输出所有的pcm文件
    #设置音频属性，根据百度的要求，采样率必须为8000，压缩格式支持pcm（不压缩）、wav、opus、speex、amr
	VOICE_RATE = 16000
	WAVE_FILE = path + i #音频文件的路径
	USER_ID = "test" #用于标识的ID，可以随意设置
	WAVE_TYPE = "pcm"


	#打开音频文件，并进行编码
	f = open(WAVE_FILE, "r")
	speech = base64.b64encode(f.read()) 
	size = os.path.getsize(WAVE_FILE)
	update = json.dumps({"format":WAVE_TYPE, "rate":VOICE_RATE, 'channel':1,'cuid':USER_ID,'token':token,'speech':speech,'len':size})
	headers = { 'Content-Type' : 'application/json' } 
	url = "http://vop.baidu.com/server_api"
	req = urllib2.Request(url, update, headers)

	r = urllib2.urlopen(req)

	t = r.read()
	result = json.loads(t)

	file = open('test.json','a')
	json.dump(result,file)
	file.close()


	print result
	if result['err_msg']=='success.':
	    word = result['result'][0].encode('utf-8')
	    if word!='':
	        if word[len(word)-3:len(word)]=='，':
	            print word[0:len(word)-3]
	        else:
	            print word
	    else:
	        print "音频文件不存在或格式错误"
	else:
	    print "错误"

