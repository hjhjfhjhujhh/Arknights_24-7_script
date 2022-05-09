import json
import os
CONFIGDIR = "config.json"
configs: dict = dict()
if os.path.exists(CONFIGDIR):
    try:
        with open(CONFIGDIR, 'r') as f:
            configs: dict = json.load(f)
            print("配置文件加载成功")
    except json.decoder.JSONDecodeError:
        try:
            string = "{}已存在并且读取失败 ".format(os.path.split(CONFIGDIR)[1])
            os.rename(CONFIGDIR, CONFIGDIR+".bak")
        except:
            string += "请手动删除文件后重试"
            print(string, close=True)
            input("按回车键退出...")
        string += "已为您备份为{}并重新创建{}".format(os.path.split(CONFIGDIR)[1]+".bak", os.path.split(CONFIGDIR)[1])
        print(string)

else:
    print("{}不存在，将自动创建".format(CONFIGDIR))
print("配置文件保存在{}".format(os.getcwd()))

ACTTIME = configs.get("ACTTIME", ["2:00:00", "9:00:00", "17:00:00"])
"""每日执行脚本的时间,默认2点、9点、17点"""
"""如果为空则单次运行"""

MAXWEEKANNTIMES = configs.get("MAXWEEKANNTIMES", 6)
"""每周剿灭打满次数 默认为6"""

SKIPANNINSTART = False
"""在开启软件的本周跳过剿灭"""

ARKUPGRADE_COORD = configs.get("ARKUPGRADE_COORD", [950, 730])
"""大版本过低提示框的确认键位置,用来跳转其他应用. 1080P 16:9的手机大概是这个坐标"""

PINGWEBSITE = configs.get("PINGWEBSITE", "www.baidu.com")
"""用于ping网络测试的网站"""

DEVICEADDRESS = configs.get("DEVICEADDRESS", ["127.0.0.1:5555"])
"""你的设备地址/名称(可选).如果有报错请编辑此处"""
EMULATOR = configs.get("EMULATOR", [False,False])
"""设备是否是模拟器.[False,False]"""
COULDPLAY = configs.get("COULDPLAY", [False,True])
"""日常/剿灭是否使用云玩 默认为[False,True]"""


ADBPATH = configs.get("ADBPATH", "")
"""你的adb.exe路径.请保持留空以自动配置"""

ASSTPATH = configs.get("ASSTPATH", "")
"""自动化脚本的路径. 留空以自动配置"""

SRC_FILE = configs.get("SRC_FILE", "")
"""截屏文件位置,用于OCR. 除非出现问题,请保持留空以自动配置"""

tasklist = configs.get("tasklist", [
    ['fight', 'LastBattle', 0, 0, 999],
    ['infrast', 1, ['Mfg', 'Trade', 'Control', 'Power', 'Reception', 'Office', 'Dorm'],"Money",0.3],
    ['visit'],
    ['mall', True],
    ['award'],
    ['recruit', 4, [4, 5, 6], [3, 4, 5, 6], True, False]])
"""任务列表 请参考interface.py"""

print("缺省设置已写入.\n")
status = 0
while status <= 10:
    try:
        if status == 0:
            print("正在编辑每日执行脚本的时间")
            print("当前为：{}".format(ACTTIME))
            print("请输入一条执行时间，格式为 时:分:秒，例如8:00:00")
            print("请注意使用英文符号")
            print("如果此项为空，则单次运行脚本.输入emp设置此项为空")
            print("输入空行跳过并保持当前设置")
            inp = input(">>>")
            if inp != "":
                ACTTIME = []
                ACTTIME.append(inp)
            if inp == "emp":
                ACTTIME = []
                inp = ""
            while inp != "":
                print("当前为：{}".format(ACTTIME))
                print("请输入下一条执行时间，格式为[时:分:秒]，例如8:00:00")
                print("输入的时间条目不必排序. 请注意使用英文符号")
                print("输入空行退出，输入r删除上一条")
                inp = input(">>>")
                if inp == "r":
                    ACTTIME.pop()
                    continue
                ACTTIME.append(inp)
            status += 1

        elif status == 1:
            print("正在编辑每周剿灭打满次数")
            print("当前为：{}".format(MAXWEEKANNTIMES))
            print("请输入当前最新剿灭，你的代理记录几次能够打满1800玉，默认为6")
            print("手动剿灭请填0")
            print("输入空行跳过并保持当前设置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r": 
                status -= 1
                continue
            if inp != "":
                MAXWEEKANNTIMES = int(inp)
            status += 1

        elif status == 2:
            print("正在编辑启动软件的当周是否跳过剿灭")
            print("当前为：{}".format(SKIPANNINSTART))
            print("请输入True或False，默认为False")
            print("输入空行跳过并保持当前设置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue
            if inp != "":
                if inp == "True":
                    SKIPANNINSTART = True
                elif inp == "False":
                    SKIPANNINSTART = False
                else:
                    print("输入错误！")
                    continue
            status += 1

        elif status == 3:
            print("正在编辑大版本过低提示框的确认键位置")
            print("当前为：{}".format(ARKUPGRADE_COORD))
            print("本软件使用此按钮跳转其他应用。")
            print("1080P 16:9的手机大概是[950, 730]")
            print("请输入第一个坐标(数字)，例如950")
            print("输入空行跳过并保持当前设置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue
            if inp != "":
                ARKUPGRADE_COORD[0] = int(inp)
                print("请输入第二个坐标(数字)，例如730")
                inp = input(">>>")
                ARKUPGRADE_COORD[1] = int(inp)
            status += 1

        elif status == 4:
            print("正在编辑用于ping网络测试的网站")
            print("当前为：{}".format(PINGWEBSITE))
            print("请输入网站地址，例如www.baidu.com")
            print("输入空行跳过并保持当前设置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue
            if inp != "":
                PINGWEBSITE = inp
            status += 1

        elif status == 5:
            print("正在编辑设备地址/名称，如果只有一个实体机可以忽略此项")
            print("如果有多设备，请先填写用来执行日常任务的设备")
            print("当前为：{}".format(DEVICEADDRESS))
            print("请注意使用英文符号")
            print("输入空行跳过并保持当前设置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue
            
            if inp != "":
                DEVICEADDRESS = []
                DEVICEADDRESS.append(inp)

            print("是否在此设备使用云玩打日常任务？")
            print("True或False，默认为False")
            print("输入空行跳过并保持当前设置")
            inp = input(">>>")
            if inp == "True":
                COULDPLAY[0] = True
            else:
                print("已设置为False")
                COULDPLAY[0] = False

            print("请填写用来执行每周剿灭的设备")
            print("输入空行与上一项相同")
            inp = input(">>>")
            if inp != "":
                DEVICEADDRESS.append(inp)
                
                print("是否在此设备使用云玩打每周剿灭？")
                print("True或False，默认为False")
                print("输入空行跳过并保持当前设置")
                inp = input(">>>")
                if inp == "True":
                    COULDPLAY[-1] = True
                else:
                    print("已设置为False")
                    COULDPLAY[-1] = False
            else:
                print("在此设备上使用云玩打剿灭已被自动设为"+str(not COULDPLAY[0]))
                COULDPLAY[-1] = not COULDPLAY[0]

            status += 1

        elif status == 6:
            status += 1  # 跳过模拟器编辑
            continue
            print("正在编辑设备是否是模拟器")
            print("当前为：{}".format(EMULATOR))
            print("请输入True或False，默认为False")
            print("输入空行跳过并保持当前设置")
            inp = input(">>>")
            if inp != "":
                if inp == "True":
                    EMULATOR = True
                elif inp == "False":
                    EMULATOR = False
                else:
                    print("输入错误！")
                    continue
            status += 1

        elif status == 7:
            print("正在编辑adb路径")
            print("当前为：{}".format(ADBPATH))
            print("指定adb工具的路径，末尾是adb.exe")
            print("输入空行跳过并保持当前设置")
            print("建议保持留空，由软件自动搜寻上级文件夹")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 2  # 跳过模拟器编辑
                continue
            if inp != "":
                ADBPATH = inp
            status += 1

        elif status == 8:
            print("正在编辑自动化脚本的路径")
            print("当前为：{}".format(ASSTPATH))
            print("可以指定自动化脚本文件夹的路径")
            print("输入空行跳过并保持当前设置")
            print("建议保持留空，由软件自动搜寻上级文件夹")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue
            if inp != "":
                ASSTPATH = inp
            status += 1

        elif status == 9:
            print("正在编辑截屏文件的路径")
            print("当前为：{}".format(SRC_FILE))
            print("可以指定截屏所在文件夹的路径")
            print("输入空行跳过并保持当前设置")
            print("除非出现问题,请保持留空以自动配置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue
            if inp != "":
                SRC_FILE = inp
            status += 1

        elif status == 10:
            print("正在编辑任务列表")
            print("当前为：")
            for t in tasklist:
                print(t)
            print("输入要执行的第一条任务对应数字：")
            print("1:刷理智 2:基建换班 3:访问好友 4:领取日常奖励")
            print("5:公开招募 6:领取信用及购物 7:无限肉鸽")
            print("输入空行跳过并保持当前设置")
            print("输入r返回上一条")
            inp = input(">>>")
            if inp == "r":
                status -= 1
                continue

            if inp != "":
                tasklist = []
            while inp != "":
                t = []

                if inp == "1":
                    t.append("fight")
                    print("选择每日要刷的关卡")
                    print("1:上次作战  2:CE-5  3:AP-5  4:LS-5  5:CA-5")
                    i = input(">>>")
                    if i == "1":
                        t.append("LastBattle")
                    elif i == "2":
                        t.append("CE-5")
                    elif i == "3":
                        t.append("AP-5")
                    elif i == "4":
                        t.append("LS-5")
                    elif i == "5":
                        t.append("CA-5")
                    else:
                        print("输入错误！")
                        continue
                    print("输入最多吃多少理智药 建议为0")
                    t.append(int(input(">>>")))

                    print("输入最多吃多少源石 建议为0")
                    t.append(int(input(">>>")))

                    print("输入最多刷多少次 建议为999")
                    t.append(int(input(">>>")))
                    print("设置成功:", t)
                    tasklist.append(t)

                elif inp == "2":
                    t.append("infrast")
                    t.append(1)
                    print("按顺序输入换班房间：")
                    inflist = {"制造站": "Mfg", "贸易站": "Trade", "控制中枢": "Control",
                               "发电站": "Power", "会客室": "Reception", "办公室": "Office", "宿舍": "Dorm"}
                    infnum = ["制造站", "贸易站", "控制中枢", "发电站", "会客室", "办公室", "宿舍"]
                    i = " "
                    tt = []
                    while i != "":
                        if len(infnum) == 0:
                            break
                        print("当前剩余的房间：")
                        for p in range(len(infnum)):
                            print(p, ":", infnum[p], end="  ")
                        print("")
                        print("输入空行结束")
                        i = input(">>>")
                        if i != "":
                            i = int(i)
                            if i <= len(infnum):
                                tt.append(inflist[infnum[i]])
                                del infnum[i]
                            else:
                                print("输入错误！")
                                continue
                    if len(infnum) > 0 and infnum[-1] == "宿舍":
                        print("！！您没有安排宿舍换班，这可能会导致异常")
                    i==""
                    t.append(tt)
                    while i == "":
                        print("输入基建无人机加速用途：")
                        print("1:闲置  2:贸易站龙门币  3:贸易站合成玉  4:制造站作战记录  5:制造站赤金  6:制造站原石碎片  7:制造站芯片")
                        i = int(input(">>>"))
                        if i == 1:
                            t.append("_NotUse")
                        elif i == 2:
                            t.append("Money")
                        elif i == 3:
                            t.append("SyntheticJade")
                        elif i == 4:
                            t.append("CombatRecord")
                        elif i == 5:
                            t.append("PureGold")
                        elif i == 6:
                            t.append("OriginStone")
                        elif i == 7:
                            t.append("Chip")
                        else:
                            print("输入错误！")
                            i = ""
                            continue
                    print("输入宿舍入住心情阈值 0.00~1.00 默认为0.30")
                    t.append(round(float(input(">>>")), 2))
                    tasklist.append(t)

                elif inp == "3":
                    tasklist.append(["visit"])

                elif inp == "4":
                    tasklist.append(["award"])

                elif inp == "5":
                    t.append("recruit")
                    print("输入招募次数(建议为4):")
                    t.append(int(input(">>> ")))
                    print("输入自动选中的tag级别(3-6)，用英文逗号隔开:")
                    print("示例: 4,5,6     >如果出现4,5,6星tag，会自动选中")
                    inp = input(">>> ").split(",")
                    for n in range(len(inp)):
                        inp[n] = int(inp[n])
                    t.append(inp)
                    print("输入确认招募的tag级别(3-6)，用英文逗号隔开:")
                    print("示例: 3,4,5,6   >如果出现3,4,5,6星tag，会确认招募")
                    print("此配置的用处是，如果不写6，那么出现六星tag就会跳过当前栏位，等待手动处理")
                    inp = input(">>> ").split(",")
                    for n in range(len(inp)):
                        inp[n] = int(inp[n])
                    t.append(inp)
                    print("输入是否刷新3级tag(True 或 False):")
                    inp = input(">>> ")
                    if inp == "True":
                        t.append(True)
                    elif inp == "False":
                        t.append(False)
                    else:
                        raise ValueError("输入错误")
                    print("输入是否使用加急许可(True 或 False):")
                    inp = input(">>> ")
                    if inp == "True":
                        t.append(True)
                    elif inp == "False":
                        t.append(False)
                    else:
                        raise ValueError("输入错误")

                    tasklist.append(t)
                    #tasklist.append(["recruit", 4, [4, 5, 6], [3, 4, 5, 6], True, False])

                elif inp == "6":
                    t.append("mall")
                    print("输入领取信用后是否购物(True 或 False)")
                    print("购物规则请更改MeoAsst的配置文件")
                    i = input(">>>")
                    if i == "True":
                        t.append(True)
                    elif i == "False":
                        t.append(False)
                    else:
                        print("输入错误！")
                        continue
                    tasklist.append(t)

                elif inp == "7":
                    t.append("roguelike")
                    print("输入肉鸽模式：")
                    print("0:尽可能一直往后打  1:第一层投资完源石锭就退出\n2:投资过后再退出，没有投资就继续往后打")
                    t.append(int(input(">>>")))
                    tasklist.append(t)
                    print("因为肉鸽无限执行，后续添加任务已被跳过")
                    break

                elif inp == "r":
                    tasklist.pop()

                else:
                    print("输入错误！")

                print("当前任务列表为：", "空" if len(tasklist) == 0 else "")
                for t in tasklist:
                    print(t)

                print("输入下一条任务，输入空行退出，输入r删除上一条")
                print("1:刷理智 2:基建换班 3:访问好友 4:领取日常奖励")
                print("5:公开招募 6:领取信用及购物 7:无限肉鸽")
                inp = input(">>>")
            status += 1

            print("最终任务列表为：")
            for t in tasklist:
                print(t)

        else:
            print("内部错误")
            break
    except:
        print("捕捉到错误，请重新输入")

print("配置文件生成完毕")
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
configs["COULDPLAY"] = COULDPLAY
print(configs)
with open(CONFIGDIR, 'w') as f:
    json.dump(configs, f, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    #json.dump(configs, f)

input("按回车键退出...")
