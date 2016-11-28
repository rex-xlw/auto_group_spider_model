#input xpath
grpname = '//*[@id="dnf_class_values_student_group__name__widget"]'
grpdesc = '//*[@id="dnf_class_values_student_group__purpose__widget"]'
grpaddress = ''
grpemail = '//div[@id="dnf_class_values_student_group__email__widget"]/a'
tags = ''
contactName = '//div[@id="dnf_class_values_student_group__advisers__0__fullname__widget"]'
grpurl = ''

#all the picurl should be included in the src tag
picurl = '//div[@class="detailed_logo"]/img'
#input the list of community
community = ["american", "agnes"]

#input url #format: "http(s)://xx.xxx.edu(com/net)/xxx/xxx/xxx" The domain name should be the same
mainUrlList = [
				'https://american-community.symplicity.com/index.php?mode=list',
				]
				
#input a list of regular expression #format: "http(s)://xx.xxx.edu(com/net)/xxx""
urlREList = [
				'\?mode=form&amp;id=\w*&amp;tab=profile',
				'\?_so_list_from\w*=\d*?&amp;_so_list_from\w*_page=\d*',
			]
#remove url partial pattern
subUrlList = []

#element modify list
grpnameModifiedList = []
grpdescModifiedList = []
grpaddressModifiedList = []

#input specific location, can ignore
specificAddress = ''

#input a list of half regualr experssion
urlPrefixList = []

#input addtional tags for the crawlers
additionalTags = []

#input domain, can ignore
domain = ''

#input grpsource, can ignore
source = ''

#input grptype, can ignore
grptype = ''

#Preset parameter
filterElementList = ['.jpg', '.css', '.png', '.js', '.ico', '.pdf', '.docx', '.jpeg']

#custom header
customHeaders = {
					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Encoding':'gzip, deflate, sdch, br',
					'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
					'Connection':'keep-alive',
					'Cookie':'PHPSESSID=8791b51facbc1615e06daf02b35673e0; sympcsm_cookies_checked=1; BALANCEID=balancer.172.16.120.64',
					'Host':'american-community.symplicity.com',
					'Referer':'https://american-community.symplicity.com/?mode=list',
					'Upgrade-Insecure-Requests':1,
					'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
				}