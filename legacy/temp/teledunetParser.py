import urllib2,re
f = open('telesource.html', 'r')
link2=f.read()
f.close()
match =re.findall('set_favoris\(\'(.*?)\',\'(.*?)\'\s?(.)',link2,  re.IGNORECASE)
total=0
totalfound=0
cstream='<channels>'
infostream='<streamingInfos>'
try:
	if len(match)>0:
		total=len(match)
		totalfound=0
		for id,name,image in match:

			imageUrl = 'http://www.teledunet.com/tv_/icones/%s.jpg'%id
			cstream+='<channel><id>%s</id><cname>%s</cname><imageurl>%s</imageurl><enabled>True</enabled></channel>'%(id,name,imageUrl)
			infostream+='<streaminginfo><id>%s</id><url>%s</url></streaminginfo>'%(id,id)
	cstream+='</channels>'
	infostream+='</streamingInfos>'

	print cstream
	print infostream
except KeyboardInterrupt:
	print 'Stopped!'
print 'Total tried %d, found %d'%(total,totalfound)				
				
				