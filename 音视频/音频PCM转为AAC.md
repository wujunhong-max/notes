# 音频PCM转为AAC

 PCM数据就是未被压缩的音频原始数据 ，而aac,mp3等都是被有损压缩后的数据。 

 未被压缩的pcm数据所占用的储存空间比较大，而被压缩后的PCM数据所占用的空间会比较小 

## 设置的压缩参数

```tcl
1.sample_rate: 采样率，也就是每秒采集多少次声音样本
2.channel:声道的数目，有单通道和双通道
3.sample_fmt:采样的格式
4.channel_layout:声道布局
5.bit_rate:比特率
需要将这些数据为AVCodecContext设置
```

## 主要流程

### 1.初始化输出环境

```c
// 初始化所有组件，只有调用了该函数，才能使用复用器和编解码器
  av_register_all();

//封装上下文AVFormatContext，该函数用于分配空间创建一个AVFormatContext对象，并且强调使用avformat_free_context方法来清理并释放该对象的空间。
AVFormatContext *ofmt_ctx = avformat_alloc_context();

//封装上下文内部结构体，这是一个决定视频输出时封装方式的函数,其中有三个参数，写任何一个参数，都会自动匹配相应的封装方式
AVOutputFormat *oformat =av_guess_format(NULL,output,NULL);

  if (oformat==NULL){
      // 日志输出的核心函数 av_log()
    av_log(NULL,AV_LOG_ERROR,"fail to find the output format\n");
    return -1;
  }
  if(avformat_alloc_output_context2(&ofmt_ctx,oformat,oformat->name,output) <0){
    av_log(NULL,AV_LOG_ERROR,"fail to alloc output context\n");
    return -1;
  } 
// 流结构体AVStream，创建输出流通道
  AVStream *out_stream = avformat_new_stream(ofmt_ctx,NULL);
  if (out_stream == NULL){
    av_log(NULL,AV_LOG_ERROR,"fail to create new stream\n");
    return -1;
  }
```

### 2.设置AAC编码格式

```c
// 设置AAC编码格式
  // AVCodecContext 相当于虚基类，需要用具体的编码器实现来给他赋值
  AVCodecContext *pCodecCtx = out_stream->codec; // 封装流参数
  //编码器的ID号
  pCodecCtx->codec_id = oformat->audio_codec;  // 编解码器的信息
  //编码器编码的数据类型
  pCodecCtx->codec_type = AVMEDIA_TYPE_AUDIO;  // 编解码器的信息
 //音频采样格式
  pCodecCtx->sample_fmt = AV_SAMPLE_FMT_FLTP; //其他会出错
  // 用来设置输出通道布局
  pCodecCtx->channel_layout = AV_CH_LAYOUT_MONO; 
  // 声道数，音频一般有双通道或者单通道之分
  pCodecCtx->channels = av_get_channel_layout_nb_channels(pCodecCtx->channel_layout); // 双通道
  // 采样频率 
  pCodecCtx->sample_rate = 44100; //8kHz(电话)、44.1kHz(CD)、48kHz(DVD)
  //目标的码率，即采样的码率
  pCodecCtx->bit_rate = 128000;
```

### 3.打开编码器并向输出文件中写入文件头信息

```c
/* 查找FFmpeg的编码器
   函数的参数是一个编码器的ID，返回查找到的编码器（没有找到就返回NULL）*/
AVCodec *pCodec = avcodec_find_encoder(pCodecCtx->codec_id);
  if (pCodec == NULL){
    av_log(NULL,AV_LOG_ERROR,"fail to find codec\n");
    return -1;
  }
 // 该函数用于初始化一个视音频编解码器的AVCodecContext
  if (avcodec_open2(pCodecCtx,pCodec,NULL) < 0){
    av_log(NULL,AV_LOG_ERROR,"fail to open codec\n");
    return -1;
  }
 // 打印流媒体的信息
  av_dump_format(ofmt_ctx,0,output,1);
// 打开FFmpeg的输入输出文件
  if (avio_open(&ofmt_ctx->pb,output,AVIO_FLAG_WRITE) < 0){
    av_log(NULL,AV_LOG_ERROR,"fail to open output\n");
    return -1;
  }
 // 用于写视频文件头
  if (avformat_write_header(ofmt_ctx,NULL) < 0){
    av_log(NULL,AV_LOG_ERROR,"fail to write header");
    return -1;
  }
```

### 4.设置一些参数，需要将pcm raw data 压缩为aac格式

```c
 // 用于AVFrame结构体的初始化
AVFrame *pframe = av_frame_alloc();
  pframe->channels = pCodecCtx->channels;
  pframe->format = pCodecCtx->sample_fmt;
  pframe->nb_samples = pCodecCtx->frame_size;
  //从文件中读取原始数据，缓冲区
  int size = av_samples_get_buffer_size(NULL,pCodecCtx->channels,pCodecCtx->frame_size,pCodecCtx->sample_fmt,1);
  uint8_t *out_buffer = (uint8_t*)av_malloc(size);
  avcodec_fill_audio_frame(pframe,pCodecCtx->channels,pCodecCtx->sample_fmt,(const uint8_t*)out_buffer,size,1);

  //新版本需要使用到转换参数，将读取的数据转换成输出的编码格式
  uint8_t  **data = (uint8_t**)av_calloc( pCodecCtx->channels,sizeof(*data) );
  av_samples_alloc(data,NULL,pCodecCtx->channels,pCodecCtx->frame_size,pCodecCtx->sample_fmt,1);
 
  SwrContext *pSwrCtx  = swr_alloc();
  swr_alloc_set_opts(pSwrCtx,pCodecCtx->channel_layout,pCodecCtx->sample_fmt,pCodecCtx->sample_rate,
      pCodecCtx->channel_layout,AV_SAMPLE_FMT_S16,44100,0,NULL);
  swr_init(pSwrCtx);
  //需要使用AVPacket进行压缩储存
  AVPacket *pkt = av_packet_alloc();
  av_new_packet(pkt,size);
  pkt->data = NULL;
  pkt->size = 0;
```

### 5. 读取pcm raw data并压缩为aac格式的数据写入输出文件中 

```c
int count = 1;
  while(1){
    //读取的长度要 和原始数据的采样率，采样格式以及通道有关 如果size设置的不对，会导致音频错误
    size = pframe->nb_samples * av_get_bytes_per_sample(AV_SAMPLE_FMT_S16) * pframe->channels;
    if (fread(out_buffer,1,size,fp) < 0){
      printf("fail to read raw data\n");
      return -1;
    }else if (feof(fp)){
      break;
    }

    swr_convert(pSwrCtx,data,pCodecCtx->frame_size,(const uint8_t **)pframe->data,pframe->nb_samples);
    //转换后的数据大小与采样率和采样格式有关
    size = pCodecCtx->frame_size * av_get_bytes_per_sample(pCodecCtx->sample_fmt);
    memcpy(pframe->data[0],data[0],size);
    memcpy(pframe->data[1],data[1],size);
    pframe->pts = count * 100;
    //编码写入
    if (avcodec_send_frame(pCodecCtx,pframe) < 0){
      printf("fail to send frame\n");
      return -1;
    }
    //读取编码好的数据
    if (avcodec_receive_packet(pCodecCtx,pkt)  >= 0){
      pkt->stream_index = out_stream->index;
      av_log(NULL,AV_LOG_INFO,"write %d frame\n",count);
      av_write_frame(ofmt_ctx,pkt);
    }
    count++;
    av_packet_unref(pkt);
  }
```

### 6. 刷新编码器，将编码器中的数据写入到文件中 

```c
int flush_encoder(AVFormatContext *ofmt_ctx,int stream_index){
  if (!(ofmt_ctx->streams[stream_index]->codec->codec->capabilities & AV_CODEC_CAP_DELAY)){
    return 0;
  }
  int got_fame = 0;
  AVPacket *pkt = av_packet_alloc();

  while(1)
  {
    pkt->data = NULL;
    pkt->size = 0;
    av_init_packet(pkt);
    int ret = avcodec_encode_audio2(ofmt_ctx->streams[stream_index]->codec,pkt,NULL,&got_fame);
    if (ret < 0){
      break;
    }
    if (got_fame == 0){
      break;
    }
    //mux the frame data
    ret = av_write_frame(ofmt_ctx,pkt);
    if (ret < 0){
      break;
    }
  }
  av_packet_free(&pkt);
  return 0;
}
```

### 7.写入文件尾部信息

```c
av_write_trailer(ofmt_ctx);
```

### 8.释放所有申请的资源

```c
av_packet_free(&pkt);
swr_free(&pSwrCtx);
av_free(out_buffer);
av_frame_free(&pframe);

avio_close(ofmt_ctx->pb);
avformat_free_context(ofmt_ctx);
```

## 总代码

```shell
ffmpeg version 4.4
```

编译：

```bash
g++ test1.cpp -o test1.out -I /usr/include -L /usr/lib -lavformat -lavcodec -lavutil -lswresample
```

```

```

