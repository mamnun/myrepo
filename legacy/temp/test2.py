import urllib2,re
f = open('arabichannels.comindex.php', 'r')
link2=f.read()
print link2
url="http://www.hdarabic.com/"
req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
response = urllib2.urlopen(req)
link=response.read()
response.close()
match =re.findall('iptv.php.*nume\">(.*?)<.*src=\"\.\/images\/(.*?)\.',link,  re.IGNORECASE)
total=0
totalfound=0
try:
	if len(match)>0:
		total=len(match)
		totalfound=0
		for name1,name2 in match:
			trynum=1
			found=False
			while trynum<=3 and not found:
				if trynum==2:
					newurl=url+name2.strip()+'.php'
					newurl=newurl.replace(' ','_').lower()
				elif trynum==3:
					newurl=url+name1.strip()+'.php'
					newurl=newurl.replace(' ','_').lower()				
				#elif trynum==5:
				#	newurl=url+name2.strip()+'.php'
			#		newurl=newurl.replace(' ','').lower()
				#elif trynum==4:
				#	newurl=url+name2.strip()+'.php'
				#	newurl=newurl.replace(' ','').lower()
				#elif trynum==3:
				#	newurl=url+name1.strip().replace('Al ','')+'.php'
				#	newurl=newurl.replace(' ','_').lower()
				elif trynum==1:
					match2 =re.findall('.src=\'(.*?)\'.*?me\">(' +name1+ ')<',link2,  re.IGNORECASE)
					if len(match2)>0:
						newurl=url+match2[0][0]
						#print 'inside',newurl
					#else:
					#	print 'not in file'
					#	print '.src=\'(.*?)\'.*?me\">(' +name1+ ')<'
				try:
					
					req = urllib2.Request(newurl)
					req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
					response = urllib2.urlopen(req)
					link=response.read()
					found=True
					print '(\''+name1 +'\',\''+newurl+'\',\''+name2+'\'),'
					#print newurl
				except KeyboardInterrupt: raise
				except:	pass			
				trynum=trynum+1	
			if not found:
				print 'not found' + name1
			else: totalfound+=1
except KeyboardInterrupt:
	print 'Stopped!'
print 'Total tried %d, found %d'%(total,totalfound)				
				
				