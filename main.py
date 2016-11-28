# -*- coding: utf-8 -*-
import CONFIG as Config
import urllib2
import re
import gzip
import zlib
import StringIO

from lxml import etree
import lxml
import dateutil.parser as dparser
import datetime
import connection
import sys
import time
import HTMLParser
import unidecode

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8') 

#####################
#database setting
conn = connection.conn
Agnes = conn.Agnes
itemFilter = conn.itemFilter
groups = Agnes.groups_auto
urlFilter = itemFilter.urlFilter_group_auto
######################

visitList = []
visitedList = []
crawledItem = 0

stopSign = False

#preset parameter
grpnamePattern = ""
grpdescPattern = ""
grpaddressPattern = ""
grpemailPattern = ""
tagsPattern = []
picurlPattern = ""
contactNamePattern = ""
community = []
mainUrlList = ""
urlREList = []
subUrlList = []
grpnameModifiedList = []
grpdescModifiedList = []
grpaddressModifiedList = []
specificAddress = ""
urlPrefixList = []
additionalTags = []
domain = ""
grpsource = ""
grptype = ""
filterElementList = []
grpurlPattern = ""
customHeaders = ""

unqualifiedStarttimeCount = 0
unqualifiedEndtimeCount = 0
unqualifiedFlag = 3

def main():
	load_element()
	visit()

def visit():
	global mainUrlList

	visitList.extend(mainUrlList)
	visit_page()

def load_element():
	global grpnamePattern
	global grpdescPattern
	global grpaddressPattern
	global grpemailPattern
	global tagsPattern
	global picurlPattern
	global community
	global mainUrlList
	global urlREList
	global subUrlList
	global grpnameModifiedList
	global grpdescModifiedList
	global grpaddressModifiedList
	global specificAddress
	global urlPrefixList
	global additionalTags
	global domain
	global grpsource
	global grptype
	global filterElementList
	global contactNamePattern
	global grpurlPattern
	global customHeaders

	grpnamePattern = Config.grpname
	grpdescPattern = Config.grpdesc
	grpaddressPattern = Config.grpaddress
	grpemailPattern = Config.grpemail
	community = Config.community
	grpsource = Config.source
	mainUrlList = Config.mainUrlList
	urlREList = Config.urlREList
	subUrlList = Config.subUrlList
	domain = Config.domain
	grptype = Config.grptype
	urlPrefixList = Config.urlPrefixList
	filterElementList = Config.filterElementList
	picurlPattern = Config.picurl
	additionalTags = Config.additionalTags
	tagsPattern = Config.tags
	grpnameModifiedList = Config.grpnameModifiedList
	grpdescModifiedList = Config.grpdescModifiedList
	grpaddressModifiedList = Config.grpaddressModifiedList
	specificAddress = Config.specificAddress
	contactNamePattern = Config.contactName
	grpurlPattern = Config.grpurl
	customHeaders = Config.customHeaders

	if grpsource == "":
		grpsource = re.sub(r'https?:(//)?(www\.)?', '', mainUrlList[0])
		grpsource = re.sub(r'(?<=com|net|edu|org)/[\w\W]*', '', grpsource)

	if domain == "":
		domain = re.sub(r'(?<=com|net|edu|org)/[\w\W]*', '', mainUrlList[0])


def visit_page():
	global visitList
	global visitedList
	global crawledItem

	while len(visitList) != 0:
		requrl = visitList[0]

		
		#check custom header
		if customHeaders == "":
			req = urllib2.Request(requrl)
		else:
			req = urllib2.Request(requrl, headers = customHeaders)

		res_data = urllib2.urlopen(req, timeout = 10)
		encoding = res_data.info().get('Content-Encoding')
		
		if encoding in ('gzip','x-zip','deflate'):
			res = decode(res_data, encoding)
		else:
			res = res_data.read()

		analyze_page(res, requrl)
		"""
		if "/frontpage?field_event_sub_type_tid[7]=7&field_event_sub_type_tid[8]=8&field_event_sub_type_tid[9]=9&field_event_sub_type_tid[11]=11&field_event_sub_type_tid[12]=12&field_event_sub_type_tid[13]=13&field_event_sub_type_tid[14]=14&field_event_sub_type_tid[15]=15&page=1" in requrl:
			print visitList
			raw_input("23")
		"""
		visitList.remove(requrl)
		visitedList.append(requrl)
		#print visitedList
		#raw_input("visitList")
		
		#sys.stdout.write('visited quantity: '+ str(len(visitedList))+ "\r")
		#sys.stdout.flush()
		print requrl
		#print visitedList
		#print visitList
		#raw_input("123")


	time.sleep(0.5)
	print
	print "visited quantity: " + str(len(visitedList))
	print "crawledItem: " + str(crawledItem)
	#print visitList
	#print visitedList

def decode(res_data, encoding):
	res = res_data.read()
	if encoding == "deflate":
		data = StringIO.StringIO(zlib.decompress(res))
	else:
		data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(res))
	res = data.read()
	return res

def analyze_page(HTML, requrl):
	global stopSign
	#remove script content
	HTML = re.sub(r'<script[\w\W]*?</script>', '', HTML)
	soup = BeautifulSoup(HTML)
	HTML = str(soup.body)
	#print HTML
	#raw_input("HTML")
	if stopSign == False:
		fetch_url(HTML)
	
	fetch_information(HTML, requrl)

def fetch_url(HTML):
	global urlREList
	global domain
	global visitList
	global visitedList
	global urlPrefixList

	pendingUrlList = []

	urlList = []
	isUrlPrefix = False

	#print HTML
	#print domain
	#raw_input(123)


	for urlRE in urlREList:
		urlStr = urlRE
		urlStr = "(?<=href=\")" + urlStr + "(?=\")"
		urlREPattern = re.compile(urlStr)
		tempUrlList = urlREPattern.findall(HTML)
		urlList.extend(tempUrlList)

		urlStr = re.sub(domain, '', urlRE)
		urlStr = "(?<=href=\")" + urlStr + "(?=\")"
		urlREPattern = re.compile(urlStr)
		tempUrlList = urlREPattern.findall(HTML)
		urlList.extend(tempUrlList)

	#print urlList
	#raw_input("urlList")

	if urlPrefixList != []:
		isUrlPrefix = True

	for url in urlList:
		if not checkUselessUrl(url):
			if "http" not in url:
				url = domain + url
			if url not in visitedList and url not in visitList:
				if not isUrlPrefix:
					if domain in url:
						url = modifyUrl(url)
						#visitList.append(url)
						pendingUrlList.append(url)
				else:
					for urlPrefix in urlPrefixList:
						if urlPrefix in url:
							url = modifyUrl(url)
							#visitList.append(url)
							pendingUrlList.append(url)

	print pendingUrlList
	for url in pendingUrlList:
		if not check_url(url) and url not in visitList and url not in visitedList:
			visitList.append(url)
		else:
			#print "Visited this page before, won't record this url: ",
			#print url
			pass

	#print visitedList
	#print visitList
	#raw_input('123')

def modifyUrl(url):
	global subUrlList
	url = HTMLParser.HTMLParser().unescape(url)
	for subUrl in subUrlList:
		url = re.sub(subUrl, "", url)
	return url

def checkUselessUrl(url):
	global filterElementList
	isUseless = False
	uselessList = filterElementList
	for useless in uselessList:
		if useless in url.lower():
			isUseless = True
			break
	return isUseless

def fetch_information(HTML, requrl):
	global grpnamePattern
	global grpdescPattern
	global grpaddressPattern
	global grpemailPattern
	global community
	global grpsource
	global grptype
	global picurlPattern
	global tagsPattern
	global additionalTags
	global specificAddress
	global contactNamePattern
	global grpurlPattern

	currentTime =  datetime.datetime.now()
	currentDate = currentTime.strftime('%Y-%m-%d')
	currentDate = datetime.datetime.strptime(currentDate, '%Y-%m-%d')
	formerDate = currentDate + datetime.timedelta(days=-1)

	parser = etree.XMLParser(recover = True)
	tree = etree.fromstring(HTML, parser)
	
	grpname = ""
	grpdesc = ""
	grpaddress = ""
	picurl = ""
	tags = []
	grpurl = ""

	#raw_input(requrl)
	#print HTML
	#raw_input(123)

	grpname = tree.xpath(grpnamePattern)
	grpname = get_text(grpname)

	grpdesc = tree.xpath(grpdescPattern)
	grpdesc = get_text(grpdesc)

	grpemail = tree.xpath(grpemailPattern)
	grpemail = get_text(grpemail)

	contactName = tree.xpath(contactNamePattern)
	contactName = get_text(contactName)

	if specificAddress != "":
		grpaddress = specificAddress

	if grpname == "":
		print "grpname unqualified: ",
		print requrl
		return 0

	if grpaddressPattern != "":
		grpaddress = tree.xpath(grpaddressPattern)
		grpaddress = get_text(grpaddress)

	if picurlPattern != "":
		picurl = tree.xpath(picurlPattern)
		picurl = get_picurl(picurl)

	if tagsPattern != "":
		tags = tree.xpath(tagsPattern)
		tags = get_text(tags)
		tags = analyze_tags(tags)

	if grpurlPattern != "":
		grpurl = tree.xpath(grpurlPattern)
		grpurl = get_text(grpurl)

	if "www" not in picurl and "http" not in picurl:
		picurl = domain + "/" + picurl
	#raw_input(picurl)

	url = requrl

	#decode as unicode and analyze text
	grpname = analyze_text(unidecode.unidecode(grpname))
	grpdesc = analyze_text(unidecode.unidecode(grpdesc))

	grpaddress = analyze_text(grpaddress)

	fetch_data(url, grpname, grpdesc, grpaddress, community, grpsource, formerDate, tags, additionalTags, picurl, contactName, grpemail, grptype, grpurl)

def get_picurl(lxmlItems):
	picurl = ""
	for lxmlItem in lxmlItems:
		picurl += lxmlItem.get("src")
	picurl = re.sub(r"^\W*?(?=\w)", "", picurl)

	return picurl

def get_text(lxmlItems):
	text = ""
	for lxmlItem in lxmlItems:
		if isinstance(lxmlItem, unicode) or isinstance(lxmlItem, str):
			text = text + "\n" + lxmlItem
		else:
			for item in lxmlItem.itertext():
				text = text + "\r\n" + item
	text = text.strip()
	return text

def analyze_tags(tags):
	tagsSplitCharList = [",", "|", ";", "\\", "/", "."]
	tagsSplitChar = ""
	for tagsSplitCharItem in tagsSplitCharList:
		if tagsSplitCharItem in tags:
			tagsSplitChar = tagsSplitCharItem
			break
	if tagsSplitChar != "":
		tagsList = tags.split(tagsSplitChar)
	else:
		tagsList = [tags]		
	return tagsList

def analyze_text(text):
	text = re.sub(r'<br>', ' ', text)
	text = re.sub(r'<[\w\W]*?>', '', text)
	text = re.sub(r'\s{2,}', ' ', text)
	text = text.strip()
	return text

def modify_grpname(grpname):
	global grpnameModifiedList

	for grpnameModifiedItem in grpnameModifiedList:
		grpname = re.sub(grpnameModifiedItem, '', grpname)
	return grpname

def modify_grpdesc(grpdesc):
	global grpdescModifiedList

	for grpdescModifiedItem in grpdescModifiedList:
		grpdesc = re.sub(grpdescModifiedItem, '', grpdesc)
	return grpdesc

def modify_grpaddress(grpaddress):
	global grpaddressModifiedList

	for grpaddressModifiedItem in grpaddressModifiedList:
		grpaddress = re.sub(grpaddressModifiedItem, '', grpaddress)
	return grpaddress

def lowerKeywords(keywords):
	returnKeywords = []
	for keyword in keywords:
		returnKeywords.append(keyword.lower())
	return returnKeywords

def decide_group_gender(grpname, grpdesc, keywords):
	womenGrpnameKeywordList = ["all-female", "all female", "panhellenic", "women's club", "womens club", "club softball"]
	womenKeywordsList = ["all-female", "all female"]
	womenGrpdescKeywordList = ["all-female", "all female"]
	menGrpnameKeywordList = ["interfraternity", "men's club", "mens club", "club baseball"]
	menKeywordsList = ["all-male", "all male"]
	menGrpdescList = ["all-male", "all male"]

	keywords = lowerKeywords(keywords)
	grpname = grpname.lower()
	grpdesc = grpdesc.lower()

	for womenGrpnameKeyword in womenGrpnameKeywordList:
		if womenGrpnameKeyword in grpname:
			return "female"
	for womenKeyword in womenKeywordsList:
		if womenKeyword in keywords:
			return "female"
	for womenGrpdescKeyword in womenGrpdescKeywordList:
		if womenGrpdescKeyword in grpdesc:
			return "female"
	for menGrpnameKeyword in menGrpnameKeywordList:
		if menGrpnameKeyword in grpname:
			return "male"
	for menKeyword in menKeywordsList:
		if menKeyword in keywords:
			return "male"
	for menGrpdesc in menGrpdescList:
		if menGrpdesc in grpdesc:
			return "male"
	return "both"

def decide_group_audience(keywords, grpname):
	graduateKeywordList = ["grad", "grad student", "grad students", "graduate student", "graduate students"]
	graduateGrpnameList = [" graduate", " graduates", " grads"]
	
	keywords = lowerKeywords(keywords)
	grpname = grpname.lower()

	for graduateKeyword in graduateKeywordList: 
		if graduateKeyword in keywords:
			return "grad"
	for graduateGrpname in graduateGrpnameList:
		if graduateGrpname in grpname:
			return "grad"
	return "both"
	
def fetch_data(url, grpname, grpdesc, grpaddress, community, grpsource, formerDate, tags, additionalTags, picurl, contactName, grpemail, grptype, grpurl):
	if not check_url(url):
		grpname = modify_grpname(grpname)
		grpdesc = modify_grpdesc(grpdesc)
		grpaddress = modify_grpaddress(grpaddress)
		grpGender = decide_group_gender(grpname, grpdesc, tags)
		audience = decide_group_audience(tags, grpname)
		if grptype == "":
			grptype = "private"
		feed_item(url, grpname, grpdesc, grpaddress, community, grpsource, formerDate, tags, additionalTags, picurl, contactName, grpemail, grpGender, audience, grptype, grpurl)
	else:
		print "Exist: ",
		print url

def check_url(url):
	isExist = False
	ele = {"url":url}
	for flag in urlFilter.find(ele):
		isExist = True
	return isExist

def feed_item(url, grpname, grpdesc, grpaddress, community, grpsource, formerDate, tags, additionalTags, picurl, contactName, grpemail, grpGender, audience, grptype, grpurl):
	item = {}
	item["grpname"] = grpname
	item["grpaddress"] = grpaddress
	item["grpdesc"] = grpdesc
	item["grpemail"] = grpemail
	item["createdate"] = formerDate
	item["community"] = community
	item["picurl"] = picurl
	item["keywords"] = []
	
	item["weburl"] = []
	item["weburl"].append(url)
	if grpurl != "":
		item["weburl"].append(grpurl)
	
	item["grptype"] = grptype
	item["status"] = True

	item["audience"] = audience
	item["members"] = []
	item["memcount"] = len(item["members"])
	item["pendingreq"] = []

	item["events"] = []
	item["evtcount"] = len(item["events"])
	item["admin"] = []
	item["gender"] = grpGender
	
	item["grpsource"] = grpsource
	item["other"] = {"tags":tags}
	if contactName != "":
		item["other"]["contact name"] = contactName
	item["other"]["tags"].extend(additionalTags)
	item["just_crawled"] = True
	item["isAvailable"] = True

	#print item
	#print item["grpaddress"]
	#raw_input("item")

	insert_item(item)

def feed_url(url):
	ele = {"url":url}
	urlFilter.insert(ele)

def insert_item(item):
	global crawledItem

	print "Insert!"
	crawledItem += 1
	print item["grpname"]
	#print item
	raw_input(item["weburl"][0])
	
	groups.insert(item)
	feed_url(item["weburl"][0])

if __name__ == '__main__':
	main()


	