# FFmpeg

是一个音视频处理的开源库，提供了C接口用于音视频的编解码、封装、流处理，可以允许音频和视频多种格式的录影、转换、流功能。

包含了libavcodec---------- 音频和视频的解码器库

libavformat------------音频与视频格式转换库



## 命令行工具的使用

### ffprobe

是用于查看媒体文件头信息的工具

常用命令有：

> ```
> ffprobe INPUT
> ffprobe -show_format INPUT
> ffprobe -show_streams INPUT
> ffprobe -show_frames INPUT
> ffprobe -show_packets INPUT
> ...
> ```

show_format 用于查看文件格式、时长、码率等信息，较为简略；

show_streams 用于查看视频流、音频流的信息，包括编码器、帧率、采样率、宽高、像素格式、采样格式、码率、时长、总帧率等等，较为详细，是最常用的一个功能；

show_frames、show_packets 用于查看每一帧（解码前/解码后）的信息，可以配合 select_streams 使用；

### ffplay

是用于播放媒体文件的工具

常用命令有：

> ```
> ffplay INPUT -loop 10 // 循环播放 10 次
> ffplay INPUT -ast 1 // 播放视频中的第一路音频流
> ffplay INPUT -vst 1 // 播放视频中的第一路视频流
> ffplay INPUT -x WIDTH -y HEIGHT // 指定宽高播放
> ...
> ```
>
> 播放原始音频/视频数据：
>
> ```
> ffplay INPUT.pcm -f s16le -channels 2 -ar 44100
> ffplay -f rawvideo -pixel_format yuv420p -s 480*480 INPUT.yuv(或 rgb)
> ```
>
> 指定播放过程中音视频同步的方式：
>
> ```
> // 以音频（或视频、或外部时钟）作为基准进行音视频同步
> ffplay INPUT -sync audio(或 video、ext) 
> ```

### ffmpeg

是强大的媒体文件转换工具，常用于转码，编码器、视频时长、帧率、分辨率、像素格式、采样格式、码率、裁剪选项、声道数等等都可以自由选择

> ```
>  ffmpeg -i INPUT -codec:v h264 -codec:a aac -s 644x360 OUTPUT
> ```

### 通用选项

用于查看 ffmpeg 支持的编解码器、像素格式、采样格式等信息

> ```
> ffmpeg -encoders
> ffprobe -sample_fmts
> ffplay -pix_fmts
> ```

## FFmpeg源码结构

最关键的结构体可以分成以下几类：

a)        解协议（http,rtsp,rtmp,mms）

AVIOContext，URLProtocol，URLContext主要存储视音频使用的协议的类型以及状态。URLProtocol存储输入视音频使用的封装格式。每种协议都对应一个URLProtocol结构。（注意：FFMPEG中文件也被当做一种协议“file”）

b)        解封装（flv,avi,rmvb,mp4）

AVFormatContext主要存储视音频封装格式中包含的信息；AVInputFormat存储输入视音频使用的封装格式。每种视音频封装格式都对应一个AVInputFormat 结构。

c)        解码（h264,mpeg2,aac,mp3）

每个AVStream存储一个视频/音频流的相关数据；每个AVStream对应一个AVCodecContext，存储该视频/音频流使用解码方式的相关数据；每个AVCodecContext中对应一个AVCodec，包含该视频/音频对应的解码器。每种解码器都对应一个AVCodec结构。

d) 存数据

视频的话，每个结构一般是存一帧；音频可能有好几帧

解码前数据：AVPacket

解码后数据：AVFrame
他们之间的对应关系如下所示：

![img](https://img-blog.csdn.net/20130914204051125?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbGVpeGlhb2h1YTEwMjA=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)



## 推流和拉流

![img](https://upload-images.jianshu.io/upload_images/1682758-4b8fe91be5f3155b.png?imageMogr2/auto-orient/strip|imageView2/2/w/647)

### 概念

**推流**：指的是把采集阶段封包好的内容传输到服务器的过程

目前主流的推送协议：

- RTMP
- HLS
- WebRTC

**拉流**：是指服务器已有直播内容，用指定地址进行拉取的过程

![img](https://upload-images.jianshu.io/upload_images/1682758-713196b9d07cec45.png?imageMogr2/auto-orient/strip|imageView2/2/w/1143)

推流是直播端，拉流是客户端

## RTMP、RTSP、HTTP视频协议详解

都属于互联网 **TCP/IP** 五层体系结构中应用层的协议。理论上这三种都可以用来做视频直播或点播。但通常来说，直播一般用 **RTMP**、**RTSP**。而点播用 **HTTP**


### **RTMP协议**

（1）是流媒体协议。

（2）RTMP协议是 **Adobe** 的私有协议，未完全公开。

（3）RTMP协议一般传输的是 **flv**，**f4v** 格式流。

（4）RTMP一般在 **TCP** **1**个通道上传输命令和数据

###  **RTSP协议**

（1）是流媒体协议。

（2）RTSP协议是共有协议，并有专门机构做维护。.

（3）RTSP协议一般传输的是 **ts**、**mp4** 格式的流。

（4）RTSP传输一般需要 **2-3** 个通道，命令和数据通道分离。

### **HTTP协议**

（1）不是是流媒体协议。

（2）HTTP协议是共有协议，并有专门机构做维护。 

（3）HTTP协议没有特定的传输流。 

（4）HTTP传输一般需要 **2-3** 个通道，命令和数据通道分离。

## FFmpeg的常用命令和参数

>```
>-i		设置输入的文档名或路径
>-y		覆盖输出的同名文档
>-vcodec和-acodec分别是指定视频解码器和音频解码器
>-s 		指定输出文档的分辨率
>-r		指定输出文档的帧数
>-b		指定压缩比特率
>-an和-vn		是表示不输出音频和视频
>-ss		搜索到指定时间处
>
>-f concat		表示输出格式为concat格式，即filelist.txt中的格式，用来连接视频，用法为：
>ffmpge -f concat -safe 0 -i filelist.txt -c copy output.mp4
>其中-safe 0表示不检查filelist.txt中的文档格式，如果是绝对路径，则必须加上，如果是相对路径就不用，推荐加上
>//直接使用"/"代表从根目录开始的目录路径，这个叫绝对路径
>//填写目录时候以填写目录文件为参考，使用“../”或"./"指向上一级 或 使用"../../"指向上上一级叫相对路径
>
>-sn 取消字幕
>-title 添加标题
>-author 添加作者
>-copyright 添加版权信息
>-comment 添加评论
>```

## ffmpy的安装调用

在命令行下`pip install ffmpy3`即可安装，安装后在python下`import ffmpy3`或`from ffmpy3 import FFmpeg` 导入包。

注：python调用FFmpeg实际上是通过ffmpy调用命令行，输入参数后通过命令行调用FFmpeg，和在命令行下使用FFmpeg一样

官方文档：https://ffmpy3.readthedocs.io/en/latest/

```python
import ffmpy3
from ffmpy3 import FFmpeg

if __name__ == '__main__':

    ff = ffmpy3.FFmpeg(

    inputs = {'input.mp4': None},

    outputs = {'output.avi': None }
         )
    print(ff.cmd)		# 可以打印出在cmd中的命令
    ff.run()			# 执行命令
    
 输出结果：ffmpeg -i input.mp4 output.avi
```

# 音视频编解码

## 1.图像与编码



# 实现视频播放器

## 流程

- 拉流
- 解析输入
- 打开码流
- 音视频队列
- 音视频解码
- 播放控制   
  - 开始播放
  - 停止播放
  - 暂停播放
  - 跳到（seek）指定位置播放
- 音频输出
- 视频输出
- ffplay快捷键支持

## 第三方库

1.FFMPEG 用来读取码流以及解码

2.SDL2 用来进行视频渲染和音频播放

## 前置知识

首先要了解音视频的一些基本知识，平常所说的MP4，mkv文件是一个音视频封装文件，里面一般包含音频视频两条流，每条流存储着编码信息以及展示时间基等信息。

## 播放器的流程图

首先从服务器拉流，或者从本地打开视频文件（用FFmpeg处理时接口都一样，只是提供的地址不一样）。打开之后进行解封装，每次读取一个packet，是音频则解码成音频帧，视频则解码成视频帧。再对音视频帧做一个转换，转换成可以播放和渲染的格式，进行播放。

![img](FFmpeg.assets/v2-b2879503901bf6ffffae4224d48f8999_720w.jpg)

## 程序的流程图

首先需要写好Qt  UI，对FFmpeg进行初始化，对SDL进行初始化，然后打开输入源，同时打开相应的解码器，设置播放格式，根据输入源格式和播放格式创建转换器。再创建音视频播放线程，接着就可以开始读文件了，每次读到一个packet就根据stream_index判断是否为音视频，是音频则放入音频解码器解码成音频帧，再转换格式，送入音频缓存中，是视频则放入视频解码器并转换。再继续读下一packet.音视频播放则由不同的线程完成，所以还需要时间同步。一般而言以音频为准，视频根据音频的播放时间进行渲染

![img](FFmpeg.assets/v2-84803dabb9599771f325fb5c429cbfab_720w.jpg)

![img](FFmpeg.assets/v2-cfd0f62ba24189b453e307d7c732624a_720w.jpg)

## ![img](FFmpeg.assets/6285199-678bbc3d7b853682.jpg)代码实现

（1）注册FFmpeg组件

//注册和初始化FFmpeg封装器和网络设备

（2）打开文件和创建输入设备

AVFormatContext 表示一个封装器，在读取多媒体文件的时候，它负责保存与封装和编解码有关的上下文信息

（3）遍历流并初始化解码器

封装器中保存了各种流媒体的通道，通常视频通道为0，音频通道为1。除此以外可能还包含字幕流通道等。

第2步和第3步基本就是打开多媒体文件的主要步骤，

解码和转码的所有参数都可以在这里获取。

（4）读取压缩数据

/*之所以称为压缩数据主要是为了区分AVPacket和AVFrame两个结构体。

AVPacket表示一幅经过了关键帧或过渡帧编码后的画面，

AVFrame表示一个AVPacket经过解码后的完整YUV画面*/

（5）解码

（6）视频转码

// 720p输出标准

/*

这里需要解释一下outWidth * outHeight * 4计算理由：

720p标准的视频画面包含720 * 480个像素点，

每一个像素点包含了RGBA4类数据，每一类数据分别由1个byte即8个bit表示。

因此一幅完整画面所占的大小为outWidth * outHeight * 4。

（7）音频转码





# python ctypes 模块

这个模块是Python内建的用于调用**动态链接库函数**的功能模块，一定程度上可以用于Python与其他语言的混合编程。

这是Python标准库自带的。

ctypes有以下优点：

- Python内建，不需要单独安装
- 可以直接调用二进制的动态链接库 
- 在Python一侧，不需要了解Python内部的工作方式
- 在C/C++一侧，也不需要了解Python内部的工作方式
- 对基本类型的相互映射有良好的支持

有以下缺点：

- 平台兼容性差
- 不能够直接调用动态链接库中未经导出的函数或变量
- 对C++的支持差 

## ctypes数据类型

它定义了专有的数据类型来衔接这两种编程语言。如下表，

None：对应 C 中的 NULL

int, long： 对应 C 中的 int，具体实现时会根据机器字长自动适配。

Byte String：对应 C 中的一个字符串指针 char * ，指向一块内存区域。

Unicode String ：对应 C 中一个宽字符串指针 wchar_t *，指向一块内存区域 

![img](FFmpeg.assets/986259-20171129140831581-1373706197.png)



# python subprocess模块

套壳命令行模块

# PyAv









