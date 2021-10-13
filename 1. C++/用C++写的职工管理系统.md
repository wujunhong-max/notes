# 一、管理系统需求

主要利用C++来实现一个基于多态的职工管理系统

公司中职工分为三类：普通员工，经理，老板。 
显示信息时，需要显示职工编号、职工姓名、职工岗位、以及职责

普通员工职责：完成经理交给的任务
经理职责：完成老板交给的任务，并下发任务给员工
老板职责：管理公司所有事务

管理系统中需要实现的功能如下：
- 退出管理系统：退出当前管理系统
- 增加职工信息：实现批量添加职工功能，将信息录入到文件中，职工信息为：职工编号、姓名、部门编号
- 显示职工信息：显示公司内部所有职工的信息
- 删除离职职工：按照编号删除指定的职工
- 修改职工信息：按照编号修改职工个人信息
- 查找职工信息：按照职工的编号或者职工的姓名进行查找相关的人员信息
- 按照编号排序：按照职工编号，进行排序，排序规则由用户指定
- 清空所有文档：清空文件中记录的所有职工信息（清空前需要再次确认，防止误删）	
# 二、创建几个对象
## 1. 抽象类

```cpp
//worker.h
#pragma once		//防止头文件重复包含
#include <iostream>
#include <string>
using namespace std;


//职工抽象类
class worker
{
public:

	//显示个人信息
	virtual void showinfo() = 0;
	//获取岗位名称
	virtual string getdeptname() = 0;

	int m_id; //职工编号
	string m_name;	//职工姓名
	int m_deptip;	//职工所在部门名称编号
};
```
## 2. 普通员工类

```cpp
//employee.h
#pragma once		//防止头文件重复包含
#include "worker.h"
using namespace std;


class employee :public worker
{
public:
	//构造函数
	employee(int id, string name, int did);
	
	//显示个人信息
	virtual void showinfo();
	//获取职工岗位名称
	virtual string getdeptname();
}; 

```

```cpp
//employee.cpp
#include "employee.h"

employee::employee(int id, string name, int did)
{
	this->m_id = id;
	this->m_name = name;
	this->m_deptip = did;
}
void employee::showinfo()
{
	cout << "职工编号：" << this->m_id<<" "
		<< "\t职工姓名：" << this->m_name<<" "
		<< "\t岗位：" << this->getdeptname()<<" "
		<< "\t岗位职责：完成经理交给的任务" << endl;
}
string employee::getdeptname()
{
	return string("员工");
}

```
## 3. 经理类

```cpp
//manage.h
#pragma once		//防止头文件重复包含
#include "worker.h"
using namespace std;


//创建经理类
class manage :public worker
{
public:
	//构造函数
	manage(int id, string name, int did);

	//显示个人信息
	virtual void showinfo();
	//获取职工岗位名称
	virtual string getdeptname();
}; 
```

```cpp
//manage.cpp
#include "manage.h"

manage::manage(int id, string name, int did)	//初始化
{
	this->m_id = id;
	this->m_name = name;
	this->m_deptip = did;
}
void manage::showinfo()
{
	cout << "职工编号：" << this->m_id<<" "
		<< "\t职工姓名：" << this->m_name<<" "
		<< "\t岗位：" << this->getdeptname()<<" "
		<< "\t岗位职责：完成老板交给的任务，并下发任务给员工" << endl;
}
string manage::getdeptname()
{
	return string("经理");
}
```
## 3. 老板类

```cpp
//boss.h
#pragma once		//防止头文件重复包含
#include "worker.h"
using namespace std;


class boss : public worker		//继承
{
public:
	//构造函数
	boss(int id, string name, int did);

	//显示个人信息
	virtual void showinfo();
	//获取岗位名称
	virtual string getdeptname();
}; 

```

```cpp
//boss.cpp
#include "boss.h"

boss::boss(int id, string name, int did)
{
	this->m_id = id;
	this->m_name = name;
	this->m_deptip = did;
}
void boss::showinfo()
{
	cout << "职工编号：" << this->m_id<<" "
		<< "\t职工姓名：" << this->m_name<<" "
		<< "\t岗位：" << this->getdeptname()<<" "
		<< "\t岗位职责：管理公司所有事务" << endl;
}

string boss::getdeptname()
{
	return string("老板");
}
```
# 三、main函数

```cpp
//main.cpp
#include "WorkerManager.h"
using namespace std;


int main()
{
	//创建对象
	workerManager wm;

	int choice = -1;	//菜单选择
	while ( true )	//会一直循环
	{
		//展示菜单
		wm.show_menu();
		cout << "请输入您的选择：" << endl;
		cin >> choice;
		switch (choice)
		{
		case 0: wm.exit_system(); 			//退出系统
			break;	
		case 1: wm.add_emp(); 				//增加职工信息
			break;
		case 2: wm.show_emp();			//显示职工信息
			break;
		case 3: wm.del_emp();				//删除离职职工
			break;
		case 4: wm.mod_emp();			//修改职工信息
			break;
		case 5: wm.Find_emp();			//查找职工信息
			break;
		case 6: wm.sort_emp();			//排序职工
			break;
		case 7: wm.clean_file();		//清空所有文档
			break;
		default:
			system("cls");  						//清屏操作
			break;
		}
	}
	system("pause");
	return 0;
}
```
# 四、 workerManager.h头文件

```cpp
#pragma once		//防止头文件重复包含
#include "worker.h"
#include "employee.h"
#include "boss.h"
#include "manage.h"
#include <fstream>
#include <unistd.h>
#include <stdlib.h>
using namespace std;

#define FILENAME "empfile.txt"


class workerManager
{
public:

	//构造函数
	workerManager();
	
	//菜单
	void show_menu();
	//退出系统
	void exit_system();
	//增加职工employee
	void add_emp();	
	//保存文件
	void save();
	//初始化员工
	void init_emp();
	//统计人数
	int get_empnum();
	//显示职工
	void show_emp();
	//删除职工
	void del_emp();
	//判断职工是否存在(按照职工编号)，若存在返回职工在数组中位置，不存在返回-1
	int IsExit(int id);
	//修改职工
	void mod_emp();
	//查找职工
	void Find_emp();
	//职工排序
	void sort_emp();
	//清空文件
	void clean_file();

	//析构函数
	~workerManager();

	//记录职工的人数
	int m_empnum;
	//员工数组的指针
	worker** m_emparray;
	//判断文件是否为空
	bool m_FileIsEmpty;	
};
```
# 五、各功能的实现

```cpp
#include"workerManager.h"

workerManager::workerManager()
{
	ifstream ifs;
	ifs.open(FILENAME, ios::in);	//读文件	


	//1.文件不存在情况
	if(!ifs.is_open())
	{
		cout<<"文件不存在"<<endl; //测试输出
		this->m_empnum = 0; 	//初始化人数
		this->m_FileIsEmpty = true;		//初始文件为空标志
		this->m_emparray = NULL;	//初始化数据
		ifs.close();	//关闭文件
		return;
	}

	//2.文件存在，并且没有记录
	char ch;
	ifs>>ch;
	if(ifs.eof())		//end of file	判断文件为空或检测文件的结束
	{
		cout<<"文件为空	!"<<endl;
		this->m_emparray = 	NULL;
		this->m_empnum = 0;
		this->m_FileIsEmpty = true;
		ifs.close();
		return;
	}

	//3.文件存在，并且记录数据
	int num = this->get_empnum();
	cout << "职工人数为:  " << num << endl;
	this->m_empnum = num;	//更新成员属性
	//开辟空间
	this->m_emparray = new worker *[this->m_empnum];
	//将文件中的数据，存在数组中
	this->init_emp();

	for (int i = 0; i < this->m_empnum; i++)
	{
		cout << "职工编号： " << this->m_emparray[i]->m_id<<" "
			 << "姓名： " << this->m_emparray[i]->m_name<<" "
			 << "部门编号：" << this->m_emparray[i]->m_deptip <<" " << endl;
	}
	ifs.close();
	this->m_FileIsEmpty = false;
}
//菜单
void workerManager::show_menu()
{
	cout << "*****************************************************" << endl;
	cout << "***************欢迎使用职工管理系统！****************" << endl;
	cout << "******************0.退出管理系统*********************" << endl;
	cout << "******************1.增加职工信息*********************" << endl;
	cout << "******************2.显示职工信息*********************" << endl;
	cout << "******************3.删除离职职工*********************" << endl;
	cout << "******************4.修改职工信息*********************" << endl;
	cout << "******************5.查找职工信息*********************" << endl;
	cout << "******************6.按照编号排序*********************" << endl;
	cout << "******************7.清空所有文档*********************" << endl;
	cout << "*****************************************************" << endl;
	cout << endl;
}
//退出系统
void workerManager::exit_system()
{
	cout << "欢迎下次使用" << endl;
	exit(0);	//退出系统
}
//增加职工
void workerManager::add_emp()
{
	cout << "请输入添加职工数量：" << endl;

	int addnum = 0;	//用户的输入数量
	cin >> addnum;
	if (addnum > 0)
	{
		//添加
		//计算添加新空间大小
		int newsize = this->m_empnum + addnum; 
		//开辟新空间
		worker** newspace = new worker * [newsize];

		//将原来空间下的数据，拷贝到新空间
		if (this->m_emparray != NULL)
		{
			for (int i = 0; i < this->m_empnum; i++)
			{
				newspace[i] = this->m_emparray[i];
			}
		}
		//添加新数据
		for (int i = 0; i < addnum; i++)
		{
			int id;//职工编号
			string name; //职工姓名
			int dselect;   //部门选择

			cout << "请输入第" << i + 1 << "个新职工编号："<<endl;
			cin >> id;
			cout << "请输入第" << i + 1 << "个新职工姓名：" << endl;
			cin >> name;
			cout << "请选择该职工的岗位：" << endl;
			cout << "1.普通职工" << endl;
			cout << "2.经理" << endl;
			cout << "3.老板" << endl;
			cin >> dselect;

			worker* worker = NULL;
			switch (dselect)
			{
			case 1:
				worker = new employee(id, name, 1); break;
			case 2:
				worker = new manage(id, name, 2); break;
			case 3:
				worker = new boss(id, name, 3); break;
			default:
				break;
			}
			//当创建职工职责，保存到数组中
			newspace[this->m_empnum + i] = worker;
		}
		//释放原有空间
		delete[] this->m_emparray;
		//更改新空间的指向
		this->m_emparray = newspace;

		//更新新的职工人数
		this->m_empnum = newsize;

		//提示添加成功
		cout << "成功添加" << addnum << "名新职工！" << endl;
		//保存到文件中
		this->save();
	}
	else {
		cout << "输入数据有误" << endl;
	}
	
	//按任意键后，清屏回到上级目录
	system("pause");
	system("cls");

}

//保存文件
void workerManager::save()
{
	ofstream ofs;
	ofs.open(FILENAME, ios::out);

	for (int i = 0; i < this->m_empnum; i++)
	{
		ofs << this->m_emparray[i]->m_id << " "
		<< this->m_emparray[i]->m_name << " "
		<< this->m_emparray[i]->m_deptip << endl;
	}
	ofs.close();
}

//初始化员工
void workerManager::init_emp()
{
	ifstream ifs;
	ifs.open(FILENAME, ios::in);

	int id;
	string name;
	int did;

	int index = 0; //数组的索引位置
	while(ifs>>id&&ifs >> name && ifs>>did )
	{
		worker *worker = NULL;		//创建一个父指针
		//根据不同的部门id创建不同对象
		if(did == 1)//1.普通员工
		{
			worker = new employee(id , name, did);
		}else if (did == 2)//2.经理
		{
			worker = new manage(id, name, did);
		}else  //3.老板
		{
			worker = new boss(id, name, did);
		}
		//存放在数组中
		this->m_emparray[index] = worker;
		index++;
	}
	//关闭文件
	ifs.close();
}
//统计人数
	int workerManager::get_empnum()
	{
		ifstream ifs;
		ifs.open(FILENAME, ios::in);

		int id;
		string name;
		int did;

		int num = 0;

		while(ifs >> id && ifs >> name && ifs >> did)
			{
				//记录人数
				num++;
			}
			ifs.close();

			return num;
	}

//显示职工
void workerManager::show_emp()
{
	//判断文件是否为空
	if(this->m_FileIsEmpty)
	{
		cout << "文件不存在或记录为空!" << endl;
	}else{
		for (int i = 0; i < m_empnum; i++)
		{
			//利用多态调用接口
			this->m_emparray[i]->showinfo();
		}
	}
	system("pause");
	system("cls");
}
//判断职工是否存在
int workerManager::IsExit(int id)
{
	int index = -1;
	for (int i = 0; i < this->m_empnum; i++)
	{
		if(this->m_emparray[i]->m_id == id)
		{
			index = i;
			break;
		}
	}
	return index;
}
//删除职工
void workerManager::del_emp()
{
	if(this->m_FileIsEmpty)
	{
		cout << "文件不存在或记录为空!" << endl;
	}else{
		//按照职工编号删除
		cout << "请输入想要删除的职工编号：" << endl;
		int id = 0;
		cin >> id;
		int index  = this->IsExit(id);
		if(index != -1) 		//说明职工存在并且要删除掉index位置上的职工
		{
			//数据前移
			for (int i = index; i < this->m_empnum - 1; i++)
			{
				this->m_emparray[i] = this->m_emparray[i + 1];
			}
			this->m_empnum--;		//更新数组中记录人员个数
			//数据同步更新到文件中
			this->save();
			cout << "删除成功!" << endl;
		}else{
			cout << "删除失败，未找到该职工" << endl;
		}
	}
	//按任意键   清屏
	system("pause");
	system("cls");
}
void workerManager::mod_emp()
{
	if(this->m_FileIsEmpty)
	{
		cout << "文件不存在或记录为空!" << endl;
	}else{
		cout << "请输入修改职工的编号：" << endl;
		int id;
		cin >> id;

		int ret = this->IsExit(id);
		if(ret != -1)
		{
			//查找到该编号员工

			delete this->m_emparray[ret];

			int newid = 0;
			string newname = " ";
			int newdid = 0;

			cout << "查到: " << id << "号职工，请输入新职工号: " << endl;
			cin >> newid;

			cout << "请输入新姓名: " << endl;
			cin >> newname;

			cout << "请输入岗位：" << endl;
			cout << "1.普通员工" << endl;
			cout << "2.经理" << endl;
			cout << "3.老板" << endl;
			cin >> newdid;

			worker *worker = NULL;
			switch(newdid)
			{
				case1:
					worker = new employee(newid, newname, newdid);
					break;
				case 2:
					worker = new manage(newid, newname, newdid);
					break;
				case 3:
					worker = new boss(newid, newname, newdid);
					break;
				default:
					break;
			}
			//更改数据 	到数组中
			this->m_emparray[ret] = worker;
			cout << "修改成功!" << endl;

			//保存到文件中
			this->save();
		}else{
			cout << "修改失败，查无此人" << endl;
		}
	}
		//按任意键清屏
	system("pause");
	system("cls");
}
//查找职工
void workerManager::Find_emp()
{
	if(this->m_FileIsEmpty)
		{
			cout << "文件不存在或记录为空" << endl;
		}else{
			cout << "请输入查找的方式：" << endl;
			cout << "1、按职工编号查找	" << endl;
			cout << "2、按姓名查找" << endl;

			int select = 0;
			cin >> select;

			if(select ==1) 		//按职工号查找
			{
				int id;
				cout << "请输入要查找的职工编号：" << endl;
				cin >> id;
				int ret = IsExit(id);
				if(ret != -1)
				{
					cout << "查找成功！该职工信息如下：" << endl;
					this->m_emparray[ret]->showinfo();
				}
			}
			if(select == 2)			//	按姓名查找
			{
				string name;
				cout << "请输入查找的姓名：" << endl;
				cin >> name;

				bool flag = false;	//查找到的标志
				for (int i = 0; i < m_empnum;i++)
				{
					if(this->m_emparray[i]->m_name == name)
					{
						cout << "查找成功，职工编号为："
							 << m_emparray[i]->m_id
							 << "号的信息如下：" << endl;

						flag = true;
						this->m_emparray[i]->showinfo();
					}
				}
				if(flag == false)
				{
					//查无此人
					cout << "查找失败，查无此人" << endl;
				}
			}
			else
			{
				cout << "输入选项有误" << endl;

			}
		}
		system("pause");
		system("cls");
}
//职工排序
	void workerManager::sort_emp()
	{
		if(this->m_FileIsEmpty)
		{
			cout << "文件不存在或记录为空！" << endl;
			system("pause");
			system("cls");
		}else{
			cout << "请选择排序方式：" << endl;
			cout << "1.按职工号进行升序" << endl;
			cout << "2.按职工号进行降序" << endl;

			int select = 0;
			cin >> select;

			//选择排序
			for (int i = 0; i < m_empnum; i++)
			{
				int minormax = i;
				for (int j = 1 + i; j < m_empnum; j++)
				{
					if(select == 	1)	//升序
					{
						if(m_emparray[minormax]->m_id  > m_emparray[j]->m_id)
						{
							minormax = j;
						}
					}
					else	//降序
					{
						if(m_emparray[minormax]->m_id  < m_emparray[j]->m_id)
						{
							minormax = j;
						}
					}	
				}
				if(i != minormax)
				{
					worker *temp = m_emparray[i];
					m_emparray[i] = m_emparray[minormax];
					m_emparray[minormax] = temp;
				}
			}
			cout << "排序成功，排序后结果为：" << endl;
			this->save();
			this->show_emp();
		}
	}

//清空文件
void workerManager::clean_file()
{
	cout << "确认清空？" << endl;
	cout << "1、确认" << endl;
	cout << "2、返回" << endl;

	int select = 0;
	cin >> select;

	if(select == 1)
	{
		//打开模式 ios::trunc 如果存在删除文件并重新创建
		ofstream ofs(FILENAME, ios::trunc);
		ofs.close();

		if(this->m_emparray != NULL)
		{
			//删除堆区的每个职工对象
			for (int i = 0; i < this->m_empnum;i++)
			{
				if(this->m_emparray[i] != NULL)
				{
					delete this->m_emparray[i];
				}
			}
			this->m_empnum = 0;
			//删除堆区的数组指针
			delete[] this->m_emparray;
			this->m_emparray = NULL;
			this->m_FileIsEmpty = true;
		}
		cout << "清空成功!" << endl;
	}
	system("pause");
	system("cls");
}
workerManager::~workerManager()
{
	if (this->m_emparray != NULL)
	{
		for (int i = 0; i < this->m_empnum;i++)
		{
			if(this->m_emparray[i] != NULL)
			{
				delete this->m_emparray[i];
			}
		}
	}
		delete[] this->m_emparray;
		this->m_emparray = NULL;
	
}
```