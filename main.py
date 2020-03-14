# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       Kang
   date：          2020/03/13
-------------------------------------------------
   Change Activity:
                   2020/03/13
-------------------------------------------------
"""

#系统库
import requests,datetime
import json,random,time,os

from lxml import etree
from multiprocessing import Pool

#自己全局设置
from ip_proxies.tools import setting
from ip_proxies.save_ip_to_mysql import Save_ip_to_mysql


#主函数
class IP_PROXIES():
    def __init__(self):
        self.UserAgent = random.choice(setting.user_agent_list)#随机请求头
        self.testurl='https://www.baidu.com'#测试网址
        self.ip_list_not_to_check = []#存放ip，未检查
        self.ip_list_is_check = []#存放ip，已检查

    def ip_to_format(self,ip,port):
        '''
        :param ip:
        :param port:
        :return:  转化代理格式
        # return {'http': f'http://{ip}:{port}','https': f'http://{ip}:{port}',}
        '''
        return  {'http': f'http://{ip}:{port}','https': f'http://{ip}:{port}', }

    def ip_info_to_format(self,ip, port,ip_from_where, ip_level='高匿', ip_type='http', country='None', city='None', yunyingshang='None', ip_speed='None', time='None', last_time=str(datetime.datetime.now())[:19]):
        '''
        :param : 默认参数，无则使用
        :return: 保存ip格式
        '''
        ip_info_dict = {}#字典
        if not ip :
            return ip_info_dict

        ip_info_dict['ip']=ip
        ip_info_dict['port'] = port
        ip_info_dict['ip_level'] = ip_level
        ip_info_dict['ip_type'] = ip_type
        ip_info_dict['country'] = country
        ip_info_dict['city'] = city
        ip_info_dict['yunyingshang'] = yunyingshang
        ip_info_dict['ip_speed'] = ip_speed
        ip_info_dict['time'] = time
        ip_info_dict['last_time'] = last_time
        ip_info_dict['ip_from_where'] = ip_from_where
        #ip_info_dict['ip_speed'] = ip_speed

        return ip_info_dict

    def ip_info_to_save(self,ip_info):
        '''
        :param ip_info:
        :return: 合法保存的字符串
        '''

        ip = ip_info['ip']
        port = ip_info['port']
        ip_level = ip_info['ip_level'].upper()
        ip_type = ip_info['ip_type']
        city = ip_info['city']
        country = ip_info['country']
        yunyingshang = ip_info['yunyingshang']
        ip_speed = ip_info['ip_speed']
        time = ip_info['time']
        last_time = ip_info['last_time'].replace(' ','-')
        ip_from_where=ip_info['ip_from_where']

        #print(type(ip),type(port),type(ip_level),type(ip_type),type(city),type(country),type(yunyingshang),type(ip_speed),type(time),type(last_time),type(ip_from_where))
        #如果不是字符串，则转换成str
        ip=self.to_str(ip)
        port = self.to_str(port)
        ip_level = self.to_str(ip_level)
        ip_type = self.to_str(ip_type)
        city = self.to_str(city)
        country = self.to_str(country)
        yunyingshang = self.to_str(yunyingshang)
        ip_speed = self.to_str(ip_speed)
        time = self.to_str(time)
        last_time = self.to_str(last_time)
        ip_from_where = self.to_str(ip_from_where)

        #去空格
        ip = self.delete_blank_space(ip)
        port = self.delete_blank_space(port)
        ip_level = self.delete_blank_space(ip_level).upper()
        ip_type = self.delete_blank_space(ip_type)
        city = self.delete_blank_space(city)
        country = self.delete_blank_space(country)
        yunyingshang = self.delete_blank_space(yunyingshang)
        ip_speed = self.delete_blank_space(ip_speed)
        time = self.delete_blank_space(time)
        last_time = self.delete_blank_space(last_time)
        ip_from_where = self.delete_blank_space(ip_from_where)

        result=ip+':'+port+' '+ip_level+' '+ip_type+' '+city+' '+country+' '+yunyingshang+' '+ip_speed+' '+time+' '+last_time+' '+ip_from_where
        return result

    def to_str(self,things):
        '''
        转换为字符串
        '''
        if not isinstance(things, str):
            things = str(things)
        return things

    def delete_blank_space(self,things):
        '''
        去空格
        '''
        return things.replace(' ', '')

    def get_headers(self):
        '''
        获取请求头
        '''
        headers = {
            'User-Agent': self.UserAgent,
                   }
        return headers

    def get_api_to_ip(self,want_to_get=100):
        """
        获取端口ip
        want_to_get默认获取的数量
        :return:
        """
        url='http://proxy.1again.cc:35050/api/v1/proxy/?type=1'
        print('----------------get_api_to_ip---------------- 正在爬取ip的地址：',url)
        ip_from_where='api'
        url_pass=True
        error_count=0 #错误次数
        #    1:'高匿',2:'普通',3:'透明',
        get_total=0
        while True:
            if get_total>=want_to_get:
                break
            if url_pass:
                try:
                    data_json = requests.get(url,self.get_headers(),timeout=3).text
                except TimeoutError:
                    print('time out 连接网络时间超时')
                    data_json = ''
                except Exception as e:
                    print(f'该api出现以下错误，退出抓取，请检查该网站{url}是否可登录---{e}')
                    break

                if data_json:
                    data = json.loads(data_json)
                    ip_p = data['data']['proxy']
                    ip=ip_p.split(':')[0]
                    port=ip_p.split(':')[-1]
                    country=data['data']['region_list']
                    country=''.join(country)
                    city=data['data']['region_list']
                    city=''.join(city)

                    if data['data']['https'] == 1:
                        ip_type = 'https'
                    else:
                        ip_type = 'http'
                    ip_level='高匿'
                    if ip_level == setting.ip_levels[1]:
                        ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, ip_type=ip_type,city=city,country=country,ip_from_where=ip_from_where)
                        self.ip_list_not_to_check.append(ip_info)
                        get_total+=1
                        print(f'设置爬取{want_to_get},现在爬取第{get_total}个,ip信息为{ip_info}')
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
                        url_pass = True
                else:
                    print('返回数据有误')
                    time.sleep(3)
                    error_count += 1
                    if error_count <=3:
                        print(f'错误次数 is {error_count} (最多3次)')
                        url_pass = True
                    else:
                        print(f'错误次数 is {error_count} (已超3次)')
                        url_pass = False  #退出while循环
                time.sleep(random.random() * 3)
            else:
                print(f'url_pass is {url_pass}')

    def get_freeip(self):
        """
        获取freeip
        :return:
        """
        ip_from_where='freeip'
        #print(setting.sourceLists[2]['origin'])
        url_list = setting.sourceLists[2]['urls']
        pattern = setting.sourceLists[2]['pattern']
        position = setting.sourceLists[2]['position']
        headers=self.get_headers()
        headers['Host']='www.freeip.top'
        headers['Referer']='https://www.freeip.top/?page=1'

        for url in url_list:
            print('----------------get_freeip---------------- 正在爬取ip的地址：',url)
            try:
                response = requests.get(url=url, headers=headers,timeout=3).text
            except TimeoutError:
                print('time out 连接网络时间超时')
                response=''
            except Exception as e:
                print(f'request {url}  happen error')
                continue

            if response:
                html = etree.HTML(response)
                results = html.xpath(f'{pattern}')

                for result in results:
                    ip = result.xpath(f'{position}')[0]
                    port = result.xpath(f'{position}')[1]
                    ip_level = result.xpath(f'{position}')[2]
                    ip_type = result.xpath(f'{position}')[3]
                    country = result.xpath(f'{position}')[4]
                    city = result.xpath(f'{position}')[5]
                    yunyingshang = result.xpath(f'{position}')[6]
                    try:
                        ip_speed = result.xpath(f'{position}')[7]
                        ip_time = result.xpath(f'{position}')[8]
                        last_time = result.xpath(f'{position}')[9]
                    except IndexError:
                        ip_speed='None'
                        ip_time='None'
                        last_time='None'

                    #print(ip, port, ip_level, ip_type, country, city, yunyingshang, ip_speed, ip_time, last_time)
                    #    1:'高匿',2:'普通',3:'透明',
                    if (ip_level == setting.ip_levels[1]) or  ('高匿'in ip_level):
                        ip_level='高匿'
                        ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, ip_type=ip_type, country=country, city=city, yunyingshang=yunyingshang,
                                                         ip_speed=ip_speed, time=ip_time, last_time=last_time,ip_from_where=ip_from_where)
                        #print(ip_info)
                        self.ip_list_not_to_check.append(ip_info)
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
            else:
                continue
        time.sleep(random.random() * 3)

    def get_89ip(self):
        """
        获取89ip
        :return:
        """
        ip_from_where='89ip'
        #print(setting.sourceLists[0]['origin'])
        pattern = setting.sourceLists[0]['pattern']
        position = setting.sourceLists[0]['position']
        url_list = setting.sourceLists[0]['urls']
        headers = self.get_headers()
        headers['Host'] = 'www.89ip.cn'

        for url in url_list:
            print('----------------get_89ip---------------- 正在爬取ip的地址：',url)
            try:
                response = requests.get(url=url, headers=headers,timeout=3).text
            except TimeoutError:
                print('time out 连接网络时间超时')
                response=''
            except Exception as e:
                print(f'request {url}  happen error')
                continue

            if response:
                html = etree.HTML(response)
                results = html.xpath(pattern)
                for result in results:
                    ip = result.xpath(position['ip'])[0].strip()
                    port = result.xpath(position['port'])[0].strip()
                    city = result.xpath(position['area'])[0].strip()
                    country=city
                    #    1:'高匿',2:'普通',3:'透明',
                    ip_level = '高匿'
                    if (ip_level == setting.ip_levels[1]) or  ('高匿'in ip_level):
                        ip_info = self.ip_info_to_format(ip=ip, port=port, city=city,country=country,ip_from_where=ip_from_where)
                        print(ip_info)
                        self.ip_list_not_to_check.append(ip_info)
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
            else:
                continue
        time.sleep(random.random() * 3)

    def get_data5uip(self):
        """
        获取data5uip
        :return:
        采用了js加密代理IP端口号的方式。请求初次返回的HTML中的端口号和实际网页中显示的不一样
        """
        ip_from_where='data5u'
        #print(setting.sourceLists[1]['origin'])
        url_list = setting.sourceLists[1]['urls']
        pattern = setting.sourceLists[1]['pattern']
        position = setting.sourceLists[1]['position']
        headers=self.get_headers()
        headers['Host']='www.data5u.com'

        for url in url_list:
            print('----------------get_data5uip---------------- 正在爬取ip的地址：',url)
            try:
                response = requests.get(url=url, headers=headers,timeout=3).text
            except TimeoutError:
                print('time out 连接网络时间超时')
                response=''
            except Exception as e:
                print(f'request {url}  happen error')
                continue

            if response:
                html = etree.HTML(response)
                results = html.xpath(pattern)
                for result in results:
                    ip = result.xpath(position.format(1))[0]
                    port = result.xpath('./span[2]/li/@class')[0].replace('port', '').replace(' ', '')
                    ip_level = result.xpath(position.format(3))[0]
                    ip_type = result.xpath(position.format(4))[0]
                    country = result.xpath(position.format(5))[0]
                    city = result.xpath(position.format(6))[0]
                    yunyingshang = result.xpath(position.format(7))[0]
                    ip_speed = result.xpath(position.format(8))[0]
                    #time = result.xpath(position.format(9))[0]
                    #last_time = result.xpath(position.format(9))[0]

                    port = port.replace('A', '0').replace('B', '1').replace('C', '2').replace('D', '3').replace('E','4').replace( 'F', '5').replace('G', '6').replace('H', '7').replace('I', '8').replace('Z', '9')
                    port = int(int(port) / 8)

                    #print(ip, port, ip_level, ip_type, country, city, yunyingshang, ip_speed)

                    #    1:'高匿',2:'普通',3:'透明',
                    if (ip_level == setting.ip_levels[1]) or  ('高匿'in ip_level):
                        ip_level = '高匿'
                        ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, ip_type=ip_type, country=country, city=city, yunyingshang=yunyingshang,
                                                         ip_speed=ip_speed,ip_from_where=ip_from_where)
                        print(ip_info)
                        self.ip_list_not_to_check.append(ip_info)
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
            else:
                continue
        time.sleep(random.random() * 3)

    def get_xiciip(self):
        '''
        获取西刺ip
        :return:
        '''
        ip_from_where='xici'
        #print(setting.sourceLists[3]['origin'])
        url_list = setting.sourceLists[3]['urls']
        pattern = setting.sourceLists[3]['pattern']
        position = setting.sourceLists[3]['position']
        headers = self.get_headers()
        headers['Host'] = 'www.xicidaili.com'

        #print(url_list, pattern, position, headers)
        for url in url_list:
            print('----------------get_data5uip---------------- 正在爬取ip的地址：', url)
            try:
                response = requests.get(url=url, headers=headers, timeout=3).text
            except TimeoutError:
                print('time out 连接网络时间超时')
                response = ''
            except Exception as e:
                print(f'request {url}  happen error')
                continue

            if response:
                html = etree.HTML(response)
                results = html.xpath(pattern)
                for result in results[1:]:
                    ip = result.xpath(position.format(2))[0].strip()#可类似转换，按自己喜欢
                    port = result.xpath("./td[3]/text()")[0].strip()
                    city = result.xpath("./td[4]//text()")
                    ip_level = result.xpath("./td[5]/text()")[0].strip()
                    ip_type = result.xpath("./td[6]/text()")[0].strip()
                    ip_speed = result.xpath("./td[7]//text()")[0].strip()
                    ip_time = result.xpath("./td[9]/text()")[0].strip()
                    last_time = result.xpath("./td[10]/text()")[0].strip()
                    city = ''.join(city).strip()
                    country=city
                    #print(ip, port, city,country, ip_level, ip_type, ip_speed, ip_time, last_time)

                    #    1:'高匿',2:'普通',3:'透明',
                    if (ip_level == setting.ip_levels[1]) or  ('高匿'in ip_level):
                        ip_level = '高匿'
                        ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, ip_type=ip_type, country=country, city=city,
                                                         time=ip_time,last_time=last_time,ip_from_where=ip_from_where)
                        print(ip_info)
                        self.ip_list_not_to_check.append(ip_info)
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
                else:
                    continue
            else:
                continue
        time.sleep(random.random() * 3)

    def get_goubanjia_ip(self):
        url = "http://www.goubanjia.com/"
        print('----------------get_goubanjia_ip---------------- 正在爬取ip的地址：', url)
        ip_from_where='goubanjia'
        headers=self.get_headers()
        headers['Accept']= '*/*'
        headers['Connection']= 'keep-alive'
        headers['Accept-Language']="zh-CN,zh;q=0.8"
        header = None
        timeout = 30

        if header and isinstance(header, dict):
            headers.update(header)
            print(headers)
        try:
            html = requests.get(url, headers=headers, timeout=timeout,).content

        except Exception as e:
            html = ' '
        if not html:
            return False

        tree = etree.HTML(html)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                            and not(contains(@style, 'display:none'))
                                            and not(contains(@class, 'port'))
                                            ]/text()
                                    """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))

                # HTML中的port是随机数，真正的端口编码在class后面的字母中。
                # 比如这个：
                # <span class="port CFACE">9054</span>
                # CFACE解码后对应的是3128。
                port = 0
                for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                                          "/attribute::class")[0]. \
                        replace("port ", ""):
                    port *= 10
                    port += (ord(_) - ord('A'))
                port /= 8
                port=str(int(port))
                #print('{}:{}'.format(ip_addr,port))
                other_info=each_proxy.xpath('..//td//text()')
                ip_level=other_info[-13]
                ip_type= other_info[-12]
                country= other_info[-10]
                city=other_info[-6] + other_info[-8]
                yunyingshang=other_info[-4]

                #last_time=other_info-1]
                #time=other_info-2]
                ip_speed=other_info[-3]
                #print(ip_addr, port, ip_level, ip_type, country, city,yunyingshang,ip_speed)

                #    1:'高匿',2:'普通',3:'透明',
                if (ip_level == setting.ip_levels[1]) or  ('高匿' in ip_level):
                    ip_level = '高匿'
                    ip_info = self.ip_info_to_format(ip=ip_addr, port=port, ip_level=ip_level, ip_type=ip_type, country=country,
                                                     city=city,yunyingshang=yunyingshang,ip_speed=ip_speed,ip_from_where=ip_from_where)
                    #print(ip_info)
                    self.ip_list_not_to_check.append(ip_info)
                else:
                    print(f'ip {ip_addr} is not 高匿 暂时不保存')
            except Exception as e:
                pass
        time.sleep(random.random() * 3)

    def get_66ip(self):
        """
        获取66ip
        :return:
        """
        ip_from_where = '66ip'
        #print(setting.sourceLists[4]['origin'])
        pattern = setting.sourceLists[4]['pattern']
        position = setting.sourceLists[4]['position']
        url_list = setting.sourceLists[4]['urls']
        headers = self.get_headers()
        headers['Host'] = 'www.66ip.cn'
        headers['referer']='http://www.66ip.cn/index.html'

        for url in url_list:
            print('----------------get_66_ip---------------- 正在爬取ip的地址：', url)
            try:
                response = requests.get(url, headers=headers)
                response.encoding = 'gbk'
                page_html = response.text
                html = etree.HTML(page_html)
                content_lists = html.xpath(pattern)[1:]
                for content_list in content_lists:
                    ip = content_list.xpath(position.format(1))[0]
                    port = content_list.xpath(position.format(2))[0]
                    city = content_list.xpath(position.format(3))[0]
                    country = content_list.xpath(position.format(3))[0]
                    ip_level = content_list.xpath(position.format(4))[0]
                    last_time=content_list.xpath(position.format(5))[0][:-3]

                    # print(ip, port, city, country, ip_level)

                    if (ip_level == setting.ip_levels[1]) or ('高匿' in ip_level):
                        ip_level = '高匿'
                        ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level,country=country, city=city, last_time=last_time,ip_from_where=ip_from_where)
                        # print(ip_info)
                        self.ip_list_not_to_check.append(ip_info)
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
            except:
                pass
            time.sleep(random.random())

    def get_kuaidaili_ip(self):
        """
        获取kuaidaili_ip
        :return:
        """
        ip_from_where = 'kuaidaili'
        #print(setting.sourceLists[5]['origin'])
        pattern = setting.sourceLists[5]['pattern']
        position = setting.sourceLists[5]['position']
        url_list = setting.sourceLists[5]['urls']
        headers = self.get_headers()
        headers['Host'] = 'www.kuaidaili.com'
        headers['referer']='https://www.kuaidaili.com/free/'
        #print(url_list, pattern, position, headers)

        for url in url_list:
            print('----------------get_kuaidaili_ip---------------- 正在爬取ip的地址：', url)
            try:
                response = requests.get(url, headers=headers).text

            except:
                print('get_kuaidaili_ip error')
                response=''
            if response:
                html = etree.HTML(response)
                content_lists = html.xpath(pattern)
                time.sleep(1)  # 必须sleep 不然第二条请求不到数据

                for content_list in content_lists[1:]:
                    ip = content_list.xpath(position.format(1))[0]
                    port = content_list.xpath(position.format(2))[0]
                    ip_level = content_list.xpath(position.format(3))[0]
                    ip_type = content_list.xpath(position.format(4))[0]
                    city = content_list.xpath(position.format(5))[0]
                    country = content_list.xpath(position.format(5))[0]
                    ip_speed=content_list.xpath(position.format(6))[0]
                    last_time=content_list.xpath(position.format(7))[0]
                    print(ip, port, ip_level, ip_type, city, country, ip_speed, last_time)

                    if (ip_level == setting.ip_levels[1]) or ('高匿' in ip_level):
                        ip_level = '高匿'
                        ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, country=country, city=city, last_time=last_time, ip_from_where=ip_from_where)
                        print(ip_info)
                        self.ip_list_not_to_check.append(ip_info)
                    else:
                        print(f'ip {ip} is not 高匿 暂时不保存')
            else:
                print('kuaidaili response is none')
        time.sleep(random.random() * 3)

    def get_freeproxylist_for_ip(self):
        """
        获取freeproxylist
        :return:
        """
        url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
        print('----------------freeproxylist---------------- 正在爬取ip的地址：', url)
        ip_from_where='freeproxylist'

        try:
            response = requests.get(url, headers=self.get_headers())
        except Exception as e:
            response=''
        if response:
            proxies_list = response.text.split('\n')
        else:
            proxies_list=[]
        for proxy_str in proxies_list:
            if not proxy_str:
                continue
            info = json.loads(proxy_str)
            ip = info['host']
            port = info['port']
            ip_type = info['type']
            ip_level = info['anonymity']
            country = info['country']
            city = info['country']
            #ip_from_where = info['from']
            ip_speed=info['response_time']
            print(ip, port, ip_type, ip_level, country,city,ip_speed, ip_from_where)
            if ip_level == 'high_anonymous':
                ip_level = '高匿'
            elif ip_level == 'anonymous':
                ip_level = '普通'
            elif ip_level == 'transparent':
                ip_level='透明'
            else:
                print(f'{ip} 这里ip格式error，请查看该{url}了解是否改了获取规则')
            #    1:'高匿',2:'普通',3:'透明',
            if (ip_level == setting.ip_levels[1]) or ('高匿' in ip_level):
                ip_level = '高匿'
                ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, ip_type=ip_type, country=country, city=city,ip_speed=ip_speed, ip_from_where=ip_from_where)
                #print(ip_info)
                self.ip_list_not_to_check.append(ip_info)
            else:
                print(f'ip {ip} is not 高匿 暂时不保存')
        time.sleep(random.random() * 3)

    def get_qiyun_ip(self):
        """
        获取freeproxylist
        :return:
        """
        ip_from_where='7yip'
        #print(setting.sourceLists[6]['origin'])
        pattern = setting.sourceLists[6]['pattern']
        position = setting.sourceLists[6]['position']
        url_list = setting.sourceLists[6]['urls']

        for url in url_list:
            print('----------------get_qiyun_ip---------------- 正在爬取ip的地址：', url)
            try:
                response = requests.get(url, headers=self.get_headers()).text
            except Exception as e:
                response = ''
                print(f'{ip_from_where} 出现 error 原因是{e}')
            if not response:
                continue

            tree = etree.HTML(response)
            proxy_list = tree.xpath('.//table[@class="table table-bordered table-striped"]//tr')
            for tr in proxy_list[1:]:
                ip = tr.xpath("./td[1]//text()")[0] #同理可用position代替
                port = tr.xpath("./td[2]//text()")[0]
                ip_level = tr.xpath("./td[3]//text()")[0]
                ip_type = tr.xpath("./td[4]//text()")[0]
                city = tr.xpath("./td[5]//text()")[0]
                country = tr.xpath("./td[5]//text()")[0]
                ip_speed = tr.xpath("./td[6]//text()")[0]
                last_time = tr.xpath("./td[7]//text()")[0]
                # print(ip, port, ip_level, ip_type, city, country, ip_speed, last_time)
                #    1:'高匿',2:'普通',3:'透明',
                if (ip_level == setting.ip_levels[1]) or ('高匿' in ip_level):
                    ip_level = '高匿'
                    ip_info = self.ip_info_to_format(ip=ip, port=port, ip_level=ip_level, ip_type=ip_type, country=country, city=city,ip_speed=ip_speed, ip_from_where=ip_from_where)
                    #print(ip_info)
                    self.ip_list_not_to_check.append(ip_info)
                else:
                    print(f'ip {ip} is not 高匿 暂时不保存')
            time.sleep(random.random())

    def save_ip(self,path=setting.save_txt_path):
        """
        保存ip
        :return:
        """
        ip_total=len(self.ip_list_not_to_check)
        can_use_ip_list=[]

        with open(path, 'a', encoding='utf-8') as f:
            for ip_info in self.ip_list_is_check:
                #结果中有False结果
                if not ip_info:
                    continue
                can_use_ip_list.append(ip_info)
                data=self.ip_info_to_save(ip_info)

                f.writelines(data)

                f.write('\n')
                print(f'write {data} is ok')

        ip_is_ok_total = len(can_use_ip_list)
        print(f'一共抓取到{ip_total}个ip,有效ip有{ip_is_ok_total}个，可用ip比例为{str((ip_is_ok_total)/ip_total*100)[:5]}%    ')

    def save_again_ip(self,can_use_ip,path=setting.save_txt_path):
        """
        保存HTTP-ip:port 格式的数据
        :return:ip_can_use
        """
        with open(path, 'w', encoding='utf-8') as f:
            for data in can_use_ip:
                f.writelines(data)
                f.write('\n')
                print(f'save {data} ok')

    def check_txt_ip(self,proxies):
        '''
        检查txt ip
        :return:
        '''
        headers = self.get_headers()
        headers['Connection'] = 'close'
        headers['Host'] = 'www.baidu.com'
        headers['Referer'] = self.testurl
        print(headers)
        print(f'当前检查ip为：{proxies}')

        try:
            result = requests.get(self.testurl, headers, proxies=proxies, timeout=5).status_code
            if result == 200:
                print(f'{proxies}---可用')
                return True

            else:
                print(f'{proxies}---不可用')
                return False
        except TimeoutError:
            print('time out 连接网络时间超时')
            return False
        except Exception as e:
            print(f'{proxies}---不可用---因为{e}报错')
            return False

    def take_out_ip_to_use(self,path=setting.save_txt_path):
        #随机从可用的ip取出
        with open(path, 'r', encoding='utf-8') as f:
            ip_txt = []
            for s in f.readlines():
                ip_txt.append(s.strip())

            ip_txt = list(set(ip_txt))
            return random.choice(ip_txt)

    def refresh(self,path=setting.save_txt_path):
        #刷新一次txt里的ip可行性
        num=0
        can_use_ip=[]
        with open(path, 'r', encoding='utf-8') as f:
            info_total=f.readlines()
            for s in info_total:
                ip_info=s.strip()
                ip=ip_info.split(':')[0]
                port=ip_info.split(':')[1][:4]
                proxies = self.ip_to_format(ip, port)
                result=self.check_txt_ip(proxies)
                if result == True:
                    can_use_ip.append(ip_info)
                num+=1

                print(f'\r{path}里有{len(info_total)}条数据，正在检查第{num}个，刷新后能用的ip还有{len(can_use_ip)}个，占比{str((len(can_use_ip)/len(info_total))*100)[:5]}%')
        #去重
        can_use_ip=list(set(can_use_ip))
        self.save_again_ip(can_use_ip)

    def multiprocessing_to_check_ip(self,ip_info):
        '''
        多进程调用此函数
        :param ip_info:
        :return:
        '''

        headers = self.get_headers()
        headers['Connection'] = 'close'
        headers['Host'] = 'www.baidu.com'
        headers['Referer'] = self.testurl

        ip = ip_info['ip']
        port = ip_info['port']
        proxies = self.ip_to_format(ip,port)
        print(f'当前检查ip为：{proxies}')

        try:
            result = requests.get(self.testurl, headers, proxies=proxies, timeout=5).status_code
            if result == 200:
                print(f'{proxies}---可用')
                print(ip_info)
                return ip_info
            else:
                print(f'{proxies}---不可用')
                return False

        except TimeoutError:
            print('time out 连接网络时间超时')
            return False

        except Exception as e:
            print(f'{proxies}---不可用---因为{e}报错')
            return False

    def spider_total_ip(self):
        self.get_api_to_ip(want_to_get=setting.get_api_to_ip_num) #持续api端口
        self.get_freeip()
        self.get_data5uip()
        self.get_89ip()
        self.get_xiciip()
        self.get_goubanjia_ip()
        self.get_66ip()
        self.get_kuaidaili_ip()
        self.get_freeproxylist_for_ip()#这个是别人的代理池
        self.get_qiyun_ip()

    def multiprocessing_to_run(self):
        pool = Pool(processes=4)
        return_ip_list =pool.map(self.multiprocessing_to_check_ip,self.ip_list_not_to_check)
        #返回一个list，对应输入list的结果list
        self.ip_list_is_check.extend(return_ip_list)


    def run(self):
        self.spider_total_ip()#获取全部ip放进列表

        self.multiprocessing_to_run()#多进程运行

        print('----------------这里开始保存----------------')
        self.save_ip()#将可行的ip保存

        #保存ip到mysql  ----主函数
        # # 打开mysql服务
        # os.system('net start mysql')
        # print('正在打开mysql服务')
        # time.sleep(5)
        # save_ip_to_mysql = Save_ip_to_mysql()
        # save_ip_to_mysql.run()

        self.refresh()#刷新可行ip是否继续可行
        # print(self.take_out_ip_to_use())

if __name__ == '__main__':
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print(f"nowtime:{nowtime}")
    start = time.time()

    IP_PROXIES().run()

    end = time.time()
    print(f'time:{str(end-start)[:6]}s')
