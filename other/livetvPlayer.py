# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
import cookielib
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
import datetime
import sys
import time
import CustomPlayer
import captcha

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
communityStreamPath = os.path.join(addonPath,'resources/community')
COOKIEFILE = communityStreamPath+'/livePlayerLoginCookie.lwp'
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))

def PlayStream(sourceEtree, urlSoup, name, url):
	try:
		playpath=urlSoup.chnumber.text
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('XBMC', 'Communicating with Livetv')
		pDialog.update(40, 'Attempting to Login')
		if shouldforceLogin():
			if performLogin():
				print 'done login'
		print 'ooops'

		code=getcode();

		print 'firstCode',code

		if 1==2 and not code or code[0:1]=="w":
			pDialog.update(40, 'Refreshing Login')
			code=getcode(True);
			print 'secondCode',code
		liveLink= sourceEtree.findtext('rtmpstring')
		pDialog.update(80, 'Login Completed, now playing')
		print 'rtmpstring',liveLink
		#liveLink=liveLink%(playpath,match)
		liveLink=liveLink%(playpath,code)
		name+='-LiveTV'
		print 'liveLink',liveLink
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
		pDialog.close()
		player = CustomPlayer.MyXBMCPlayer()
		start = time.time()
		#xbmc.Player().play( liveLink,listitem)
		player.play( liveLink,listitem)
		while player.is_active:
			xbmc.sleep(200)
		#return player.urlplayed
		#done = time.time()
		done = time.time()
		elapsed = done - start
		if player.urlplayed and elapsed>=3:
			return True
		else:
			return False 
	except:
		traceback.print_exc(file=sys.stdout)    
	return False    

def getcode():
	#url = urlSoup.url.text
	cookieJar=getCookieJar()
	link=getUrl('http://www.livetv.tn/index.php',cookieJar)
	captcha=None
	
	match =re.findall('<img src=\"(.*?)\" alt=\"CAPT', link)
	if len(match)>0:
		captcha="http://www.livetv.tn"+match[0]
	else:
		captcha=None
	solution=None


	if captcha:
		local_captcha = os.path.join(profile_path, "captchaC.img" )
		localFile = open(local_captcha, "wb")
		localFile.write(getUrl(captcha,cookieJar))
		localFile.close()
		cap=parseCaptcha(local_captcha)
		print 'parsed cap',cap
		if cap=="" or not len(cap)==3:
			solver = InputWindow(captcha=local_captcha)
			solution = solver.get()
		else:
			solution=cap

	if solution:
		#do captcha post
		post={'capcode':solution}

		post = urllib.urlencode(post)
		link=getUrl("http://www.livetv.tn/",cookieJar,post)
	
	code =re.findall('code=(.*?)[\'\"]', link)[0]
	return code

def parseCaptcha(filePath):
	retVal=""
	try:
		print 'the val is'
		retVal=captcha.getString(filePath)
		print 'the val is',retVal
	except:  traceback.print_exc(file=sys.stdout)
	return retVal
def getUrl(url, cookieJar=None,post=None):

	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	#opener = urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	response = opener.open(req,post)
	link=response.read()
	response.close()
	return link;

    
def getCookieJar():
	cookieJar=None

	try:
		cookieJar = cookielib.LWPCookieJar()
		cookieJar.load(COOKIEFILE,ignore_discard=True)
	except: 
		cookieJar=None
	
	if not cookieJar:
		cookieJar = cookielib.LWPCookieJar()

	return cookieJar

	
def performLogin():
	cookieJar=cookielib.LWPCookieJar()
	html_text=getUrl("http://www.livetv.tn/login.php",cookieJar)
	cookieJar.save (COOKIEFILE,ignore_discard=True)
	print 'cookie jar saved',cookieJar

	match =re.findall('<img src=\"(.*?)\" alt=\"Cap', html_text)
	if len(match)>0:
		captcha="http://www.livetv.tn/"+match[0]
	else:
		captcha=None
	

		
	if captcha:
		local_captcha = os.path.join(profile_path, "captcha.img" )
		localFile = open(local_captcha, "wb")
		localFile.write(getUrl(captcha,cookieJar))
		localFile.close()
		cap=parseCaptcha(local_captcha)
		print 'login parsed cap',cap

		if cap=="" or not len(cap)==4:
			solver = InputWindow(captcha=local_captcha)
			solution = solver.get()
		else:
			solution=cap
	if solution or captcha==None:

		print 'performing login'
		userName=selfAddon.getSetting( "liveTvLogin" )
		password=selfAddon.getSetting( "liveTvPassword")
		if captcha:
			post={'pseudo':userName,'epass':password,'capcode':solution}
		else:
			post={'pseudo':userName,'epass':password}
		post = urllib.urlencode(post)
		getUrl("http://www.livetv.tn/login.php",cookieJar,post)

		return shouldforceLogin(cookieJar)==False
	else:
		return False


def shoudforceLogin2():
    try:
#        import dateime
        lastUpdate=selfAddon.getSetting( "lastLivetvLogin" )
        print 'lastUpdate',lastUpdate
        do_login=False
        now_datetime=datetime.datetime.now()
        if lastUpdate==None or lastUpdate=="":
            do_login=True
        else:
            print 'lastlogin',lastUpdate
            try:
                lastUpdate=datetime.datetime.strptime(lastUpdate,"%Y-%m-%d %H:%M:%S")
            except TypeError:
                lastUpdate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(lastUpdate, "%Y-%m-%d %H:%M:%S")))
        
            t=(now_datetime-lastUpdate).seconds/60
            print 'lastUpdate',lastUpdate,now_datetime
            print 't',t
            if t>15:
                do_login=True
        print 'do_login',do_login
        return do_login
    except:
        traceback.print_exc(file=sys.stdout)
    return True

def shouldforceLogin(cookieJar=None):
    try:
        url="http://www.livetv.tn/index.php"
        if not cookieJar:
            cookieJar=getCookieJar()
        html_txt=getUrl(url,cookieJar)
        
            
        if '<a  href="http://www.livetv.tn/login.php">' in html_txt:
            return True
        else:
            return False
    except:
        traceback.print_exc(file=sys.stdout)
    return True
    
class InputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,30,624,60,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        time.sleep(3)        
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False
