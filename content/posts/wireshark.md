# Traffic Analysis

[Wireshark · Go Deep](https://www.wireshark.org/)
我选择网卡时报错说我没有设置混合模式(解决方法建议使用后者)：

```
The capture session could not be initiated on interface '\Device\NPF_Loopback' (Error opening adapter: The system cannot find the path specified. (3)).
```

管理员权限启动`cmd`并执行`net start npcap`，重新启动`Wireshark`问题解决。或者使用如下方法：

![image-20230317100348328](.\Data_Analyse\WiresharkSetting.png)

## BasicUsage

### 基本语法

过滤匹配表达式：

```shell
#过滤IP
ip.addr eq/== x.x.x.x #eq即equal 也是等于 ==和eq都可以 使用其一
ip.src eq/== x.x.x.x #只对源地址IP过滤
ip.dst eq/== x.x.x.x #只对目的地址IP过滤
#过滤端口 判断的==也可以换成">=", "<=", ">", "<"
tcp.port == 80 #过滤tcp协议的80端口
tcp.srcport == 80 #过滤源端口为tcp协议的80端口
tcp.dstport == 80 #过滤目的端口为tcp协议的80端口
#过滤协议
tcp #即只看tcp
http #只看http
...
!udp #加上'!'表示非 不查看udp协议 结果为udp协议以外的协议
#过滤指定字符
http.request.uri contains "shell.php" #在所有http协议的头信息中查找"shell.php"
http.request.uri matches "shell.php$" #matches过滤的字符串中可以使用正则表达
#http模式过滤
http contains "Host: 192.168.228.135" #在所有http协议的内容中寻找包含"Host: 192.168.228.135"的内容
tcp contains "Host: 192.168.228.135"
http.request.method == POST #寻找请求方式为post方法的http协议
```

`Ctrl + F`打开`WireShark`的内容搜索，可以直接查找协议中的字符串

### 协议分级

![image-20230317200203129](.\Data_Analyse\howtoUseWireshark01.png)

打开后如下图所示
![image-20230317200312905](.\Data_Analyse\howtoUseWireshark02.png)

### 文件导出

![image-20230318152713196](.\Data_Analyse\howtoUseWireshark03.png)

![image-20230318161845721](.\Data_Analyse\howtoUseWireshark04.png)

### 无线流量

遇到WIFI密码破解的流量包时可以直接使用Kali的工具进行破解

```shell
aircrack-ng -w /usr/share/wordlists/wfuzz/general/big.txt ctf.pcapng
```

通过字典爆破得到密码之后，点击`编辑`==>`首选项`

![image-20230318192313229](.\Data_Analyse\howtoUseWireshark05.png)

进入首选项找协议中的`IEEE 802.11`无线协议

![image-20230318192457450](.\Data_Analyse\howtoUseWireshark06.png)

添加该无线流量包的密码点击OK即可 点击视图中的重新加载就能查看该加密流量包(此处Key Type应为wpa-pwd)

![image-20230318193438375](C:\Users\SxyLao1\AppData\Roaming\Typora\typora-user-images\image-20230318193438375.png)

TLS协议的证书也可以通过该位置的选项导入对应整数打开加密的流量包

### SQL流量包

```bash
strings sqltest.pcapng | grep "ascii" > 1.txt #直接输出流量包中的信息到文本中
```

## BUUCTF

### 被嗅探的流量

[题目链接](https://buuoj.cn/challenges#%E8%A2%AB%E5%97%85%E6%8E%A2%E7%9A%84%E6%B5%81%E9%87%8F)
[流量包下载](https://files.buuoj.cn/files/ff965ff87437e3fda765ba928da94821/efa02e35-ee20-476f-94a2-cadbcef7d076.zip)
`Ctrl + F`直接在所有协议里面查找字符串`flag{`

![image-20230317110757104](.\Data_Analyse\BuuCTF_level0.png)

![image-20230317110933368](.\Data_Analyse\BuuCTF_level0_flag.png)

### 大流量分析(一)

附件链接: https://pan.baidu.com/s/1EgLI37y6m9btzwIWZYDL9g 提取码: 9jva **后面几道大流量分析都是这条链接的文件**

![image-20230317113250141](.\Data_Analyse\BuuCTF_level1_find.png)

![image-20230317113331888](.\Data_Analyse\BuuCTF_level1_ipStatistics.png)

如图该出现频率最高的IP地址中，唯一一个外网IP地址是非常可疑的，这个就是黑客的IP地址，`flag{183.129.152.140}`

### 大流量分析(二)

SMTP是一种提供可靠且有效的[电子邮件传输](https://baike.baidu.com/item/电子邮件传输/22035911?fromModule=lemma_inlink)的协议。SMTP是建立在FTP[文件传输服务](https://baike.baidu.com/item/文件传输服务/5389842?fromModule=lemma_inlink)上的一种邮件服务，主要用于系统之间的邮件信息传递，并提供有关来信的通知。SMTP独立于特定的传输子系统，且只需要可靠有序的数据流信道支持，SMTP的重要特性之一是其能跨越网络传输邮件，即“SMTP邮件中继”。使用SMTP，可实现相同网络处理进程之间的邮件传输，也可通过[中继器](https://baike.baidu.com/item/中继器/1867747?fromModule=lemma_inlink)或网关实现某处理进程与其他网络之间的邮件传输。

![image-20230317134118624](.\Data_Analyse\BuuCTF_level2_smtp.png)

既然题目涉及到了邮件，自然查找与电子邮件传输相关的协议，很简单就查到了相关的邮箱信息，flag{xsser@live.cn}

### 大流量分析(三) 

![image-20230317164817194](.\Data_Analyse\BuuCTF_admin_bak.png)

phpinfo是一个服务器的[运行指令](https://baike.baidu.com/item/运行指令/2919148?fromModule=lemma_inlink)，可以显示php服务器的配置信息。
后门程序是可运行的脚本`.php`，查找包含该信息的所有数据包，找不到就换下一个数据包继续查找后门程序，flag{admin.bak.php}

### 荷兰宽带数据泄露

解压得到.bin文件，为路由器文件。使用工具查看：https://1108dx.0098118.com/lc6/routerpassview186.zip
打开后寻找泄露的特别信息作为`flag`，flag{053700357621}

![image-20230317173822042](.\Data_Analyse\BuuCTF-RouterData.png)

### 数据包中的线索

到手发现文件并不大，直接找http过滤，发现一个很吸引人的文件名，右键追踪**HTTP**流。

![image-20230317193155176](.\Data_Analyse\BuuCTF_level3_Base64png.png)

追踪后发现一长串编码：

![image-20230317193406600](.\Data_Analyse\BUUCTF_level3_Base64flag.png)

结果有"="号很有可能是base64编码，将编码复制到浏览器作为png的base64编码打开：

```cmd
data:image/png;base64,这里跟编码
```

![image-20230317193623742](.\Data_Analyse\BUUCTF_level3_final_flag.png)

### 被劫持的神秘礼物

链接:https://pan.baidu.com/s/1pwVVpA5_WWY8Og6dhCcWRw 提取码: 31vk

直接过滤找HTTP，不多，追踪进去发现`name=admina&word=adminb`

![image-20230407094456655](.\Data_Analyse\被劫持的流量.png)

拼起来`adminaadminb`丢给[md5加密,sha1加密--md5在线解密 (cmd5.com)](https://www.cmd5.com/hash.aspx?s=123456)加密，取md5加密作为flag



## 杂七杂八

### 2018 铁人三项

链接：https://pan.baidu.com/s/1b6bkW-J8vKASr8C2r9vsdQ 提取码：nux4
[2018.5.18信息安全铁人三项赛数据赛复现_lemonl1的博客-CSDN博客](https://blog.csdn.net/qq_43431158/article/details/107258218?ops_request_misc=%7B%22request%5Fid%22%3A%22167918893816800226510658%22%2C%22scm%22%3A%2220140713.130102334.pc%5Fall.%22%7D&request_id=167918893816800226510658&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~pc_rank_34-4-107258218-null-null.142^v74^pc_new_rank,201^v4^add_ask,239^v2^insert_chatgpt&utm_term=2018CTF 铁人三项 数据流量分析&spm=1018.2226.3001.4187)

