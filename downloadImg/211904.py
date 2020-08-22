import urllib.request, urllib.parse, urllib.error
import http.cookiejar
from lxml import etree
import hashlib
import datetime
import simplejson as json
from ttshitu import base64_api
import base64
import os
import time
from util import saveimg

def index():
    cookie = http.cookiejar.CookieJar() # 声明一个CookieJar对象实例来保存cookie
    handler = urllib.request.HTTPCookieProcessor(cookie) # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    URL_ROOT="https://www.wishpost.cn/welcome/"
    handler = urllib.request.HTTPCookieProcessor(cookie) # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    opener = urllib.request.build_opener(handler) # 通过handler来构建opener
    response = opener.open(URL_ROOT) # 此处的open方法同urllib2的urlopen方法，也可以传入request
    h=""
    for item in cookie:
        h+=item.name+'='+item.value+';'
    wb_data=response.read().decode('utf-8')
    html = etree.HTML(wb_data)
    html_data = html.xpath('//*[@id=\"xsrf-container\"]/input')
    for i in html_data:
        _rf=i.attrib['value']
        return h,_rf

    return h

def img(cookie,issave):
    GMT_FORMAT =  '%a, %d %b %Y %H:%M:%S GMT'
    dtN_GMT= datetime.datetime.utcnow().strftime(GMT_FORMAT)
    img_url="https://www.wishpost.cn/get-new-captcha?version={0}".format(urllib.parse.quote(dtN_GMT))
    m = hashlib.md5()
    # 携带cookie进行访问
    headers = {
        'Cookie':cookie
    }
    request = urllib.request.Request(img_url,headers=headers)
    response = urllib.request.urlopen(request)
    img_byte = response.read()
    if issave:
      m.update(img_byte)
      img_name = m.hexdigest()
      saveimg(img_byte,img_name,"./data/211904/test/")
  
    return img_byte

def tracking(code,xrf,cookie):
 try:
    time.sleep(5)
    urlR = "https://www.wishpost.cn/api/tracking/search"
    headers = {
        #伪装一个火狐浏览器
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        "host":'www.wishpost.cn',
        "X-XSRFToken":xrf,
        "Cookie":cookie,
        "Content-Type":"application/json"
    }
    data=bytes(json.dumps({"ids[]":["WI001187021582EPC"],"params_num":1,"api_name":"tracking/search","captcha":code}),'utf8')
    #如果给urlopen这个函数传递了data这个参数，那么它的请求方式则不是get请求，而是post请求
    req = urllib.request.Request(url=urlR,data=data,headers=headers,method="POST")
    response = urllib.request.urlopen(req)
    resp=response.read().decode('utf-8')
    return resp
 except urllib.error.URLError as e:
         if hasattr(e,"code"):
               print(e.code)
         if hasattr(e,"reason"):
               print(e.reason)
 return resp

def DownLoad():
    try:
        cookie,xrf=index()
        img_byte=img(cookie,False)
        base64_data = base64.b64encode(img_byte)
        #TODO:请求识别
        resp = ttshitu.base64_api(base64_data)
        if resp['success']:
            code=resp["data"]["result"]
            try:
                result=tracking(code,xrf,cookie)
                data2 = json.loads(result)
                print(data2['code'])
                if data2['code']==0:
                    filename="./data/211904/train/"+code+".png"
                    i=0
                    while True:
                        filacode=code
                        if os.path.exists(filename)==False:
                            saveimg(img_byte,filacode,"./data/211904/train/")
                        break
                        i+=1
                        code=str(code)+"("+str(i)+")"
                        filename="./data/211904/train/"+str(code)+".png"
        
            except:
                saveimg(img_byte,code,"./data/211904/test/")
                print(resp["message"])
        else:
                saveimg(img_byte,code,"./data/211904/test/")
                print(resp["message"])
    except:
        print("failure")
 

if __name__ == '__main__':
     for i in range(50000):
       DownLoad()