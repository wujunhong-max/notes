# FFmpeg常见的结构体

##  最关键的结构体可以分成以下几类： 

### 1.解协议（http,rtsp,rtmp,mms） 

 AVIOContext，URLProtocol，URLContext主要**存储视音频使用的协议的类型以及状态**。URLProtocol**存储输入视音频使用的封装格式**。每种协议都对应一个URLProtocol结构。（注意：FFMPEG中文件也被当做一种协议“file”） 

### 2. 解封装（flv,avi,rmvb,mp4） 

 AVFormatContext主要**存储视音频封装格式中包含的信息**；AVInputFormat存储**输入视音频使用的封装格式**。每种视音频封装格式都对应一个AVInputFormat 结构。 输入文件格式结构体AVInputFormat，输出文件结构体AVOutputFormat

### 3. 解码（h264,mpeg2,aac,mp3） 

 每个AVStream存储**一个视频/音频流的相关数据**；每个AVStream对应一个AVCodecContext，**存储该视频/音频流使用解码方式的相关数据**；每个AVCodecContext中对应一个AVCodec，**包含该视频/音频对应的解码器**。每种解码器都对应一个AVCodec结构。 

### 4. 存数据 

视频的话，每个结构一般是存一帧；音频可能有好几帧

解码前数据：AVPacket

解码后数据：AVFrame

## AVFormatContext

 这个结构体描述了一个媒体文件或媒体流的构成和基本信息

 下面看几个主要变量的作用（在这里考虑解码的情况）： 

```c
AVIOContext *pb：输入数据的缓存

unsigned int nb_streams：视音频流的个数

AVStream **streams：视音频流

char filename[1024]：文件名

int64_t duration：时长（单位：微秒us，转换为秒需要除以1000000）

int bit_rate：比特率（单位bps，转换为kbps需要除以1000）

AVDictionary *metadata：元数据
```

 视频的时长可以转换成HH:MM:SS(时:分:秒)的形式，示例代码如下： 

```c
AVFormatContext *pFormatCtx;
CString timelong;
...
//duration是以微秒为单位
//转换成hh:mm:ss形式
int tns, thh, tmm, tss;
tns  = (pFormatCtx->duration)/1000000;
thh  = tns / 3600;
tmm  = (tns % 3600) / 60;
tss  = (tns % 60);
timelong.Format("%02d:%02d:%02d",thh,tmm,tss);
```

 视频的原数据（metadata）信息可以通过AVDictionary获取。元数据存储在AVDictionaryEntry结构体中，如下所示 

```c
typedef struct AVDictionaryEntry {
    char *key;
    char *value;
} AVDictionaryEntry;
```

每一条元数据分为key和value两个属性。

在ffmpeg中通过av_dict_get()函数获得视频的原数据。

 下列代码显示了获取元数据并存入meta字符串变量的过程，注意每一条key和value之间有一个"\t:"，value之后有一个"\r\n" 

```c
//MetaData------------------------------------------------------------
//从AVDictionary获得
//需要用到AVDictionaryEntry对象
//CString author,copyright,description;
CString meta=NULL,key,value;
AVDictionaryEntry *m = NULL;
//不用一个一个找出来
/*	m=av_dict_get(pFormatCtx->metadata,"author",m,0);
author.Format("作者：%s",m->value);
m=av_dict_get(pFormatCtx->metadata,"copyright",m,0);
copyright.Format("版权：%s",m->value);
m=av_dict_get(pFormatCtx->metadata,"description",m,0);
description.Format("描述：%s",m->value);
*/
//使用循环读出
//(需要读取的数据，字段名称，前一条字段（循环时使用），参数)
while(m=av_dict_get(pFormatCtx->metadata,"",m,AV_DICT_IGNORE_SUFFIX)){
	key.Format(m->key);
	value.Format(m->value);
	meta+=key+"\t:"+value+"\r\n" ;
}
```

## AVPacket

 **存储压缩编码数据相关信息的结构体 **

 结构体的定义（位于avcodec.h文件中 )

 在AVPacket结构体中，重要的变量有以下几个： 

```c
uint8_t *data：压缩编码的数据。

例如对于H.264来说。1个AVPacket的data通常对应一个NAL。

注意：在这里只是对应，而不是一模一样。他们之间有微小的差别：使用FFMPEG类库分离出多媒体文件中的H.264码流

因此在使用FFMPEG进行视音频处理的时候，常常可以将得到的AVPacket的data数据直接写成文件，从而得到视音频的码流文件。

int   size：data的大小

int64_t pts：显示时间戳

int64_t dts：解码时间戳

int   stream_index：标识该AVPacket所属的视频/音频流。
```

## AVFrame

  AVFrame结构体一般用于**存储原始数据**（即非压缩数据，例如对视频来说是YUV，RGB，对音频来说是PCM） 

 此外还包含了一些相关的信息。比如说，解码的时候存储了宏块类型表，QP表，运动矢量表等数据。编码的时候也存储了相关的数据。因此在使用FFMPEG进行码流分析的时候，AVFrame是一个很重要的结构体。 

 下面看几个主要变量的作用（在这里考虑解码的情况）： 

```c
uint8_t *data[AV_NUM_DATA_POINTERS]：解码后原始数据（对视频来说是YUV，RGB，对音频来说是PCM）

int linesize[AV_NUM_DATA_POINTERS]：data中“一行”数据的大小。注意：未必等于图像的宽，一般大于图像的宽。

int width, height：视频帧宽和高（1920x1080,1280x720...）

int nb_samples：音频的一个AVFrame中可能包含多个音频帧，在此标记包含了几个

int format：解码后原始数据类型（YUV420，YUV422，RGB24...）

int key_frame：是否是关键帧

enum AVPictureType pict_type：帧类型（I,B,P...）

AVRational sample_aspect_ratio：宽高比（16:9，4:3...）

int64_t pts：显示时间戳

int coded_picture_number：编码帧序号

int display_picture_number：显示帧序号

int8_t *qscale_table：QP表

uint8_t *mbskip_table：跳过宏块表

int16_t (*motion_val[2])[2]：运动矢量表

uint32_t *mb_type：宏块类型表

short *dct_coeff：DCT系数，这个没有提取过

int8_t *ref_index[2]：运动估计参考帧列表（貌似H.264这种比较新的标准才会涉及到多参考帧）

int interlaced_frame：是否是隔行扫描

uint8_t motion_subsample_log2：一个宏块中的运动矢量采样个数，取log的
```

#### 1.data[ ]

对于packed格式的数据（例如RGB24），会存到data[0]里面。

对于planar格式的数据（例如YUV420P），则会分开成data[0]，data[1]，data[2]...（YUV420P中data[0]存Y，data[1]存U，data[2]存V）

 FFmpeg音频解码后的数据是存放在AVFrame结构中的。 Packed格式，frame.data[0]或frame.extended_data[0]包含所有的音频数据中。 Planar格式，frame.data[i]或者frame.extended_data[i]表示第i个声道的数据（假设声道0是第一个）, AVFrame.data数组大小固定为8，如果声道数超过8，需要从frame.extended_data获取声道数据。 

## AVStream

 其中AVStream是存储**每一个视频/音频流信息**的结构体 

 结构体的定义（位于avformat.h文件中）

 AVStream重要的变量如下所示： 

```c
int index：标识该视频/音频流

AVCodecContext *codec：指向该视频/音频流的AVCodecContext（它们是一一对应的关系）

AVRational time_base：时基。通过该值可以把PTS，DTS转化为真正的时间。FFMPEG其他结构体中也有这个字段，但是根据我的经验，只有AVStream中的time_base是可用的。PTS*time_base=真正的时间

int64_t duration：该视频/音频流长度

AVDictionary *metadata：元数据信息

AVRational avg_frame_rate：帧率（注：对视频来说，这个挺重要的）

AVPacket attached_pic：附带的图片。比如说一些MP3，AAC音频文件附带的专辑封面。
```

## AVCodecContext

 结构体的定义（位于avcodec.h） 

```c
enum AVMediaType codec_type：编解码器的类型（视频，音频...）

struct AVCodec  *codec：采用的解码器AVCodec（H.264,MPEG2...）

int bit_rate：平均比特率

uint8_t *extradata; int extradata_size：针对特定编码器包含的附加信息（例如对于H.264解码器来说，存储SPS，PPS等）

AVRational time_base：根据该参数，可以把PTS转化为实际的时间（单位为秒s）

int width, height：如果是视频的话，代表宽和高

int refs：运动估计参考帧的个数（H.264的话会有多帧，MPEG2这类的一般就没有了）

int sample_rate：采样率（音频）

int channels：声道数（音频）

enum AVSampleFormat sample_fmt：采样格式

int profile：型（H.264里面就有，其他编码标准应该也有）

int level：级（和profile差不太多）
```

 在这里需要注意：AVCodecContext中很多的参数是编码的时候使用的，而不是解码的时候使用的。 

###  **1.codec_type** 

 编解码器类型有以下几种： 

```c
enum AVMediaType {
    AVMEDIA_TYPE_UNKNOWN = -1,  ///< Usually treated as AVMEDIA_TYPE_DATA
    AVMEDIA_TYPE_VIDEO,
    AVMEDIA_TYPE_AUDIO,
    AVMEDIA_TYPE_DATA,          ///< Opaque data information usually continuous
    AVMEDIA_TYPE_SUBTITLE,
    AVMEDIA_TYPE_ATTACHMENT,    ///< Opaque data information usually sparse
    AVMEDIA_TYPE_NB
};
```

### 2.sample_fmt

 在FFMPEG中音频采样格式有以下几种： 

```c
enum AVSampleFormat {
    AV_SAMPLE_FMT_NONE = -1,
    AV_SAMPLE_FMT_U8,          ///< unsigned 8 bits
    AV_SAMPLE_FMT_S16,         ///< signed 16 bits
    AV_SAMPLE_FMT_S32,         ///< signed 32 bits
    AV_SAMPLE_FMT_FLT,         ///< float
    AV_SAMPLE_FMT_DBL,         ///< double
 
    AV_SAMPLE_FMT_U8P,         ///< unsigned 8 bits, planar
    AV_SAMPLE_FMT_S16P,        ///< signed 16 bits, planar
    AV_SAMPLE_FMT_S32P,        ///< signed 32 bits, planar
    AV_SAMPLE_FMT_FLTP,        ///< float, planar
    AV_SAMPLE_FMT_DBLP,        ///< double, planar
 
    AV_SAMPLE_FMT_NB           ///< Number of sample formats. DO NOT USE if linking dynamically
};
```

### 3.profile

 在FFMPEG中型有以下几种，可以看出AAC，MPEG2，H.264，VC-1，MPEG4都有型的概念。 

```c
#define FF_PROFILE_UNKNOWN -99
#define FF_PROFILE_RESERVED -100
 
#define FF_PROFILE_AAC_MAIN 0
#define FF_PROFILE_AAC_LOW  1
#define FF_PROFILE_AAC_SSR  2
#define FF_PROFILE_AAC_LTP  3
#define FF_PROFILE_AAC_HE   4
#define FF_PROFILE_AAC_HE_V2 28
#define FF_PROFILE_AAC_LD   22
#define FF_PROFILE_AAC_ELD  38
 
#define FF_PROFILE_DTS         20
#define FF_PROFILE_DTS_ES      30
#define FF_PROFILE_DTS_96_24   40
#define FF_PROFILE_DTS_HD_HRA  50
#define FF_PROFILE_DTS_HD_MA   60
 
#define FF_PROFILE_MPEG2_422    0
#define FF_PROFILE_MPEG2_HIGH   1
#define FF_PROFILE_MPEG2_SS     2
#define FF_PROFILE_MPEG2_SNR_SCALABLE  3
#define FF_PROFILE_MPEG2_MAIN   4
#define FF_PROFILE_MPEG2_SIMPLE 5
 
#define FF_PROFILE_H264_CONSTRAINED  (1<<9)  // 8+1; constraint_set1_flag
#define FF_PROFILE_H264_INTRA        (1<<11) // 8+3; constraint_set3_flag
 
#define FF_PROFILE_H264_BASELINE             66
#define FF_PROFILE_H264_CONSTRAINED_BASELINE (66|FF_PROFILE_H264_CONSTRAINED)
#define FF_PROFILE_H264_MAIN                 77
#define FF_PROFILE_H264_EXTENDED             88
#define FF_PROFILE_H264_HIGH                 100
#define FF_PROFILE_H264_HIGH_10              110
#define FF_PROFILE_H264_HIGH_10_INTRA        (110|FF_PROFILE_H264_INTRA)
#define FF_PROFILE_H264_HIGH_422             122
#define FF_PROFILE_H264_HIGH_422_INTRA       (122|FF_PROFILE_H264_INTRA)
#define FF_PROFILE_H264_HIGH_444             144
#define FF_PROFILE_H264_HIGH_444_PREDICTIVE  244
#define FF_PROFILE_H264_HIGH_444_INTRA       (244|FF_PROFILE_H264_INTRA)
#define FF_PROFILE_H264_CAVLC_444            44
 
#define FF_PROFILE_VC1_SIMPLE   0
#define FF_PROFILE_VC1_MAIN     1
#define FF_PROFILE_VC1_COMPLEX  2
#define FF_PROFILE_VC1_ADVANCED 3
 
#define FF_PROFILE_MPEG4_SIMPLE                     0
#define FF_PROFILE_MPEG4_SIMPLE_SCALABLE            1
#define FF_PROFILE_MPEG4_CORE                       2
#define FF_PROFILE_MPEG4_MAIN                       3
#define FF_PROFILE_MPEG4_N_BIT                      4
#define FF_PROFILE_MPEG4_SCALABLE_TEXTURE           5
#define FF_PROFILE_MPEG4_SIMPLE_FACE_ANIMATION      6
#define FF_PROFILE_MPEG4_BASIC_ANIMATED_TEXTURE     7
#define FF_PROFILE_MPEG4_HYBRID                     8
#define FF_PROFILE_MPEG4_ADVANCED_REAL_TIME         9
#define FF_PROFILE_MPEG4_CORE_SCALABLE             10
#define FF_PROFILE_MPEG4_ADVANCED_CODING           11
#define FF_PROFILE_MPEG4_ADVANCED_CORE             12
#define FF_PROFILE_MPEG4_ADVANCED_SCALABLE_TEXTURE 13
#define FF_PROFILE_MPEG4_SIMPLE_STUDIO             14
#define FF_PROFILE_MPEG4_ADVANCED_SIMPLE           15
```

## AVCodec

 其中AVCodec是**存储编解码器信息**的结构体 

 结构体的定义（位于avcodec.h文件中） 

 下面说一下最主要的几个变量： 

```c
const char *name：编解码器的名字，比较短

const char *long_name：编解码器的名字，全称，比较长

enum AVMediaType type：指明了类型，是视频，音频，还是字幕

enum AVCodecID id：ID，不重复

const AVRational *supported_framerates：支持的帧率（仅视频）

const enum AVPixelFormat *pix_fmts：支持的像素格式（仅视频）

const int *supported_samplerates：支持的采样率（仅音频）

const enum AVSampleFormat *sample_fmts：支持的采样格式（仅音频）

const uint64_t *channel_layouts：支持的声道数（仅音频）

int priv_data_size：私有数据的大小
```

 详细介绍几个变量： 

### 1.enum AVMediaType type 

 AVMediaType定义如下： 

```c
enum AVMediaType {
    AVMEDIA_TYPE_UNKNOWN = -1,  ///< Usually treated as AVMEDIA_TYPE_DATA
    AVMEDIA_TYPE_VIDEO,
    AVMEDIA_TYPE_AUDIO,
    AVMEDIA_TYPE_DATA,          ///< Opaque data information usually continuous
    AVMEDIA_TYPE_SUBTITLE,
    AVMEDIA_TYPE_ATTACHMENT,    ///< Opaque data information usually sparse
    AVMEDIA_TYPE_NB
};
```

###  2.enum AVCodecID id 

 AVCodecID定义如下： 

```c
enum AVCodecID {
    AV_CODEC_ID_NONE,
 
    /* video codecs */
    AV_CODEC_ID_MPEG1VIDEO,
    AV_CODEC_ID_MPEG2VIDEO, ///< preferred ID for MPEG-1/2 video decoding
    AV_CODEC_ID_MPEG2VIDEO_XVMC,
    AV_CODEC_ID_H261,
    AV_CODEC_ID_H263,
    AV_CODEC_ID_RV10,
    AV_CODEC_ID_RV20,
    AV_CODEC_ID_MJPEG,
    AV_CODEC_ID_MJPEGB,
    AV_CODEC_ID_LJPEG,
    AV_CODEC_ID_SP5X,
    AV_CODEC_ID_JPEGLS,
    AV_CODEC_ID_MPEG4,
    AV_CODEC_ID_RAWVIDEO,
    AV_CODEC_ID_MSMPEG4V1,
    AV_CODEC_ID_MSMPEG4V2,
    AV_CODEC_ID_MSMPEG4V3,
    AV_CODEC_ID_WMV1,
    AV_CODEC_ID_WMV2,
    AV_CODEC_ID_H263P,
    AV_CODEC_ID_H263I,
    AV_CODEC_ID_FLV1,
    AV_CODEC_ID_SVQ1,
    AV_CODEC_ID_SVQ3,
    AV_CODEC_ID_DVVIDEO,
    AV_CODEC_ID_HUFFYUV,
    AV_CODEC_ID_CYUV,
    AV_CODEC_ID_H264,
    ...（代码太长，略）
}
```

### 3.const enum AVPixelFormat *pix_fmts 

 AVPixelFormat定义如下： 

```c
enum AVPixelFormat {
    AV_PIX_FMT_NONE = -1,
    AV_PIX_FMT_YUV420P,   ///< planar YUV 4:2:0, 12bpp, (1 Cr & Cb sample per 2x2 Y samples)
    AV_PIX_FMT_YUYV422,   ///< packed YUV 4:2:2, 16bpp, Y0 Cb Y1 Cr
    AV_PIX_FMT_RGB24,     ///< packed RGB 8:8:8, 24bpp, RGBRGB...
    AV_PIX_FMT_BGR24,     ///< packed RGB 8:8:8, 24bpp, BGRBGR...
    AV_PIX_FMT_YUV422P,   ///< planar YUV 4:2:2, 16bpp, (1 Cr & Cb sample per 2x1 Y samples)
    AV_PIX_FMT_YUV444P,   ///< planar YUV 4:4:4, 24bpp, (1 Cr & Cb sample per 1x1 Y samples)
    AV_PIX_FMT_YUV410P,   ///< planar YUV 4:1:0,  9bpp, (1 Cr & Cb sample per 4x4 Y samples)
    AV_PIX_FMT_YUV411P,   ///< planar YUV 4:1:1, 12bpp, (1 Cr & Cb sample per 4x1 Y samples)
    AV_PIX_FMT_GRAY8,     ///<        Y        ,  8bpp
    AV_PIX_FMT_MONOWHITE, ///<        Y        ,  1bpp, 0 is white, 1 is black, in each byte pixels are ordered from the msb to the lsb
    AV_PIX_FMT_MONOBLACK, ///<        Y        ,  1bpp, 0 is black, 1 is white, in each byte pixels are ordered from the msb to the lsb
    AV_PIX_FMT_PAL8,      ///< 8 bit with PIX_FMT_RGB32 palette
    AV_PIX_FMT_YUVJ420P,  ///< planar YUV 4:2:0, 12bpp, full scale (JPEG), deprecated in favor of PIX_FMT_YUV420P and setting color_range
    AV_PIX_FMT_YUVJ422P,  ///< planar YUV 4:2:2, 16bpp, full scale (JPEG), deprecated in favor of PIX_FMT_YUV422P and setting color_range
    AV_PIX_FMT_YUVJ444P,  ///< planar YUV 4:4:4, 24bpp, full scale (JPEG), deprecated in favor of PIX_FMT_YUV444P and setting color_range
    AV_PIX_FMT_XVMC_MPEG2_MC,///< XVideo Motion Acceleration via common packet passing
    AV_PIX_FMT_XVMC_MPEG2_IDCT,
    ...（代码太长，略）
}
```

###  4.const enum AVSampleFormat *sample_fmts 

```c
enum AVSampleFormat {
    AV_SAMPLE_FMT_NONE = -1,
    AV_SAMPLE_FMT_U8,          ///< unsigned 8 bits
    AV_SAMPLE_FMT_S16,         ///< signed 16 bits
    AV_SAMPLE_FMT_S32,         ///< signed 32 bits
    AV_SAMPLE_FMT_FLT,         ///< float
    AV_SAMPLE_FMT_DBL,         ///< double
 
    AV_SAMPLE_FMT_U8P,         ///< unsigned 8 bits, planar
    AV_SAMPLE_FMT_S16P,        ///< signed 16 bits, planar
    AV_SAMPLE_FMT_S32P,        ///< signed 32 bits, planar
    AV_SAMPLE_FMT_FLTP,        ///< float, planar
    AV_SAMPLE_FMT_DBLP,        ///< double, planar
 
    AV_SAMPLE_FMT_NB           ///< Number of sample formats. DO NOT USE if linking dynamically
};
```

 每一个编解码器对应一个该结构体 

下面简单介绍一下遍历ffmpeg中的解码器信息的方法（这些解码器以一个链表的形式存储）：
1.注册所有编解码器：av_register_all();

2.声明一个AVCodec类型的指针，比如说AVCodec* first_c;

3.调用av_codec_next()函数，即可获得指向链表下一个解码器的指针，循环往复可以获得所有解码器的信息。注意，如果想要获得指向第一个解码器的指针，则需要将该函数的参数设置为NULL。

## AVIOContext

 AVIOContext是FFMPEG管理输入输出数据的结构体 

 结构体的定义（位于avio.h） 

 AVIOContext中有以下几个变量比较重要： 

```c
unsigned char *buffer：缓存开始位置

int buffer_size：缓存大小（默认32768）

unsigned char *buf_ptr：当前指针读取到的位置

unsigned char *buf_end：缓存结束的位置

void *opaque：URLContext结构体
```

 在解码的情况下，buffer用于存储ffmpeg读入的数据。例如打开一个视频文件的时候，先把数据从硬盘读入buffer，然后在送给解码器用于解码。 

## 总结

```c
AVFormatContext：统领全局的基本结构体。主要用于处理封装格式（FLV/MKV/RMVB等）。

AVIOContext：输入输出对应的结构体，用于输入输出（读写文件，RTMP协议等）。

AVStream，AVCodecContext：视音频流对应的结构体，用于视音频编解码。

AVFrame：存储非压缩的数据（视频对应RGB/YUV像素数据，音频对应PCM采样数据）

AVPacket：存储压缩数据（视频对应H.264等码流数据，音频对应AAC/MP3等码流数据）
```

| 结构体          | 初始化函数                              | 销毁函数                |
| --------------- | --------------------------------------- | ----------------------- |
| AVFormatContext | avformat_alloc_context()                | avformat_free_context() |
| AVIOContext     | avio_alloc_context()                    |                         |
| AVStream        | avformat_new_stream()                   |                         |
| AVCodecContext  | avcodec_alloc_context3()                |                         |
| AVFrame         | av_frame_alloc();av_image_fill_arrays() | av_frame_free()         |
| AVPacket        | av_init_packet();av_new_packet()        | av_free_packet()        |

