> 参考大佬博客：[《王道操作系统》学习笔记总目录+思维导图][Link 1]  
> b站王道操作系统：[王道计算机考研 操作系统][Link 2]  
> 操作系统系列目录：  
> [第一章：操作系统引论][Link 3]  
> [第二章：进程的描述与控制][Link 4]  
> [第三章：处理机调度与死锁][Link 5]  
> [第四章：存储器管理][Link 5]  
> [第五章：虚拟存储器][Link 6]  
> [第六章：输入输出系统][Link 7]  
> [第七章：文件管理][Link 7]

#### 输入输出系统 

 *  [一、I/O管理概述][I_O]
 *   *  [1.什么是I/O设备？有几类I/O设备？][1._I_O_I_O]
     *  [2.控制I/O设备的I/O控制器][2._I_O_I_O]
     *  [3.控制I/O设备的几种方式？(程序直接控制方式、中断驱动方式、DMA、通道控制)][3._I_O_DMA]
     *  [4. I/O软件的层次结构（用户层软件-设备独立性软件-设备驱动程序-中断处理程序-硬件）][4. I_O_-_-_-_-]
 *  [二、 I/O核心子系统][I_O 1]
 *   *  [1. 内核的I/O核心子系统及功能][1. _I_O]
     *  [2. I/O设备假脱机技术(SPOOLing)][2. I_O_SPOOLing]
     *  [3.I/O设备的分配与回收（DCT-COCT-CHCT-SDT）][3.I_O_DCT-COCT-CHCT-SDT]
     *  [4. 缓冲区管理（单缓冲-双缓冲-循环缓冲-缓冲池）][4. _-_-_-]

## 一、I/O管理概述 

### 1.什么是I/O设备？有几类I/O设备？ 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0614880b63a8c7a56fd1010bb74edb8a.png)

> 参考博客：[什么是I/O设备？有几类I/O设备？][I_O_I_O]

  
  
  
  


### 2.控制I/O设备的I/O控制器 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ee156cb51cf4c142f2bc29b7ea703e50.png)

> 参考博客：[控制I/O设备的I/O控制器][I_O_I_O 1]

  
  
  
  


### 3.控制I/O设备的几种方式？(程序直接控制方式、中断驱动方式、DMA、通道控制) 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/862e9964ec975dc144729d38006cbd2c.png)

> 参考博客：[控制I/O设备的几种方式？(程序直接控制方式、中断驱动方式、DMA、通道控制)][I_O_DMA]

  
  
  
  


### 4. I/O软件的层次结构（用户层软件-设备独立性软件-设备驱动程序-中断处理程序-硬件） 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dc22df5ba23e2ea0bff4b3c9ca49bf6e.png)

> 参考博客：[I/O软件的层次结构（用户层软件-设备独立性软件-设备驱动程序-中断处理程序）][I_O_-_-_-]

  
  
  
  


## 二、 I/O核心子系统 

### 1. 内核的I/O核心子系统及功能 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7401edf8d10f28571e6a7c9f0d867b78.png)

> 参考博客：[内核的I/O核心子系统及功能][I_O 2]

  
  
  
  


### 2. I/O设备假脱机技术(SPOOLing) 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/6567adf042bc3e8898b742d993852eca.png)

> 参考博客：[I/O设备假脱机技术(SPOOLing)][I_O_SPOOLing]

  
  
  
  


### 3.I/O设备的分配与回收（DCT-COCT-CHCT-SDT） 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1aec6039bb3c93419400868506569307.png)

> 参考博客：[I/O设备的分配与回收（DCT-COCT-CHCT-SDT）][I_O_DCT-COCT-CHCT-SDT]

  
  
  
  


### 4. 缓冲区管理（单缓冲-双缓冲-循环缓冲-缓冲池） 

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/776e3ce710d3730a12c11b788ef2bd9a.png)

> 参考博客：[缓冲区管理（单缓冲-双缓冲-循环缓冲-缓冲池）][-_-_-]


[Link 1]: https://blog.csdn.net/weixin_43914604/article/details/104415990?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163473008716780261954971%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=163473008716780261954971&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-104415990.first_rank_v2_pc_rank_v29&utm_term=%E7%8E%8B%E9%81%93%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F&spm=1018.2226.3001.4187
[Link 2]: https://www.bilibili.com/video/BV1YE411D7nH?p=63&spm_id_from=pageDriver
[Link 3]: https://blog.csdn.net/weixin_42214698/article/details/119898085
[Link 4]: https://blog.csdn.net/weixin_42214698/article/details/119927993
[Link 5]: https://blog.csdn.net/weixin_42214698/article/details/119980799
[Link 6]: https://blog.csdn.net/weixin_42214698/article/details/120875028
[Link 7]: https://blog.csdn.net/weixin_42214698/article/details/120875693
[I_O]: #IO_15
[1._I_O_I_O]: #1IOIO_18
[2._I_O_I_O]: #2IOIO_25
[3._I_O_DMA]: #3IODMA_34
[4. I_O_-_-_-_-]: #4_IO_43
[I_O 1]: #_IO_52
[1. _I_O]: #1_IO_55
[2. I_O_SPOOLing]: #2_IOSPOOLing_63
[3.I_O_DCT-COCT-CHCT-SDT]: #3IODCTCOCTCHCTSDT_72
[4. _-_-_-]: #4__80
[I_O_I_O]: https://blog.csdn.net/weixin_43914604/article/details/106136127
[I_O_I_O 1]: https://blog.csdn.net/weixin_43914604/article/details/106136990
[I_O_DMA]: https://blog.csdn.net/weixin_43914604/article/details/106144829
[I_O_-_-_-]: https://blog.csdn.net/weixin_43914604/article/details/106147270
[I_O 2]: https://blog.csdn.net/weixin_43914604/article/details/106147949
[I_O_SPOOLing]: https://blog.csdn.net/weixin_43914604/article/details/106150766
[I_O_DCT-COCT-CHCT-SDT]: https://blog.csdn.net/weixin_43914604/article/details/106151353
[-_-_-]: https://blog.csdn.net/weixin_43914604/article/details/106274269