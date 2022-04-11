from paddleocr import PaddleOCR
import json
from time import sleep
import datetime
import os
import sys
from interface import Asst, Message


def upper(path, n=1):
    for i in range(n):
        path = os.path.split(path)[0]
    return path


def ring(string: str, close=False):
    print(string)
    os.popen("msg %username% /time:10 \"{}:{}\"".format(os.path.split(os.path.realpath(sys.argv[0]))[1], string))
    if close:
        input("按回车键退出...")
        sys.exit()


ISPACK = True
"""是否打包 如果你直接运行python脚本,请将此参数设置为False """
"""此常量只影响文件的查找目录"""
FILEPATH_THIS = upper(os.path.realpath(sys.argv[0]))
if not ISPACK:  # 如果你没有打包 将在脚本所在目录查找文件
    FILEPATH = upper(os.path.realpath(sys.argv[0]))
else:  # 如果决定打包 将在上级目录查找文件
    FILEPATH = upper(os.path.realpath(sys.argv[0]), 2)

CONFIGDIR = FILEPATH + "\\config.json"
"""配置文件位置"""
configs: dict = dict()
if os.path.exists(CONFIGDIR):
    try:
        with open(CONFIGDIR, 'r') as f:
            configs: dict = json.load(f)
    except json.decoder.JSONDecodeError:
        try:
            string = "{}已存在并且读取失败 ".format(os.path.split(CONFIGDIR)[1])
            os.rename(CONFIGDIR, CONFIGDIR+".bak")
        except:
            string += "请手动删除文件后重试"
            ring(string, close=True)
        string += "已为您备份为{}并重新创建{}".format(os.path.split(CONFIGDIR)[1]+".bak", os.path.split(CONFIGDIR)[1])
        ring(string)

DEBUG = configs.get("DEBUG", False)
"""是否控制台输出日志"""
"""此选项在配置文件中隐藏"""

ACTTIME = configs.get("ACTTIME", ["2:00:00", "9:00:00", "17:00:00"])
"""每日执行脚本的时间,默认2点、9点、17点"""
"""如果为空则单次运行"""
MAXWEEKANNTIMES = configs.get("MAXWEEKANNTIMES", 6)
"""每周剿灭打满次数 默认为6 如果你没有成年实名的taptap账号请填0"""
SKIPANNINSTART = False
"""在开启软件的当周跳过剿灭"""

ARKUPGRADE_COORD = configs.get("ARKUPGRADE_COORD", [950, 730])
"""大版本过低提示框的确认键位置,用来跳转其他应用. 1080P 16:9的手机大概是这个坐标"""

PINGWEBSITE = configs.get("PINGWEBSITE", "www.baidu.com")
"""用于ping网络测试的网站"""

DEVICEADDRESS = configs.get("DEVICEADDRESS", "127.0.0.1:5555")
"""你的设备地址/名称(可选).如果有报错请编辑此处"""
#EMULATOR = configs.get("EMULATOR", False)
"""设备是否是模拟器.默认为False"""

ADBPATH = configs.get("ADBPATH", "")
"""你的adb.exe路径. 已经设置了系统PATH,可以直接填写"adb".建议保持留空以自动配置"""

ASSTPATH = configs.get("ASSTPATH", "")
"""自动化脚本的路径. 建议保持留空以自动配置"""

SRC_FILE = configs.get("SRC_FILE", "")
"""截屏文件位置,用于OCR. 除非出现问题,请保持留空以自动配置"""

tasklist = configs.get("tasklist", [
    ['fight', 'LastBattle', 0, 0, 999],
    ['infrast', 1, ['Mfg', 'Trade', 'Control', 'Power', 'Reception', 'Office', 'Dorm'], "Money", 0.3],
    ['visit'],
    ['mall', True],
    ['award'],
    ['recruit', 4, [4, 5, 6], [3, 4, 5, 6], True, False]])
"""任务列表 请参考interface.py"""

configs["ACTTIME"] = ACTTIME
configs["MAXWEEKANNTIMES"] = MAXWEEKANNTIMES
configs["SKIPANNINSTART"] = SKIPANNINSTART
configs["ARKUPGRADE_COORD"] = ARKUPGRADE_COORD
configs["PINGWEBSITE"] = PINGWEBSITE
configs["DEVICEADDRESS"] = DEVICEADDRESS
#configs["EMULATOR"] = EMULATOR
configs["ADBPATH"] = ADBPATH
configs["ASSTPATH"] = ASSTPATH
configs["SRC_FILE"] = SRC_FILE
configs["tasklist"] = tasklist
with open(CONFIGDIR, 'w') as f:
    json.dump(configs, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

if ADBPATH == "" or ADBPATH.isspace():
    ADBPATH = FILEPATH + "\\platform-tools\\adb.exe"
if ASSTPATH == "" or ASSTPATH.isspace():
    for d in os.listdir(FILEPATH):
        if "MeoAssistantArknights" in d:
            ASSTPATH = FILEPATH + "\\" + d
            break
os.environ["PATH"] += os.pathsep + ASSTPATH
if SRC_FILE == "" or SRC_FILE.isspace():
    SRC_FILE = FILEPATH + '\\src.png'

# 检测以上路径是否存在
if not (os.path.exists(ADBPATH) and os.path.exists(ASSTPATH) and os.path.exists(upper(SRC_FILE))):
    ring("配置路径错误！")
    print(FILEPATH)
    print("ADBPATH(adb路径)存在") if os.path.exists(ADBPATH) else print("ADBPATH(adb路径)不存在")
    print("ASSTPATH(脚本路径)存在")if os.path.exists(ASSTPATH) else print("ASSTPATH(脚本路径)不存在")
    print("SRC_FILE(截屏文件路径)存在")if os.path.exists(upper(SRC_FILE)) else print("SRC_FILE(截屏文件路径)不存在")
    input("按回车键退出...")
    sys.exit()

if ISPACK:
    ocr = PaddleOCR(det_model_dir=FILEPATH_THIS+'\\whl\\det',
                    rec_model_dir=FILEPATH_THIS+'\\whl\\rec',
                    cls_model_dir=FILEPATH_THIS+'\\whl\\cls',
                    use_angle_cls=False, lang="ch", show_log=False)
else:
    ocr = PaddleOCR(lang="ch", use_angle_cls=False, show_log=False)


def console(command: str) -> str:
    try:
        return os.popen(command).read().strip()
    except:
        r = os.popen(command)
        r = r.buffer.read().decode("utf-8").strip()
        return r


def timefull():
    "返回[完整时间]"
    return "[" + str(datetime.datetime.now()) + "]"


def timeshort():
    "返回[日期]"
    return "[" + str(datetime.datetime.now().date()) + "]"


def nexttime(timeHMS: str) -> datetime:
    """
    返回下一次字符串时间对应的datetime对象
    """
    t = datetime.datetime.combine(datetime.datetime.now().date(
    ), datetime.datetime.strptime(timeHMS, "%H:%M:%S").time())

    if t < datetime.datetime.now():
        t = t + datetime.timedelta(days=1)
    return t


def findneartime(timelist: list) -> datetime:
    """
    返回列表中下一次最近时间对应的datetime对象
    """
    t = nexttime(timelist[0])
    for i in timelist:
        if nexttime(i) < t:
            t = nexttime(i)
    return t


class Log:
    def __init__(self, filename):
        """
        params: 日志文件名
        """
        self.filename = filename
        self.file = open(self.filename, "a")

    def open(self):
        self.file = open(self.filename, "a")

    def write(self, info):
        self.file.write(info)
        self.file.flush()
        return info

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


def logprint(string, *logs, Print=False):
    """
    向日志文件输出
    :params:
        ``string``: 日志条目
        ``logs``: 输出的log对象
    """
    for log in logs:
        log.write(timefull()+string+"\n")
    if Print or DEBUG:
        print(timefull()+string)  # [debug]


def errprint(string, *logs, close=True):
    """
    向日志文件输出错误
    :params:
        ``string``: 日志条目
        ``logs``: 输出的log对象
    """
    for log in logs:
        log.write(timefull()+"[ERR]"+string+"\n\n\n")
        del log

    print(timefull()+string)  # [debug]
    if close:
        input("按回车键退出...")
        sys.exit()


class Device:
    def __init__(self, adbaddress: str, deviceaddress: str, callback=None, emulator=False):
        """
        params:
            ``deviceaddress``: 设备名称或IP地址
            ``adbaddress``: adb.exe路径
            ``emulator``: 是否是模拟器
            ``callback``: 回调函数
        """
        self.deviceaddress: str = deviceaddress
        self.adbaddress: str = adbaddress
        self.callback = callback
        self.emulator = emulator

    def console(self, command: str):
        if self.callback:
            self.callback(self.deviceaddress + " adb: " + command)
        return console("{} -s {} {}".format(self.adbaddress, self.deviceaddress, command))

    def click(self, x, y, delay=0.5):
        self.console("shell input tap {} {}".format(x, y))
        sleep(delay)

    def clickText(self, text: str, delay=0.5, strong=False, retry=1):
        place = OCR_result(callback=self.callback).get(self).find(text, strong=strong, retry=retry)
        if place:
            self.console("shell input tap {} {}".format(place[0], place[1]))
            sleep(delay)
            return True
        else:
            return False

    def isawake(self) -> bool:
        """
        检测设备是否在屏幕上
        """
        return "mAwake=true" in self.console("shell dumpsys window policy")

    def keyevent(self, key):
        self.console("shell input keyevent {}".format(key))

    def back(self):
        self.keyevent(4)

    def home(self):
        self.keyevent(3)

    def power(self):
        if not self.emulator:
            self.keyevent(26)


class App:
    def __init__(self, packname: str, openactivity: str, device: Device):
        """
        params:
            ``packname``: 软件包名
            ``openactivity``: 启动包活动
            ``device``: ADB设备对象
        """
        self.packname: str = packname
        self.openactivity: str = openactivity
        self.device: Device = device

    def isinstalled(self) -> bool:
        return self.device.console("shell pm path {}".format(self.packname)) != ""

    def isrunning(self):
        return self.device.console("shell ps |findstr {}".format(self.packname)) != ""

    def isopen(self) -> bool:
        return self.packname in self.device.console("shell dumpsys activity top |findstr ACTIVITY")

    def open(self, delay=0) -> bool:
        if not self.isinstalled():
            raise Exception("open(): {}未安装".format(self.packname))
        if not self.isopen():
            self.device.console(
                "shell am start -n {}/{}".format(self.packname, self.openactivity))
            sleep(delay)
            return True
        else:
            return False

    def close(self, delay=0):
        if self.isopen():
            self.device.console(
                "shell am force-stop {}".format(self.packname))
            sleep(delay)

    def kill(self, delay=0):
        if self.isrunning():
            self.device.console("shell am kill {}".format(self.packname))
            sleep(delay)

    def restart(self, delay=10, rest=5):
        self.close(rest)
        return self.open(delay)


class OCR_result:
    def __init__(self, OCR: list = "", callback=None):
        self.OCR: list = OCR
        self.callback = callback

    def find(self, OCR: str, strong=False, retry=0) -> list:
        """
        定位OCR结果中某个字符串
            return:
            ``place``: 字符串位置: [x:int , y:int]
            ``Flase``: 没找到
        """
        for i in range(retry + 1):
            for a in self.OCR:
                if OCR in a[1][0]:
                    if strong and a[1][0] != OCR:
                        self.callback("OCR定位: "+OCR+" >存在，但由于强判断舍弃")
                        continue
                    place = [0, 0]
                    place[0] = (a[0][0][0]+a[0][2][0])/2
                    place[1] = (a[0][0][1]+a[0][2][1])/2
                    if self.callback:
                        self.callback("OCR定位: "+OCR+" >存在:"+str(place))
                    return place
            if i < retry:
                self.get(device)
            if self.callback:
                self.callback("OCR定位: "+OCR+" >不存在")
        return False

    def have(self, OCR: str, strong=False, retry=0) -> bool:
        """
        判断OCR结果是否有某个字符串
        """
        for i in range(retry + 1):
            for a in self.OCR:
                if OCR in a[1][0]:
                    if strong and a[1][0] != OCR:
                        self.callback("OCR判断: "+OCR+" >存在，但由于强判断舍弃")
                        continue
                    if self.callback:
                        self.callback("OCR判断: "+OCR+" >存在")
                    return True
            if i < retry:
                self.get(device)
            if self.callback:
                self.callback("OCR判断: "+OCR+" >不存在")
        return False

    def __str__(self) -> str:
        return str(self.OCR)

    def get(self, device: Device):
        """
        获取截图,并进行OCR
        return: OCR结果
        """
        if self.callback:
            self.callback("OCR获取.")
        device.console("shell screencap -p /sdcard/src.png")
        device.console("pull /sdcard/src.png {}".format(SRC_FILE))

        self.OCR = ocr.ocr(SRC_FILE, cls=False)
        return self


_Message = ""
"""全局变量,用于传递回调消息"""

if __name__ == "__main__":
    #########################初始化##########################
    if ACTTIME != []:
        natime = findneartime(ACTTIME)
    """
    next action time
    下次活动时间(datetime对象)
    """

    mainlog = Log(FILEPATH+"\\主日志.log")
    """主日志"""
    fulllog = Log(FILEPATH+"\\"+timeshort()+".log")
    """全局日志,记录回调消息,以日期命名"""

    @Asst.CallBackType
    def my_callback(msg, details, arg):
        m = Message(msg)
        d = json.loads(details.decode('utf-8'))
        global _Message
        _Message = str(m)
        logprint("{}{}{}\n".format(m, d, arg), fulllog)

    asst = Asst(dirname=ASSTPATH, callback=my_callback)

    logprint("\n\n===================================", mainlog, fulllog)
    logprint('asst version:'+asst.get_version(), mainlog, fulllog)
    if not os.path.exists(ASSTPATH + "\\platform-tools"):
        logprint("MeoAsst路径没有找到platform-tools文件夹，正在复制", Print=True)
        console("xcopy /e /k \"" + upper(ADBPATH)+"\\\" \"" + ASSTPATH + "\\platform-tools\\\"")
    c = console("{} connect {}".format(ADBPATH, DEVICEADDRESS))
    c = console("{} devices".format(ADBPATH))

    if c.count("device") <= 1:
        errprint("ADB连接失败", mainlog, fulllog)

    elif c.count("device") >= 3:
        print("\n多个设备已连接:")
        c = c.split("\n")
        n = 0
        il = []
        for i in c:
            i = i.split("\t")
            if len(i) > 1 and i[1] == "device":
                n += 1
                i = i[0]
                print("{}:{}".format(n, i), end=" ")
                if "emulator-" in i or "127.0.0.1" in i or "localhost" in i:
                    print("模拟器")
                else:
                    print("实体机")
                il.append(i)
        if DEVICEADDRESS in il:
            print("\n已连接配置文件:", DEVICEADDRESS, end=" ")
        else:
            print("输入序号选择设备")
            n = int(input(">>>"))
            DEVICEADDRESS = il[n-1]
            print("已选择设备:", DEVICEADDRESS, end=" ")
    else:
        print("\n设备已连接:", end=" ")
        DEVICEADDRESS = console("{} get-serialno".format(ADBPATH))
        print("{}".format(DEVICEADDRESS), end=" ")

    if "emulator-" in DEVICEADDRESS or "127.0.0.1" in DEVICEADDRESS or "localhost" in DEVICEADDRESS:
        print("模拟器")
        EMULATOR = True
    else:
        print("实体机")
        EMULATOR = False

    if asst.catch_custom(DEVICEADDRESS):
        logprint('设备连接成功:', mainlog, fulllog, Print=True)
    else:
        errprint('设备连接失败', mainlog, fulllog)

    device = Device(ADBPATH, DEVICEADDRESS,
                    callback=lambda x: logprint(x, fulllog), emulator=EMULATOR)
    ark = App("com.hypergryph.arknights", "com.u8.sdk.U8UnityContext", device)
    logprint(device.deviceaddress, mainlog, fulllog, Print=True)
    logprint("（模拟器）" if EMULATOR else "（实体机）", mainlog, fulllog, Print=True)
    result = OCR_result(callback=lambda x: logprint(x, fulllog))
    WeekAnnTimes = MAXWEEKANNTIMES if SKIPANNINSTART else 0
    """weak Annihilation 每周剿灭完成次数"""

    print("============初始化完成==============\n")
    if not DEBUG:
        if ACTTIME != []:
            print("下次活动时间：", natime)
            print("距下次活动还有", natime - datetime.datetime.now(), "时间")
        print("其余日志请查看日志文件")
        print("\n")
    #############################初始化完成###############################
    ##############################循环开始################################
    while True:

        if DEBUG and ACTTIME != []:
            print("[debug]等待中...")
            print("[debug]当前时间：", datetime.datetime.now())
            print("[debug]下次活动时间：", natime)
            print("[debug]距下次活动还有", natime - datetime.datetime.now(), "时间")
            print("\n")

        if datetime.datetime.now().minute == 0:
            mainlog = Log(FILEPATH+"\\主日志.log")
            fulllog = Log(FILEPATH+"\\"+timeshort()+".log")
            logprint("[debug]整点报时", fulllog)
            if datetime.datetime.now().hour == 0 and datetime.datetime.now().weekday() == 0:  # 周一凌晨重置剿灭
                WeekAnnTimes = 0
                logprint("每周剿灭已重置", mainlog, fulllog)
            mainlog.close()
            fulllog.close()

        if (ACTTIME == [] or datetime.datetime.now() > natime):  # 活动开始###########
            with open(CONFIGDIR, 'r') as f:  # 重新读取活动时间和任务列表
                configs: dict = json.load(f)
                ACTTIME = configs.get("ACTTIME")
                tasklist = configs.get("tasklist")

            if ACTTIME != []:
                natime = findneartime(ACTTIME)  # 设置下一次活动时间
                logprint("下次活动时间：" + str(natime), mainlog, fulllog, Print=True)

            mainlog = Log(FILEPATH+"\\主日志.log")
            fulllog = Log(FILEPATH+"\\"+timeshort()+".log")

            asst.stop()
            ark.close()

            for i in range(3):  # 网络测试
                j = console('ping {}'.format(PINGWEBSITE))
                logprint(j, fulllog)
                if j.find("100%") == -1:  # 这个-1不能改
                    break
                elif i == 2:
                    errprint("网络连接失败", mainlog, fulllog)

                sleep(5)
            logprint("网络测试通过", mainlog, fulllog)

            if result.get(device).OCR == []:  # 屏幕熄灭
                logprint("唤醒屏幕...", fulllog)
                device.power()
            ##############################################################
            ###########################处理剿灭############################
            if WeekAnnTimes < MAXWEEKANNTIMES:  # 剿灭 <<剿灭没有代理作战的处理

                logprint("剿灭开始", mainlog, fulllog)
                # 使用taptap云玩打剿灭 防止剿灭干扰"上次作战"判定
                taptap = App(
                    "com.taptap", "com.play.taptap.ui.SplashAct", device)
                taptap.restart(delay=60)

                if result.get(device).have("发现新版本"):  # 关闭taptap升级框
                    logprint("关闭taptap升级框...", mainlog, fulllog)
                    device.back()
                    sleep(5)

                count = 0
                while count <= 100 and (not (device.clickText("我的游戏", delay=4) and device.clickText("明日方舟", delay=4) and device.clickText("云玩", delay=2))):
                    sleep(1)
                    count += 1

                if result.get(device).have("升级客户端"):
                    # vvv不知道会不会有这个错误 先报错 等遇到了再处理
                    errprint("升级tap客户端", mainlog, fulllog)

                while result.get(device).have("排队"):
                    logprint("云玩排队...", fulllog)
                    sleep(5)

                sleep(30)
                if result.get(device).have("图像"):
                    errprint("云玩手动验证", mainlog, fulllog)
                else:
                    asst.append_startup()
                    asst.start()
                    while count <= 360:
                        count += 1
                        if _Message == "Message.AllTasksCompleted":
                            _Message = ""
                            break
                        if count >= 360:
                            errprint("Message捕获失败", mainlog, fulllog)
                        sleep(1)
                    # 等待唤醒 随后进入终端 如果有"关卡已开放" 以及今天不是周日 则跳过
                    device.clickText("终端", delay=4)
                    skip = (datetime.datetime.now().weekday() != 6) and result.get(device).have("关卡已开放")
                    if skip:
                        logprint("活动已开启 非周日跳过剿灭", mainlog, fulllog)
                    for i in range(0 if skip else MAXWEEKANNTIMES - WeekAnnTimes):
                        asst.append_fight("Annihilation", 0, 0, 1)
                        asst.start()
                        count = 0
                        while count <= 360:
                            count += 1
                            if _Message == "Message.AllTasksCompleted":
                                _Message = ""
                                break
                            if count >= 360:
                                errprint("Message捕获失败", mainlog, fulllog)
                            sleep(10)

                        if count <= 3:  # 小于30s 理智不足
                            logprint("剿灭理智不足", mainlog, fulllog)
                            break

                        elif count <= 30:  # 30s - 5分钟 本周剿灭完成    <<<<此处单纯靠时间而不是回调函数 软件逻辑更改可能会出问题
                            logprint("本周已剿灭完成", mainlog, fulllog)
                            WeekAnnTimes = MAXWEEKANNTIMES
                            break
                        else:
                            WeekAnnTimes += 1
                            logprint("剿灭完成{}次".format(i+1), mainlog, fulllog)
                device.back()
                sleep(1)
                device.clickText("退出云玩", delay=4, strong=True)
                taptap.close(delay=2)
                del taptap
            ##############################################################
            logprint("打开游戏窗口", fulllog)
            if not ark.restart(delay=20):
                logprint("[debug]窗口已经打开", fulllog)
            result.get(device)
            ##############################################################
            ########################处理版本更新###########################
            if result.have("已过时"):  # ark大版本更新
                logprint("开始更新...", mainlog, fulllog)
                device.click(ARKUPGRADE_COORD[0],
                             ARKUPGRADE_COORD[1], delay=10)  # 跳转taptap
                result.get(device)

                place = result.find("更新")  # taptap更新按钮
                if place:
                    logprint("taptap更新按钮...", mainlog, fulllog)
                    device.click(place[0], place[1])
                else:
                    errprint("未找到taptap更新按钮", mainlog, fulllog)

                count = 0
                while count <= 360:
                    if device.clickText("继续安装", delay=5):  # 系统安装按钮
                        logprint("系统安装按钮...", mainlog, fulllog)
                        break
                    sleep(10)
                    count += 1
                    if count >= 360:
                        errprint("更新失败", mainlog, fulllog)

                count = 0
                while count <= 360:
                    if device.clickText("打开", delay=10):  # 系统安装完成
                        logprint("安装完成", mainlog, fulllog)
                        break
                    if count >= 360:
                        errprint("更新失败", mainlog, fulllog)
            ##############################################################
            ########################处理闪断更新###########################
            count = 0
            while count < 360:

                if result.have("使用日文配音"):  # 选择配音
                    logprint("选择配音...", mainlog, fulllog)
                    place = result.find("使用日文配音")
                    device.click(place[0], place[1])
                    logprint("确认选项...", mainlog, fulllog)
                    place = result.find("确认")
                    device.click(place[0], place[1])

                elif result.have("确认"):  # 带确认按钮的选项框
                    logprint("确认选项...", mainlog, fulllog)
                    place = result.find("确认")
                    device.click(place[0], place[1])

                elif result.have("正在"):  # 等待加载
                    logprint("正在等待...", mainlog, fulllog)
                    count += 1
                    sleep(10)

                else:
                    break

                result.get(device)  # 判断结束后更新结果 节省算力
            ##############################################################
            #######################ASST主流程#############################
            count = 0
            while not result.get(device).have("终端"):  # 持续唤醒直到进入主界面，避免性能太差导致任务链出错
                device.clickText("开始唤醒", delay=20)  # 解决卡在开始唤醒界面的奇怪bug
                asst.append_startup()
                asst.start()
                while count <= 360:
                    count += 1
                    if _Message == "Message.AllTasksCompleted":
                        _Message = ""
                        logprint("唤醒...", mainlog, fulllog)
                        break
                    if count >= 360:
                        errprint("唤醒失败", mainlog, fulllog)
                    sleep(10)

            logprint("任务链开始执行.", mainlog, fulllog)
            rogmode = -1
            for t in tasklist:
                if t[0] == "fight":
                    asst.append_fight(t[1], t[2], t[3], t[4])  # 战斗
                elif t[0] == "infrast":
                    asst.append_infrast(t[1], t[2], t[3], t[4])  # 基建
                elif t[0] == "visit":
                    asst.append_visit()  # 好友
                elif t[0] == "award":
                    asst.append_award()  # 奖励
                elif t[0] == "recruit":
                    asst.append_recruit(t[1], t[2], t[3], t[4], t[5])  # 招募
                elif t[0] == "mall":
                    asst.append_mall(t[1])  # 信用购物
                elif t[0] == "roguelike":
                    rogmode = t[1]  # 肉鸽 <<肉鸽不会选择模式 请至少进入战斗一次

            asst.start()
            count = 400 if (len(tasklist) == 0 or tasklist[0][0] == "roguelike") else 0
            while count <= 360:
                count += 1
                if _Message == "Message.AllTasksCompleted":
                    _Message = ""
                    logprint("任务链结束\n\n", mainlog, fulllog)
                    break
                if count >= 360:
                    errprint("Message捕获失败", mainlog, fulllog)

                sleep(10)

            if rogmode != -1:
                logprint("开始肉鸽", mainlog, fulllog)
                asst.append_roguelike(rogmode)
                asst.start()

            if rogmode == -1 and device.emulator == False:
                ark.close()
                device.power()

            elif ACTTIME == []:
                if rogmode != -1:
                    print("单次肉鸽模式 无限运行")
                    while True:
                        sleep(10)
                else:
                    print("单次活动结束")
                    input("按回车键退出...")
                    sys.exit()

            mainlog.close()
            fulllog.close()
        sleep(60)
