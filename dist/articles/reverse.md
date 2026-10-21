# Reverse

## Basic

### PE加壳脱壳

PE文件：portable executable（可移植的可执行文件），主要在Windows系统中，包括exe/dll/sys文件。
加壳：是利用特殊的算法，对EXE、DLL文件里的资源进行压缩、加密。类似WINZIP 的效果，只不过这个压缩之后的文件，可以独立运行，解压过程完全隐蔽，都在内存中完成。它们附加在原程序上通过Windows加载器载入内存后，先于原始 程序执行，得到控制权，执行过程中对原始程序进行解密、还原，还原完成后再把控制权交还给原始程序，执行原来的代码部分。加上外壳后，原始程序代码在磁盘 文件中一般是以加密后的形式存在的，只在执行时在内存中还原，这样就可以比较有效地防止破解者对程序文件的非法修改，同时也可以防止程序被静态反编译。

## Tools

### [ALL](https://github.com/BlackINT3/OpenArk/releases)

OpenArk64 逆向工具包

### [UPX](https://objects.githubusercontent.com/github-production-release-asset-2e65be/67031040/203032b6-383a-410d-bf91-ee8528a96447?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230401%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230401T012327Z&X-Amz-Expires=300&X-Amz-Signature=8f03ddc2e265b25ed3445eaef324253ccd57b2112ad29eb2303b3a0b13aa1277&X-Amz-SignedHeaders=host&actor_id=112177376&key_id=0&repo_id=67031040&response-content-disposition=attachment%3B%20filename%3Dupx-4.0.2-win64.zip&response-content-type=application%2Foctet-stream)

```cmd
#配置环境变量后在命令行使用
upx [PE] #加壳
upx -d [PE] #脱壳
upx -o 别名.exe -d 现名.exe
upx -l [PE] #加壳列出其信息
upx -t [PE] #测试压缩过的可执行文件
upx -V #查看版本
upx -L #软件许可声明
```

### [PEID](https://softpedia-secure-download.com/dl/69ac1ba7dcf9a0dd16b047907e974bd5/642783ab/100004102/software/programming/PEiD-0.95-20081103.zip)

### [jd-gui](https://objects.githubusercontent.com/github-production-release-asset-2e65be/32844456/012e1e80-272e-11ea-9941-5a32c9f59220?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230401%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230401T080343Z&X-Amz-Expires=300&X-Amz-Signature=b9dd512b0766225c648ad551e99a4cf42565453c43c0ccec97ef4cb3d7bfa2c4&X-Amz-SignedHeaders=host&actor_id=112177376&key_id=0&repo_id=32844456&response-content-disposition=attachment%3B%20filename%3Djd-gui-1.6.6.jar&response-content-type=application%2Foctet-stream)

### [OllyICE](https://sm.myapp.com/original/Development/OllyICEv2.zip)

### [jadx-gui](https://github.com/skylot/jadx/releases/download/v1.4.6/jadx-1.4.6.zip)

### [UPXShell](https://jaist.dl.sourceforge.net/project/upxshell/upxshell-beta/UPXshell%20v3.4.2.2007/UPXShell-3.4.2.2007-Setup.exe)

### [ExeinfoPE](https://softpedia-secure-download.com/dl/b15161150a6f1578794dc6a5b9ff3f4d/6426db95/100038188/software/programming/exeinfope.zip) 

### [Reshacker](http://angusj.com/resourcehacker/reshacker_setup.exe)

### [AndroidKiiler](https://codeload.github.com/liaojack8/AndroidKiller/zip/refs/heads/master)

## BuuCTF

[j311y的逆向日记的个人空间\_哔哩哔哩\_bilibili](https://space.bilibili.com/509688938/video)

### easyre

winhex打开搜索flag拿下

### reverse1

丢进ExeinfoPE得到` x64 Microsoft Visual C++ v.14.00 - 2015 - ExE Debug ( jmp/jmp/jmp/int3 ) - microsoft.com [ Win Vista ]`
得知该文件为64位程序后丢给`IDA64`，Shift+F12查看字符串发现`this is the right flag!\n`，点击进入并选中flag字符串，`ctrl+x`跳转到被调用的相关信息，`Tab`进入伪代码，进行代码分析：

```c
__int64 sub_1400118C0()
{
  char *v0; // rdi
  __int64 i; // rcx
  size_t v2; // rax
  char v4[36]; // [rsp+0h] [rbp-20h] BYREF
  int j; // [rsp+24h] [rbp+4h]
  char Str1[224]; // [rsp+48h] [rbp+28h] BYREF
  __int64 v7; // [rsp+128h] [rbp+108h]

  v0 = v4;
  for ( i = 82i64; i; --i )
  {
    *(_DWORD *)v0 = -858993460;
    v0 += 4;
  }
  for ( j = 0; ; ++j )
  {
    v7 = j;
    if ( j > j_strlen(Str2) )
      break;
    if ( Str2[j] == 'o' ) //点击数字按r转为ASCII字符
      Str2[j] = '0';
  }
  sub_1400111D1("input the flag:");
  sub_14001128F("%20s", Str1); //推测为scanf函数
  v2 = j_strlen(Str2);
  if ( !strncmp(Str1, Str2, v2) ) //点击进入Str2发现{hello_world}
    sub_1400111D1("this is the right flag!\n");
  else
    sub_1400111D1("wrong flag\n");
  sub_14001113B(v4, &unk_140019D00);
  return 0i64;
}
```

在`for循环`中会将字母`o`替换为数字`0`，所以真实比较的应该是{hell0_w0rld}，拿到flag

### reverse2

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int stat_loc; // [rsp+4h] [rbp-3Ch] BYREF
  int i; // [rsp+8h] [rbp-38h]
  __pid_t pid; // [rsp+Ch] [rbp-34h]
  char s2[24]; // [rsp+10h] [rbp-30h] BYREF
  unsigned __int64 v8; // [rsp+28h] [rbp-18h]

  v8 = __readfsqword(0x28u);
  pid = fork();
  if ( pid )
  {
    waitpid(pid, &stat_loc, 0);
  }
  else
  {
    for ( i = 0; i <= strlen(&flag); ++i )
    {
      if ( *(&flag + i) == 'i' || *(&flag + i) == 'r' ) //i和r换成数字1
        *(&flag + i) = '1';
    }
  }
  printf("input the flag:");
  __isoc99_scanf("%20s", s2);
  if ( !strcmp(&flag, s2) ) //点击flag进入发现 hacking_for_fun}
    return puts("this is the right flag!");
  else
    return puts("wrong flag!");
}
```

在`for循环`中会将字母`i & r`替换为数字`1`，所以真实比较的应该是{hack1ng_fo1_fun}，拿到flag

### 内涵的软件

直接运行一下，告诉我们放在变量里了，Exeinfo后扔给IDA32，看见变量，拿到`flag{49d3c93df25caad81232130f3d2ebfad}`

### 新年快乐

运行一下告诉我们脱壳，丢给PEID发现有壳

#### 工具脱壳

```cmd
upx -d 新年快乐.exe #使用UPX脱壳
```

#### 人工脱壳

脱壳时找`pushad`和`popad`，两个指令的目的是`保存程序入口参数`。加壳程序初始化时保存各个寄存器的值(堆栈)，外壳执行完毕后，再恢复各个寄存器的值，最后再跳到源程序执行。

程序喂给`OllyICE`，看见第一个是`pushad`，需要找到对应的`popad`，F8走一步发现ESP&EIP发生了改变。
单击选中寄存器ESP右键选择`数据窗口中跟随`，在数据窗口内随便选中数据后设置一个`硬件访问`的Dword断点，再开始运行。
运行后程序来到`lea eax, dword ptr [esp-80]`，往上滑第一个就是`popad`，`(如果直接在lea指令处脱壳会导致栈不平衡，生成伪代码错误)`
F8往下执行会发现有一个循环，可以断掉跳过循环，也可以右键直接运行到循环结束后的位置，继续执行执行到：
`0040E493   .- E9 E82DFFFF   jmp     00401280`
执行进入并发生跳转，此时来到了`00401280    83EC 1C         sub     esp, 1C`
得到的就是程序真正的入口点，即脱壳后的程序，选中该条指令右键`Dump process(OllyDumpEx)`，直接Dump(转储)即可。

再喂给Exeinfo已经没有加壳了，丢给IDA32看见`HappyNewYear!`，拿到flag

### xor

Exeinfo得到信息MacOS的64位程序，扔给IDA64，分析程序：

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+2Ch] [rbp-124h]
  char __b[264]; // [rsp+40h] [rbp-110h] BYREF

  memset(__b, 0, 0x100uLL);
  printf("Input your flag:\n");
  get_line(__b, 256LL);
  if ( strlen(__b) != 33 )
    goto LABEL_7;
  for ( i = 1; i < 33; ++i ) //此处会对字符串进行处理
    __b[i] ^= __b[i - 1];
  if ( !strncmp(__b, global, 0x21uLL) ) //点击global跳转并追溯得到字符串
//'f',0Ah,'k',0Ch,'w&O.@',11h,'x',0Dh,'Z;U',11h,'p',19h,'F',1Fh,'v"M#D',0Eh,'g',6,'h',0Fh,'G2O',0
    printf("Success");
  else
LABEL_7:
    printf("Failed");
  return 0;
}
```

```python
str1 = ['f',0x0A,'k',0x0C,'w','&','O','.','@',0x11,'x',0x0D,'Z',';','U',0x11,'p',0x19,'F',0x1F,'v','"','M','#','D',0x0E,'g',6,'h',0x0F,'G','2','O']
x = 'f'
for i in range(1,len(str1))
	if (isinstance(str1[i], str)):
        if (isinstance(str1[i - 1], str)):
            x += chr(ord(str1[i]) ^ ord(str1[i - 1]))
        else:
            x += chr(ord(str1[i]) ^ str1[i - 1])
    else:
        x += chr(str1[i] ^ ord(str1[i - 1]))

print(x) #flag{QianQiuWanDai_YiTongJiangHu}
```

### helloword

丢给AndroidKiller解析后进入工程信息的主函数直接看见flag

### reverse3

喂给ExeinfoPE，未加壳，Winx32位。丢进IDA32，找到`e3nifIH9b_C@n@dH`字符串比较，同时审计for循环对该字符串的处理。

```c
int __cdecl main_0(int argc, const char **argv, const char **envp)
{
  size_t StrLen; // eax
  const char *v4; // eax
  size_t v5; // eax
  char v7; // [esp+0h] [ebp-188h]
  char v8; // [esp+0h] [ebp-188h]
  signed int j; // [esp+DCh] [ebp-ACh]
  int i; // [esp+E8h] [ebp-A0h]
  signed int v11; // [esp+E8h] [ebp-A0h]
  char Destination[108]; // [esp+F4h] [ebp-94h] BYREF
  char Str[28]; // [esp+160h] [ebp-28h] BYREF
  char v14[8]; // [esp+17Ch] [ebp-Ch] BYREF

  for ( i = 0; i < 100; ++i )
  {
    if ( (unsigned int)i >= 0x64 )
      j____report_rangecheckfailure();
    Destination[i] = 0;
  }
  printf("please enter the flag:", v7);
  scanf("%20s", (char)Str);
  StrLen = j_strlen(Str);
  v4 = (const char *)sub_4110BE(Str, StrLen, v14); //下方会写上该函数追进去的源码
  strncpy(Destination, v4, 0x28u);
  v11 = j_strlen(Destination);
  for ( j = 0; j < v11; ++j )
    Destination[j] += j;
  v5 = j_strlen(Destination);
  if ( !strncmp(Destination, Str2, v5) )
    printf("rigth flag!\n", v8);
  else
    printf("wrong flag!\n", v8);
  return 0;
}
```

```c
void *__cdecl sub_411AB0(char *a1, unsigned int a2, int *a3)
{
  int v4; // [esp+D4h] [ebp-38h]
  int v5; // [esp+D4h] [ebp-38h]
  int v6; // [esp+D4h] [ebp-38h]
  int v7; // [esp+D4h] [ebp-38h]
  int i; // [esp+E0h] [ebp-2Ch]
  unsigned int v9; // [esp+ECh] [ebp-20h]
  int v10; // [esp+ECh] [ebp-20h]
  signed int v11; // [esp+ECh] [ebp-20h]
  void *v12; // [esp+F8h] [ebp-14h]
  char *v13; // [esp+104h] [ebp-8h]

  if ( !a1 || !a2 )
    return 0;
  v9 = a2 / 3;
  if ( (int)(a2 / 3) % 3 )
    ++v9;
  v10 = 4 * v9;
  *a3 = v10;
  v12 = malloc(v10 + 1);
  if ( !v12 )
    return 0;
  j_memset(v12, 0, v10 + 1);
  v13 = a1;
  v11 = a2;
  v4 = 0;
  while ( v11 > 0 )
  {
    byte_41A144[2] = 0;
    byte_41A144[1] = 0;
    byte_41A144[0] = 0;
    for ( i = 0; i < 3 && v11 >= 1; ++i )
    {
      byte_41A144[i] = *v13;
      --v11;
      ++v13;
    }
    if ( !i )
      break;
    switch ( i )
    {
      case 1:
        *((_BYTE *)v12 + v4) = aAbcdefghijklmn[(int)(unsigned __int8)byte_41A144[0] >> 2];
        v5 = v4 + 1;
        *((_BYTE *)v12 + v5) = aAbcdefghijklmn[((byte_41A144[1] & 0xF0) >> 4) | (16 * (byte_41A144[0] & 3))];
        *((_BYTE *)v12 + ++v5) = aAbcdefghijklmn[64]; 
//该数组进入后看到"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" 推测该函数为base64加密
        *((_BYTE *)v12 + ++v5) = aAbcdefghijklmn[64];
        v4 = v5 + 1;
        break;
      case 2:
        *((_BYTE *)v12 + v4) = aAbcdefghijklmn[(int)(unsigned __int8)byte_41A144[0] >> 2];
        v6 = v4 + 1;
        *((_BYTE *)v12 + v6) = aAbcdefghijklmn[((byte_41A144[1] & 0xF0) >> 4) | (16 * (byte_41A144[0] & 3))];
        *((_BYTE *)v12 + ++v6) = aAbcdefghijklmn[((byte_41A144[2] & 0xC0) >> 6) | (4 * (byte_41A144[1] & 0xF))];
        *((_BYTE *)v12 + ++v6) = aAbcdefghijklmn[64];
        v4 = v6 + 1;
        break;
      case 3:
        *((_BYTE *)v12 + v4) = aAbcdefghijklmn[(int)(unsigned __int8)byte_41A144[0] >> 2];
        v7 = v4 + 1;
        *((_BYTE *)v12 + v7) = aAbcdefghijklmn[((byte_41A144[1] & 0xF0) >> 4) | (16 * (byte_41A144[0] & 3))];
        *((_BYTE *)v12 + ++v7) = aAbcdefghijklmn[((byte_41A144[2] & 0xC0) >> 6) | (4 * (byte_41A144[1] & 0xF))];
        *((_BYTE *)v12 + ++v7) = aAbcdefghijklmn[byte_41A144[2] & 0x3F];
        v4 = v7 + 1;
        break;
    }
  }
  *((_BYTE *)v12 + v4) = 0;
  return v12;
}
```

```python
res = ''
str1 = "e3nifIH9b_C@n@dH"
for i in range(len(str1)):
	res += chr(ord(str1[i]) - i);
print(res) #e2lfbDB2ZV95b3V9
```

```python
import base64
src = input("please input:")
des = base64.b64decode(sec)
print(des)
```

### 不一样的flag

ExeinfoPE ==> 未加壳Win32bit，在IDA32中发现25位字符串`*11110100001010000101111#`，推测为二维数组的迷宫题

```bash
1 up	2 down	3 left	4 right
*1111\n01000\n01010\n00010\n1111#
        *	1	1	1	1
        0	1	0	0	0
        0	1	0	1	0
        0	0	0	1	0
        1	1	1	1	#
#从*号走向井号，输入的数字即是flag 222441144222
```

### SimpleRev

ExeinfoPE ==> ELFx64 ==> IDA64

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  char Choose; // [rsp+Fh] [rbp-1h]

  while ( 1 )
  {
    while ( 1 )
    {
      printf("Welcome to CTF game!\nPlease input d/D to start or input q/Q to quit this program: ");
      Choose = getchar();
      if ( Choose != 100 && Choose != 68 )
        break;
      Decry("Welcome to CTF game!\nPlease input d/D to start or input q/Q to quit this program: ", argv);
    }
    if ( Choose == 113 || Choose == 81 )
      Exit("Welcome to CTF game!\nPlease input d/D to start or input q/Q to quit this program: ", argv);
    puts("Input fault format!");
    v3 = getchar();
    putchar(v3);
  }
}
```

```c
unsigned __int64 Decry()
{
  char v1; // [rsp+Fh] [rbp-51h]
  int v2; // [rsp+10h] [rbp-50h]
  int v3; // [rsp+14h] [rbp-4Ch]
  int i; // [rsp+18h] [rbp-48h]
  int v5; // [rsp+1Ch] [rbp-44h]
  char src[8]; // [rsp+20h] [rbp-40h] BYREF
  __int64 v7; // [rsp+28h] [rbp-38h]
  int v8; // [rsp+30h] [rbp-30h]
  __int64 v9[2]; // [rsp+40h] [rbp-20h] BYREF
  int v10; // [rsp+50h] [rbp-10h]
  unsigned __int64 v11; // [rsp+58h] [rbp-8h]

  v11 = __readfsqword(0x28u);
  *(_QWORD *)src = 'SLCDN';                     // NDCLS
  v7 = 0LL;
  v8 = 0;
  v9[0] = 'wodah';                              // hadow
  v9[1] = 0LL;
  v10 = 0;
  text = (char *)join(key3, v9);                // killshadow
  strcpy(key, key1);                            // ADSFK
  strcat(key, src);                             // ASDFKNDCLS
  v2 = 0;
  v3 = 0;
  getchar();                                    // 吸收缓冲区\n
  v5 = strlen(key);                             // v5 = 10
  for ( i = 0; i < v5; ++i )
  {
    if ( key[v3 % v5] > '@' && key[v3 % v5] <= 'Z' )// 大写字母+ASCII_32 即转为小写
      key[i] = key[v3 % v5] + 32;               // asdfkndcls
    ++v3;                                       // v5 = 10 所以循环十次后++v3值也是10
  }
  printf("Please input your flag:");
  while ( 1 )
  {
    v1 = getchar();
    if ( v1 == '\n' )
      break;
    if ( v1 == ' ' )
    {
      ++v2;
    }
    else
    {
      if ( v1 <= 96 || v1 > 122 )               // h键字符变ASCII码值
      {
        if ( v1 > 64 && v1 <= 90 )
        {
          str2[v2] = (v1 - 39 - key[v3 % v5] + 97) % 26 + 97;
          ++v3;
        }
      }
      else
      {
        str2[v2] = (v1 - 39 - key[v3 % v5] + 97) % 26 + 97;
        ++v3;
      }
      if ( !(v3 % v5) )
        putchar(32);
      ++v2;
    }
  }
  if ( !strcmp(text, str2) )
    puts("Congratulation!\n");
  else
    puts("Try again!\n");
  return __readfsqword(0x28u) ^ v11;
}
```

```c
#include<stdio.h>
int main()
{
    char key[] = "adsfkndcls"; //已转换大小写
    char text[] = "killshadow";
    int v3 = 10;
    int v5 = 10;
    for (int i = 0; i < 10; i++)
    {
        for (int j = 0; j < 128; j++)
        {
            if (j < 'A' || j > 'z' || j > 'Z' && j < 'a')
            {
                continue;
            }
            if ((j -39 - key[v3 % v5] + 97) % 26 +97 == text[i])
            {
                printf("%c", j);
                v3++;
                break;
            }
        }
    }
} //KLDQCUDFZO
```

### Java逆向解密

丢给`jd-gui`，进行代码审计

```java
import java.util.ArrayList;
import java.util.Scanner;

public class Reverse {
  public static void main(String[] args) {
    Scanner s = new Scanner(System.in);
    System.out.println("Please input the flag );
    String str = s.next();
    System.out.println("Your input is );
    System.out.println(str);
    char[] stringArr = str.toCharArray();
    Encrypt(stringArr);
  }
  
  public static void Encrypt(char[] arr) {
    ArrayList<Integer> Resultlist = new ArrayList<>();
    for (int i = 0; i < arr.length; i++) {
      int result = arr[i] + 64 ^ 0x20;
      Resultlist.add(Integer.valueOf(result));
    } 
    int[] KEY = { 
        180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 
        133, 191, 134, 140, 129, 135, 191, 65 };
    ArrayList<Integer> KEYList = new ArrayList<>();
    for (int j = 0; j < KEY.length; j++)
      KEYList.add(Integer.valueOf(KEY[j])); 
    System.out.println("Result:");
    if (Resultlist.equals(KEYList)) {
      System.out.println("Congratulations);
    } else {
      System.err.println("Error);
    } 
  }
}
```

```python
res = ''
key = [180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 133, 191, 134, 140, 129, 135, 191, 65]
for i in range(0, len(key)):
    res += chr(key[i] - 64 ^ 0x20)
print(res) #This_is_the_flag_!
```

### [GXYCTF2019]luck_guy

ExeinfoPE ==> ELFx64 ==> IDA64

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned int v4; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  welcome(argc, argv, envp);
  puts("_________________");
  puts("try to patch me and find flag");
  v4 = 0;
  puts("please input a lucky number");
  __isoc99_scanf("%d", &v4);
  patch_me(v4);
  puts("OK,see you again");
  return 0;
}

int __fastcall patch_me(int a1)
{
  if ( a1 % 2 == 1 ) //输入奇数程序死掉 偶数继续获取flag
    return puts("just finished");
  else
    return get_flag();
}

unsigned __int64 get_flag()
{
  unsigned int v0; // eax
  int i; // [rsp+4h] [rbp-3Ch]
  int j; // [rsp+8h] [rbp-38h]
  __int64 s; // [rsp+10h] [rbp-30h] BYREF
  char v5; // [rsp+18h] [rbp-28h]
  unsigned __int64 v6; // [rsp+38h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  v0 = time(0LL);
  srand(v0);
  for ( i = 0; i <= 4; ++i )
  {
    switch ( rand() % 200 )
    {
      case 1:
        puts("OK, it's flag:");
        memset(&s, 0, 0x28uLL);
        strcat((char *)&s, f1); //f1 GXY{do_not_
        strcat((char *)&s, &f2);
        printf("%s", (const char *)&s);
        break;
      case 2:
        printf("Solar not like you");
        break;
      case 3:
        printf("Solar want a girlfriend");
        break;
      case 4:
        s = 0x7F666F6067756369LL; //重要信息
        v5 = 0;
        strcat(&f2, (const char *)&s);
        break;
      case 5:
        for ( j = 0; j <= 7; ++j )
        {
          if ( j % 2 == 1 )
            *(&f2 + j) -= 2;
          else
            --*(&f2 + j);
        }
        break;
      default:
        puts("emmm,you can't find flag 23333");
        break;
    }
  }
  return __readfsqword(0x28u) ^ v6;
}
```

```c
#include <stdio.h>
int main()
{
    char f1[] = "GXY{do_not_";
    char f2[] = "icug`of\x7"; //小端序:\x7Ffo`guci  ==>  大端序:icug`of\x7
    //根据case 5的循环进行反向操作
    for (int j = 0; j <= 7; ++j)
    {
        if (j % 2 == 1)
            f2[j] -= 2;
        else
            --f2[j];
    }
    printf("%s", f1);
    printf("%s", f2);

    return 0; //do_not_hate_me
}
```

### [BJDCTF2020]JustRE

https://github.com/BjdsecCA/BJDCTF2020

ExeinfoPE ==> Winx32 ==> IDA32，来到`DialogFunc`函数处发现`sprintf(String, " BJD{%d%d2069a45792d233ac}", 19999, 0);`

```c
INT_PTR __stdcall DialogFunc(HWND hWnd, UINT a2, WPARAM a3, LPARAM a4)
{
  CHAR String[100]; // [esp+0h] [ebp-64h] BYREF

  if ( a2 != 272 )
  {
    if ( a2 != 273 )
      return 0;
    if ( (_WORD)a3 != 1 && (_WORD)a3 != 2 )
    {
      sprintf(String, &Format, ++dword_4099F0);
      if ( dword_4099F0 == 19999 ) 
          //除了下方方法 可以点击进入存储点击次数的变量dword_4099F0地址为0x004099F0
		 //程序丢进OllyICE在左下方0x004099F0地址下硬件写入断点，F9执行后单击click发现eax寄存器变成了1
          //双击寄存器修改值为19999，确定后F9执行程序输出flag
      {
        sprintf(String, " BJD{%d%d2069a45792d233ac}", 19999, 0); //将此处的数值代入表达式即可拿到flag
        SetWindowTextA(hWnd, String);
        return 0;
      }
      SetWindowTextA(hWnd, String);
      return 0;
    }
    EndDialog(hWnd, (unsigned __int16)a3);
  }
  return 1;
}
```

### 刮开有奖

ExeinfoPE ==> Winx32 ==> IDA32

```c
INT_PTR __stdcall DialogFunc(HWND hDlg, UINT a2, WPARAM a3, LPARAM a4)
{
  const char *v4; // esi
  const char *v5; // edi
  int v7[2]; // [esp+8h] [ebp-20030h] BYREF
  int v8; // [esp+10h] [ebp-20028h]
  int v9; // [esp+14h] [ebp-20024h]
  int v10; // [esp+18h] [ebp-20020h]
  int v11; // [esp+1Ch] [ebp-2001Ch]
  int v12; // [esp+20h] [ebp-20018h]
  int v13; // [esp+24h] [ebp-20014h]
  int v14; // [esp+28h] [ebp-20010h]
  int v15; // [esp+2Ch] [ebp-2000Ch]
  int v16; // [esp+30h] [ebp-20008h]
  CHAR String[65536]; // [esp+34h] [ebp-20004h] BYREF
  char v18[65536]; // [esp+10034h] [ebp-10004h] BYREF

  if ( a2 == 272 )
    return 1;
  if ( a2 != 273 )
    return 0;
  if ( (_WORD)a3 == 1001 )
  {
    memset(String, 0, 0xFFFFu);
    GetDlgItemTextA(hDlg, 1000, String, 0xFFFF);
    if ( strlen(String) == 8 )
    {
      v7[0] = 90;
      v7[1] = 74;
      v8 = 83;
      v9 = 69;
      v10 = 67;
      v11 = 97;
      v12 = 78;
      v13 = 72;
      v14 = 51;
      v15 = 110;
      v16 = 103;
      sub_4010F0(v7, 0, 10);
      memset(v18, 0, 0xFFFFu);
      v18[0] = String[5];
      v18[2] = String[7];
      v18[1] = String[6];
      v4 = (const char *)sub_401000(v18, strlen(v18));
      memset(v18, 0, 0xFFFFu);
      v18[1] = String[3];
      v18[0] = String[2];
      v18[2] = String[4];
      v5 = (const char *)sub_401000(v18, strlen(v18));
      if ( String[0] == v7[0] + 34 // sub_4010F0函数后的第一位等于51+34=85-->'U'
        && String[1] == v10 // 第2位，等于v13,即sub_4010F0函数返回值的第5位值-->'J'
        && 4 * String[2] - 141 == 3 * v8
        && String[3] / 4 == 2 * (v13 / 9)
        && !strcmp(v4, "ak1w") //解码得到'jMp'
        && !strcmp(v5, "V1Ax")) //'WP1'
      {
        MessageBoxA(hDlg, "U g3t 1T!", "@_@", 0); 
      }
    }
    return 0;
  }
  if ( (_WORD)a3 != 1 && (_WORD)a3 != 2 )
    return 0;
  EndDialog(hDlg, (unsigned __int16)a3);
  return 1;
}
```

```c
int __cdecl sub_4010F0(int a1, int a2, int a3)
{
  int result; // eax
  int i; // esi
  int v5; // ecx
  int v6; // edx

  result = a3;
  for ( i = a2; i <= a3; a2 = i )
  {
    v5 = 4 * i;
    v6 = *(_DWORD *)(4 * i + a1);
    if ( a2 < result && i < result )
    {
      do
      {
        if ( v6 > *(_DWORD *)(a1 + 4 * result) )
        {
          if ( i >= result )
            break;
          ++i;
          *(_DWORD *)(v5 + a1) = *(_DWORD *)(a1 + 4 * result);
          if ( i >= result )
            break;
          while ( *(_DWORD *)(a1 + 4 * i) <= v6 )
          {
            if ( ++i >= result )
              goto LABEL_13;
          }
          if ( i >= result )
            break;
          v5 = 4 * i;
          *(_DWORD *)(a1 + 4 * result) = *(_DWORD *)(4 * i + a1);
        }
        --result;
      }
      while ( i < result );
    }
LABEL_13:
    *(_DWORD *)(a1 + 4 * result) = v6;
    sub_4010F0(a1, a2, i - 1);
    result = a3;
    ++i;
  }
  return result;
}
```

进入第65行byte_407830，如下，猜测这个函数应该是base64加密

```bash
.rdata:00407830 ; char byte_407830[]
.rdata:00407830 byte_407830     db 41h                  ; DATA XREF: sub_401000+C0↑r
.rdata:00407831 aBcdefghijklmno db 'BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',0
```

```c
#include <stdio.h>
#include <string.h>
int sub_4010F0(char* a1, int a2, int a3)
{
    int result; //eax
    int i; //esi
    int v5; //ecx
    int v6; //edx
    
    result = a3;
    for (i = a2; i <= a3; a2 = i)
    {
        v5 = i;
        v6 = a1[i];
        if (a2 < result && i < result)
        {
            do
            {
                if (v6 > a1[result])
                {
                    if (i >= result)
                        break;
                    ++i;
                    a1[v5] = a1[result];
                    if (i >= result)
                        break;
                    while (a1[i] <= v6)
                    {
                        if (++i >= result)
                            goto LABEL_13;
                    }
                    if (i > result)
                        break;
                    v5 = i;
                    a1[result] = a1[i];
                }
                --result;
            } while (i < result);
        }
    LABEL_13:
        a1[result] = v6;
        sub_4010F0(a1, a2, i - 1);
        result = a3;
        ++i;
    }
    return result;
}
int main()
{
    char v[] = "ZJSECaNH3ng";
    sub_4010F0(v, 0, 10);
    printf("%s\n", v);
    printf("%c%c", v[0]+34,v[4]);
    return 0;
} //UJ 加上解码得到'jMp'和'WP1'组成 UJWP1jMp
```

### 简单注册器

jadx-gui打开反编译，得到：

```java
public void onClick(View v) {
                int flag = 1;
                String xx = editview.getText().toString();
                flag = (xx.length() == 32 && xx.charAt(31) == 'a' && xx.charAt(1) == 'b' && (xx.charAt(0) + xx.charAt(2)) + (-48) == 56) ? 0 : 0;
                if (flag == 1) {
                    char[] x = "dd2940c04462b4dd7c450528835cca15".toCharArray();
                    x[2] = (char) ((x[2] + x[3]) - 50);
                    x[4] = (char) ((x[2] + x[5]) - 48);
                    x[30] = (char) ((x[31] + x[9]) - 48);
                    x[14] = (char) ((x[27] + x[28]) - 97);
                    for (int i = 0; i < 16; i++) {
                        char a = x[31 - i];
                        x[31 - i] = x[i];
                        x[i] = a;
                    }
                    String bbb = String.valueOf(x);
                    textview.setText("flag{" + bbb + "}");
                    return;
                }
                textview.setText("输入注册码错误");
            }
```

```c
#include <stdio.h>
int main()
{
    char x[] = "dd2940c04462b4dd7c450528835cca15";
    x[2] = (char) ((x[2] + x[3]) - 50);
    x[4] = (char) ((x[2] + x[5]) - 48);
    x[30] = (char) ((x[31] + x[9]) - 48);
    x[14] = (char) ((x[27] + x[28]) - 97);
    for (int i = 0; i < 16; i++) {
        char a = x[31 - i];
        x[31 - i] = x[i];
        x[i] = a;
    }
    printf("%s",x);
    return 0;
} //59acc538825054c7de4b26440c0999dd
```

### [GWCTF 2019]pyre

```cmd
pip install uncompyle6
uncompyle6 xxx.pyc #直接输出反编译文本
```

[python反编译 - 在线工具 (tool.lu)](https://tool.lu/pyc/)

```python
#!/usr/bin/env python
# visit https://tool.lu/pyc/ for more information
# Version: Python 2.7

print 'Welcome to Re World!'
print 'Your input1 is your flag~'
l = len(input1)
for i in range(l):
    num = ((input1[i] + i) % 128 + 128) % 128
    code += num

for i in range(l - 1):
    code[i] = code[i] ^ code[i + 1]

print code
code = [
    '%1f',
    '%12',
    '%1d',
    '(',
    '0',
    '4',
    '%01',
    '%06',
    '%14',
    '4',
    ',',
    '%1b',
    'U',
    '?',
    'o',
    '6',
    '*',
    ':',
    '%01',
    'D',
    ';',
    '%',
    '%13']
```

```python
print('Welcome to Re World!')
print('Your input1 is your flag~')

code = [0x1f,0x12,0x1d, 0x28,0x30,0x34, 0x01,0x06,0x14, 0x34,
        0x2c, 0x1b, 0x55,0x3f,0x6f,0x36,0x2a,0x3a, 0x01, 0x44,
        0x3b,0x25, 0x13]

code.reverse()
l = len(code)

for i in range(l-1):
    code[i + 1] = code[i] ^ code[i + 1]

code.reverse()

for i in range(len(code)):
    if code[i] - i < 0:
        code[i] = code[i] + 128 -i
    else:
        code[i] -= i

flag = ''.join(chr(i) for i in code)
print(flag)

# GWHT{Just_Re_1s_Ha66y!}
```

### [ACTF新生赛2020]easyre

ExeinfoPE ==> Winx32Bit(unpacked) ==> `UPXShell` / `upx -d easyre.exe` ==> IDA32

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  _BYTE v4[12]; // [esp+12h] [ebp-2Eh] BYREF
  _DWORD v5[3]; // [esp+1Eh] [ebp-22h]
  _BYTE v6[5]; // [esp+2Ah] [ebp-16h] BYREF
  int v7; // [esp+2Fh] [ebp-11h]
  int v8; // [esp+33h] [ebp-Dh]
  int v9; // [esp+37h] [ebp-9h]
  char v10; // [esp+3Bh] [ebp-5h]
  int i; // [esp+3Ch] [ebp-4h]

  __main();
  qmemcpy(v4, "*F'\"N,\"(I?+@", sizeof(v4));
  // [42,70,39,34,78,44,34,40,73,63,43,64]
  // [ *, f, ', ", N, ,, ", (, I, ?, +, @]
  printf("Please input:");
  scanf("%s", v6);
  if ( v6[0] != 65 || v6[1] != 67 || v6[2] != 84 || v6[3] != 70 || v6[4] != 123 || v10 != 125 )
    return 0;
  v5[0] = v7;
  v5[1] = v8;
  v5[2] = v9;
  for ( i = 0; i <= 11; ++i )
  {
    if ( v4[i] != _data_start__[*((char *)v5 + i) - 1] )
      //'~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)(\'&%$# !"'
      return 0;
  }
  printf("You are correct!");
  return 0;
}
```

![image-20230402203622554](.\Pwn\[ACTF新生赛2020]easyre.png)

```python
a = [42,70,39,34,78,44,34,40,73,63,43,64]
_data_start__ = '~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)(\'&%$# !"'
s = ""
for i in a:
    s += chr(_data_start__.find(chr(i))+1)
print(s) #flag{U9X_1S_W6@T?}
```

### findit

直接喂给`jadx-gui`

```java
package com.example.findit;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

/* loaded from: classes.dex */
public class MainActivity extends ActionBarActivity {
    /* JADX INFO: Access modifiers changed from: protected */
    @Override // android.support.v7.app.ActionBarActivity, android.support.v4.app.FragmentActivity, android.app.Activity
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button btn = (Button) findViewById(R.id.widget3);
        final EditText edit = (EditText) findViewById(R.id.widget2);
        final TextView text = (TextView) findViewById(R.id.widget1);
        final char[] a = {'T', 'h', 'i', 's', 'I', 's', 'T', 'h', 'e', 'F', 'l', 'a', 'g', 'H', 'o', 'm', 'e'};
        final char[] b = {'p', 'v', 'k', 'q', '{', 'm', '1', '6', '4', '6', '7', '5', '2', '6', '2', '0', '3', '3', 'l', '4', 'm', '4', '9', 'l', 'n', 'p', '7', 'p', '9', 'm', 'n', 'k', '2', '8', 'k', '7', '5', '}'};
        btn.setOnClickListener(new View.OnClickListener() { // from class: com.example.findit.MainActivity.1
            @Override // android.view.View.OnClickListener
            public void onClick(View v) {
                char[] x = new char[17];
                char[] y = new char[38];
                for (int i = 0; i < 17; i++) {
                    if ((a[i] < 'I' && a[i] >= 'A') || (a[i] < 'i' && a[i] >= 'a')) {
                        x[i] = (char) (a[i] + 18);
                    } else if ((a[i] >= 'A' && a[i] <= 'Z') || (a[i] >= 'a' && a[i] <= 'z')) {
                        x[i] = (char) (a[i] - '\b');
                    } else {
                        x[i] = a[i];
                    }
                }
                String m = String.valueOf(x);
                if (m.equals(edit.getText().toString())) {
                    for (int i2 = 0; i2 < 38; i2++) {
                        if ((b[i2] >= 'A' && b[i2] <= 'Z') || (b[i2] >= 'a' && b[i2] <= 'z')) {
                            y[i2] = (char) (b[i2] + 16);
                            if ((y[i2] > 'Z' && y[i2] < 'a') || y[i2] >= 'z') {
                                y[i2] = (char) (y[i2] - 26);
                            }
                        } else {
                            y[i2] = b[i2];
                        }
                    }
                    String n = String.valueOf(y);
                    text.setText(n);
                    return;
                }
                text.setText("答案错了肿么办。。。不给你又不好意思。。。哎呀好纠结啊~~~");
            }
        });
    }

    @Override // android.app.Activity
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
```

```java
'p', 'v', 'k', 'q', '{', 'm', '1', '6', '4', '6', '7', '5', '2', '6', '2', '0', '3', '3', 'l', '4', 'm', '4', '9', 'l', 'n', 'p', '7', 'p', '9', 'm', 'n', 'k', '2', '8', 'k', '7', '5', '}' //疑似凯撒加密 解密即可
```

```java
package Reverse; //脚本解法
//https://buuoj.cn/challenges#findit
public class BuuCTF_findit {
    public static void main(String[] args) {
        final char[] a = {'T', 'h', 'i', 's', 'I', 's', 'T', 'h', 'e', 'F', 'l', 'a', 'g', 'H', 'o', 'm', 'e'};
        final char[] b = {'p', 'v', 'k', 'q', '{', 'm', '1', '6', '4', '6', '7', '5', '2', '6', '2', '0', '3', '3', 'l', '4', 'm', '4', '9', 'l', 'n', 'p', '7', 'p', '9', 'm', 'n', 'k', '2', '8', 'k', '7', '5', '}'};

        char[] x = new char[17];
        char[] y = new char[38];
        for (int i = 0; i < 17; i++) {
            if ((a[i] < 'I' && a[i] >= 'A') || (a[i] < 'i' && a[i] >= 'a')) {
                x[i] = (char) (a[i] + 18);
            } else if ((a[i] >= 'A' && a[i] <= 'Z') || (a[i] >= 'a' && a[i] <= 'z')) {
                x[i] = (char) (a[i] - '\b');
            } else {
                x[i] = a[i];
            }
        }
        String m = String.valueOf(x);
        for (int i2 = 0; i2 < 38; i2++) {
            if ((b[i2] >= 'A' && b[i2] <= 'Z') || (b[i2] >= 'a' && b[i2] <= 'z')) {
                y[i2] = (char) (b[i2] + 16);
                if ((y[i2] > 'Z' && y[i2] < 'a') || y[i2] >= 'z') {
                    y[i2] = (char) (y[i2] - 26);
                }
            } else {
                y[i2] = b[i2];
            }
        }
        System.out.println(y);
    }
}
```

### [ACTF新生赛2020]rome

ExeinfoPE ==> Winx32Bit ==> IDA32

```c
int func()
{
  int result; // eax
  int v1[4]; // [esp+14h] [ebp-44h]
  unsigned __int8 v2; // [esp+24h] [ebp-34h] BYREF
  unsigned __int8 v3; // [esp+25h] [ebp-33h]
  unsigned __int8 v4; // [esp+26h] [ebp-32h]
  unsigned __int8 v5; // [esp+27h] [ebp-31h]
  unsigned __int8 v6; // [esp+28h] [ebp-30h]
  int v7; // [esp+29h] [ebp-2Fh]
  int v8; // [esp+2Dh] [ebp-2Bh]
  int v9; // [esp+31h] [ebp-27h]
  int v10; // [esp+35h] [ebp-23h]
  unsigned __int8 v11; // [esp+39h] [ebp-1Fh]
  char v12[29]; // [esp+3Bh] [ebp-1Dh] BYREF

  strcpy(v12, "Qsw3sj_lz4_Ujw@l");
  printf("Please input:");
  scanf("%s", &v2);
  result = v2;
  if ( v2 == 'A' )
  {
    result = v3;
    if ( v3 == 'C' )
    {
      result = v4;
      if ( v4 == 'T' )
      {
        result = v5;
        if ( v5 == 'F' )
        {
          result = v6;
          if ( v6 == '{' )
          {
            result = v11;
            if ( v11 == '}' )
            {
              v1[0] = v7;
              v1[1] = v8;
              v1[2] = v9;
              v1[3] = v10;
              *(_DWORD *)&v12[17] = 0;
              while ( *(int *)&v12[17] <= 15 )
              {
                if ( *((char *)v1 + *(_DWORD *)&v12[17]) > 64 && *((char *)v1 + *(_DWORD *)&v12[17]) <= 90 )
                  *((_BYTE *)v1 + *(_DWORD *)&v12[17]) = (*((char *)v1 + *(_DWORD *)&v12[17]) - 51) % 26 + 65;
                if ( *((char *)v1 + *(_DWORD *)&v12[17]) > 96 && *((char *)v1 + *(_DWORD *)&v12[17]) <= 122 )
                  *((_BYTE *)v1 + *(_DWORD *)&v12[17]) = (*((char *)v1 + *(_DWORD *)&v12[17]) - 79) % 26 + 97;
                ++*(_DWORD *)&v12[17];
              }
              *(_DWORD *)&v12[17] = 0;
              while ( *(int *)&v12[17] <= 15 )
              {
                result = (unsigned __int8)v12[*(_DWORD *)&v12[17]];
                if ( *((_BYTE *)v1 + *(_DWORD *)&v12[17]) != (_BYTE)result )
                  return result;
                ++*(_DWORD *)&v12[17];
              }
              return printf("You are correct!");
            }
          }
        }
      }
    }
  }
  return result;
}
```

```python
word ="Qsw3sj_lz4_Ujw@l"
flag = ""
for i in range(16):
    for j in range(32, 127):
        k = j
        if j > 64 and j <= 90:
            j = (j - 51) % 26 + 65
        if j > 96 and j <= 122:
            j = (j - 79) % 26 + 97
        if chr(j) == word[i]:
            flag += chr(k)
print(flag)
```

### rsa

[RSA算法原理](https://blog.csdn.net/dbs1215/article/details/48953589)
[Python下RSA加解密](https://www.cnblogs.com/hhh5460/p/5243410.html)
[利用gmpy2破解RSA](https://www.cnblogs.com/ESHLkangi/p/8576222.html)

`cat pub.key`拖入网址 http://tool.chacuo.net/cryptrsakeyparse 进行解密后得到

**公钥指数及模数信息:**

| key长度： | 256                                                          |
| --------- | ------------------------------------------------------------ |
| 模数：    | C0332C5C64AE47182F6C1C876D42336910545A58F7EEFEFC0BCAAF5AF341CCDD |
| 指数：    | 65537 (0x10001)                                              |

E(即指数)=65537 & N(模数)=C0332C5C64AE47182F6C1C876D42336910545A58F7EEFEFC0BCAAF5AF341CCDD
[python进制转换 - Marvin-wen - 博客园 (cnblogs.com)](https://www.cnblogs.com/marvin-wen/p/12172424.html)
N(模数):Hex ==> Dec = 86934482296048119190666062003494800588905656017203025617216654058378322103517

进入 http://www.factordb.com/index.php 计算 p 和 q

![image-20230403093216648](.\Reverse\rsa.png)
p = 285960468890451637935629440372639283459
q = 304008741604601924494328155975272418463

```shell
pip install gmpy2 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install rsa -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
import gmpy2
import rsa
num = "C0332C5C64AE47182F6C1C876D42336910545A58F7EEFEFC0BCAAF5AF341CCDD"
N = int(num,16)
E = 65537
p = 285960468890451637935629440372639283459
q = 304008741604601924494328155975272418463
D = int(gmpy2.invert(E,(p-1)*(q-1)))
privkey = rsa.PrivateKey(N, E, D, p, q)
with open("F:\\Info\\Information\\CTF_File\\BUUCTF\\Reverse\\rsa", "rb+") as file:
    text = file.read()
message = rsa.decrypt(text,privkey)
print(message) #flag{decrypt_256}
```

### [FlareOn4]login

```bash
cat login.html
<!DOCTYPE Html />
<html>
    <head>
        <title>FLARE On 2017</title>
    </head>
    <body>
        <input type="text" name="flag" id="flag" value="Enter the flag" />
        <input type="button" id="prompt" value="Click to check the flag" />
        <script type="text/javascript">
            document.getElementById("prompt").onclick = function () {
                var flag = document.getElementById("flag").value;
                var rotFlag = flag.replace(/[a-zA-Z]/g, function(c){return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);});
                if ("PyvragFvqrYbtvafNerRnfl@syner-ba.pbz" == rotFlag) {
                    alert("Correct flag!");
                } else {
                    alert("Incorrect flag, rot again");
                    #在源码中添加如下指令 网页输入"PyvragFvqrYbtvafNerRnfl@syner-ba.pbz" 输出flag
                    alert(rotFlag); #ClientSideLoginsAreEasy@flare-on.com
                }
            }
        </script>
    </body>
</html>
```

### CrackRTF

ExeinfoPE ==> Winx32Bit ==> IDA32

```c
int __cdecl main_0(int argc, const char **argv, const char **envp)
{
  DWORD v3; // eax
  DWORD v4; // eax
  char Str[260]; // [esp+4Ch] [ebp-310h] BYREF
  int v7; // [esp+150h] [ebp-20Ch]
  char String1[260]; // [esp+154h] [ebp-208h] BYREF
  char Destination[260]; // [esp+258h] [ebp-104h] BYREF

  memset(Destination, 0, sizeof(Destination));
  memset(String1, 0, sizeof(String1));
  v7 = 0;
  printf("pls input the first passwd(1): ");
  scanf("%s", Destination);
  if ( strlen(Destination) != 6 ) //需要输入六位密码
  {
    printf("Must be 6 characters!\n");
    ExitProcess(0);
  }
  v7 = atoi(Destination);
  if ( v7 < 100000 ) //密码需要比100000大
    ExitProcess(0);
  strcat(Destination, "@DBApp"); //字符串拼接(?) @DBApp
  v3 = strlen(Destination); //v3接收长度为12
  sub_40100A((BYTE *)Destination, v3, String1); //Hash加密
  if ( !_strcmpi(String1, "6E32D0943418C2C33385BC35A1470250DD8923A9") ) //比较
  {
    printf("continue...\n\n");
    printf("pls input the first passwd(2): ");
    memset(Str, 0, sizeof(Str));
    scanf("%s", Str);
    if ( strlen(Str) != 6 ) //6位
    {
      printf("Must be 6 characters!\n");
      ExitProcess(0);
    }
    strcat(Str, Destination);
    memset(String1, 0, sizeof(String1));
    v4 = strlen(Str);
    sub_401019((BYTE *)Str, v4, String1);
    if ( !_strcmpi("27019e688a4e62a649fd99cadaafdb4e", String1) )
    {
      if ( !(unsigned __int8)sub_40100F(Str) ) //点此进入标识码是0x8003u 查询得知md5加密 进入后有FindResourceA()提示
      {
        printf("Error!!\n");
        ExitProcess(0);
      }
      printf("bye ~~\n");
    }
  }
  return 0;
}
```

```c
char __cdecl sub_4014D0(LPCSTR lpString)
{
  LPCVOID lpBuffer; // [esp+50h] [ebp-1Ch]
  DWORD NumberOfBytesWritten; // [esp+58h] [ebp-14h] BYREF
  DWORD nNumberOfBytesToWrite; // [esp+5Ch] [ebp-10h]
  HGLOBAL hResData; // [esp+60h] [ebp-Ch]
  HRSRC hResInfo; // [esp+64h] [ebp-8h]
  HANDLE hFile; // [esp+68h] [ebp-4h]

  hFile = 0;
  hResData = 0;
  nNumberOfBytesToWrite = 0;
  NumberOfBytesWritten = 0;
  hResInfo = FindResourceA(0, (LPCSTR)0x65, "AAA"); //找AAA文件
  if ( !hResInfo )
    return 0;
  nNumberOfBytesToWrite = SizeofResource(0, hResInfo);
  hResData = LoadResource(0, hResInfo);
  if ( !hResData )
    return 0;
  lpBuffer = LockResource(hResData);
  sub_401005(lpString, (int)lpBuffer, nNumberOfBytesToWrite);
  hFile = CreateFileA("dbapp.rtf", 0x10000000u, 0, 0, 2u, 0x80u, 0);
  if ( hFile == (HANDLE)-1 )
    return 0;
  if ( !WriteFile(hFile, lpBuffer, nNumberOfBytesToWrite, &NumberOfBytesWritten, 0) )
    return 0;
  CloseHandle(hFile);
  return 1;
}
```

```c
unsigned int __cdecl sub_401420(LPCSTR lpString, int a2, int a3)
{
  unsigned int result; // eax
  unsigned int i; // [esp+4Ch] [ebp-Ch]
  unsigned int v5; // [esp+54h] [ebp-4h]

  v5 = lstrlenA(lpString);
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( i >= a3 )
      break;
    *(_BYTE *)(i + a2) ^= lpString[i % v5]; //
  }
  return result;
}
```

```python
import hashlib
string = "@DBApp"
encrypt = "6E32D0943418C2C33385BC35A1470250DD8923A9".lower() #踩坑记录 一定要转小写
for i in range(100000, 999999):
    y = hashlib.sha1((str(i)+string).encode("utf-8")).hexdigest()
    if encrypt == y:
        print(str(i)+string) #123321@DBApp
        break
```

[2022-06-28 【CTF杂项】常见文件文件头文件尾格式总结及各类文件头 - 简书 (jianshu.com)](https://www.jianshu.com/p/ea3faf5a0646)
[MD5免费在线解密破解_MD5在线加密-SOMD5](https://www.somd5.com/)

解密`27019e688a4e62a649fd99cadaafdb4e1`后得到`~!3a@0123321@DBApp`，输入程序中在当前文件夹得到flag文件。

或者使用Reshacker，根据FindResourceA()提示，进入后发现AAA目录取文件标志位前六位和AAA文件中的前六位进行异或得出~!3a@0

![image-20230403122509066](F:\Info\Information\Typora\Reverse\CrackRTF.png)

```python
s = "{\\rtf1"
a = [0x05, 0x7D, 0x41, 0x15, 0x26, 0x01]
flag = ""
for i in range(0, len(s)):
    x = ord(s[i]^a[i])
    flag += chr(x)
print(flag)
```

### [WUSTCTF2020]level1

ExeinfoPe ==> ELF64bit ==> IDA64

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+4h] [rbp-2Ch]
  FILE *stream; // [rsp+8h] [rbp-28h]
  char ptr[24]; // [rsp+10h] [rbp-20h] BYREF
  unsigned __int64 v7; // [rsp+28h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  stream = fopen("flag", "r");
  fread(ptr, 1uLL, 0x14uLL, stream);
  fclose(stream);
  for ( i = 1; i <= 19; ++i )
  {
    if ( (i & 1) != 0 ) //对下标索引为奇数进行移位，偶数进行乘法
      printf("%ld\n", (unsigned int)(ptr[i] << i));
    else
      printf("%ld\n", (unsigned int)(i * ptr[i]));
  }
  return 0;
}
```

```python
a = [198,232,816,200,1536,300,6144,984,51200,570,92160,1200,565248,756,1474560,800,6291456,1782,65536000]
flag = ""
for i in range(19):
    if ((i+1) & 1):
        flag += (chr(a[i] >> (i+1))) 
    else:
        flag += (chr(a[i] / (i+1))) #windows下需要强转 flag += (chr(int(a[i] / (i+1))))
print(flag) #ctf2020{d9-dE6-20c}
```

### [GUET-CTF2019]re

ExeinfoPE ==> ELFx64bit ==> `upx -d re` ==> IDA64

```c
__int64 __fastcall sub_400E28(__int64 a1, int a2, int a3, int a4, int a5, int a6)
{
  int v6; // edx
  int v7; // ecx
  int v8; // er8
  int v9; // er9
  __int64 result; // rax
  __int64 v11; // [rsp+0h] [rbp-30h] BYREF
  unsigned __int64 v12; // [rsp+28h] [rbp-8h]

  v12 = __readfsqword(0x28u);
  sub_40F950((unsigned int)"input your flag:", a2, a3, a4, a5, a6, 0LL, 0LL, 0LL, 0LL);
  sub_40FA80((unsigned int)"%s", (unsigned int)&v11, v6, v7, v8, v9, v11);
  if ( (unsigned int)sub_4009AE(&v11) )
    sub_410350("Correct!");
  else
    sub_410350("Wrong!");
  result = 0LL;
  if ( __readfsqword(0x28u) != v12 )
    sub_443550();
  return result;
}
```

```c
_BOOL8 __fastcall sub_4009AE(char *a1)
{
  if ( 1629056 * *a1 != 166163712 )
    return 0LL;
  if ( 6771600 * a1[1] != 731332800 )
    return 0LL;
  if ( 3682944 * a1[2] != 357245568 )
    return 0LL;
  if ( 10431000 * a1[3] != 1074393000 )
    return 0LL;
  if ( 3977328 * a1[4] != 489211344 )
    return 0LL;
  if ( 5138336 * a1[5] != 518971936 )
    return 0LL;
  if ( 7532250 * a1[7] != 406741500 )
    return 0LL;
  if ( 5551632 * a1[8] != 294236496 )
    return 0LL;
  if ( 3409728 * a1[9] != 177305856 )
    return 0LL;
  if ( 13013670 * a1[10] != 650683500 )
    return 0LL;
  if ( 6088797 * a1[11] != 298351053 )
    return 0LL;
  if ( 7884663 * a1[12] != 386348487 )
    return 0LL;
  if ( 8944053 * a1[13] != 438258597 )
    return 0LL;
  if ( 5198490 * a1[14] != 249527520 )
    return 0LL;
  if ( 4544518 * a1[15] != 445362764 )
    return 0LL;
  if ( 3645600 * a1[17] != 174988800 )
    return 0LL;
  if ( 10115280 * a1[16] != 981182160 )
    return 0LL;
  if ( 9667504 * a1[18] != 493042704 )
    return 0LL;
  if ( 5364450 * a1[19] != 257493600 )
    return 0LL;
  if ( 13464540 * a1[20] != 767478780 )
    return 0LL;
  if ( 5488432 * a1[21] != 312840624 )
    return 0LL;
  if ( 14479500 * a1[22] != 1404511500 )
    return 0LL;
  if ( 6451830 * a1[23] != 316139670 )
    return 0LL;
  if ( 6252576 * a1[24] != 619005024 )
    return 0LL;
  if ( 7763364 * a1[25] != 372641472 )
    return 0LL;
  if ( 7327320 * a1[26] != 373693320 )
    return 0LL;
  if ( 8741520 * a1[27] != 498266640 )
    return 0LL;
  if ( 8871876 * a1[28] != 452465676 )
    return 0LL;
  if ( 4086720 * a1[29] != 208422720 )
    return 0LL;
  if ( 9374400 * a1[30] == 515592000 )
    return 5759124 * a1[31] == 719890500;
  return 0LL;
}
```

```python
flag=''
flag+=chr(166163712//1629056)
flag+= chr(731332800 // 6771600)
flag += chr(357245568 // 3682944)
flag += chr(1074393000 // 10431000)
flag += chr(489211344 // 3977328)
flag += chr(518971936 // 5138336)
flag+='?'
flag += chr(406741500 // 7532250)
flag += chr(294236496 // 5551632)
flag += chr(177305856 // 3409728)
flag += chr(650683500 // 13013670)
flag += chr(298351053 // 6088797)
flag += chr(386348487 // 7884663)
flag+= chr(438258597 // 8944053)
flag+= chr(249527520 // 5198490)
flag+= chr(445362764 // 4544518)
flag+= chr(981182160 // 10115280)
flag+= chr(174988800 // 3645600)
flag+= chr(493042704 // 9667504)
flag += chr(257493600 // 5364450)
flag+= chr(767478780 // 13464540)
flag+= chr(312840624 // 5488432)
flag += chr(1404511500 // 14479500)
flag+= chr(316139670 // 6451830)
flag+= chr(619005024 // 6252576)
flag+= chr(372641472 // 7763364)
flag+= chr(373693320 // 7327320)
flag+= chr(498266640 // 8741520)
flag+= chr(452465676 // 8871876)
flag+= chr(208422720 // 4086720)
flag+= chr(515592000 // 9374400)
flag+= chr(719890500 // 5759124)
print(flag) #flag{e?65421110ba03099a1c039337} 蒙了一下？是1结果直接过了
```

### [2019红帽杯]easyRE

ExeinfoPE ==> Elf_64Bit ==> IDA64，搜索字符串跳转到关键函数

```c
__int64 sub_4009C6()
{
  __int64 result; // rax
  int i; // [rsp+Ch] [rbp-114h]
  __int64 v2; // [rsp+10h] [rbp-110h]
  __int64 v3; // [rsp+18h] [rbp-108h]
  __int64 v4; // [rsp+20h] [rbp-100h]
  __int64 v5; // [rsp+28h] [rbp-F8h]
  __int64 v6; // [rsp+30h] [rbp-F0h]
  __int64 v7; // [rsp+38h] [rbp-E8h]
  __int64 v8; // [rsp+40h] [rbp-E0h]
  __int64 v9; // [rsp+48h] [rbp-D8h]
  __int64 v10; // [rsp+50h] [rbp-D0h]
  __int64 v11; // [rsp+58h] [rbp-C8h]
  char v12[13]; // [rsp+60h] [rbp-C0h] BYREF
  char v13[4]; // [rsp+6Dh] [rbp-B3h] BYREF
  char v14[19]; // [rsp+71h] [rbp-AFh] BYREF
  char v15[32]; // [rsp+90h] [rbp-90h] BYREF
  int v16; // [rsp+B0h] [rbp-70h]
  char v17; // [rsp+B4h] [rbp-6Ch]
  char v18[72]; // [rsp+C0h] [rbp-60h] BYREF
  unsigned __int64 v19; // [rsp+108h] [rbp-18h]

  v19 = __readfsqword(0x28u);
  qmemcpy(v12, "Iodl>Qnb(ocy", 12);
  v12[12] = 127;
  qmemcpy(v13, "y.i", 3);
  v13[3] = 127;
  qmemcpy(v14, "d`3w}wek9{iy=~yL@EC", sizeof(v14));
  memset(v15, 0, sizeof(v15));
  v16 = 0;
  v17 = 0;
  sub_4406E0(0LL, v15, 37LL);
  v17 = 0;
  if ( sub_424BA0(v15) == 36 )
  {
    for ( i = 0; i < (unsigned __int64)sub_424BA0(v15); ++i )
    {
      if ( (unsigned __int8)(v15[i] ^ i) != v12[i] )
      {
        result = 4294967294LL;
        goto LABEL_13;
      }
    }
    sub_410CC0("continue!");
    memset(v18, 0, 65);
    sub_4406E0(0LL, v18, 64LL);
    v18[39] = 0;
    if ( sub_424BA0(v18) == 39 )
    {
      v2 = sub_400E44(v18);
      v3 = sub_400E44(v2);
      v4 = sub_400E44(v3);
      v5 = sub_400E44(v4);
      v6 = sub_400E44(v5);
      v7 = sub_400E44(v6);
      v8 = sub_400E44(v7);
      v9 = sub_400E44(v8);
      v10 = sub_400E44(v9);
      v11 = sub_400E44(v10);
      if ( !(unsigned int)sub_400360(v11, off_6CC090) )
      {
        sub_410CC0("You found me!!!");
        sub_410CC0("bye bye~");
      }
      result = 0LL;
    }
    else
    {
      result = 4294967293LL;
    }
  }
  else
  {
    result = 0xFFFFFFFFLL;
  }
LABEL_13:
  if ( __readfsqword(0x28u) != v19 )
    sub_444020();
  return result;
}
```

## CTF-Show

### Challenges

#### re2

```python
#!/usr/bin/python
#coding=utf-8

user = "DH~mqqvqxB^||zll@Jq~jkwpmvez{"

flag = ''
for x in range(0, 29):
    for y in range(256):
        if(ord(user[x])==y^0x1f):
            flag+=chr(y)

print(flag) #[Warnning]Access_Unauthorized
```

### 内部赛

#### 真的是签到

```
#include<stdio.h>
int main()
{
	int res[18]= { 0x6c,0x2f,0x30,0x31,0x32,0x33,0xffffffb6,0xffffffbf,0xffffffa0,0xffffffcf,0x7c,0x71,0x6a,0x6c,0x70,0x64,0x75,0x63 };
	for (int i = 17; i>=0; i--)
	{
		res[i] ^= 17-i;
		printf("%c", res[i]);
	}
	printf("\n");
	return 0;
}
// ctfshow{签到?????}
```

