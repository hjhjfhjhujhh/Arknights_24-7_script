# 基于MaaAssistantArknights的明日方舟全天候挂机脚本
![GitHub](https://img.shields.io/github/license/hjhjfhjhujhh/hjhjfhj-s_test) 
![GitHub](https://img.shields.io/badge/platform-Windows-brightgreen)
![GitHub](https://img.shields.io/badge/code-Python-blue)

## 说明
**本软件还处于极早期测试阶段 出现bug请及时反馈**  
我自用的挂机脚本，基于[MaaAssistantArknights](https://github.com/MaaAssistantArknights/MaaAssistantArknights)的py接口  
虽然我py水平不怎么样，但是功能越写越多，就决定不如发布出来  
功能包括：
- 全自动操作，插上手机/模拟器就可以完全AFK
- 每日在指定（复数）时间点执行指定任务链————支持所有[MaaAssistantArknights支持的任务！](https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/master/README.md)
- - 包括刷理智、基建换班、访问好友、领取日常奖励、自动公招、领取信用、信用购物
- - 支持无限刷肉鸽，逻辑是在任务链其他任务执行完毕后开始刷，直到下次任务链开始自动停止
- 每周自动安排剿灭————开启活动的情况下，在活动结束或者周日到来前不打剿灭，避免影响活动代币获取
- - 使用taptap云玩打每周剿灭，防止剿灭干扰“上次作战”判定
- - 使用云玩需要你拥有成年实名taptap账号，否则请在设置文件里关闭此功能，自行解决每周剿灭
- - 这会**消耗你的云玩时长**，建议使用闲置账号
- 自动解决闪断更新
- 自动安装大版本更新 **（！未实验！）**

## 注意事项（Releases版）
- 建议体验过[MaaAssistantArknights](https://github.com/MaaAssistantArknights/MaaAssistantArknights)后再使用本软件，搞清软件能做到的基本功能
- 为一些低配机型考虑，本软件在某些动作后可能会有很大（1分钟以上）的停顿，此为正常现象，只要软件不报错就请视作正常运行
- 打包后软件体积有点大，解压后会占用将近1个G的空间。这是我用pyinstaller把各种库都拉进来的结果，如果有谁能帮助我缩减文件体积，在此感激不尽
- 本软件理论上支持多设备，不过对每个设备你都要复制一份软件，然后在配置文件里写入对应设备名
- **taptap云玩有时会出现图形验证码**，目前本人没摸清验证码出现规律。出现此问题会跳过云玩，手动上线一次云玩可暂时解决
- - 计划使用opencv解决验证码问题（咕咕咕）
- 如果选择每日打特定**资源收集**可能会出现当日不开放的情况，可以在任务后面追加一个上次作战
- 各种功能都**未在B服测试**

## 使用教程（Releases版）
- 需要一个手机/模拟器,安装有**taptap**和**从taptap软件内下载的明日方舟**
- 模拟器强烈建议使用**蓝叠**，使用其他模拟器可能会出现问题
- - *不安装taptap也能使用本软件基础功能。在大版本更新时可能出现问题*
- - *如果没有安装taptap，请在配置文件内关闭剿灭*
- [下载压缩包](https://github.com/hjhjfhjhujhh/Arknights_24-7_script/releases)并解压（最好路径上不要有中文和空格），内容如图：  
![image](https://user-images.githubusercontent.com/89215821/162499773-ac5701b9-94f2-414a-8d53-465f192f1750.png)
- 从上到下三个文件夹依次为  主程序  MAA程序  ADB工具
- - *如果MAA版本过低，可以直接替换新的文件夹，名字开头一定要为"MeoAssistantArknights"*
- 插上你的手机/模拟器，运行**adbtest.exe**，如果一切正常就会显示"设备已连接"，可以进行下一步
- - *否则，参照[这个文档](https://github.com/hjhjfhjhujhh/Arknights_24-7_script/blob/main/docs/%E8%AE%BE%E5%A4%87%E8%BF%9E%E6%8E%A5.md)*
- 打开**配置文件编辑器**，按照提示编辑[配置文件](https://github.com/hjhjfhjhujhh/Arknights_24-7_script/blob/main/docs/%E5%85%B3%E4%BA%8E%E8%AE%BE%E7%BD%AE%E6%96%87%E4%BB%B6.md)，成功后当前目录会出现config.json
- - *不打开编辑器直接启动程序，会自动生成默认配置文件*
- 启动**start.bat**
- - ~~祈祷不要出现报错~~

## BUG反馈
- 请在issue内详细描述问题，并提交发生bug时设备的截图、软件的两个日志、MAA文件夹中的asst.log
- *软件的两个日志：在根目录内名为"主日志.log"的日志，以及最近的以"\[日期\].log"命名的日志*

## 开发相关
- 本软件代码全部在auto.py内, interface.py和message.py是MAA的接口文件。其中interface较官方提供版本略有修改，参见[此issue](https://github.com/MaaAssistantArknights/MaaAssistantArknights/issues/312)
- 在每次执行任务链时，程序会重新读取配置文件中的执行时间表和任务列表。如果你有每天执行不同任务的需要，可以用第三方程序修改配置文件
- 在配置文件中手动加入  **"DEBUG":true,**  可以在控制台窗口中输出日志

## 鸣谢
- 开源库：[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- **核心软件**：[MaaAssistantArknights](https://github.com/MaaAssistantArknights/MaaAssistantArknights)
- 以及制作了软件的[MistEO](https://github.com/MistEO)
