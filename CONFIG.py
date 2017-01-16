#input xpath
grpname = '//h2[@class="h2__avatarandbutton text__shadow"]'
grpdesc = '//div[@class="row container-orgabout"]/div[@class="col-xs-12 col-sm-7"]/p'
grpaddress = ''
grpemail = ''
tags = ''
contactName = '//ul[@class="list-unstyled list-inline pull-left"]/li[2]/text()'
grpurl = ''

#all the picurl should be included in the src tag
picurl = '//img[@class="img-circle img__orgavatar"]'
#input the list of community
community = ["cua", "agnes"]

#input url #format: "http(s)://xx.xxx.edu(com/net)/xxx/xxx/xxx" The domain name should be the same
mainUrlList = [
				'https://getconnected.gmu.edu/organizations\?SearchType=None&amp;SelectedCategoryId=0&amp;CurrentPage=1',
				]
				
#input a list of regular expression #format: "http(s)://xx.xxx.edu(com/net)/xxx""
#/organization/ActiveMinds_CUA
#/organizations?SearchType=None&amp;SelectedCategoryId=0&amp;CurrentPage=2
urlREList = [
				'/organization/\w+',
				'/organizations\?SearchType=None&amp;SelectedCategoryId=0&amp;CurrentPage=\d+'
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
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'en-US,en;q=0.8',
			'Connection': 'keep-alive',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
			}