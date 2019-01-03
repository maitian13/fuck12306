import requests, pickle, time
from PIL import Image
from json import loads
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from order import Order
import information
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class LoginTic(object):
    def __init__(self):
        # 获取cookie
        cookie_post = "https://kyfw.12306.cn/otn/login/conf"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
        # 创建一个网络请求session实现登录验证
        self.session = requests.session()
        data = self.session.get(cookie_post)
    # 获取验证码图片
    def getImg(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand";
        response = self.session.get(url=url,headers=self.headers,verify=False)
        # 把验证码图片保存到本地
        with open('img.jpg','wb') as f:
            f.write(response.content)
        # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
        try:
            im = Image.open('img.jpg')
            # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
            im.show()
            # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
            im.close()
        except:
            print(u'请输入验证码')
        #=======================================================================
        # 根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置，例如：2,5
        # ---------------------------------------
        #         |         |         |
        #    0    |    1    |    2    |     3
        #         |         |         |
        # ---------------------------------------
        #         |         |         |
        #    4    |    5    |    6    |     7
        #         |         |         |
        # ---------------------------------------
        #=======================================================================
        captcha_solution = input('请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution

    # 验证结果
    def checkYanZheng(self,solution):
        # 分割用户输入的验证码位置
        soList = solution.split(',')
        # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
        yanSol = ['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']
        yanList = []
        for item in soList:
            print(item)
            yanList.append(yanSol[int(item)])
        # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
        yanStr = ','.join(yanList)
        checkUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        data = {
            'login_site':'E',           #固定的
            'rand':'sjrand',            #固定的
            'answer':yanStr    #验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }
        # 发送验证
        cont = self.session.post(url=checkUrl,data=data,headers=self.headers,verify=False)
        # 返回json格式的字符串，用json模块解析
        dic = loads(cont.content.decode('utf-8'))
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        if str(code) == '4':
            return True
        else:
            return False

    # 获取用户信息
    def getUserInfo(self, token):
        get_useiInfo_url = 'https://kyfw.12306.cn/otn/uamauthclient'
        response = self.session.post(get_useiInfo_url, {"tk": token}).json()
        if response['result_code'] == 0:
            print('登录成功，获取用户名：{}\napptk={}'.format(response['username'], response['apptk']))
        with open('login_session', 'wb') as f:
                pickle.dump(self.session.cookies, f)
    # 获取token
    def getToken(self):
        get_token_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        form_data = {"appid": "otn"}
        response = self.session.post(get_token_url, form_data).json()
        print('获取token成功,token={}'.format(response['newapptk']))
        self.getUserInfo(response['newapptk'])

    # 登陆
    def dologin(self):
        login_url = 'https://kyfw.12306.cn/passport/web/login'
        print('进入登录环节')
        form_data = {
            "appid": "otn",
            "username": information.USERNAME,
            "password": information.PASSWORD,
        }
        response = self.session.post(login_url, form_data).json()
        if response['result_code'] == 0:
            print('登录成功，前去请求token')
            self.getToken()
    # 发送登录请求的方法
    def loginTo(self):
        # 用户输入用户名，这里可以直接给定字符串
        #userName = input('Please input your userName:')
        # 用户输入密码，这里也可以直接给定
        #pwd = input('Please input your password:')
        # 输入的内容不显示，但是会接收，一般用于密码隐藏
        # pwd = getpass.getpass('Please input your password:')
        loginUrl = "https://kyfw.12306.cn/passport/web/login"
        data = {
            'username':information.USERNAME,
            'password':information.PASSWORD,
            'appid':'otn'
        }
        result = self.session.post(url=loginUrl,data=data,headers=self.headers,verify=False)
        dic = loads(result.content.decode("utf-8-sig"))
        print(result.content)
        mes = dic['result_message']
        # 结果的编码方式是Unicode编码，所以对比的时候字符串前面加u,或者mes.encode('utf-8') == '登录成功'进行判断，否则报错
        if mes == u'登录成功':
            print('恭喜你，登录成功，可以购票!')
            with open('login_session', 'wb') as f:
                pickle.dump(self.session.cookies, f)
        else:
            print('对不起，登录失败，请检查登录信息!')

    def loginFromFile(self):
        with open('login_session', 'rb') as f:
            self.session.cookies.update(pickle.load(f))
    def testLoginStatus(self):
        url = "https://kyfw.12306.cn/otn/login/conf"
        r = self.session.post(url=url, headers=self.headers)
        print(r.text)
        url = "https://kyfw.12306.cn/otn/index/initMy12306Api"
        r = self.session.post(url=url, headers=self.headers)
        print(r.text)

if __name__ == '__main__':
    login = LoginTic()
    isFromFile = input('是否文件登录：')
    if isFromFile == "1":
        login.loginFromFile()
    else:
        yan = login.getImg()
        chek = False
        #只有验证成功后才能执行登录操作
        while not chek:
            chek = login.checkYanZheng(yan)
            if chek:
                print('验证通过!')
                login.dologin()
            else:
                print('验证失败，请重新验证!')
    login.testLoginStatus()
    myorder = Order(headers = login.headers, session = login.session)
    myorder.main()
    # login("", "")