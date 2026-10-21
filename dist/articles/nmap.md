# Nmap

Nmap是一款开源、免费的网络探测、安全审计的工具。

Nmap的获取，建议无论任何软件的获取，都是通过对应官网获取。
Nmap官网：https://nmap.org/

## Nmap列举远程机器开放的端口原理

首先判断nmap输入的命令行中是否包含域名，如果包含需要利用DNS服务器进行域名解析，然后发送ICMP Echo Request来探测主机存活性。

使用nmap scanme.nmap.org来列举该站，点的端口信息，以下给出zenamp下扫描结果，也可以是使用命令行下的nmap来探测。

nmap进行探测之前要把域名通过DNS服务器解析为IP地址，我们也可以使用指定的DNS服务器进行解析。使用--dns-servers数来指定。
nmap --dns-servers 8.8.8.8 scanme.nmap.org 使用google的dns域名解析

对于已经知道主机存活或者防火墙开启的机器，可以使用-Pn参数来停止探测之前的ICMP请求。以达到不触发防火墙安全机制进行突破。
nmap -Pn scanme.nmap.org

对于默认的端口范围，并不能满足日常工作需要。可以使用-p m-n来指定探测端口范围为m-n之间的所有端口。
nmap -p 1-1000 scanme.nmap.org

### 端口状态

-Open 表示端口处于开放状态；
-Closed 表示端口处于关闭状态；
-Filterd 表示端口处于过滤无法收到返回的probe状态；
-UnFilterd 表示端口收到返回的probe,但是无法确认；
-Opend/UnFilterd 表示端口处于开放或者是过滤状态；
-Closed/UnFilterd 表示端口处于关闭或者未过滤状态。

### Nmap扫描技术查看

在命令行中，输入nmap -h来查看nmap自带的帮助信息。

## 识别目标机器上的服务指纹

### 服务指纹

为了确保有一个成功的渗透测试或网络设备监控，必须需要知道目标系统中服务的指纹信息。服务指纹信息包括服务端口、服务名和版本等。
通过分析目标往Nmap发送的数据包中某些议标记、选项和数据，我们可以推断发送这些数据包的操作系统等。
nmap通过向目标主机发送多个UDP与TCP数据包并分析其响应来进行操作系统指纹识别工作。

### Nmap识别服务指纹

使用命令 nmap -sV IP地址 来识别目标机器的服务信息。

### Nmap侵略性的探测

使用命令 nmap -A -V -T4 IP地址 来探测目标机器的操作系统、服务等信息。

使用 nmap -sC -sV -O IP地址 来探测目标机器的操作系统、服务等信息。
其中sC参数表示使用Nmap脚本进行探测，sV表示探测目标机器上的服务信息，O表示探测目标机器的操作系统信息。-sC:equivalent to   --script=default

## Nmap发现局域网中存活主机

### 主机发现

一个局域网中肯定是连接着多台设备，那么我们如何获取哪些设备正在开机状态呢？
使用 ping ip地址 进行探测，但是如果一个网络很大的情况下，这样的手工探测显得很费劲。

可以使用不同的工具来进行批量探测，在探测之前需要明白CIDR的含义。
CIDR CIDR(无类别域间路由，Classless Inter-Domain Routing),可以快速表示一个网络。
比如：172.16.1.1/24表示在172.168.1.1-172.168.1.255之间的所有主机IP地址

使用Nmap命令：nmap -sP CIDR对该网络中所有主机进行ping扫描，以探测主机存活性。扫描过程中使用了TCP SYN扫描、ICMP echo Request:来探测主机存活。

使用Nmap命令：nmap -sn CIDR 对该网络中所有主机进行ping扫描，以探测主机存活性。

### Nmap结果输出

使用Nmap命令：nmap -sn CIDR -ox test.xml 对该网络中所有主机进行ping扫描，以探测主机存活性。同时将结果输出到test.xml文件中，以便后续使用。

## Nmap端口探测技巧

在实际环境中，当系统管理员对设备进行管理时，或者渗透测试人员对设备进行检测时，并不一定对所有的服务进行操作。极有可能是对某个或某个范围内的服务进行检测。

如果对所有服务进行探测，那么就会出现耗时长，费力不讨好的情况。针对这样的情况，我们很有必要了解如何使用Nmap来更加灵活的进行服务探测，避免全端口探测对服务器造成压力。

对某个端口进行探测 nmap -p80 scanme.nmap.org
对某几个端口进行探测 nmap -p80, 135 scanme.nmap.org
对某个范围端口进行探测 nmap -p 1-100 scanme.nmap.org
对所有端口进行探测 nmap -p- scanme.nmap.org
指定协议探测端口 nmap -p T:25, U:53 scanme.nmap.org #T:25表示TCP的25端口 U:53表示UDP的53端口
通过名称范围扫描 nmap -p s* scanme.nmap.org
扫描注册在nmap中的端口 nmap -p [1-65535] scanme.nmap.org

## Nmap NSE脚本使用

### NSE介绍

NSE(Nmap Script Engine)Nmap脚本引擎，内置很多可以用来扫描的、针对特定任务的脚本。通过NSE可以不断拓展Nmap的扫描策略，加强Nmap的功能。

Nmap中使用--script参数来指定调用的脚本，Windows脚本存储在Nmap安装路径下的script文件夹下，对于kali Linux存在/usr/share/nmap/script/下。

### NSE使用

使用Nmap探测Web服务的title信息。nmap --script 脚本名称 目标
nmap --script http-title scanme.nmap.org

以上通过Nmap使用http-title脚本进行探测，还可以使用其他脚本进行探测。目前为止可以用的有589个脚本，每个脚本都有其独特的作用。

使用Nmap探测http服务的http头。nmap --script http-headers 目标
nmap --script http-headers 192.168.1.100

### NES分类使用

对于目标使用多个分类脚本进行探测，可以更快的找到目标的信息与弱点。

使用Nmap中漏洞分类脚本对目标进行探测，使用命令如下：
nmap -sV --script vuln 目标

使用Nmap中http\*的脚本，但是除了(http-brute和http-slowlors),使用命令如下:
nmap -sV --script "(http*) and not(http-slowlors and http-brute)” 目标

### NES调试功能使用

使用Nmap中exploit,但是在使用的同时开启调试模式。使用命令如下：
nmap -sV --script exploit -d 3 --script-trace 目标 
注意：-d(debug范围0~9)

使用nmap的http-title脚本，并且指定使用对应的User-Agent。命令如下：
nmap -sV --script http-title --script-args http.useragent="Mozilla 999" 目标

### NSE更新

nmap --script-updatedb

### NSE脚本分类

auth
broadcast
brute
default
 sc
discovery
dos
exploit
external
fuzzer
intrusive
malware
safe
version
vuln

脚本分类手册 https://nmap.org/nsedoc/

## Nmap指定特定网卡进行探测

Nmap是一款可拓展性强的工具，并且有些NSE脚本支持嗅探。但是这种功能需要网卡支持混杂模式才可以。或者当计算机上有两张网卡，并且两张网卡对应的不同网络。

NMap中提供了切换使用特定网卡进行探测的参数 -e

### 指定网卡进行探测

使用Nmap命令行：nmap -e interface CIDR
nmap -e etho 192.168.1.1/24

如果一台主机有很多块网卡且配置有不同的网络环境 扫描时会造成超时现象影响扫描效率
Windows环境下使用nmap需要改成nmap.exe 加上 --iflist 列出所有的网卡以及详细信息

nmap.exe --iflist
或者
ipconfig /all

根据网卡的详细信息决定指定哪一张网卡进行探测



## Nmap对比扫描结果ndiff

对某个网路进行探测的时候，有可能之前有探测过的结果，现在探测过后，需要对之前的结果与现在的结果来对比，找到两次不同点。

监视网络变化，达到网络监控的目的。

### 工具ndi介绍

在Nmap整个工程中，除了主要的nmap工具之外，还包括很多其他工具。如接下来要使用到的ndiff工具。

在Windows的Nmap目录下的命令行中，输入ndiff -h来查看ndiff自带的帮助信息。

### 比较Nmap两次扫描结果

使用命令：ndiff File1 File2 (Fi1e1和Fi1e2是Nmap扫描结果的xml格式。-oX)

## 可视化Nmap(Zenmap)的使用

Nmap命令参数复杂，组合类型多种多样，如果使用命令行类型的Nmap需要记忆大量命令，对于网络管理最和渗透测试者都是一项艰巨的任务。但是如果使用可视化Nmap(Zenmap)，那么就不存在这样的问题。

在安装Nmap的同时，会自动安装可视化Nmap(Zenmap),可以在安装目录中找到。

### Zenmap的使用

#### 配置扫描策略

进入配置选择自己需要的脚本点击保存即可