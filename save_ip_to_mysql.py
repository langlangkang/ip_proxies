# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     save_ip_to_mysql.py
   Description :  免费代理入库
   Author :       Kang
   date：          2020/02/29
-------------------------------------------------
   Change Activity:
                   2020/02/29
-------------------------------------------------
"""

import time
import pymysql


mysql_database_name='ip_info'
mysql_table_name='ip_info'


class Save_ip_to_mysql():
    def __init__(self):
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': 'root',
            'charset': 'utf8mb4',
            #'database': mysql_database_name,
        }
        self.ip_info_column = ['ip', 'port', 'ip_level', 'ip_type', 'city', 'country', 'yunyingshang', 'ip_speed', 'time','last_time', 'ip_from_where']


    def connect_mysql(self):
        db = pymysql.connect(**self.config)  # 连接数据库
        print('连接数据库ok')
        cursor = db.cursor()  # 创建指针
        print('创建指针ok')
        return cursor,db

    def create_database(self):
        return f'create database {mysql_database_name};'

    def show_databases(self):
        return f'show databases;'

    def use_database(self):
        return f'use {mysql_database_name};'

    def show_tables(self):
        return f'show tables;'


    def create_table_and_column(self):

        print('字段长度：', len(self.ip_info_column))
        data=self.column_to_format()
        sqll = f"CREATE TABLE {mysql_table_name}("+"{} VARCHAR(255) NOT NULL primary key,"+"{} VARCHAR(255) NOT NULL ," * (len(self.ip_info_column)-1) + ") charset=utf8;"

        sqll = sqll.replace(",)", ")")
        sqll = "'" + sqll + "'.format(" + data + ")"

        can_execute_sql = eval(sqll)

        print('can_execute_sql:',can_execute_sql)
        return can_execute_sql

    def column_to_format(self):
        a = []
        for i in range(len(self.ip_info_column)):
            a.append(self.ip_info_column[i])

        a = "'" + "','".join(a) + "'"
        print(a)
        return a

    def data_to_format(self):
        a = []
        for i in range(len(self.ip_info_column)):
            a.append(self.ip_info_column[i])

        a = ','.join(a)
        print(a)
        return a

    def insert_ip_to_table(self,ip,port,ip_level,ip_type,city,country,yunyingshang,ip_speed,time,last_time,ip_from_where,cursor, db):
        data=self.data_to_format()
        sqll=f"insert {mysql_table_name} ({data}) values ('{ip}','{port}','{ip_level}','{ip_type}','{city}','{country}','{yunyingshang}','{ip_speed}','{time}','{last_time}','{ip_from_where}');"

        self.execute_mysql(sqll,cursor, db)

    def read_txt(self,cursor, db,path='./ip_proxies_pool.txt'):
        with open(path,'r',encoding='utf-8') as f:
            for s in f.readlines():

                ip_info = s.strip().split(' ')
                print(ip_info)
                ip=ip_info[0].split(':')[0]
                port = ip_info[0].split(':')[-1]
                ip_level = ip_info[1]
                ip_type = ip_info[2]
                city = ip_info[3]
                country = ip_info[4]
                yunyingshang=ip_info[5]
                ip_speed = ip_info[6]
                time = ip_info[7]
                last_time=ip_info[8]
                ip_from_where  =ip_info[9]
                print(ip,port,ip_level,ip_type,city,country,yunyingshang,ip_speed,time,last_time,ip_from_where)
                self.insert_ip_to_table(ip,port,ip_level,ip_type,city,country,yunyingshang,ip_speed,time,last_time,ip_from_where,cursor, db)



    def execute_mysql(self,sql,cursor,db):
        try:
            # 提交sql语句
            cursor.execute(sql)
            db.commit()
            print(f'{sql} success')
        except Exception as e:
            print(f'{sql} 出错', e)
            db.rollback()

    def close_mysql(self,cursor,db):
        cursor.close()
        print('关闭指针ok')
        db.close()
        print('关闭数据库ok')

    def sql_sentence(self,cursor,db):
        create_database_sql = self.create_database()
        self.execute_mysql(create_database_sql, cursor, db)

        show_databases_sql=self.show_databases()
        self.execute_mysql(show_databases_sql,cursor,db)

        use_database_sql = self.use_database()
        self.execute_mysql(use_database_sql, cursor, db)

        create_table_and_column_sql = self.create_table_and_column()
        self.execute_mysql(create_table_and_column_sql, cursor, db)


    def run(self):
        cursor, db=self.connect_mysql()
        self.sql_sentence(cursor=cursor, db=db)

        self.read_txt(cursor, db)

        self.close_mysql(cursor, db)

if __name__ == '__main__':
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"nowtime:{nowtime}")
    start = time.time()

    # 打开mysql服务
    import os
    os.system('net start mysql')
    print('正在打开mysql服务')
    time.sleep(5)

    #主函数
    save_ip_to_mysql = Save_ip_to_mysql()
    save_ip_to_mysql.run()


    end = time.time()
    print(f'\ntime:{str(end-start)[:6]}s')
