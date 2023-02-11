from flask import Flask, request
import json
import requests
import urllib
import time
import openai
import re

app = Flask(__name__)
 

def talk_with_robot(msg, robot_name=None):
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    html = requests.get(url)
    rt = html.json()["content"]
    rt = rt.replace("{br}","\n")
    if robot_name is not None:
        rt = rt.replace("菲菲", robot_name)
    return rt

def send_msg(wxid, is_img, msg):
    if is_img:
        payload = {"type": "Q0010", "data": {"wxid": wxid, "path": msg}}
    else:
        payload = {"type": "Q0001", "data": {"wxid": wxid, "msg": msg}}

    headers = {
        'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
        'Content-Type': 'application/json'
    }
    # 请求url
    url = 'http://127.0.0.1:8055/DaenWxHook/client/'#8055
    # 请求参数

    # 调用post
    response = requests.post(url, json=payload,
                             headers=headers)  # response 响应对象
    # 获取响应状态码
    #print('状态码：', response.status_code)
    # 获取响应头
    #print('响应头信息：', response.headers)
    # 获取响应正文
    #print('响应正文：', response.text)

    #服务器无响应
    if response.status_code != '200' or response.text==[]:
        return '请求失败'

def savetext(text,name):#文本追加模式
    with open(name+".txt", "a", encoding='utf-8') as f:
        f.write(text)
        f.close()
def readtext(name):#文本只读
    with open(name+".txt", "r", encoding='utf-8') as f:
        text=f.read()
        f.close()
        return text
        

def send_txt_msg(wxid, msg, txt):
    send_msg(wxid, False, 'chat'+txt)
    writemslog(wxid,msg,txt,msglogname)
    print('回复消息-收件人：'+wxid+',信息内容：'+txt)


def send_img_msg(wxid, msg,imgname):
    img_path='img//'+imgname+'.jpg'
    send_msg(wxid, True, img_path)


def on_rcv_chatroom_msg(from_wxid, msg):
    print("收到群消息")

def on_rcv_p2p_txt(from_wxid, msg_txt):#收到个人消息
    
    res = talk_with_robot(msg_txt,"2084222530")
    # print("收到文本消息", from_wxid, msg_txt)
    send_txt_msg(from_wxid, res)
    # send_img_msg(from_wxid, 'C:\\Users\\Administrator\\Desktop\\6.gif')

#机器人接口
def qingyun(msg_txt):
    res = talk_with_robot(msg_txt,"小C")
    return res

def chatgpt(msg,max_tokens):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            #model="text-curie-001",
            #model="text-babbage-001",
            #model="text-ada-001",
            prompt=msg,
            temperature=0.9,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2
            )
        reply = response.choices[0].text
        return reply
    except:
        return '请求openai失败，可能网络问题'



def dwz(imglink):
    cookies = {
        'Hm_lvt_6188d53492b3951c5aa16a77f0b0e858': '1676111142',
        'XSRF-TOKEN': 'eyJpdiI6IjErbkdYZnN6NVNKY0ZlY0grb3BHZWc9PSIsInZhbHVlIjoib2NzSFRsa0hQXC9XeXpadnVVbzQ3TWN4Zzl1OXIyU1Z5XC94dHNmRzg2Zmt1dHJ1RGlCS2ozZHMrWEJUQ0xSZzB6IiwibWFjIjoiYmU5NGZiYzMyOTg5ZTlmMmU1YjM2MWVmMjc4MGVlN2U3MTczMDU0ZWNlOTU2ZjQ4NmRmYmY0ZTI0YTVmMzYyOCJ9',
        'laravel_session': 'eyJpdiI6IklmMXZOenBhK1JlT0tEdW84Qis2M1E9PSIsInZhbHVlIjoiOWJscHFRWUR3VjRrbmVJUmxCWk4xaU04bmxucXZEVll6a1dySVpmK3ZtdFhvVjRCclUxTHZjd0F5ejJ4RVBcL2giLCJtYWMiOiI5ZDYwY2U4OTM5NmI5ZTYzMjliNWI4MjRiOGY1MGRjNGE4MjYyYWNmYWU5ZTFjZWE2MmRiMzkxNTViNmFiZTQxIn0%3D',
        'Hm_lpvt_6188d53492b3951c5aa16a77f0b0e858': '1676112588',
    }

    headers = {
        'authority': 'www.free-api.com',
        'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
        'x-csrf-token': 't04tRcTUiwBgM2wkfwTBMmYFg6l4tY9QQfVXzbPU',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.free-api.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.free-api.com/use/300',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': 'Hm_lvt_6188d53492b3951c5aa16a77f0b0e858=1676111142; XSRF-TOKEN=eyJpdiI6IjErbkdYZnN6NVNKY0ZlY0grb3BHZWc9PSIsInZhbHVlIjoib2NzSFRsa0hQXC9XeXpadnVVbzQ3TWN4Zzl1OXIyU1Z5XC94dHNmRzg2Zmt1dHJ1RGlCS2ozZHMrWEJUQ0xSZzB6IiwibWFjIjoiYmU5NGZiYzMyOTg5ZTlmMmU1YjM2MWVmMjc4MGVlN2U3MTczMDU0ZWNlOTU2ZjQ4NmRmYmY0ZTI0YTVmMzYyOCJ9; laravel_session=eyJpdiI6IklmMXZOenBhK1JlT0tEdW84Qis2M1E9PSIsInZhbHVlIjoiOWJscHFRWUR3VjRrbmVJUmxCWk4xaU04bmxucXZEVll6a1dySVpmK3ZtdFhvVjRCclUxTHZjd0F5ejJ4RVBcL2giLCJtYWMiOiI5ZDYwY2U4OTM5NmI5ZTYzMjliNWI4MjRiOGY1MGRjNGE4MjYyYWNmYWU5ZTFjZWE2MmRiMzkxNTViNmFiZTQxIn0%3D; Hm_lpvt_6188d53492b3951c5aa16a77f0b0e858=1676112588',
    }

    data = {
        'url': imglink,
        'dwzapi': 'urlcn',
        'fzsid': '300',
    }

    response = requests.post('https://www.free-api.com/urltask', cookies=cookies, headers=headers, data=data)


    durl=response.text

    durl=re.findall("ae_url"+'.*?'+'}', durl)[0]
    durl=durl.replace('ae_url":"','').replace('"}','').replace('\/','/')

    return durl

def chatgptimg(msg,num=1):
    try:
        response = openai.Image.create(
            prompt=msg,
            n=num,
            size="512x512"
        )
        image_url = response['data'][0]['url']

        image = requests.get(image_url).content
        name=msg.replace(' ','')
        with open('img//'+name+'.jpg','wb') as f:
            f.write(image)

        durl=dwz(image_url)
        
        return durl
    
    except:
        return ''



def writemslog(wxid,msg,reply,logdir):#写发信人和信息内容日志
    txt=wxid+','+msg+','+reply+'\n'
    savetext(txt,logdir)

#得到消息之后的操作
def getdmsg(from_wxid,msg,logdor):
    print('收到消息-发件人：'+from_wxid+',信息内容：'+msg)
    #1.如果有白名单，且不在白名单内，不回复
    if hwhitename==1 and from_wxid not in whitename:
        txt='此用户不在白名单内'
        writemslog(from_wxid,msg,txt, msglogname)
        print('未回复'+from_wxid+',内容'+txt)
        return ''
    #2.如果有黑名单，且在黑名单内,不回复
    elif hblackname==1 and from_wxid not in blackename:
        txt='此用户在黑名单内'
        writemslog(from_wxid,msg,txt, msglogname)
        print('未回复'+from_wxid+',内容'+txt)
        return ''
    #3.如果字数大于200
    elif len(msg)>200:
        send_txt_msg(from_wxid, msg, '字数不可以超过200字哦')
        return ''
    #4.访问次数大于10

    #过滤结束，调用机器人
    else:
        reply=''
        if ai==1:
            reply=qingyun(msg)#得到机器人返回结果
        #对结果进行过滤
        
        #如果是普通用户，返回字数小于300字
        framelong=500
        #如果vip,返回字数500
        if from_wxid in vip:
            framelong=800
        #如果ssvip返回字数1000
        elif from_wxid in svip:
            framelong=1000
        
        #调用openai
        if ai==2:
            if msg[0:2]=='画图':
                msg=msg[2:]
                imglink = chatgptimg(msg,1)
                if imglink=='':
                    send_txt_msg(from_wxid,msg,'画图错误')
                else:
                    send_txt_msg(from_wxid,msg,imglink)
            else:
                reply = chatgpt(msg,1000)
                reply = reply.replace('\n','')
                reply = reply[0:1000]
                #发送
                send_txt_msg(from_wxid,msg,reply)

@app.route('/wechat/', methods=['get', 'post'])
def wechat():
    data = request.stream.read()
    data = data.decode('utf-8')
    data = json.loads(data)
    type = data['type']

    if type == 'D0003':#收到消息
        data = data['data']
        msg = data['msg']

        #如果没有唤醒词，结束
        if wakename not in msg:
            return ''
        msg=msg.replace(wakename,'')
        from_wxid = data['fromWxid']
        fromType=data['fromType']#消息来源 1|私聊 2|群聊 3|公众号
        msgType=data['msgType']#消息类型 1|文本 3|图片 34|语音

        #if "@chatroom" in from_wxid:#收到群消息
            #on_rcv_chatroom_msg(from_wxid, msg)

        if fromType==1 and msgType ==1:#收到私聊文字信息
            getdmsg(from_wxid,msg,msglogname)

    return ''


if __name__ == '__main__':
    openai.api_key = ''
    msglogname='msglog'
    hwhitename=0
    whitename=[]
    hblackname=0
    blackename=[]
    vip=[]
    svip=[]
    wakename='chat'
    ai=2  #1是轻与，2是chatgpt
    app.run(debug=False, port=8089)
