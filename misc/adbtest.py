from os import popen
from os import path

adb = ".\\platform-tools\\adb.exe"
def console(command: str) -> str:
    try:
        return popen(adb+" "+command).read().strip()
    except:
        r = popen(adb + " " + command)
        r = r.buffer.read().decode("utf-8").strip()
        return r



if not path.exists(adb):
    print("{}未找到".format(adb))
    print("请确认本软件和platform-tools文件夹在同一目录")
    input("按回车键退出...")
    exit()
while True:
    c = console("devices")
    print(c)
    if c.count("device") <= 1:
        print("手机\模拟器未连接，请检查相关设置")
        print("手动连接--输入设备名 输入空行退出：")
        inp = input(">>>")
        if  inp != "":
            console("connect {}".format(inp))
            continue
        else:
            exit()
    elif c.count("device") >= 3:
        print("\n多个设备已连接:")
    else:
        print("\n设备已连接:")

    c = c.split("\n")
    for i in c:
        i=i.split("\t")
        if len(i)>1 and i[1] == "device":
            i = i[0]
            print(i, end=" ")
            if "emulator-" in i or "127.0.0.1" in i:
                print("模拟器")
            else:
                print("实体机")
    #print("设备名称：", console("get-serialno"))
    input("按回车键退出...")
    exit()