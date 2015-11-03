import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver
import urlparse
import HTMLParser
import xbmcaddon
from dirCreator import parseList;
from TurlLib import getURL;
import thread
import time
#from f4mDownloader import F4MDownloader
from operator import itemgetter
import traceback
import os
import sys
import traceback
import threading
import cookielib


REMOTE_DBG=False;
#stopPlaying=threading.Event()
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)  


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                
    return param

addon_id = 'plugin.video.pitelevision'
selfAddon = xbmcaddon.Addon(id=addon_id)
__addonname__   = selfAddon.getAddonInfo('name')
__icon__        = selfAddon.getAddonInfo('icon')
DIR_USERDATA   = xbmc.translatePath(selfAddon.getAddonInfo('profile'))#selfAddon["profile"])


COOKIEFILE = DIR_USERDATA+'/PiTVLoginCookie.lwp'  
 
mainurl='http://www.pitelevision.com/international/'



def Addtypes():
    parseList(getMainMenu());#caching here
    return

def getMainMenu():
    list=[]
    list.append({'name':'Video On Demand','url':'http://cat','mode':'VOD'})
    list.append({'name':'Live Channels','url':'http://pitelevision.com/international/channels.php','mode':'ALLC'})
    list.append({'name':'Settings','url':'Settings','mode':'Settings','isFolder':False})
    #print list;
    return list;

    

    
def AddVOD(Fromurl,mode):
    parseList(getVODList(Fromurl,mode));#caching here

def getVODList(Fromurl,mode):

    listToReturn=[]
    listToReturn.append({'name':'Dramas','url':'http://pitelevision.com/international/vodlist.php?vodCatId=1&page=1','mode':'VOD-Dramas','iconimage':''})
    listToReturn.append({'name':'Movies','url':'http://pitelevision.com/international/vodlist.php?vodCatId=3&page=1','mode':'VOD-Movies','iconimage':''})
    listToReturn.append({'name':'Shows','url':'http://pitelevision.com/international/vodlist.php?vodCatId=4&page=1','mode':'VOD-Shows','iconimage':''})
    listToReturn.append({'name':'Music Videos','url':'http://pitelevision.com/international/vodlist.php?vodCatId=5&page=1','mode':'VOD-Music','iconimage':''})
    return listToReturn;

	
def ShowSettings(Fromurl):
	#playF4mLink('http://bbcfmhds.vo.llnwd.net/hds-live/livepkgr/_definst_/bbc1/bbc1_480.f4m','mymovie')
	#playF4mLink2('http://zaphod-live.bbc.co.uk.edgesuite.net/hds-live/livepkgr/_definst_/bbc1/bbc1_1500.f4m','Bbc')
	#return
    selfAddon.openSettings()


def AddLiveEnteries(Fromurl,PageNumber,mode):
    parseList(getLiveEnteriesList(Fromurl,PageNumber,mode));#caching here
    

def getLiveEnteriesList(Fromurl,PageNumber,mode):

    if shouldforceLogin():
        print 'performing login'
        if not performLogin():
            print 'login failed'
#    link=getURL(Fromurl,cookieJar=getCookieJar())
    link=getUrl(Fromurl,cookieJar=getCookieJar())
    #print 'getEnteriesList',link
    patt='<a href="(.*?)".*?title="(.*?)".*\s*.*img src="(.*?)"'
    match =re.findall(patt, link)
    #print 'match',match
    listToReturn=[]
    rmode='PlayLive'
    for cname in match:
        imageurl=cname[2].replace(' ','%20');
        url=cname[0];
        
        if not imageurl.startswith('http'): imageurl=mainurl+'/'+imageurl
        if not url.startswith('http'): url=mainurl+url
        #print imageurl    
        listToReturn.append({'name':cname[1],'url':url,'mode':rmode,'iconimage':imageurl,'isFolder':False})
    return listToReturn

def AddEnteries(Fromurl,PageNumber,mode):
    parseList(getEnteriesList(Fromurl,PageNumber,mode));#caching here
    
def getEnteriesList(Fromurl,PageNumber,mode):
    link=getURL(Fromurl).result;
    #print 'getEnteriesList',link
    
    
    listToReturn=[]
    

    links=link.split('<div class="col-md-12">')
    rmode='PlayVOD';
    for lnk in links:
        if '<h1>' in lnk:
            pat='<h1>(.*?)<\/h1>'
#            print lnk
            SName=re.findall(pat,lnk)[0]
            match =re.findall('<a href="(.*)" class="ajax"><img src="(.*?)".*?\s*.*title">(.*?)<', lnk)
            listToReturn.append({'name':SName,'url':'http://ignoreme','mode':'ignore','iconimage':'http://ignoreme','isFolder':False})
            for cname in match:
                #print cname[2]
                #addDir(cname[2] ,mainurl+cname[0] ,5,cname[1],isItFolder=False)
                imageurl=cname[1].replace(' ','%20');
                url=cname[0];
                
                if not imageurl.startswith('http'): imageurl=mainurl+'/'+imageurl
                if not url.startswith('http'): url=mainurl+url
                #print imageurl    
                listToReturn.append({'name':'  '+cname[2],'url':url,'mode':rmode,'iconimage':imageurl,'isFolder':False})
    if 'Page ' in link:
#        print 'ppppppppppppppppppage'
        try:
            patt='Page ([0-9]*) of ([0-9]*)'
            match =re.findall(patt, link)
            currentPage=match[0][0]
            lastPage=match[0][1]
#            print 'currentPage',currentPage
            url=Fromurl;
            nextPage=''
            previousPage=''
            prevurl=''
            if not currentPage==lastPage:
                nextPage='>>Next Page'
                nextPageNum=int(currentPage)+1
                nexturl= url.split('page=')[0]+'page='+str(nextPageNum)
            if not currentPage=="1":
                previousPage='<<<< Previous Page'
                nextPageNum=int(currentPage)-1
                prevurl= url.split('page=')[0]+'page='+str(nextPageNum)

            p='Page %s of %s'
            p=p%(currentPage,lastPage)
            currentpage='[COLOR FF11b500]'+p+'[/COLOR]'
            
            prevpage='[COLOR FF11b500]'+previousPage+'[/COLOR]'
            #addDir('Next Page' , url ,4,'',pageNum=pNumber)

            listToReturn.insert(0,{'name': currentpage,'url':nexturl,'mode':'null','iconimage':''})
            listToReturn.append({'name': currentpage,'url':nexturl,'mode':'null','iconimage':''})                

            if not nextPage=='':
                nextpage='[COLOR FF11b500]'+nextPage+'[/COLOR]'
                listToReturn.insert(1,{'name': nextpage,'url':nexturl,'mode':mode,'iconimage':''})
                listToReturn.append({'name': nextpage,'url':nexturl,'mode':mode,'iconimage':''})
            
            if not prevurl=='':
                listToReturn.insert(1,{'name': prevpage,'url':prevurl,'mode':mode,'iconimage':''})
                listToReturn.append({'name': prevpage,'url':prevurl,'mode':mode,'iconimage':''})

            
            
        except: traceback.print_exc()
    return listToReturn
	
def PlayShowLink ( url, name ): 
    list=getShowUrl(url); #cachinghere
    #print 'list',list
    if len(list)>0:
        urlToPlay=list["url"]
        if 'youtube' not in urlToPlay:
            line1 = "Playing Video"
            timeWait=2000
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))
    
            playlist = xbmc.PlayList(1)
            playlist.clear()
            listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
            listitem.setInfo("Video", {"Title":name})
            listitem.setProperty('IsPlayable', 'true')
            playlist.add(urlToPlay,listitem)
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(playlist)
        else:
            line1 = "Playing Youtube Video"
            timeWait=2000
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))
            youtubecode= match =re.findall('watch\?v=(.*)', urlToPlay)
            #print 'youtubecode',youtubecode
            youtubecode=youtubecode[0]
            uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
            #print 'going to play',uurl;
        #    print uurl
            xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
    else:
        line1='Unable to find url'
        timeWait=2000
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))
    return
    
def getShowUrl(url):
    line1="Fetching URL";
    timeWait=2000
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))
    if shouldforceLogin():
        print 'performing login'
        if not performLogin():
            print 'login failed'
        
    link=getUrl(url,cookieJar=getCookieJar())
    match= re.findall('url:"(.*?)"', link)
    urlToPlay=match[0]
    urlToPlay=urlToPlay.replace(" ","%20")
    
    return {'url':urlToPlay}
    
    
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
    
def shouldforceLogin(cookieJar=None, currentPage=None):
    try:
        url=mainurl+'/index.php'
        if not cookieJar:
            cookieJar=getCookieJar()
        if currentPage==None:
            html_txt=getUrl(url,cookieJar=cookieJar)
        else:
            html_txt=currentPage
            print 'html_txt',currentPage
            
        if 'Login / Sign up' in html_txt:
            return True
        else:
            return False
    except:
        traceback.print_exc(file=sys.stdout)
    return True
def getUrl(url, cookieJar=None,post=None, timeout=30, headers=None):


	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	#opener = urllib2.install_opener(opener)
	req = urllib2.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	if headers:
		for h,hv in headers:
			req.add_header(h,hv)

	response = opener.open(req,post,timeout=timeout)
	link=response.read()
	response.close()
	return link;
    
def performLogin():
    cookieJar=cookielib.LWPCookieJar()
    userName=selfAddon.getSetting( "piTvLogin" )
    password=selfAddon.getSetting( "piTvPwd")


    post={'username':userName,'password':password}

    post = urllib.urlencode(post)

    link=getUrl('http://pitelevision.com/international/include/login.php',post=post, cookieJar=cookieJar)
    
    cookieJar.save (COOKIEFILE,ignore_discard=True)
    #return shouldforceLogin(cookieJar, link)==False
    return True
def getLiveUrl(url):
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('XBMC', 'Communicating with piTV')
    pDialog.update(20, 'checking Login status')
    print 'checking logiin'
    if shouldforceLogin():
        print 'performing login'
        pDialog.update(40, 'Performing login')
        if not performLogin():
            print 'login failed'
            pDialog.update(60, 'Login failed')
          
    pDialog.update(70, 'Fetching Live URL')          


#    print 'fetching url',url
    link=getUrl(url,cookieJar=getCookieJar())
    pDialog.update(90, 'Fetching Live URL')   
    match= re.findall('url:"(.*?.f4m.*?)"', link)
#    print 'match',match
    url=""
    if len(match)>0:

         url=match[0]#+'.f4m'#url=match[0]+'.m3u8'
         #url='rtsp://202.125.131.170:554/pitelevision/starsports41'
    #print 'url',url
    pDialog.close()
    return {'url':url}
    
    
        
    return	
#flashvars="src=(.*?)\.f

def PlayLiveLink ( url,name ): 
    line1="fetching URL";
    timeWait=2000
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))

    urlDic=getLiveUrl(url)
    #urlDic='rtsp://202.125.131.170:554/pitelevision/starsports41'	
    if not urlDic==None and len(urlDic["url"])>0:
        line1="Url found, Preparing to play";
        timeWait=2000
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))

        playfile=urlDic["url"]
        #progress.update( 100, "", "Almost done..", "" )
        #print 'playfile',playfile
        #listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        #print "playing stream name: " + str(name) 
        #xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( playfile, listitem)
        print 'playfile',playfile
        proxy=None#getProxy()
        if proxy:
            line1="using proxy %s"%proxy;
            timeWait=2000
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))
        playF4mLink(playfile,name,proxy, True)
    else:
          line1="Url not found";
          timeWait=2000
          xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeWait, __icon__))

    return
    
def getProxy():
    isproxy=selfAddon.getSetting( "isProxyEnabled" ) 
    proxy=None
    if isproxy=="true":
        is_custom_proxy=selfAddon.getSetting( "isCustomProxy" )
        if is_custom_proxy=="true":
            proxy="%s:%s"%(selfAddon.getSetting( "proxyName" ),selfAddon.getSetting( "proxyPort" ))
        else:
            proxy=selfAddon.getSetting( "selectedProxy" )
    return proxy


#def playF4mLinkOld(url,name,proxy=None):
#	print "URL: " + url
#	listitem = xbmcgui.ListItem("myfile")
#	downloader=F4MDownloader()
#	runningthread=thread.start_new_thread(downloader.download,('myfile.flv',url,stopPlaying,proxy,))
#	progress = xbmcgui.DialogProgress()
#	progress.create('Starting Stream')
#	stream_delay = 10
#	if proxy:
#		stream_delay+=20
#	cancelled=False
#	for i in range(stream_delay):
#		percent=(i*100/stream_delay)
#		print 'percent',percent
#		progress.update( percent, "", 'Trying to cache data...'+downloader.status +' seq:' +str(downloader.seqNumber), "" )
#		if downloader.status=="play" and downloader.seqNumber>5:
#			break
#		if downloader.status=="finished":
#			stopPlaying.set()
#			cancelled=True
#			break
                        
#		if progress.iscanceled():
#			stopPlaying.set()
#			cancelled=True
#			break
#		xbmc.sleep(1000)
#	mplayer = MyPlayer()
#
#	if not cancelled:
#		filename =downloader.outputfile;#DIR_USERDATA + "/myfile.flv"
#		progress.close()
#		mplayer.play(filename,listitem)
#		while True:
#			xbmc.log('Sleeping...')
#			xbmc.sleep(1000)
#			if stopPlaying.isSet():
#				break;
#	print 'Job done'
#	try:    
#		os.remove(filename)
#	except: pass
#	return

#def playF4mLinkOld2(url,name,proxy=None,use_proxy_for_chunks=False):
#	print "URL: " + url
#	progress = xbmcgui.DialogProgress()
#	listitem = xbmcgui.ListItem("myfile")
#	f4m_proxy=f4mProxy()
#	stopPlaying.clear()
#	runningthread=thread.start_new_thread(f4m_proxy.start,(stopPlaying,))
#	progress.create('Starting local proxy')
#	stream_delay = 1
#	progress.update( 50, "", 'Loading local proxy', "" )
#	xbmc.sleep(stream_delay*1000)
#	url_to_play=f4m_proxy.prepare_url(url,proxy,use_proxy_for_chunks)
#	mplayer = MyPlayer()    
#	progress.close() 
#	mplayer.play(url_to_play,listitem)
#	while True:
#		if stopPlaying.isSet():
#			break;
#		xbmc.log('Sleeping...')
#		xbmc.sleep(200)
#
#	print 'Job done'
#	return
    
def playF4mLink(url,name,proxy=None,use_proxy_for_chunks=False):
    from F4mProxy import f4mProxyHelper
    player=f4mProxyHelper()
    player.playF4mLink(url, name, proxy, use_proxy_for_chunks)
    return    

def playF4mLink2(url,name,proxy=None,use_proxy_for_chunks=False):
    from F4mProxy import f4mProxyHelper
    helper=f4mProxyHelper()
    url_to_play,stopEvent = helper.start_proxy(url, name, proxy, use_proxy_for_chunks)
    mplayer = MyPlayer()    
    mplayer.stopPlaying = stopEvent
    listitem = xbmcgui.ListItem(name)
    mplayer.play(url_to_play,listitem)
    while True:
        if stopEvent.isSet():
            break;
        xbmc.log('Sleeping...')
        xbmc.sleep(200)
    return   
    
class MyPlayer (xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def play(self, url, listitem):
        print 'Now im playing... %s' % url
        self.stopPlaying.clear()
        xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(url, listitem)
    def onPlayBackEnded( self ):
        # Will be called when xbmc stops playing a file
        print "seting event in onPlayBackEnded " 
        self.stopPlaying.set();
        print "stop Event is SET" 
    def onPlayBackStopped( self ):
        # Will be called when user stops xbmc playing a file
        print "seting event in onPlayBackStopped " 
        self.stopPlaying.set();
        print "stop Event is SET" 

VIEW_MODES = {
    'thumbnail': {
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
    },
}

def get_view_mode_id( view_mode):
    view_mode_ids = VIEW_MODES.get(view_mode.lower())
    if view_mode_ids:
        return view_mode_ids.get(xbmc.getSkinDir())
    return None

params=get_params()
url=None
name=None
mode=None
linkType=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=urllib.unquote_plus(params["mode"])
except:
    pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
    linkType=args.get('linkType', '')[0]
except:
    pass


PageNumber=''
try:
    PageNumber=args.get('limitstart', '')[0]
except:
    PageNumber=''

if PageNumber==None: PageNumber=""


print     mode,url,name

		
try:

    if mode==None or url==None or len(url)<1:
        print "InAddTypes"
        Addtypes()

    elif mode=='VOD':
        print "AddVOD url is ",name,url
        AddVOD(url,mode) #adds series as well as main VOD section, both are cat.

    elif 'VOD-' in mode:
        print " AddEnteries Play url is "+url
        AddEnteries(url,PageNumber, mode)
    elif mode=='ALLC':
        print " AddEnteries Play url is "+url
        AddLiveEnteries(url,PageNumber, mode)
        
    elif mode=='PlayVOD':
        print " PlayShowLink Play url is "+url
        
        PlayShowLink(url,name)
    elif mode=='PlayLive':
        print "Play url is "+url,mode
        PlayLiveLink(url,name)
    elif mode=='Settings':
        print "Play url is "+url,mode
        ShowSettings(url)
except:
    print 'something wrong', sys.exc_info()[0]
    traceback.print_exc()

if (not mode==None) and mode>1:
    view_mode_id = get_view_mode_id('thumbnail')
    if view_mode_id is not None:
        #print 'view_mode_id',view_mode_id
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        #print 'Container.SetViewMode(%d)' % view_mode_id
        xbmc.executebuiltin('Container.SetViewMode(%d)' % view_mode_id)
   
if not mode==None and 'VOD-' in mode:
    print 'update listing'
    xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
elif not (mode=='PlayVOD' or  mode=='PlayLive' or mode=='Settings'): 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


