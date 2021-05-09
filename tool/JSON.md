# JSON

**轻量级的数据格式，用来存储和表示数据**

### JSON语法规则

- 以"`{`“开始，以”`}`"结束，允许嵌套使用；
- 数组(Array) 用方括号("[ ]") 表示
- 每个名称和值成对出现，名称和值之间使用“：”分隔
- 键值对之间用“，”分隔
- 在这些字符前后允许存在无意义的空白符
- 名称(name) 置于**双引号**中，值(value)有**字符串、数值、布尔值、null、对象和数组**

对于键值，可以有如下值：

- 一个新的JSON对象
- 数组：使用" [ " 和“ ] ”表示
- 数字：直接表示，可以是整数，也可以是浮点数
- 字符串：使用引号"" 表示
- 字面值：false、null、true中的一个(必须是小写)

```json
{
        "name": "mculover666",	//字符串型
        "age":  22,			// 整型
        "weight":       55.5,	// 浮点型
        "address":      {		// 嵌套的JSON数据
                "country":      "China",
                "zip-code":     111111
        },
        "skill":        ["C", "Java", "Python"], // 数组类型
        "student":      false		// 布尔类型
}
```

## cJSON

cJSON是一个使用C语言编写的JSON数据解析器，具有超轻便，可移植，单文件的特点，使用MIT开源协议。

cJSON项目托管在Github上，仓库地址如下：

    https://github.com/DaveGamble/cJSON

使用Git命令将其拉取到本地：

```bash
$git clone https://github.com/DaveGamble/cJSON.git
```

从Github拉取cJSON源码后，文件非常多，但是其中cJSON的源码文件只有两个：

```bash
cJSON.h
cJSON.c
```

使用的时候，只需要将这两个文件复制到工程目录，然后包含头文件cJSON.h即可，如下：

```c++
#include "cJSON.h"
```

## cJSON数据结构和设计思想

cJSON使用cJSON结构体来表示**一个JSON数据**，定义在cJSON.h中，源码如下：

```c++
/* The cJSON structure: */
typedef struct cJSON
{
    /* next/prev allow you to walk array/object chains. Alternatively, use GetArraySize/GetArrayItem/GetObjectItem */
    struct cJSON *next;
    struct cJSON *prev;
    /* An array or object item will have a child pointer pointing to a chain of the items in the array/object. */
    struct cJSON *child;

    /* The type of the item, as above. */
    int type;

    /* The item's string, if type==cJSON_String  and type == cJSON_Raw */
    char *valuestring;
    /* writing to valueint is DEPRECATED, use cJSON_SetNumberValue instead */
    int valueint;
    /* The item's number, if type==cJSON_Number */
    double valuedouble;

    /* The item's name string, if this item is the child of, or is in the list of subitems of an object. */
    char *string;
} cJSON;
```

- String：用于表示该键值对的**名称**；
- type：用于表示该键值对中**值**的类型；
- valuestring：如果键值类型(type)是字符串，则将该指针指向键值；
- valueint：如果键值类型(type)是整数，则将该指针指向键值；
- valuedouble：如果键值类型(type)是浮点数，则将该指针指向键值；

**使用链表来存储整段JSON数据**

- `next`指针：指向下一个键值对
- `prev`指针指向上一个键值对
- 因为一个**键值对的值会是一个新的JSON数据对象（一条新的链表）**，也有可能是一个数组。当该键值对的值是一个嵌套的JSON数据或者一个数组时，由`child`指针指向该条新链表。

## cJSON数据封装

创建链表和向链表中添加节点的过程

- 头指针：指向链表头结点的指针；
- 头结点：不存放有效数据，方便链表操作；
- 首节点：第一个存放有效数据的节点；
- 尾节点：最后一个存放有效数据的节点；

（1）创建头指针：

```c
 cJSON* cjson_test = NULL;
```

（2）创建头结点，并将头指针指向头结点：

```c
cjson_test = cJSON_CreateObject();
```

(3) 尽情的向链表中添加节点：

```c
cJSON_AddNullToObject(cJSON * const object, const char * const name);

cJSON_AddTrueToObject(cJSON * const object, const char * const name);

cJSON_AddFalseToObject(cJSON * const object, const char * const name);

cJSON_AddBoolToObject(cJSON * const object, const char * const name, const cJSON_bool boolean);

cJSON_AddNumberToObject(cJSON * const object, const char * const name, const double number);

cJSON_AddStringToObject(cJSON * const object, const char * const name, const char * const string);

cJSON_AddRawToObject(cJSON * const object, const char * const name, const char * const raw);

cJSON_AddObjectToObject(cJSON * const object, const char * const name);

cJSON_AddArrayToObject(cJSON * const object, const char * const name);
```

（4）输出JSON数据

cJSON提供了一个API，可以将整条链表中存放的JSON信息输出到一个字符串中：

```c
char *) cJSON_Print(const cJSON *item);
```

使用的时候，只需要接收该函数返回的指针地址即可

示例Demo在cJSON文件夹中。

## cJSON数据解析

解析JSON数据的过程，其实就是剥离一个一个链表节点(键值对)的过程。

（1）创建链表头指针：

```c
cJSON* cjson_test = NULL;
```

(2) 解析整段JSON数据，并将链表头结点返回，赋值给头指针：

解析整段数据使用的API只有一个：

```c
(cJSON *) cJSON_Parse(const char *value);
```

(3) 根据键值对的名称从链表中取出对应的值，返回该键值对(链表节点)的地址

```c
(cJSON *) cJSON_GetObjectItem(const cJSON * const object, const char * const string);
```

(4) 如果JSON数据的值是数组，使用下面的两个API提取数据：

```c
(int) cJSON_GetArraySize(const cJSON *array);
(cJSON *) cJSON_GetArrayItem(const cJSON *array, int index);
```

示例Demo在cJSON文件夹中。

## cJSON使用过程中的内存问题

### 内存及时释放

cJSON的所有操作都是基于链表的，所以cJSON在使用过程中**大量的使用`malloc`从堆中分配动态内存的，所以在使用完之后，应当及时调用下面的函数，清空cJSON指针所指向的内存**，该函数也可用于删除某一条数据：

```c
(void) cJSON_Delete(cJSON *item);
```

> 注意：该函数删除一条JSON数据时，如果有嵌套，会连带删除。

### 内存钩子

cJSON在支持自定义malloc函数和free函数，方法如下：

(1)  使用`cJSON_Hooks`来连接自定义malloc函数和free函数：

```c
typedef struct cJSON_Hooks
{
      /* malloc/free are CDECL on Windows regardless of the default calling convention of the compiler, so ensure the hooks allow passing those functions directly. */
      void *(CJSON_CDECL *malloc_fn)(size_t sz);
      void (CJSON_CDECL *free_fn)(void *ptr);
} cJSON_Hooks;
```

（2）初始化钩子cJSON_Hooks

```c
(void) cJSON_InitHooks(cJSON_Hooks* hooks);
```

