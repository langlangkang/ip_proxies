# ip_proxies
# ip代理池

这是一个抓取网络上免费的ip，检测可用性并保存成本地txt的项目

运行时需要的库：
 import requests,datetime,json,random,time,os
 from lxml import etree
 from multiprocessing import Pool
架构：
 main.py主函数
 settings全局设置
 save_ip_to_mysql.py保存ip到mysql数据库脚本
 
#此版为V1.0版本
#主体架构庞大，仍需改进

  
免费ip主要来源（可自己添加）：
 1.高可用全球免费代理IP库 -----> www.freeip.top
 2.89ip -----> www.89ip.cn
 3.无忧代理 -----> www.data5u.com
 4.西刺代理 -----> www.xicidaili.com
 5.全网代理ip -----> www.goubanjia.com
 6.66免费代理网 -----> www.66ip.cn
 7.快代理 -----> www.kuaidaili.com
 8.齐云代理 -----> www.qydaili.com
 9.朋友开源的代理ip -----> https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list
 10.其他作者开源的端口 http://proxy.1again.cc:35050/api/v1/proxy/?type=1
