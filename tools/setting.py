#每个代理ip地址的信息
sourceLists = [
	{
		# 总共29页，仅取前2页
		"urls": ["http://www.89ip.cn/index_%s.html" % n for n in range(1, 5)],
		"function": "GeneralXpath",
		"pattern": "//tbody/tr",#所有节点
		"position": {"ip": "./td[1]/text()", "port": "./td[2]/text()", "area": "./td[3]/text()"},
		"origin": "89ip",
	},
	{
		# 刷新会变化
		"urls": ["http://www.data5u.com/%s" % n for n in [""]],
		"function": "GeneralXpath",
        "pattern": "//ul[@class='l2']",#所有节点
        "position": "./span[{}]//text()",
		"origin": "data5u",
	},
    {
		# 仅取前4页
        "urls": ['https://www.freeip.top/?page=%s' % n for n in range(1,5)],
        "function": "GeneralXpath",
        "pattern": "//table[@class='layui-table']/tbody//tr",#所有节点
        "position": "./td/text()",
        "origin": "freeip",
    },
    {

        "urls":['http://www.xicidaili.com/%s/%s'%(type,pagenum) for type in ['nt','nn','wn','wt'] for pagenum in range(1, 4)],
        "function": "GeneralXpath",
        "pattern": "//table[@id='ip_list']//tr",#所有节点
        "position": "./td[{}]/text()",
        "origin": "xiciip",

    },
    {   # 仅取前4页
        "urls":["http://www.66ip.cn/{}.html".format(i) for i in range(1,5)],
        "function": "GeneralXpath",
        "pattern": "//div[@align='center']/table/tr",#所有节点
        "position": "./td[{}]/text()",
        "origin": "66ip",
    },
    {   # 仅取前2页
            "urls":['https://www.kuaidaili.com/free/inha/{}/'.format(i)for i in range(1,3)],
            "function": "GeneralXpath",
            "pattern": ".//table//tr",#所有节点
            "position": "./td[{}]/text()",
            "origin": "kuaidaili_ip",
        },
    {   # 仅取前4页
            "urls":['http://www.qydaili.com/free/?action=china&page={}'.format(i)for i in range(1,5)],
            "function": "GeneralXpath",
            "pattern": ".//table[@class='table table-bordered table-striped']//tr",#所有节点
            "position": "./td[{}]//text()",
            "origin": "7yip",
        }
]

#随机访问头
user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

ip_levels={
    1:'高匿',
    2:'普通',
    3:'透明',
           }

ip_types={
    1:'HTTP',
    2:'HTTPS',
}

#保存ip的路径
save_txt_path='ip_proxies_pool.txt'

#某个端口你想获取的量
get_api_to_ip_num=100

