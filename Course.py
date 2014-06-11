#coding:utf-8
import urllib,urllib2,cookielib,re,time
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
headers={
        "Content-Type":"application/x-www-form-urlencoded",
        "Referer": "http://jwjz.ucas.ac.cn/Student/DefaultOld.aspx",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0",
         }
UserName="2013E8018661147"   #学号
Password="XXXXXXXX"   #身份证号
courseNum="0GX011H"        #课程编号
courseType=courseNum[0]
regular='<a id="CourseList__([\S]*)_CodeLink" href="[\S]*" target="_blank">'+courseNum+"</a>"
mainpage_url="http://jwjz.ucas.ac.cn/Student/DeskTopModules/Course/CourseManage.aspx"
posturl="http://jwjz.ucas.ac.cn/Student/DesktopModules/Course/SelectCourse.aspx?CourseTypeString="+courseType
logincount=0
postcount=0

def login():
    req=urllib2.Request("http://jwjz.ucas.ac.cn/Student/DefaultOld.aspx")
    page=urllib2.urlopen(req)
    data=page.read()
    __EVENTVALIDATION=re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([\S]*)" />',data)[0]
    __VIEWSTATE=re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([\S]*)" />',data)[0]    
    #print __EVENTVALIDATION,__VIEWSTATE
    params=urllib.urlencode({"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":__VIEWSTATE,"__EVENTVALIDATION":__EVENTVALIDATION,"UserName":UserName,"Password":Password
                        ,"imgbtLogin.x":"10","imgbtLogin.y":"1"  })   
    req=urllib2.Request("http://jwjz.ucas.ac.cn/Student/DefaultOld.aspx",params,headers)
    urllib2.urlopen(req)

while True:
    req=opener.open(mainpage_url)
    data=req.read()
    if "__VIEWSTATE" not in data:
        logincount+=1
        login()
    if courseNum in data:
        print "------------------------恭喜，选课成功！------------------------------"
        break;
    req=urllib2.Request(posturl)
    page=urllib2.urlopen(req)
    data=page.read()
    __VIEWSTATE=re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([\S]*)" />',data)[0]
    __EVENTVALIDATION=re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([\S]*)" />',data)[0]
    crl_id=re.findall(regular,data)[0]
    postparam="CourseList:_"+crl_id+":ItemCheckBox"
    params=urllib.urlencode({"__VIEWSTATE":__VIEWSTATE,"__EVENTVALIDATION":__EVENTVALIDATION,postparam:"on","SureBtn":"确定提交选课" })
    req=urllib2.Request(posturl,params,headers)
    page=urllib2.urlopen(req)
    postcount+=1
    print U"尝试登录登录"+str(logincount)+U"次,尝试提交"+str(postcount)+U"次。。。"
    time.sleep(5)



