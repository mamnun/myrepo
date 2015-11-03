import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver  
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
import CustomPlayer
try:
    from lxmlERRRORRRR import etree
    print("running with lxml.etree")
except ImportError:
    try:
        import xml.etree.ElementTree as etree
        print("running with ElementTree on Python 2.5+")
    except ImportError:
        try:
        # normal cElementTree install
            import cElementTree as etree
            print("running with cElementTree")
        except ImportError:
            try:
            # normal ElementTree install
                import elementtree.ElementTree as etree
                print("running with ElementTree")
            except ImportError:
                print("Failed to import ElementTree from any known place")
          
try:
    import json
except:
    import simplejson as json
    
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.ZemTV-shani'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))
  
willowCommonUrl=''# this is where the common url will stay
#willowCommonUrl=''

WTVCOOKIEFILE='WTVCookieFile.lwp'
WTVCOOKIEFILE=os.path.join(profile_path, WTVCOOKIEFILE)
ZEMCOOKIEFILE='ZemCookieFile.lwp'
ZEMCOOKIEFILE=os.path.join(profile_path, ZEMCOOKIEFILE)

 
mainurl=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20v')
liveURL=base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vbGl2ZS1wYWtpc3RhbmktbmV3cy1jaGFubmVscy8=')

tabURL =base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb206ODg4OC91c2Vycy9yZXgvbV9saXZlLnBocD9hcHA9JXMmc3RyZWFtPSVz')

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

def ShowSettings(Fromurl):
	selfAddon.openSettings()
	
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage,showContext=False,showLiveContext=False,isItFolder=True, linkType=None):
#	print name
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DM")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
		cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
		cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		cmd5 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "EBOUND")
		cmd6 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		
		liz.addContextMenuItems([('Show All Sources',cmd6),('Play Ebound video',cmd5),('Play Playwire video',cmd4),('Play Youtube video',cmd3),('Play DailyMotion video',cmd1),('Play Tune.pk video',cmd2)])
	if linkType:
		u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
		
#	if showLiself.wfileveContext==True:
#		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "RTMP")
#		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "HTTP")
#		liz.addContextMenuItems([('Play RTMP Steam (flash)',cmd1),('Play Http Stream (ios)',cmd2)])
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok
	
def PlayChannel ( channelName ): 
#	print linkType
	url = tabURL.replace('%s',channelName);
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
	
	match=re.compile('\"(http.*?playlist.m3u.*?)\"').findall(link)
#	print match

	strval = match[0]
#	print strval
	req = urllib2.Request(strval)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	req.add_header('Referer', base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb206ODg4OC91c2Vycy9yZXgvbV9saXZlLnBocA=='))
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
	match=re.compile('\"(http.*?hashAESkey=.*?)\"').findall(link)
#	print match
	strval = match[0]

	listitem = xbmcgui.ListItem(channelName)
	listitem.setInfo('video', {'Title': channelName, 'Genre': 'Live TV'})
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()
	playlist.add (strval)

	xbmc.Player().play(playlist)
	return

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):

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


def DisplayChannelNames(url):
	req = urllib2.Request(mainurl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	 match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)


	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	print match
#	print 'val is'
	match=sorted(match,key=itemgetter(1)   )
	for cname in match:
		if cname[0]<>'':
			addDir(cname[1] ,cname[0] ,1,'',isItFolder=False)
	return


def Addtypes():
	addDir('Latest Shows' ,'Shows' ,2,'')
	addDir('All Programs and Talk Shows' ,'ProgTalkShows' ,2,'')
	addDir('Pakistani Live Channels' ,'PakLive' ,2,'')
	addDir('Indian Live Channels' ,'IndianLive' ,2,'')
	addDir('Punjabi Live Channels' ,'PunjabiLive' ,2,'')
	addDir('Sports' ,'Live' ,13,'')
	addDir('Settings' ,'Live' ,6,'',isItFolder=False)
	return

def PlayFlashTv(url):
#    patt='(.*?)'
#    print link
#    match_url =re.findall(patt,link)[0]
    referer=[('Referer',base64.b64decode('aHR0cDovL3Nwb3J0czR1LnR2L2VtYmVkL1NreS1zcG9ydHMtMS5waHA='))]
    res=getUrl(url,headers=referer)
    stream_pat='streamer\',[\'"](.*?)[\'"]'
    playpath_pat='\'file\',\'(.*?)\''
    
    swf_url=base64.b64decode("aHR0cDovL2ZsYXNodHYuY28vZVBsYXllcnIuc3dm")
    pageUrl=base64.b64decode("aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kxJnZ3PTY1MCZ2aD00ODA=")
    rtmp_url=re.findall(stream_pat,res)[0]
    play_path=re.findall(playpath_pat,res)[0]

    
    video_url= '%s playpath=%s pageUrl=%s swfUrl=%s token=%s timeout=20'%(rtmp_url,play_path,pageUrl,swf_url,'%ZZri(nKa@#Z')
    
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(video_url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist) 
    
def PlayCricFree(url):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    res=getUrl(url)
    patt='<iframe frameborder="0" marginheight="0".*?src="(.*?)" id="iframe"'
    url2=re.findall(patt,res)[0]
    referer=[('Referer',url)]
    res=getUrl(url2,headers=referer)
    urlToPlay=None
    supported=False
    if 'theactionlive.com/' in res:
        supported=True
        progress.update( 30, "", "Finding links..stage2", "" )
        patt="id='(.*?)'.*?width='(.*)'.*?height='(.*?)'"
        gid,wd,ht=re.findall(patt,res)[0]
        referer=[('Referer',url2)]
        url3='http://theactionlive.com/livegamecr.php?id=%s&width=%s&height=%s&stretching='%(gid,wd,ht)
        res=getUrl(url3,headers=referer)    
        if 'biggestplayer.me' in res:
            progress.update( 50, "", "Finding links..stage3", "" )
            patt="id='(.*?)'.*?width='(.*)'.*?height='(.*?)'"
            gid,wd,ht=re.findall(patt,res)[0]
            referer=[('Referer',url3)]
            url4='http://biggestplayer.me/streamcr.php?id=%s&width=%s&height=%s'%(gid,wd,ht)
            progress.update( 80, "", "Finding links..last stage", "" )
            res=getUrl(url4,headers=referer)    
            patt='file: "(.*?)"'
            urlToPlay=re.findall(patt,res)[0];
            referer=[('Referer',url4)]
            urlToPlay+='|Referer='+url4
    if 'www.reytv.co' in res:
        supported=True
        progress.update( 30, "", "Finding links..stage2", "" )
        patt="fid='(.*?)'.*?v_width=(.*?);.*?v_height=(.*?);"
        gid,wd,ht=re.findall(patt,res)[0]
        referer=[('Referer',url2)]
        url3='http://reytv.co/embedo.php?live=%s&width=%s&height=%s'%(gid,wd,ht)
        progress.update( 50, "", "Finding links..stage3", "" )
        res=getUrl(url3,headers=referer)
        
        patt='file: "(.*?)"'
        rtmp=re.findall(patt,res)[0]
        patt='securetoken: "(.*?)"'
        token=re.findall(patt,res)[0]           
        urlToPlay=rtmp + ' token=' + token + ' pageUrl='+url3+ ' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf'+' timeout=20'
    
    if urlToPlay and len(urlToPlay)>0:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        playlist.add(urlToPlay,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist) 
    else:
        dialog = xbmcgui.Dialog()
        if not supported:
            ok = dialog.ok('Not Supported','This channel is not supported yet')
        
def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key[1]) ] 
    return sorted(l, key = alphanum_key)  
def AddP3gSports(url):
    pat="pe='text\/javascript'>ch='(.*?)'"
    res=getUrl("http://c247.tv/")
    channels=re.findall(pat,res)
    channels=sorted(channels,key=lambda s: s[0].lower()   )

    
    for i in channels:
        addDir('%s P3G.Tv (requires new rtmp)'%(i.replace('_','')) ,'http://c247.tv/live.php?ch=%s'%i,17,'', False, True,isItFolder=False)


        
def AddCricFree(url):
    pat='<li.*?><a href="(.*?)".*?channels-icon (.*?)"'
    res=getUrl("http://cricfree.sx/")
    channels=re.findall(pat,res)
    
    pat='<li><a href="(.*?)".*?\<span class="chclass3"\>(.*?)<'
    channels+=re.findall(pat,res)    
#    channels=sorted(channels,key=lambda s: s[1].lower()   )
    channels=sorted_nicely(channels)
    for u,n in channels:
        addDir(n.capitalize(),u,42,'', False, True,isItFolder=False)
    

##http://c247.tv/
#http://c247.tv/live.php?ch=Geo_Super
#http://c247.tv/
#    addDir('Ptv Sports P3G.Tv (requires new rtmp)' ,base64.b64decode('http://c247.tv/live.php?ch=Geo_Super') ,17,'', False, True,isItFolder=False)
#    addDir('Star Sports 1 P3G.Tv (requires new rtmp)' ,base64.b64decode('http://www.p3g.tv/embedplayer/star1dontban/2/600/420' ),17,'', False, True,isItFolder=False)
#    addDir('Star Sports 2 P3G.Tv (requires new rtmp)' ,base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvZW1iZWRwbGF5ZXIvc3RhcjJkb250YmFuLzIvNjAwLzQyMA==') ,17,'', False, True,isItFolder=False)
#    addDir('Star Sports 3 P3G.Tv (requires new rtmp)' ,base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvZW1iZWRwbGF5ZXIvc3RhcjNkb250YmFuLzIvNjAwLzQyMA==') ,17,'', False, True,isItFolder=False)
#    addDir('Star Sports 4 P3G.Tv (requires new rtmp)' ,base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvZW1iZWRwbGF5ZXIvZXNwbnN0YXI0MS8yLzYwMC80MDA=') ,17,'', False, True,isItFolder=False)
#    
#    addDir('GeoSuper P3G.Tv (requires new rtmp)' ,base64.b64decode('http://c247.tv/live.php?ch=Geo_Super') ,17,'', False, True,isItFolder=False)
#    addDir('Ten Cricket P3G.Tv (requires new rtmp)' ,base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvZW1iZWRwbGF5ZXIvdGVuY3JpY2tldHpoLzIvNjQwLzQ0MA==') ,17,'', False, True,isItFolder=False)
#    addDir('Ten sports P3G.Tv (requires new rtmp)' ,base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvZW1iZWRwbGF5ZXIvdGVucGt5YS8yLzY0MC80NDA=' ),17,'', False, True,isItFolder=False)
#    addDir('Ten action P3G.Tv (requires new rtmp)' ,base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvZW1iZWRwbGF5ZXIvcHQzbmFjdGlvbi8yLzY0MC80NDA=' ),17,'', False, True,isItFolder=False)

    
def AddFlashtv(url):
    addDir('Sky Sports 1' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kxJnZ3PTY1MCZ2aD00ODA='),32,'', False, True,isItFolder=False)
    addDir('Sky Sports 2' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kyJnZ3PTY1MCZ2aD00ODA=') ,32,'', False, True,isItFolder=False)
    addDir('Sky Sports 3' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3kzJnZ3PTY1MCZ2aD00ODA='),32,'', False, True,isItFolder=False)
    addDir('Sky Sports 4' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3k0JnZ3PTY1MCZ2aD00ODA=') ,32,'', False, True,isItFolder=False)
    addDir('Sky Sports 5' ,base64.b64decode('aHR0cDovL2ZsYXNodHYuY28vZW1iZWRvLnBocD9saXZlPXNra3k1JnZ3PTY1MCZ2aD00ODA='),32,'', False, True,isItFolder=False)

    
    
def AddSports(url):
    match=[]
    if 1==2:
        match.append((base64.b64decode('U2t5IFNwb3J0IDE=')+ ' [Not working]','manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNg=='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' [Not working]','manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMyNg=='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDM=')+' [Not working]','manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czMuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDQ=')+' [Not working]','manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNQ=='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' [Not working]','manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czUuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))

    if 1==1:    
        match.append((base64.b64decode('U2t5IFNwb3J0IDE=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czEuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czIuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDM=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czMuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDQ=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czQuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5hM2c2dDhtOS5od2Nkbi5uZXQvY2FsaXZlb3JpZ2luL3NreXNwb3J0czUuc3RyZWFtL3BsYXlsaXN0Lm0zdTg='),''))
        match.append((base64.b64decode('R2VvIFN1cGVy')+' alt HD','gen',base64.b64decode('aHR0cDovL2Nkcy5pOHc3cjVqMi5od2Nkbi5uZXQvamRvcmlnaW4vamRHZW9zdXBlcjQ3Ni5zdHJlYW0vcGxheWxpc3QubTN1OA=='),''))

        

        
    if 1==2:
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' alt HD','gen',base64.b64decode('cnRtcDovLzE2Ny4xMTQuMTE3LjIwOC9saXZlL3NreTV2'),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IGYx')+' alt HD','gen',base64.b64decode('cnRtcDovLzE2Ny4xMTQuMTE3LjIwOC9saXZlL3NreWYxdg=='),''))

    
    #v2
    if 1==2:
        match.append((base64.b64decode('U2t5IFNwb3J0IDE=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czEgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czIgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDI=')+' alt 2','manual',base64.b64decode('cnRtcDovLzE3OC4xOC4zMS41Mzo0NDMvbGl2ZXJlcGVhdGVyLzE5MDYxNCBzd2ZVcmw9aHR0cDovL2Jlcm5hcmRvdHYuY2x1Yi9mdWNraW5nY29weS5zd2YgcGFnZVVybD1odHRwOi8vYmlnZ2VzdHBsYXllci5tZS9zdHJlYW0ucGhwP2lkPTE5MDYxNCB0b2tlbj0jYXRkJSMkWkggbGl2ZT0xIHRpbWVvdXQ9MjA='),''))
        
        match.append((base64.b64decode('U2t5IFNwb3J0IDM=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czMgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))

        match.append((base64.b64decode('U2t5IFNwb3J0IDQ=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czQgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IDU=')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5czUgc3dmVXJsPWh0dHA6Ly9oZGNhc3Qub3JnL2VwbGF5ZXIuc3dmIGxpdmU9MSBwYWdlVXJsPWh0dHA6Ly93d3cuaGRjYXN0Lm9yZy9lbWJlZGxpdmU0LnBocD91PXNza3lzMSZ2dz02NTAmdmg9NDcwJmRvbWFpbj1jcmljYm94LnR2IHRva2VuPUZvNV9uMHc/VS5yQTZsMy03MHc0N2NoDQo='),''))
        match.append((base64.b64decode('U2t5IFNwb3J0IGYx')+' alt','manual',base64.b64decode('cnRtcGU6Ly80Ni4yNDYuMjkuMTYwOjE5MzUvbCBwbGF5cGF0aD1zc2t5c2YxIHN3ZlVybD1odHRwOi8vaGRjYXN0Lm9yZy9lcGxheWVyLnN3ZiBsaXZlPTEgcGFnZVVybD1odHRwOi8vd3d3LmhkY2FzdC5vcmcvZW1iZWRsaXZlNC5waHA/dT1zc2t5czEmdnc9NjUwJnZoPTQ3MCZkb21haW49Y3JpY2JveC50diB0b2tlbj1GbzVfbjB3P1UuckE2bDMtNzB3NDdjaA0K'),''))



    for m in match:
        cname=m[0]
        ty=m[1]
        curl=m[2]
        imgurl=''
        m=11 if ty=='manual' else 33
        addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,m,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    
    addDir('SmartCric.com (Live matches only)' ,'Live' ,14,'')
    addDir('CricHD.tv (Live Channels)' ,'pope' ,26,'')
#    addDir('Flashtv.co (Live Channels)' ,'flashtv' ,31,'')
    addDir('WatchCric.com (requires new rtmp)-Live matches only' ,base64.b64decode('aHR0cDovL3d3dy53YXRjaGNyaWMubmV0Lw==' ),16,'') #blocking as the rtmp requires to be updated to send gaolVanusPobeleVoKosat
    addDir('c247.tv-P3G.Tv (requires new rtmp)' ,'P3G'  ,30,'')
    addDir('Willow.Tv (login required)' ,base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYv') ,19,'')
    addDir(base64.b64decode('U3VwZXIgU3BvcnRz') ,'sss',34,'')
    addDir('PV2 Sports' ,'sss',36,'')
    addDir('Streams' ,'sss',39,'')
    addDir('cricfree.sx' ,'sss',41,'')

    
def PlayCricHD(url):

    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    videoPage =  response.read()
    response.close()
    pat='<iframe frameborder="0".*?src="(.*?)" name="iframe_a"'
    matc=re.findall(pat,videoPage)
    newurl=matc[0]
    if len(matc)>1:
        newurl=matc[1]
    
    
    req = urllib2.Request(newurl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    videoPage =  response.read()
    response.close()
    if 'scripts/p3g.js' in videoPage:
        PlayWatchCric(newurl)
        return 
    
    pat='fid="(.*?)".*width=([0-9]*).*?height=([0-9]*)'
    fid,wid,ht=re.findall(pat,videoPage)[0]

    req = urllib2.Request('http://www.yocast.tv/embed.js')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    jspage =  response.read()
    response.close()
    pat='(http.*?)\?'
    jsfinal=re.findall(pat,jspage)[0]
    
    
    newurl2="%s?live=%s&vw=%s&vh=%s"%(jsfinal,fid,wid,ht)
    
    req = urllib2.Request(newurl2)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    req.add_header('Referer', newurl)
    
    response = urllib2.urlopen(req)
    videoPage =  response.read()
    response.close()
    fpat='file:.?.?"(.*?)"'
    spat='streamer:.?.?"(.*?)"'
    
    fi=re.findall(fpat,videoPage)[0]
    streamer=re.findall(spat,videoPage)[0]
    

    

    playlist = xbmc.PlayList(1)
    #url='rtmp://rtmp.popeoftheplayers.pw:1935/redirect playpath='+url+base64.b64decode('IHN3ZlZmeT10cnVlIHN3ZlVybD1odHRwOi8vcG9wZW9mdGhlcGxheWVycy5wdy9hdGRlZGVhZC5zd2YgZmxhc2hWZXI9V0lOXDIwMTYsMCwwLDIzNSBwYWdlVXJsPWh0dHA6Ly9wb3Blb2Z0aGVwbGF5ZXJzLnB3L2F0ZGVkZWFkLnN3ZiBsaXZlPXRydWUgdGltZW91dD0yMCB0b2tlbj0jYXRkJSMkWkg=')
    url='%s playpath=%s pageUrl=%s'%(streamer,fi.split('.flv')[0],newurl2)+' live=true timeout=20'

    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist) 

##not in use        
def PlayPopeLive(url):
    playlist = xbmc.PlayList(1)
    #url='rtmp://rtmp.popeoftheplayers.pw:1935/redirect playpath='+url+base64.b64decode('IHN3ZlZmeT10cnVlIHN3ZlVybD1odHRwOi8vcG9wZW9mdGhlcGxheWVycy5wdy9hdGRlZGVhZC5zd2YgZmxhc2hWZXI9V0lOXDIwMTYsMCwwLDIzNSBwYWdlVXJsPWh0dHA6Ly9wb3Blb2Z0aGVwbGF5ZXJzLnB3L2F0ZGVkZWFkLnN3ZiBsaXZlPXRydWUgdGltZW91dD0yMCB0b2tlbj0jYXRkJSMkWkg=')
    url='rtmp://rtmp.popeoftheplayers.eu:1935/redirect playpath='+url+base64.b64decode(' swfVfy=true swfUrl=http://popeoftheplayers.eu/atdedead.swf flashVer=WIN\2016,0,0,235 pageUrl=http://popeoftheplayers.eu/atdedead.swf live=true timeout=20 token=#atd%#$ZH')

    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist) 

    
def GetSSSEvents(url):
    try:
        url=base64.b64decode('aHR0cDovL3d3dy5zdXBlcnNwb3J0LmNvbS9saXZlLXZpZGVv')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        req.add_header('Cookie', 'User_IsMobile=False; supersportcookie=country=ZA&countryName=South Africa;')
        response = urllib2.urlopen(req)
        videoPage =  response.read()
        response.close()
        pat='setallLiveStreamsVideos\\(...({.*?})\\\\\"\\"\\);'
#        print videoPage
        channels_string=re.findall(pat,videoPage)[0]
        channels_string=channels_string.replace('\\\\r','')
        channels_string=channels_string=channels_string.replace('\\\\n','')
        channels_string=channels_string.replace('\\\\','\\')
        channels_string=channels_string.replace('\\"','"')
        channels_string=channels_string.replace('\\"','"')
#        print channels_string
        
#        print 'channels_string',channels_string
        channels = json.loads(channels_string)
#        print channels

        
#            sid=series["Id"]
        addDir('Maxbitrate Settings' ,'Live' ,6,'',isItFolder=False)
        
        addDir(Colored('Live Events','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon   
        try:
            for channel in channels["EventLiveStreamNow"]:
                if channel["IsLiveNow"]:
                    ptitle=channel["Title"]
                    cname=channel["Channel"]
                    link=channel["Link"]

        #            addDir(cname ,'a',27,'', False, True,isItFolder=False)
                    addDir('  '+cname + ' ' + ptitle ,link,35,'', False, False,isItFolder=False)
        except: traceback.print_exc(file=sys.stdout)

        addDir(Colored('Channels','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon   
        try:
            for channel in channels["ChannelStream"]:

                ptitle=channel["NowPlaying"]["EventNowPlaying"]
                cname=channel["NowPlaying"]["Channel"]
                link=channel["NowPlaying"]["Link"]
#                print ptitle, cname,link
                if not link is None:
                    if ptitle is None: ptitle=''
        #            addDir(cname ,'a',27,'', False, True,isItFolder=False)
                    addDir(u'  '+cname + u' ' + ptitle ,link,35,'', False, False,isItFolder=False)
                                                                        

        except: traceback.print_exc(file=sys.stdout)
        
    except: traceback.print_exc(file=sys.stdout)
def AddPv2Sports(url=None):
    xmldata=getPV2Url()
    sources=etree.fromstring(xmldata)
    ret=[]
    for source in sources.findall('items'):
        if source.findtext('programCategory').lower()=='sports':
            cname=source.findtext('programTitle')
            cid=source.findtext('programURL')
            cimage=source.findtext('programImage')
            addDir(cname ,base64.b64encode(cid),37,cimage, False, True,isItFolder=False)
         
            
            
def AddStreamSports(url=None):
    jsondata=getUrl('http://videostream.dn.ua/list/GetLeftMenuShort?lng=en')
    sources= json.loads(jsondata)
    ret=[]
    addDir('Refresh' ,'Live' ,39,'')
    for source in sources["Value"]:
        cname=Colored(source["Sport"] ,'EB')
        if not "cyber" in cname:
            if "Opp1" in source and not source["Opp1"].encode('ascii','ignore')=="":
                cname+=" :" + source["Opp1"].encode('ascii','ignore') + " vs " +source["Opp2"].encode('ascii','ignore') 
            else:
                cname+=" :" + source["Liga"].encode('ascii','ignore')
            cid=source["VI"]
            addDir(cname ,base64.b64encode(cid),40,'', False, True,isItFolder=False)            

            
def AddCricHD(url):
    try:
        url="http://www.crichd.tv/"
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        videoPage =  response.read()
        response.close()
        pat='<a class="menuitem" href="(.*?)".*?img src="(.*?)".*?alt="(.*?)"'
        channels=re.findall(pat,videoPage)
#        print channels
#        channels=[('Sky Sports 1','1'),('Sky Sports 2','2'),('Sky Sports 3','3'),('Sky Sports 4','4'),('Sky Sports 5','5'),('Sky Sports F1','6') ,('BT Sport 1','7'),('BT Sports 2','8') ,('Willow Cricket','24') ,('Ptv Sports','15')   ]
        for channel in channels:
#            print channel
            cname=channel[2]
            cid=channel[0]
            cimg=channel[1]
            
            if not cid.startswith('http'):cid=url+cid
            if not cimg.startswith('http'):cimg=url+cimg

#            addDir(cname ,'a',27,'', False, True,isItFolder=False)
#            print 'adding'
            addDir(cname ,cid,27,cimg, False, True,isItFolder=False)

        pat='<b><a class="menuitem" href="(.*?)"><font size="4">(.*?)<'
        channels=re.findall(pat,videoPage)
#        print channels
#        channels=[('Sky Sports 1','1'),('Sky Sports 2','2'),('Sky Sports 3','3'),('Sky Sports 4','4'),('Sky Sports 5','5'),('Sky Sports F1','6') ,('BT Sport 1','7'),('BT Sports 2','8') ,('Willow Cricket','24') ,('Ptv Sports','15')   ]
        for channel in channels:
#            print channel
            cname=channel[1]
            cid=channel[0]
            cimg=""#;channel[2]
            
            if not cid.startswith('http'):cid=url+cid
            if not cimg.startswith('http'):cimg=url+cimg

#            addDir(cname ,'a',27,'', False, True,isItFolder=False)
#            print 'adding'
            addDir(cname ,cid,27,cimg, False, True,isItFolder=False)
            


    except: traceback.print_exc(file=sys.stdout)
    

#not in use
def AddPopeLive(url):
    try:
#        req = urllib2.Request(url)
#        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
#        response = urllib2.urlopen(req)
#        videoPage =  response.read()
#        response.close()
#        pat='<a href="http://.*?/.*?/(.*?)-Live.*?/(.+?)" '
#        channels=re.findall(pat,videoPage)
#        print channels
        channels=[('Sky Sports 1','1'),('Sky Sports 2','2'),('Sky Sports 3','3'),('Sky Sports 4','4'),('Sky Sports 5','5'),('Sky Sports F1','6') ,('BT Sport 1','7'),('BT Sports 2','8') ,('Willow Cricket','24') ,('Ptv Sports','15')   ]
        for channel in channels:
#            print channel
            cname=channel[0]
            cid=channel[1]

#            addDir(cname ,'a',27,'', False, True,isItFolder=False)
#            print 'adding'
            addDir(cname ,cid,27,'', False, True,isItFolder=False)
    except: traceback.print_exc(file=sys.stdout)
    
def AddWillSportsOldSeries(url):
    try:
        url_host=base64.b64decode('aHR0cDovL3dpbGxvd2ZlZWRzLndpbGxvdy50di93aWxsb3dNYXRjaEFyY2hpdmUuanNvbg==')
        req = urllib2.Request(url_host)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            res = f.read()
        else:
            res=response.read()

#        print repr(res[:100])
        res=res.split('Handle_WLSeriesDetailsObj(')[1][:-2]
        serieses = json.loads(res)
  
        response.close()

        
        for series in serieses:
            sname=series["Name"]
            sid=series["Id"]
            addDir(sname ,sid,24,'')		#name,url,mode,icon
    except: traceback.print_exc(file=sys.stdout)


def AddWillSportsOldSeriesMatches(url):
    addDir(Colored(name,'EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
    try:
        url_host=base64.b64decode('aHR0cDovL3dpbGxvd2ZlZWRzLndpbGxvdy50di93aWxsb3dNYXRjaEFyY2hpdmUuanNvbg==')
        req = urllib2.Request(url_host)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            res = f.read()
        else:
            res=response.read()

#        print repr(res[:100])
        res=res.split('Handle_WLSeriesDetailsObj(')[1][:-2]
        serieses = json.loads(res)
  
        response.close()

        
        for series in serieses:
            sname=series["Name"]
            sid=series["Id"]
            if url==sid:
                for match in series["MatchDetails"]:
                    mname=match["Name"]
                    matchid=match["Id"]
                    sdate=match["StartDate"]
                    addDir(sdate+' - '+mname ,matchid,23,'')		#name,url,mode,icon
    except: traceback.print_exc(file=sys.stdout)

def useMyOwnUserNamePwd():
    willow_username=selfAddon.getSetting( "WillowUserName" ) 
    return not willow_username==""

def getZemCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(ZEMCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar
    
def getWTVCookieJar(updatedUName=False):
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(WTVCOOKIEFILE,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar

def performWillowLogin():
    try:

        url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210L0RlZmF1bHQuYXNw')
        willow_username=selfAddon.getSetting( "WillowUserName" ) 
        willow_pwd=selfAddon.getSetting( "WillowPassword" ) 
        willow_lasstusername=selfAddon.getSetting( "lastSuccessLogin" ) 
        cookieJar=getWTVCookieJar(willow_username!=willow_lasstusername)
        mainpage = getUrl(url,cookieJar=cookieJar)


        if 'Login/Register' in mainpage:
            url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9Vc2VyTWdtdC9Mb2dpbi5hc3A=')
            post = {'Email':willow_username,'Password':willow_pwd,'LoginFormSubmit':'true'}
            post = urllib.urlencode(post)
            mainpage = getUrl(url,cookieJar=cookieJar,post=post)
            cookieJar.save (WTVCOOKIEFILE,ignore_discard=True)
            selfAddon.setSetting( id="lastSuccessLogin" ,value=willow_username)
        
        return not 'Login/Register' in mainpage,cookieJar
    except: 
            traceback.print_exc(file=sys.stdout)
    return False,None

def kodiJsonRequest(params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)

    try:
        response = json.loads(request)
    except UnicodeDecodeError:
        response = json.loads(request.decode('utf-8', 'ignore'))

    try:
        if 'result' in response:
            return response['result']
        return None
    except KeyError:
        logger.warn("[%s] %s" % (params['method'], response['error']['message']))
        return None


def setKodiProxy(proxysettings=None):

    if proxysettings==None:
        print 'proxy set to nothing'
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":false}, "id":1}')
    else:
        
        ps=proxysettings.split(':')
        proxyURL=ps[0]
        proxyPort=ps[1]
        proxyType=ps[2]
        proxyUsername=None
        proxyPassword=None
         
        if len(ps)>3 and '@' in proxysettings:
            proxyUsername=ps[3]
            proxyPassword=proxysettings.split('@')[-1]

        print 'proxy set to', proxyType, proxyURL,proxyPort
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":true}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxytype", "value":' + str(proxyType) +'}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyserver", "value":"' + str(proxyURL) +'"}, "id":1}')
        xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyport", "value":' + str(proxyPort) +'}, "id":1}')
        
        
        if not proxyUsername==None:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyusername", "value":"' + str(proxyUsername) +'"}, "id":1}')
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxypassword", "value":"' + str(proxyPassword) +'"}, "id":1}')

        
def getConfiguredProxy():
    proxyActive = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.usehttpproxy"}, 'id': 1})['value']
    print 'proxyActive',proxyActive
    proxyType = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxytype"}, 'id': 1})['value']

    if proxyActive: # PROXY_HTTP
        proxyURL = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyserver"}, 'id': 1})['value']
        proxyPort = unicode(kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyport"}, 'id': 1})['value'])
        proxyUsername = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxyusername"}, 'id': 1})['value']
        proxyPassword = kodiJsonRequest({'jsonrpc': '2.0', "method":"Settings.GetSettingValue", "params":{"setting":"network.httpproxypassword"}, 'id': 1})['value']

        if proxyUsername and proxyPassword and proxyURL and proxyPort:
            return proxyURL + ':' + str(proxyPort)+':'+str(proxyType) + ':' + proxyUsername + '@' + proxyPassword
        elif proxyURL and proxyPort:
            return proxyURL + ':' + str(proxyPort)+':'+str(proxyType)
    else:
        return None
        
def playmediawithproxy(media_url, name, iconImage,proxyip,port,progress):

    progress.create('Progress', 'Playing with custom proxy')
    progress.update( 50, "", "setting proxy..", "" )
    proxyset=False
    existing_proxy=''
    try:
        
        existing_proxy=getConfiguredProxy()
        print 'existing_proxy',existing_proxy
        #read and set here
        setKodiProxy( proxyip + ':' + port+':0')
        proxyset=True

        print 'proxy setting complete', getConfiguredProxy()
        
        progress.update( 80, "", "setting proxy complete, now playing", "" )
        progress.close()
        progress=None
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = iconImage, thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    if progress:
        progress.close()
    if proxyset:
        print 'now resetting the proxy back'
        setKodiProxy(existing_proxy)
        print 'reset here'
    return ''
    
def getwillow247(matchid,CJ):

    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Willow 24x7')
    progress.update( 10, "", "Getting Urls..")
    
    liveUrl=base64.b64decode('aHR0cDovL20ud2lsbG93LnR2L2dldFN0cmVhbWluZ1VSTFMuYXNwP21pZD05OTk5OTk=')
    pat='"URL":"(.*?)"'
    headers=[('Referer',base64.b64decode('aHR0cDovL20ud2lsbG93LnR2L2lPU0hvbWUuYXNw')),('User-Agent','Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a')]
    htm=getUrl(liveUrl,cookieJar=CJ,headers=headers) 
    if 'Failure-Region' in htm:
        progress.update( 30, "", "Not in US? Using proxy" )

        proxyserver=selfAddon.getSetting('WillowProxy')
        proxyport=selfAddon.getSetting('WillowPort')
        ##use US proxy and play with it
        cookie_handler = urllib2.HTTPCookieProcessor(CJ)
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler(),urllib2.ProxyHandler({ 'http'  : '%s:%s'%(proxyserver,proxyport)}))
        req = urllib2.Request(liveUrl)
        req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a')
        req.add_header('Referer',base64.b64decode('aHR0cDovL20ud2lsbG93LnR2L2lPU0hvbWUuYXNw'))
        response = opener.open(req,timeout=20)
        link=response.read()
        response.close()
#        print link
        progress.update( 30, "", "Got the Link, Now playing with Using proxy" )
        final_url=re.findall(pat,link)[0]
        playmediawithproxy(final_url,'24x7 willow','',proxyserver,proxyport,progress)
        return ''
    else:
        progress.close()
        final_url=re.findall(pat,htm)[0]
        return final_url
    
def getMatchUrl(matchid):
    if not useMyOwnUserNamePwd():
        url_host=willowCommonUrl
        if len(url_host)>0:
            if mode==21:#live
                if ':' in matchid:
                    matchid,partNumber=matchid.split(':')
                    post = {'matchNumber':matchid,'type':'live','partNumber':partNumber,'debug':'1'}
                else:
                    post = {'matchNumber':matchid,'type':'live','debug':'1'}
            else:
                if ':' in matchid:
                    matchid,partNumber=matchid.split(':')
                    post = {'matchNumber':matchid,'type':'replay','partNumber':partNumber,'debug':'1'}
                else:
                    post = {'matchNumber':matchid,'type':'replay','debug':'1'}
            post = urllib.urlencode(post)
            req = urllib2.Request(url_host)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
            response = urllib2.urlopen(req,post)
            link=response.read()
            response.close()
            final_url= urllib2.unquote(link)  
            final_url=final_url.split('debug')[0]
            return final_url
        else:
            Msg="Common server is not available, Please enter your own login details."
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('Login Failed', Msg)
            return ''

    else:
        loginworked,cookieJar= performWillowLogin();
        if loginworked:
            WLlive=False
            source_sectionid=''
            returnParts=False
            userid=''
            if matchid == '999999':
                return getwillow247(matchid,cookieJar)
            for i in cookieJar:

                s=repr(i)
                if 'CXMUserId' in s:
                    #print 'ssssssssssssss',s
                    userid=s.split('value=\'')[1].split('%')[0]
#            print 'userid',userid
            calltype='Live'
            if mode==21:
                WLlive=True
#                print 'matchid',matchid
                matchid,source_sectionid=matchid.split(':')
                st='LiveMatch'
                url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210LyVzVVJMLmFzcD9taWQ9JXM=')%(st,matchid)
                pat='secureurl":"(.*?)".*?priority":%s,'%source_sectionid    
                calltype='Live'                
            else:
                if ':' in matchid:
                    matchid,source_sectionid=matchid.split(':')
                    st='Replay'
                    url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9SZXBsYXlVUkwuYXNwP21pZD0lcyZ1c2VySWQ9JXM=')%(matchid,userid)
                    pat='secureurl":"(.*?)".*?priority":%s,'%source_sectionid    
                    calltype='RecordOne'     
                else:
                    returnParts=True
                    st='Replay'
                    url=base64.b64decode('aHR0cHM6Ly93d3cud2lsbG93LnR2L0V2ZW50TWdtdC9SZXBsYXlVUkwuYXNwP21pZD0lcyZ1c2VySWQ9JXM=')%(matchid,userid)
                    pat='"priority":(.+?),"title":"(.*?)",'
                    calltype='RecordAll' 
            
            videoPage = getUrl(url,cookieJar=cookieJar)    

            final_url=''
        
#            print 'calltype',calltype,mode
#            print videoPage
#            print pat
            if calltype=='Live' or calltype=='RecordOne':
                videoPage='},\n{'.join(videoPage.split("},{"))
                final_url=re.findall(pat,videoPage)[0]
            else:
                final_url=re.findall(pat,videoPage)
                final_url2=''
                for u in final_url:
                    final_url2+='#'+str(u[0]) +' ' +u[1].replace(',','')+'='+u[0]+','
                final_url=final_url2[:-1]
  
            final_url= urllib2.unquote(final_url)  
            final_url=final_url.split('debug')[0]
            return final_url
            

        else:
            Msg="Login failed, please make sure the login details are correct."
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('Login Failed', Msg)
        
def PlaySSSEvent(url):


    murl=base64.b64decode('aHR0cDovL3d3dy5zdXBlcnNwb3J0LmNvbS92aWRlby9wbGF5ZXJsaXZlanNvbi5hc3B4P3ZpZD0lcw==')
    matchid=url.split('/')[-1]
    match_url=murl%matchid
    match_json=getUrl(match_url)
    match=json.loads(match_json)
    matchurl=match['result']['services']['videoURL']
 
    finalUrl=getdecSSMatchUrl(matchurl,'LIVE')
    if 'manifest.f4m' in finalUrl:
        maxbitrate='0'
        maxbitrate_settings=selfAddon.getSetting('defualtSSSBitRate')
        if (not maxbitrate_settings=='') and 'Max' not in maxbitrate_settings:
            maxbitrate=maxbitrate_settings
        finalUrl='plugin://plugin.video.f4mTester/?url=%s&maxbitrate=%s&name=%s&swf=%s'%(urllib.quote_plus(finalUrl),maxbitrate,str(name),base64.b64decode("aHR0cDovL2NvcmUuZHN0di5jb20vdmlkZW8vZmxhc2gvUGxheWVyRFN0dlNTLnN3Zj92PTEuMTk="))
#    print 'finalUrl',finalUrl
#    playlist = xbmc.PlayList(1)
#    playlist.clear()
#    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    playlist.add(finalUrl,listitem)
#    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
#    xbmcPlayer.play(playlist) 
    xbmc.executebuiltin('XBMC.RunPlugin('+finalUrl+')') 
    

def getdecSSMatchUrl(strToDecrypt,type):
    DECRYPTION_KEY1 = "1233901199002223000111A2"
    DECRYPTION_KEY2 = "9685647821298987483258Z8"
    DECRYPTION_KEY_LIVE1 = "9685647821298987483258Z8"
    DECRYPTION_KEY_LIVE2 = "1233901199002223000111A2"
    DECRYPTION_KEY_VIDEO1 = "1233901199002223000111A2"
    DECRYPTION_KEY_VIDEO2 = "9685647821298987483258Z8"
    ds1 = ""
    if type == "LIVE": 
        import pyaes
        decryptor = pyaes.new(DECRYPTION_KEY_LIVE1, pyaes.MODE_ECB, IV='')
        ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
        if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
        else:
            decryptor = pyaes.new(DECRYPTION_KEY_LIVE2, pyaes.MODE_ECB, IV='')
            ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
            if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
    if type == "VIDEO": 
        decryptor = pyaes.new(DECRYPTION_KEY1, pyaes.MODE_ECB, IV='')
        ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
        if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
        else:
            decryptor = pyaes.new(DECRYPTION_KEY2, pyaes.MODE_ECB, IV='')
            ds1 = decryptor.decrypt(strToDecrypt.decode("hex")).replace('\x00', '')
            if ds1[:4] == "rtmp" or ds1[:4] == "http": return ds1
    return ds1
    
    
def PlayWillowMatch(url):
#    patt='(.*?)'
#    print link
#    match_url =re.findall(patt,link)[0]
    if not url.startswith('http'):
        match_url=getMatchUrl(url)
    else:
        match_url=url
    if match_url=='': return 
    keepplay=True
    if not 'www.youtube.com' in match_url:
        match_url=match_url+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
    else:
        check_url='https://www.youtube.com/get_video_info?html5=1&video_id=%s'% match_url.split('embed/')[1].split('?')[0]
        match_url= 'plugin://plugin.video.youtube/play/?video_id=%s' % match_url.split('embed/')[1].split('?')[0]
        try:
            patt=''
            txt=getUrl(check_url)
            if not 'hlsvp=' in txt:
                #play via proxy
                keepplay=False
                progress = xbmcgui.DialogProgress()
                progress.create('Progress', 'Willow youtube')
                progress.update( 10, "", "Youtube link ??")
                
                ##now play with proxy
                progress.update( 30, "", "Not in US? Using proxy" )
                proxyserver=selfAddon.getSetting('WillowProxy')
                proxyport=selfAddon.getSetting('WillowPort')
                print 'playing with proxy'
                cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
                opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler(),urllib2.ProxyHandler({ 'https'  : '%s:%s'%(proxyserver,proxyport)}))
                req = urllib2.Request(check_url)
                req.add_header('User-Agent','Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a')
                response = opener.open(req,timeout=20)
                link=response.read()
                response.close()
                print link
                progress.update( 30, "", "Got the Link, Now playing with Using proxy" )
                pat='hlsvp=(.*?)&'
                final_url=urllib.unquote(re.findall(pat,link)[0])
                print final_url
                match_url=final_url+'|User-Agent=VLC/2.2.1 LibVLC/2.2.1'
                keepplay=True
                #playmediawithproxy(final_url,str(name),'',proxyserver,proxyport,progress)
                print 'end playing with proxy'
                
        except: traceback.print_exc(file=sys.stdout)
    if keepplay:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        playlist.add(match_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist) 

def AddWillowReplayParts(url):
    try:
    
        replays=getWillowHighlights(url)
        
        addDir(Colored(name,'EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        
        addDir(Colored('Highlights and Events','blue',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        if replays and len(replays)>0:
            for section in replays:
                addDir(section[0] ,section[1],22,section[2], False, True,isItFolder=False)		#name,url,mode,icon
            
        link=getMatchUrl(url)
        sections=link.split(',')
        
        addDir(Colored('Replay','red',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        for section in sections:
            sname,section_number=section.split('=')
            addDir(sname ,url+':'+section_number,22,'', False, True,isItFolder=False)		#name,url,mode,icon

            
    except: traceback.print_exc(file=sys.stdout)

def getWillowHighlights(matchid):
    try:
        req = urllib2.Request(base64.b64decode('aHR0cDovL3dpbGxvd2ZlZWRzLndpbGxvdy50di93aWxsb3dNYXRjaERldGFpbHMvTWF0Y2hKU09ORGF0YS0lcy5qcw==')%matchid)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
        else:
            link=response.read()

        response.close()
#        print repr(link)
        pat='(\{.*})'
        link=re.findall(pat,link)[0]
        matchdata=json.loads(link)
        
        r=[]
        for m in matchdata["result"]:
            if "BGUrl" in m and  (not m["BGUrl"]=="") and base64.b64decode('d3p2b2Q6') in m["BGUrl"]:
                rurl=m["BGUrl"]
                rurl=rurl.replace(base64.b64decode('d3p2b2Q6Ly8='),base64.b64decode('aHR0cDovLzM4Ljk5LjY4LjE2MjoxOTM1L3dsbHd2b2QvX2RlZmluc3RfL3dsdm9kL3NtaWw6'));
                rurl=rurl.replace('.mp4',base64.b64decode('X3dlYi5zbWlsL3BsYXlsaXN0Lm0zdTg='));
                r.append([m["YTVideoName"],rurl,m["YTThumbId"]])
#        print 'replays',r
        return r
            
    except:
        print traceback.print_exc(file=sys.stdout)
        return None

    
def AddWillowCric(url):
    try:
    
        addDir(Colored('24x7 channel (US only, others use proxy so SLOW)','blue',True) ,'999999' ,21,'', False, True,isItFolder=False)		#name,url,mode,icon    
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        patt='json_matchbox = (.*?);'
        match_url =re.findall(patt,link)[0]
        print match_url
        matches=json.loads(match_url)
        
        print matches
        matchid=matches["result"]["past"][0]["MatchId"]
        if 1==2:
            addDir(Colored('Live Channel (Experimental)','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
            addDir('  Source 1' ,'%s:1'%str(matchid),21,'', False, True,isItFolder=False)		#name,url,mode,icon
            addDir('  Source 2' ,'%s:2'%str(matchid),21,'', False, True,isItFolder=False)		#name,url,mode,icon
            addDir('  Source 3' ,'%s:3'%str(matchid),21,'', False, True,isItFolder=False)		#name,url,mode,icon
            addDir('  Source 4' ,'%s:4'%str(matchid),21,'', False, True,isItFolder=False)		#name,url,mode,icon

        addDir(Colored('Live Games','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        if matches["result"]["live"]:
            live_games=matches["result"]["live"]
            for game in live_games:
                match_name=game["MatchName"]
                match_id=game["MatchId"]
                MatchStartDate=game["MatchStartDate"]
                entry_name=MatchStartDate+' - '+match_name
                #if useMyOwnUserNamePwd():
                #    addDir(entry_name ,match_id,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
                #else:
                loginworked,cookieJar= performWillowLogin();
                if loginworked:
                    st='LiveMatch'
                    url=base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210LyVzVVJMLmFzcD9taWQ9JXM=')%(st,match_id)
                    videoPage = getUrl(url,cookieJar=cookieJar)
                    videos=json.loads(videoPage)
                    for video in videos["roku"]["URL"]:
                        addDir(Colored('Source %s %s '%(str(video["priority"]), video["player"]),'ZM',True) +entry_name ,match_id+':'+str(video["priority"]),21,'', False, True,isItFolder=False)		#name,url,mode,icon
#                else:
#                    addDir(entry_name ,match_id,21,'', False, True,isItFolder=False)		#name,url,mode,icon           
        else:
            addDir('  No Games at the moment' ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon

            
            
        addDir(Colored('Recent Games','EB',True) ,'' ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
        past_games=matches["result"]["past"]
        for game in past_games:
            match_name=game["MatchName"]
            match_id=game["MatchId"]
#            print 'match_id',match_id
            MatchStartDate=game["MatchStartDate"]
            entry_name=MatchStartDate+' - '+match_name
#            addDir(entry_name ,match_id,23,'', False, True,isItFolder=True)		#name,url,mode,icon
            addDir(entry_name ,match_id,23,'')            
    except: traceback.print_exc(file=sys.stdout)
         
    addDir(Colored('All Recorded Series >>Click to load','ZM',True) ,base64.b64decode('aHR0cDovL3d3dy53aWxsb3cudHYvRXZlbnRNZ210L3Jlc3VsdHMuYXNw' ),20,'') #blocking as the rtmp requires to be updated to send gaolVanusPobeleVoKosat
    

    
def AddWatchCric(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    patt='<h1>(.*?)\s*</h1>(.*?)</div>'
    match_url =re.findall(patt,link,re.DOTALL)
    
    patt_sn='sn = "(.*?)"'
    for nm,div in match_url:
            curl=''
            cname=nm.split('<')[0]
            pat_options='<li><a href="(.*?)">(.*?)<'
            match_options =re.findall(pat_options,div)
            addDir(cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
            if match_options and len(match_options)>0:
                for u,n in match_options:
                    if not u.startswith('htt'):u=url+u
                    curl=u                
                    addDir('    -'+n ,curl ,17,'', False, True,isItFolder=False)		#name,url,mode,icon
            else:
                cname='No streams available'
                curl=''
                addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
                



def AddSmartCric(url):
    req = urllib2.Request(base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuY29tLw=='))
    req.add_header('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')

    response = urllib2.urlopen(req)
    link=response.read()
#    print link
    response.close()
    patt='performGet\(\'(.+)\''
    match_url =re.findall(patt,link)[0]
    channeladded=False
    patt_sn='sn = "(.*?)"'
    patt_pk='(&pk=.*?)"'
    try:
        match_sn =re.findall(patt_sn,link)[0]
        match_pk =re.findall(patt_pk,link)[0]
        final_url=  match_url+   match_sn
        req = urllib2.Request(final_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')
        req.add_header('Origin', base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuY29t'))
        req.add_header('Referer', base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuY29tLw=='))

        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        sources = json.loads(link)



        addDir('Refresh' ,'Live' ,144,'')
        
        for source in sources["channelsList"]:
            if 1==1:#ctype=='liveWMV' or ctype=='manual':
#                print source
                curl=''
                cname=source["caption"]
                fms=source["fmsUrl"]
#                print curl
                #if ctype<>'': cname+= '[' + ctype+']'
                addDir(cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
                if 'streamsList' in source and source["streamsList"] and len(source["streamsList"])>0:
                    for s in source["streamsList"]:
                        cname=s["caption"]
                        curl=s["streamName"]
                        streamid=str(s["streamId"])
                        curl1="http://"+fms+":8088/mobile/"+curl+"/playlist.m3u8?id="+streamid+match_pk;
                        addDir('    -'+cname +" (http)" ,curl1 ,15,'', False, True,isItFolder=False)		#name,url,mode,icon
                        #curl1="rtsp://"+"206.190.140.164"+":1935/mobile/"+curl+"?key="+match_sn+match_pk;
                        #curl1="rtsp://"+fms+":1935/mobile/"+curl+"?id="+streamid+"&key="+match_sn+match_pk;
                        #addDir('    -'+cname +" (rtsp)",curl1 ,15,'', False, True,isItFolder=False)		#name,url,mode,icon

                        channeladded=True
                else:
                    cname='No streams available'
                    curl=''
                    addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon
    except: traceback.print_exc(file=sys.stdout)
    if not channeladded:
        cname='No streams available'
        curl=''
        addDir('    -'+cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon 
    addDir('Refresh' ,'Live' ,144,'')
            

    return

def PlayWatchCric(url):
    progress = xbmcgui.DialogProgress()
    
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )
    pat_ifram='<iframe.*?src=(.*?).?"?>'    
    if 'c247.tv' not in url and 'crichd.tv' not in url:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_url =re.findall(pat_ifram,link)[0]
    else:
        match_url=url
        url=base64.b64decode('aHR0cDovL2VtYmVkMjQ3LmNvbS9saXZlLnBocD9jaD1QdHZfU3BvcnRzMSZ2dz02MDAmdmg9NDAwJmRvbWFpbj13d3cuc2FtaXN0cmVhbS5jb20=')
        
    req = urllib2.Request(match_url)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    req.add_header('Referer', url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
#    print 'match_url',match_url,link
        

    ccommand="";#'%s;TRUE;TRUE;'
    swfUrl=base64.b64decode('aHR0cDovL3d3dy5taXBzcGxheWVyLmNvbS9jb250ZW50L3NjcmlwdHMvZnBsYXllci5zd2Y=')
    sitename='www.mipsplayer.com'
    pat_e=' e=\'(.*?)\';'
    app='live'
    pat_js='channel=\'(.*?)\''
    
    if 'liveflashplayer.net/resources' in link:
        c='kaskatijaEkonomista'
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5saXZlZmxhc2hwbGF5ZXIubmV0L3Jlc291cmNlcy9zY3JpcHRzL2ZwbGF5ZXIuc3dm')
        sitename='www.liveflashplayer.net'
        pat_e=' g=\'(.*?)\';'
        app='stream'
        pat_js='channel=\'(.*?)\''
        ccommand=""#dont need to send

    elif 'www.mipsplayer.com' in link:
        c='ignore'#gaolVanusPobeleVoKosata
        ccommand='%s;FALSE;FALSE;' #stop sending and waiting
        
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5taXBzcGxheWVyLmNvbS9jb250ZW50L3NjcmlwdHMvZnBsYXllci5zd2Y=')
        sitename='www.mipsplayer.com'
        pat_e=' e=\'(.*?)\';'
        app='live'
        pat_js='channel=\'(.*?)\''
    elif 'www.streamifyplayer.com' in link:
        c='keGoVidishStambolSoseBardovci'
        ccommand='%s;TRUE;TRUE;'
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5zdHJlYW1pZnlwbGF5ZXIuY29tL3Jlc291cmNlcy9zY3JpcHRzL2VwbGF5ZXIuc3dm')
        sitename='www.streamifyplayer.com'
        pat_e='channel.*?g=\'(.*?)\''
        app='live'
        pat_js='channel=\'(.*?)\''
    elif 'c247.tv' or 'crichd.tv' in link:
        c='zenataStoGoPuknalaGavolot'
        ccommand=''
        swfUrl=base64.b64decode('aHR0cDovL3d3dy5wM2cudHYvcmVzb3VyY2VzL3NjcmlwdHMvZXBsYXllci5zd2Y=')
        sitename='www.p3g.tv'
        pat_e='channel.*?g=\'(.*?)\''
        app='stream'
        pat_js='channel=\'(.*?)\''
    elif 'zenexplayer.com' in link:
        c='zenataStoGoPuknalaGavolot'
        ccommand=''
        swfUrl=base64.b64decode('aHR0cDovL3d3dy56ZW5leHBsYXllci5jb20vZGF0YS9zY3JpcHRzL2ZwbGF5ZXIuc3dm')
        sitename='www.zenexplayer.com'
        pat_e='channel.*?g=\'(.*?)\''
        app='zenex'
        pat_js='channel=\'(.*?)\''
        
    progress.update( 40, "", "Building request links..", "" )
        
    match_urljs =re.findall(pat_js,link)[0]
    try:
        width='620'
        height='430'

        patt="width=([0-9]*).*?height=([0-9]*)"
        matc =re.findall(patt,link)
#        print 'matc',matc
        width, height=matc[0]
    except: pass

#    print 'width,height',width,height
    #print link
    match_e =re.findall(pat_e,link)[0]
    
    match_urljs=('http://%s/embedplayer/'%sitename)+match_urljs+'/'+match_e+'/'+width+'/'+height
    
    
    req = urllib2.Request(match_urljs)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    req.add_header('Referer', match_url)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    
    pat_flash='FlashVars\',.?\'(.*?)\''
    match_flash =re.findall(pat_flash,link)[0]
    matchid=match_flash.split('id=')[1].split('&')[0]
    if 'pk=' in match_flash:
        matchid+="&pk="+match_flash.split('pk=')[1].split('\'')[0].split('\"')[0]
    
    lb_url='http://%s:1935/loadbalancer?%s'%(sitename,matchid)
        
    req = urllib2.Request(lb_url)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    req.add_header('Referer', match_urljs)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    ip=link.split('=')[1]
    

    sid=match_flash.split('s=')[1].split('&')[0]
    progress.update( 40, "", "Finalizing request..", "" )

    if not ccommand=="":
        ccommand="ccommand="+(ccommand%c)
#    print 'ccommand',ccommand
    url='rtmp://%s/%s playpath=%s?id=%s pageUrl=%s swfUrl=%s Conn=S:OK %s flashVer=WIN\2019,0,0,185 timeout=20'%(ip,app,sid,matchid,match_urljs,swfUrl,ccommand)
#    print url
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist) 

def PlayGen(url):
    url = base64.b64decode(url)
#    print 'gen is '+url

    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist) 
        
        
def PlaySmartCric(url):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist) 
        
def AddEnteries(name, type=None):
#	print "addenT"
    if type=='Shows':
        AddShows(mainurl)
    elif type=='ProgTalkShows':
        AddProgramsAndShows(mainurl)
    elif name=='Next Page' or mode==43:
        AddShows(url)
    else:
        #addDir(Colored('ZemTv Channels','ZM',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)		#name,url,mode,icon
        #AddChannels();#AddChannels()
        isPakistani=(name=='Pakistani Live Channels')
        
        
        isYellowOff=selfAddon.getSetting( "isYellowOff" ) 
#        print 'isPakistani',isPakistani,isYellowOff
        if isPakistani and not isYellowOff=="true":        
            addDir(Colored('EboundServices Channels','EB',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)		#name,url,mode,icon
            try:
                AddChannelsFromEbound();#AddChannels()
            except: pass
        addDir(Colored('Other sources','ZM',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)
        try:
            ctype=1 if name=='Pakistani Live Channels' else ( 2 if name=='Indian Live Channels' else 3)
            AddChannelsFromOthers(ctype)
        except:
            print 'somethingwrong'
            traceback.print_exc(file=sys.stdout)
    return

def AddChannelsFromOthers(cctype):
    main_ch='(<section_name>Pakistani<\/section_name>.*?<\/section>)'
    v4link='aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9jaGFubmVsX2xpc3QvMy8='
    v4patt='<item>.*?<name>(.*?)<.*?<link>(.*?)<.*?channel_logo>(.*?)<'  
    v4patt='<channel>.*?<channel_name>(.*?)<.*?<channel_url>(.*?)<(.)' 
    usev4=True
    if cctype==2:
        main_ch='(<section_name>Hindi<\/section_name>.*?<\/section>)'
        v4link='aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9jaGFubmVsX2xpc3QvNC8='
        v4patt='<channel>.*?<channel_name>(.*?)<.*?<channel_url>(.*?)<(.)'  
        usev4=False
    if cctype==3:
        main_ch='(<section_name>Punjabi<\/section_name>.*?<\/section>)'
        v4link='aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9jaGFubmVsX2xpc3QvNjU5Lw=='
        v4patt='<channel>.*?<channel_name>(.*?)<.*?<channel_url>(.*?)<(.)'
        usev4=False
        

    patt='<item><name>(.*?)<.*?<link>(.*?)<.*?albumart>(.*?)<'
    match=[]    
    if 1==2:#enable it
        if ctype==1:
            url=base64.b64decode("aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9pdGVtcy8xMzE0LyVkLw==")
        else:
            url=base64.b64decode("aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9pdGVtcy8xMzE1LyVkLw==")

        pageIndex=0
        try:
            while True:
                newUrl=url%pageIndex
                pageIndex+=24
                req = urllib2.Request(newUrl)
                req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJ'))
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                totalcountPattern='<totalitems>(.*?)<'
                totalcount =int(re.findall(totalcountPattern,link)[0])
                
                #match =re.findall(main_ch,link)[0]
                matchtemp =re.findall(patt,link)
                for cname,curl,imgurl in matchtemp:
                    match.append((cname,'plus',curl,imgurl))
                #match+=matchtemp
                if pageIndex>totalcount:
                    break
        except: pass

  
    if 1==1 and usev4:#new v4 links
        try:
                      
            url=base64.b64decode(v4link)
            req = urllib2.Request(url)
            req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJ'))
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            print link
            match_temp=re.findall(v4patt,link)
            print 'match_temp',match_temp
            for cname,ctype,curl in match_temp:
                match.append((cname + ' v4',ctype,ctype,''))

            #match +=re.findall(patt,match_temp)
        except: pass
         
    if 1==2:#stop for time being
        try:
            patt='<channel><channel_number>.*?<channel_name>(.+?[^<])</channel_name><channel_type>(.+?)</channel_type>.*?[^<"]<channel_url>(.+?[^<])</channel_url>.*?</channel>'
            url=base64.b64decode("aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC90aWVyMi8yLzEv")
            req = urllib2.Request(url)
            req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJ'))
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            
            match_temp =re.findall(main_ch,link)[0]
            match_temp=re.findall(patt,match_temp)
            for cname,ctype,curl in match_temp:
                match.append((cname,ctype,curl,''))

            match +=re.findall(patt,match_temp)
        except: pass
        
    if 1==1:#stop for time being
        if cctype==1:
            if 1==2:
                match.append(('Ary digital','manual','cid:475',''))
                match.append(('Ary digital','manual','cid:981',''))
                match.append(('Ary digital Europe','manual','cid:587',''))
                match.append(('Ary digital World','manual','cid:589',''))
                match.append(('Ary News','manual','cid:474',''))
                match.append(('Ary News World','manual','cid:591',''))
                match.append(('Express News','manual','cid:275',''))
                match.append(('Express News','manual','cid:788',''))
                match.append(('Express Entertainment','manual','cid:260',''))
                match.append(('Express Entertainment','manual','cid:793',''))

            match.append(('ETV Urdu','manual','etv',''))
            match.append(('Ary Zindagi','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5emluZGFnaS50di8='),base64.b64decode('aHR0cDovL3d3dy5hcnl6aW5kYWdpLnR2L3dwLWNvbnRlbnQvdXBsb2Fkcy8yMDE0LzEwL0ZpbmFsLWxvZ28tMi5naWY=')))
            match.append(('QTV','manual',base64.b64decode('aHR0cDovL2xpdmUuYXJ5cXR2LnR2Lw=='),base64.b64decode('aHR0cDovL2FyeXF0di50di93cC1jb250ZW50L3VwbG9hZHMvMjAxNC8xMi9hcnktcXR2LTEtY29weS5qcGc=')))
            
            match.append((base64.b64decode('RHVueWEgKHdlYnNpdGUp'),'manual',base64.b64decode('aHR0cDovL2ltb2IuZHVueWFuZXdzLnR2OjE5MzUvbGl2ZS9zbWlsOnN0cmVhbS5zbWlsL3BsYXlsaXN0Lm0zdTg='),''))
            match.append((base64.b64decode('TmV3cyBvbmUgKHdlYnNpdGUp'),'manual','direct:'+base64.b64decode('aHR0cDovL2Nkbi5lYm91bmQudHYvdHYvbmV3c29uZS9wbGF5bGlzdC5tM3U4'),''))

            match.append((base64.b64decode('V2FzZWViICh3ZWJzaXRlKQ=='),'manual','direct:'+base64.b64decode('aHR0cDovL2Nkbi5lYm91bmQudHYvdHYvd2FzZWIvcGxheWxpc3QubTN1OA=='),''))

           
            
            
            match.append((base64.b64decode('Q2FwaXRhbCAod2Vic2l0ZSk='),'manual',base64.b64decode('ZWJvdW5kOmNhcGl0YWx0dg=='),''))
            match.append((base64.b64decode('RGF3biBuZXdzICh3ZWJzaXRlKQ=='),'manual',base64.b64decode('ZWJvdW5kOmRhd24='),''))
            match.append((base64.b64decode('Qm9sIHYy'),'manual',base64.b64decode('cHYyOkJvbCBOZXdz'),''))
            match.append((base64.b64decode('R2VvIE5ld3MgdjI='),'manual',base64.b64decode('cHYyOkdlbyBOZXdz'),''))
            match.append((base64.b64decode('R2VvIEVudGVydGFpbm1lbnQgdjI='),'manual',base64.b64decode('cHYyOkdlbyBFbnRlcnRhaW5tZW50'),''))
                        
            match.append((base64.b64decode('R2VvIEthaGFuaSB2Mg=='),'manual',base64.b64decode('cHYyOkdlbyBrYWhhbmk='),''))
            match.append((base64.b64decode('R2VvIFRleiB2Mg=='),'manual',base64.b64decode('cHYyOkdlbyB0ZXp6'),''))
            match.append((base64.b64decode('S1ROIHYy'),'manual',base64.b64decode('cHYyOktUTg=='),''))
            match.append((base64.b64decode('S1ROIE5FV1MgdjI='),'manual',base64.b64decode('cHYyOktUTiBORVdT'),''))


        elif cctype==2:
            match.append(('Color','manual','cid:316',''))

        
#    match.append((base64.b64decode('U2t5IFNwb3J0IDE='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNg=='),''))
     
#    match.append((base64.b64decode('U2t5IFNwb3J0IDI='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMyNg=='),''))
#    match.append((base64.b64decode('U2t5IFNwb3J0IDM='),'manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czMuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))
#    match.append((base64.b64decode('U2t5IFNwb3J0IDQ='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbC9wbGF5LzMxNQ=='),''))
#    match.append((base64.b64decode('U2t5IFNwb3J0IDU='),'manual',base64.b64decode('aHR0cDovL215amFkb290di5qYWRvb3R2LmNvbS9qbWFya3MvYm94L3BsYXlWaWRlby5waHA/cGxheVVybD1ydG1wOi8vcXVpbnplbGl2ZWZzLmZwbGl2ZS5uZXQvcXVpbnplbGl2ZS1saXZlL3NreXNwb3J0czUuc3RyZWFtP3NlY3VyaXR5dHlwZT0y'),''))


    pg=None
    if cctype==1:
        pg='pakistan'
    elif cctype==2:
        pg='indian'
    else:
        pg='punjabi'
    if pg:
        try:
#            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            xmldata=getPV2Url()
            sources=etree.fromstring(xmldata)
            ret=[]
            for source in sources.findall('items'):
                print pg,source.findtext('programCategory').lower()
                if pg == source.findtext('programCategory').lower():
                    cname=source.findtext('programTitle')
                    cid=source.findtext('programURL')
                    cimage=source.findtext('programImage')
#                    addDir(cname ,base64.b64encode(cid),37,cimage, False, True,isItFolder=False)
                    match.append((cname +' v3' ,'manual2', cid ,cimage))
            
        except:
            traceback.print_exc(file=sys.stdout)


#    match=sorted(match,key=itemgetter(0)   )
    match=sorted(match,key=lambda s: s[0].lower()   )
    for cname,ctype,curl,imgurl in match:
        if 1==1:#ctype=='liveWMV' or ctype=='manual':
#            print curl
            #if ctype<>'': cname+= '[' + ctype+']'
            
            addDir(Colored(cname.capitalize(),'ZM') ,base64.b64encode(curl) ,11 if not ctype=='manual2' else 37 ,imgurl, False, True,isItFolder=False)		#name,url,mode,icon
    return    
def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match

def revist_dag(page_data):
    final_url = ''
    if '127.0.0.1' in page_data:
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + ' live=true timeout=15 playpath=' + re_me(page_data, '\\?y=([a-zA-Z0-9-_\\.@]+)')
    if re_me(page_data, 'token=([^&]+)&') != '':
        final_url = final_url + '?token=' + re_me(page_data, 'token=([^&]+)&')
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'HREF="([^"]+)"')

    if 'dag1.asx' in final_url:
        return get_dag_url(final_url)

    if 'devinlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('devinlive', 'flive')
    if 'permlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('permlive', 'flive')



    return final_url
    
def get_ferrari_url(page_data,progress):


#    print 'get_dag_url2',page_data
    if not page_data.startswith('http'):
        return page_data;
    page_data2=getUrl(page_data);
#    print 'page_data2',page_data2
    patt='(http.*)'
    patt2='adsid=(.*?)&'    
    
    if 'ams.jadootv.info' in page_data2:
        page_data2=re.compile(patt).findall(page_data2)[0]
        page_data2=getUrl(page_data2);
#        page_data2=re.compile(patt).findall(page_data2)[0]
        headers=[('User-Agent','Ipad')]
        page_data2=getUrl(page_data,headers=headers);
#        print 'iam here',page_data2
        

    if 'adsid=' in page_data2:
        page_data2=re.compile(patt).findall(page_data2)[0]
        page_data=page_data2;
    elif 'ttl=' in page_data2:
        page_data2=re.compile(patt).findall(page_data2)[0]
        return page_data2
        page_data=page_data2;        
        patt2='ttl=(.*?)&'
    else:
        return page_data+'|User-Agent=iPad'
        
    progress.update( 30, "", "Found Ads", "" )
    import uuid
    playback=str(uuid.uuid1()).upper()   
    i=0
    addval=0
    opener = urllib2.build_opener(NoRedirection)

    adsid=re.compile(patt2).findall(page_data)[0]
#    print 'adsid',adsid
    adsidnew=int(adsid)-20000000
    page_data=page_data.replace(adsid,str(adsidnew))
    from datetime import datetime
    t1 = datetime.now()
    while i<1:      
        if not 'EXT-X-DISCONTINUITY' in page_data2:
#            print page_data
            page_data2=getUrl(page_data);
#            print page_data2
            links=re.compile(patt).findall(page_data2)
 #           print links
            headers=[('X-Playback-Session-Id',playback)]
            for l in links:
                addval+=1;
                progress.update( 30+addval*5, "", "Fetching Ads links #" + str(addval), "" )
                try:
                        if 1==1 or 'getDataTracker' in l:
#                            print 'playing the link'+l
                            #page_datatemp=getUrl(l,headers=headers);

                            response = opener.open(l)
                            
                except: traceback.print_exc(file=sys.stdout)

        else:
            break
        i+=1
    t2 = datetime.now()
    delta = t2 - t1
#    timetowait=18000-(delta.seconds*1000)
#    progress.update( 90, "", "wait for "+ str(timetowait/1000) , "" )
    #xbmc.sleep(timetowait)
    progress.update( 90, "", "Almost completed" , "" )
    print 'work done here '+page_data
    
    if 'elasticbeanstalk.com' in page_data:
        try:
            opener = urllib2.build_opener(NoRedirection)
            print 'page_data go',page_data
            opener.addheaders = [('User-agent', 'iPad')]
            response = opener.open(page_data)
            
            redir = response.info().getheader('Location')
            if 'hwcdn.net/' in redir:
                page_data=base64.b64decode('aHR0cDovL2FtczIuamFkb28udHYv')+redir.split(base64.b64decode('aHdjZG4ubmV0Lw=='))[1]
        except: pass
        
    return page_data+'|User-Agent=iPad&X-Playback-Session-Id='+playback
    
def get_dag_url(page_data):
#    print 'get_dag_url',page_data
    if '127.0.0.1' in page_data:
        return revist_dag(page_data)
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'href="([^"]+)"[^"]+$')
        if len(final_url)==0:
            final_url=page_data
    final_url = final_url.replace(' ', '%20')

    return final_url

def getPV2Url():
    import base64
    import time
    TIME = time.time()
    second= str(TIME).split('.')[0]
    first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
    token=base64.b64encode(base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))
    req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2FwcF9wYW5lbG5ldy9vdXRwdXQucGhwL3BsYXlsaXN0P3R5cGU9eG1sJmRldmljZVNuPXBha2luZGlhNCZ0b2tlbj0lcw==')  %token)   
    req.add_header('Authorization', base64.b64decode('QmFzaWMgWVdSdGFXNDZRV3hzWVdneFFBPT0=')) 
    response = urllib2.urlopen(req)
    link=response.read()
    return link
    
def getPV2Auth():
    import base64
    import time
    TIME = time.time()
    second= str(TIME).split('.')[0]
    first =int(second)+int(base64.b64decode('NjkyOTY5Mjk='))
    token=  base64.b64encode( base64.b64decode('JXNAMm5kMkAlcw==') % (str(first),second))
 
    req = urllib2.Request( base64.b64decode('aHR0cHM6Ly9hcHAuZHlubnMuY29tL2tleXMvYWN0aXZhdGUucGhwP3Rva2VuPQ==')+token)
    req.add_header('Authorization', "Basic %s"%base64.b64decode('Wkdsc1pHbHNaR2xzT2xCQWEybHpkRUJ1')) 
    response = urllib2.urlopen(req)
    link=response.read()
    return link

def PlayStreamSports(url):

    urlToPlay=base64.b64decode(url)
    import math,random
    servers=["OTMuMTg5LjU4LjQy","MTg1LjI4LjE5MC4xNTg=","MTc4LjE3NS4xMzIuMjEw","MTc4LjE3LjE2OC45MA=="];
    sid=int(math.floor(random.random()*len(servers)) )
    urlToPlay=base64.b64decode('cnRtcGU6Ly8lcy94bGl2ZSBwbGF5cGF0aD1yYXc6c2wxXyVzIGNvbm49UzpjbGllbnQgY29ubj1TOjMuMS4wLjQgdGltZW91dD0xMA==')%(base64.b64decode(servers[sid]),urlToPlay)
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    print "playing stream name: " + str(name) 
    xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( urlToPlay, listitem)    
    
def PlayPV2Link(url):

    if not mode==37:
        xmldata=getPV2Url()
        urlToPlay=re.findall(url+'..programTitle.*?programURL\\>(.*?)\\<',xmldata)[0]
    else:
        urlToPlay=base64.b64decode(url)
#    print 'urlToPlay',urlToPlay    
    urlToPlay+=getPV2Auth()
#    print 'urlToPlay',urlToPlay
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    print "playing stream name: " + str(name) 
    xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( urlToPlay, listitem)  
    
def PlayOtherUrl ( url ):
    url=base64.b64decode(url)
    if url.startswith('cid:'): url=base64.b64decode('aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwLzJfNS9neG1sL3BsYXkvJXM=')%url.replace('cid:','')
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    direct=False
    
    
    if "ebound:" in url:
        PlayLiveLink(url.split('ebound:')[1])
        return
    if "direct:" in url:
        PlayGen(base64.b64encode(url.split('direct:')[1]))
        return
    if "pv2:" in url:
        PlayPV2Link(url.split('pv2:')[1])
        return    
    if url==base64.b64decode('aHR0cDovL2xpdmUuYXJ5emluZGFnaS50di8=') or url==base64.b64decode('aHR0cDovL2xpdmUuYXJ5cXR2LnR2Lw=='):
        req = urllib2.Request(url)
#        req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJXygyLjQuNy41LjguMC4zNCk=')) 
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='file: "(htt.*?)"' if 'qtv' not in url else 'file: \'(.*?)\''
        if curlpatth.startswith('rtmp'): curlpatth+=' timeout=20'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[0]
    elif url=='etv':
        req = urllib2.Request(base64.b64decode('aHR0cDovL20ubmV3czE4LmNvbS9saXZlLXR2L2V0di11cmR1'))
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<source src="(.*?)"'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[0]
    elif 'dag1.asx' not in url and 'hdcast.org' not in url and '?securitytype=2' not in url and 'bernardotv.club' not in url and 'imob.dunyanews.tv' not in url:
        if '/play/' in url:
            code=base64.b64decode('MDAwNkRDODUz')+binascii.b2a_hex(os.urandom(2))[:3]
            url+=base64.b64decode('L1VTLzEv')+code
            getUrl(base64.b64decode('aHR0cDovL2ZlcnJhcmlsYi5qZW10di5jb20vaW5kZXgucGhwL3htbC9pbml0aWFsaXplLzA1LTAyLTEzMDEwNy0yNC1QT1AtNjE4LTAwMC8yLjIuMS40Lw==')+code)
        req = urllib2.Request(url)
        req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJXygyLjQuNy41LjguMC4zNCk='))   

        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<link>(.*?)<\/link>'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)
        if '[CDATA' in dag_url:
            dag_url=dag_url.split('CDATA[')[1].split(']')[0]#
        if not (dag_url and len(dag_url)>0 ):
            curlpatth='\<ENTRY\>\<REF HREF="(.*?)"'
            dag_url =re.findall(curlpatth,link)[0]
        else:
            dag_url=dag_url[0]
    else:
        if 'hdcast.org' in url or 'bernardotv.club' in url:
            direct=True
        dag_url=url
    if '[CDATA' in dag_url:
        dag_url=dag_url.split('CDATA[')[1].split(']')[0]#

#    print 'dag_url',dag_url,name
    
    if '?securitytype=2' in url:
        opener = urllib2.build_opener(NoRedirection)
        response = opener.open(url)
        dag_url = response.info().getheader('Location')
        if '127.0.0.1' not in dag_url: 
            dag_url='rtmp://quinzelivefs.fplive.net/quinzelive-live live=true timeout=15 playpath=%s'%dag_url.split('/')[-1]
#            print 'redir dag_url',dag_url
            direct=True

 

    if 'dag1.asx' in dag_url:    
        req = urllib2.Request(dag_url)
        req.add_header('User-Agent', base64.b64decode('VmVyaXNtby1CbGFja1VJXygyLjQuNy41LjguMC4zNCk='))   
        response = urllib2.urlopen(req)
        link=response.read()
        dat_pattern='href="([^"]+)"[^"]+$'
        dag_url =re.findall(dat_pattern,link)[0]
   
        
#    print 'dag_url2',dag_url
    if direct:
        final_url=dag_url
    else:
        final_url=get_dag_url(dag_url)

    print 'final_url',final_url            
    if 'token=hw_token' in final_url:
        final_url=final_url.split('?')[0]#
        print 'final_url',final_url   
    if 'token=ec_hls_token' in final_url:
        final_url=final_url.split('?')[0]#
        print 'final_url',final_url   
        
        
#    print 'final_urlllllllllllll',final_url

    if base64.b64decode('amFkb29fdG9rZW4=') in final_url or 'elasticbeanstalk' in final_url:
        print 'In Ferari url'
        final_url=get_ferrari_url(final_url,progress)        
    progress.update( 100, "", "Almost done..", "" )

        
#    print final_url
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#    print "playing stream name: " + str(name) 
    xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( final_url, listitem)    

def AddChannelsFromEbound():
	liveURL=base64.b64decode('aHR0cDovL2Vib3VuZHNlcnZpY2VzLmNvbS9pc3RyZWFtX2RlbW8ucGhw')
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<a href=".*?stream=(.*?)".*?src="(.*?)" (.)', link,re.M)

#	print match
	expressExists=False
	expressCName='express'
	arynewsAdded=False
	
	if not any('Express Tv' == x[0] for x in match):
		match.append(('Express Tv','express','manual'))
	if not any('Ary News' == x[0] for x in match):
		match.append(('Ary News','arynews','manual'))
	if not any('Ary Digital' == x[0] for x in match):
		match.append(('Ary Digital','aryentertainment','manual'))

	match.append(('Baby Tv','babytv','manual'))
	match.append(('Star Gold','stargold','manual'))
	match.append(('Ten Sports','tensports','manual'))
	match.append(('Discovery','discovery','manual'))
	match.append(('National Geographic','nationalgeographic','manual'))
	match.append(('mecca','mecca','manual'))
	match.append(('madina','madina','manual'))
	match.append(('Peace Tv','peacetv','manual'))
	match.append(('Geo Entertainment','geoentertainment','manual'))
	match.append(('Geo News','geonews','manual'))
	match.append(('Channel 92','channel92','manual'))
	match.append(('Geo Super','geosuper','manual'))
	match.append(('Bol News','bol','manual'))
	match.append(('Capital News','capitaltv','manual'))
	match.append(('Dawn News','dawn','manual'))    
	match.append(('Quran TV Urdu','aHR0cDovL2lzbDEuaXNsYW00cGVhY2UuY29tL1F1cmFuVXJkdVRW','gen'))

	match.append(('Channel 24','cnRtcDovL2RzdHJlYW1vbmUuY29tOjE5MzUvbGl2ZS8gcGxheXBhdGg9Y2l0eTQyIHN3ZlVybD1odHRwOi8vZHN0cmVhbW9uZS5jb20vanAvandwbGF5ZXIuZmxhc2guc3dmIHBhZ2VVcmw9aHR0cDovL2RzdHJlYW1vbmUuY29tL2NpdHk0Mi9pZnJhbWUuaHRtbCB0aW1lb3V0PTIw','gen'))
	match.append(('QTV','cnRtcDovLzkzLjExNS44NS4xNzoxOTM1L0FSWVFUVi9teVN0cmVhbSB0aW1lb3V0PTEw','gen'))

    
    
    

    
	match=sorted(match,key=lambda s: s[0].lower()   )

	#h = HTMLParser.HTMLParser()
	for cname in match:
		if cname[2]=='manual':
			addDir(Colored(cname[0].capitalize(),'EB') ,cname[1] ,9,cname[2], False, True,isItFolder=False)		#name,url,mode,icon
		elif cname[2]=='gen':
			addDir(Colored(cname[0].capitalize(),'EB') ,cname[1] ,33,cname[2], False, True,isItFolder=False)		#name,url,mode,icon
		else:
			addDir(Colored(cname[0].capitalize(),'EB') ,cname[0] ,9,cname[1], False, True,isItFolder=False)		#name,url,mode,icon

		if 1==2:
			if cname[0]==expressCName:
				expressExists=True
			if cname[0]=='arynews':
				arynewsAdded=True

	if 1==2:			
		if not expressExists:
			addDir(Colored('Express Tv','EB') ,'express' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		if not arynewsAdded:
			addDir(Colored('Ary News','EB') ,'arynews' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
			addDir(Colored('Ary Digital','EB') ,'aryentertainment' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		addDir(Colored('Baby Tv','EB') ,'babytv' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		addDir(Colored('Star Gold','EB') ,'stargold' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		addDir(Colored('Ten Sports','EB') ,'tensports' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
	return		

def Colored(text = '', colorid = '', isBold = False):
	if colorid == 'ZM':
		color = 'FF11b500'
	elif colorid == 'EB':
		color = 'FFe37101'
	elif colorid == 'bold':
		return '[B]' + text + '[/B]'
	else:
		color = colorid
		
	if isBold == True:
		text = '[B]' + text + '[/B]'
	return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)
        
def AddProgramsAndShows(Fromurl):
    CookieJar=getZemCookieJar()
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
#    link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    try:
        link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    except:
        import cloudflare
        cloudflare.createCookie(Fromurl,CookieJar,'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)

    CookieJar.save (ZEMCOOKIEFILE,ignore_discard=True)
    link=link.split('<select data-placeholder="Choose a Program..."')[1].split('</select>')[0]
#    print link    
    match =re.findall('<optgroup label=\'(.*?)\'', link, re.UNICODE)
    h = HTMLParser.HTMLParser()
    #'<option value="(.*?)">(.*?)<'
    #<optgroup label='(.*?)'
    for cname in match:
        addDir(Colored(cname,'ZM'),cname ,-9,'', True,isItFolder=False)
        subprogs=link.split('<optgroup label=\'%s\''%cname)[1].split('</optgroup>')[0]
        submatch=re.findall('<option value="(.*?)">(.*?)<', subprogs, re.UNICODE)
        for csubname in submatch:
    #		tname=cname[2]#
            addDir('    '+csubname[1],mainurl+ csubname[0] ,43,'', True,isItFolder=True)
    return

    
def AddShows(Fromurl):
    #	print Fromurl
    CookieJar=getZemCookieJar()
    #	req = urllib2.Request(Fromurl)
    #	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    #	response = urllib2.urlopen(req)
    #	link=response.read()
    #	response.close()
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    #	link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    try:
        link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    except:
        import cloudflare
        cloudflare.createCookie(Fromurl,CookieJar,'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        link=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)


    #	print link
    #cloudflare.createCookie('http://www.movie25.ag/',Cookie_Jar,'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    #	print "addshows"
    #	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
    #	match=re.compile('<a href="(.+?)"').findall(link)
    #	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
    #	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
    #	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
    #	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
    #	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)
    CookieJar.save (ZEMCOOKIEFILE,ignore_discard=True)

    if '<div id="top-articles">' in link:
        link=link.split('<div id="top-articles">')[0]
    match =re.findall('<div class="thumbnail">\\s*<a href="(.*?)".*\s*<img class="thumb".*?src="(.*?)" alt="(.*?)"', link, re.UNICODE)
    if len(match)==0:
        match =re.findall('<div class="thumbnail">\s*<a href="(.*?)".*\s*<img.*?.*?src="(.*?)".* alt="(.*?)"', link, re.UNICODE)


    #	print link
    #	print match

    #	print match
    h = HTMLParser.HTMLParser()

    for cname in match:
        tname=cname[2]
        tname=re.sub(r'[\x80-\xFF]+', convert,tname )
        #tname=repr(tname)
        addDir(tname,cname[0] ,3,cname[1], True,isItFolder=False)
        

    match =re.findall('<a class="nextpostslink" rel="next" href="(.*?)">', link, re.IGNORECASE)

    if len(match)==1:
        addDir('Next Page' ,match[0] ,2,'',isItFolder=True)
    #       print match

    return


def AddChannels():
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="epic-cs">\s*<a href="(.+)" rel=.*<img src="(.+)" alt="(.+)" \/>', link, re.UNICODE)

#	print match
	h = HTMLParser.HTMLParser()
	for cname in match:
		addDir(Colored(h.unescape(cname[2].replace("Watch Now Watch ","").replace("Live, High Quality Streaming","").replace("Live &#8211; High Quality Streaming","").replace("Watch Now ","")) ,'ZM'),cname[0] ,4,cname[1],False,True,isItFolder=False)		
	return	

	
	

def PlayShowLink ( url ): 
    global linkType
    #	url = tabURL.replace('%s',channelName);
#    req = urllib2.Request(url)
#    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
#    response = urllib2.urlopen(req)
#    link=response.read()
#    response.close()
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    CookieJar=getZemCookieJar()
    link=getUrl(url,cookieJar=CookieJar, headers=headers)

    #	print url

    line1 = "Playing DM Link"
    time = 5000  #in miliseconds
    defaultLinkType=0 #0 youtube,1 DM,2 tunepk
    defaultLinkType=selfAddon.getSetting( "DefaultVideoType" ) 
    #	print defaultLinkType
    #	print "LT link is" + linkType
    # if linktype is not provided then use the defaultLinkType

    if linkType.upper()=="SHOWALL" or (linkType.upper()=="" and defaultLinkType=="4"):
        ShowAllSources(url,link)
        return
    if linkType.upper()=="DM" or (linkType=="" and defaultLinkType=="0"):
    #		print "PlayDM"
        line1 = "Playing DM Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print link
        playURL= match =re.findall('src="(http.*?(dailymotion.com).*?)"',link)
        if len(playURL)==0:
            line1 = "Daily motion link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        playURL=match[0][0]
    #		print playURL
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        #src="(.*?(dailymotion).*?)"
    elif  linkType.upper()=="EBOUND"  or (linkType=="" and defaultLinkType=="3"):
        line1 = "Playing Ebound Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print "Eboundlink"
        playURL= match =re.findall(' src=".*?ebound\\.tv.*?site=(.*?)&.*?date=(.*?)\\&', link)
        if len(playURL)==0:
            line1 = "EBound link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 

        playURL=match[0]
        dt=playURL[1]
        clip=playURL[0]
        urli=base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vaWZyYW1lL25ldy92b2RfdWdjLnBocD9zdHJlYW09bXA0OnZvZC8lcy8lcyZ3aWR0aD02MjAmaGVpZ2h0PTM1MCZjbGlwPSVzJmRheT0lcyZtb250aD11bmRlZmluZWQ=')%(dt,clip,clip,dt)
        #req = urllib2.Request(urli)
        #req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        #response = urllib2.urlopen(req)
        #link=response.read()
        #response.close()
        post = {'username':'hash'}
        post = urllib.urlencode(post)
        req = urllib2.Request(base64.b64decode('aHR0cDovL2Vib3VuZHNlcnZpY2VzLmNvbS9mbGFzaHBsYXllcmhhc2gvaW5kZXgucGhw'))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
        response = urllib2.urlopen(req,post)
        link=response.read()
        response.close()
        strval =link;# match[0]

        stream_url=base64.b64decode('cnRtcDovL2Nkbi5lYm91bmQudHYvdm9kIHBsYXlwYXRoPW1wNDp2b2QvJXMvJXMgYXBwPXZvZD93bXNBdXRoU2lnbj0lcyBzd2Z1cmw9aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vbGl2ZS92Ni9wbGF5ZXIuc3dmP2RvbWFpbj13d3cuemVtdHYuY29tJmNoYW5uZWw9JXMmY291bnRyeT1FVSBwYWdlVXJsPSVzIHRjVXJsPXJ0bXA6Ly9jZG4uZWJvdW5kLnR2L3ZvZD93bXNBdXRoU2lnbj0lcyBsaXZlPXRydWUgdGltZW91dD0xNQ==')%(dt,clip,strval,clip,urli,strval)

    #		print stream_url
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="LINK"  or (linkType=="" and defaultLinkType=="1"):
        line1 = "Playing Tune.pk Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print "PlayLINK"
        playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
        if len(playURL)==0:
            line1 = "Link.pk link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 

        playURL=match[0][0]
    #		print playURL
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
    #		print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="PLAYWIRE"  or (linkType=="" and defaultLinkType=="2"):
        line1 = "Playing Playwire Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
    #		print "Playwire"
        playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
        V=1
        if len(playURL)==0:
            playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
            V=2
        if len(playURL)==0:
            line1 = "Playwire link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        if V==1:
            (playWireVar,PubId,videoID)=playURL[0]
            cdnUrl=base64.b64decode("aHR0cDovL2Nkbi5wbGF5d2lyZS5jb20vdjIvJXMvY29uZmlnLyVzLmpzb24=")%(PubId,videoID)
            req = urllib2.Request(cdnUrl)
            req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            playURL =base64.b64decode("aHR0cDovL2Nkbi5wbGF5d2lyZS5jb20vJXMvJXM=")%(PubId,re.findall('src":".*?mp4:(.*?)"', link)[0])
    #			print 'playURL',playURL
        else:
            playURL=playURL[0]
            if playURL.startswith('//'): playURL='http:'+playURL
    #			print playURL            
            reg='media":\{"(.*?)":"(.*?)"'
            req = urllib2.Request(playURL)
            req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            response = urllib2.urlopen(req)
            link=response.read()
            playURL =re.findall(reg, link)
            if len(playURL)>0:
                playURL=playURL[0]
                ty=playURL[0]
                innerUrl=playURL[1]
    #				print innerUrl
                req = urllib2.Request(innerUrl)
                req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
                response = urllib2.urlopen(req)
                link=response.read()
                reg='baseURL>(.*?)<\/baseURL>\s*?<media url="(.*?)"'
                playURL =re.findall(reg, link)[0]
                playURL=playURL[0]+'/'+playURL[1]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = playURL#urlresolver.HostedMediaFile(playURL).resolve()
    #		print 'stream_url',stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
        #bmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)#src="(.*?(tune\.pk).*?)"
    else:	#either its default or nothing selected
        line1 = "Playing Youtube Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        youtubecode= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
        if len(youtubecode)==0:
            line1 = "Youtube link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return
        youtubecode=youtubecode[0]
        uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
    #	print uurl
        xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")

    return

def ShowAllSources(url, loadedLink=None):
	global linkType
#	print 'show all sources',url
	link=loadedLink
	if not loadedLink:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	available_source=[]
	playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
#	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
#	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('src="(.*?ebound\\.tv.*?)"', link)
#	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Ebound Source')		
		 
	playURL= match =re.findall('src="(.*?(dailymotion).*?)"',link)
	if not len(playURL)==0:
		available_source.append('Daily Motion Source')

	playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
	if not len(playURL)==0:
		available_source.append('Link Source')

	playURL= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
	if not len(playURL)==0:
		available_source.append('Youtube Source')

	if len(available_source)>0:
		dialog = xbmcgui.Dialog()
		index = dialog.select('Choose your stream', available_source)
		if index > -1:
			linkType=available_source[index].replace(' Source','').replace('Daily Motion','DM').upper()
#			print 'linkType',linkType
			PlayShowLink(url);

def PlayLiveLink ( url ):
	progress = xbmcgui.DialogProgress()
	progress.create('Progress', 'Fetching Streaming Info')
	progress.update( 10, "", "Finding links..", "" )
	if mode==4:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		#print link
		#print url
		match =re.findall('"http.*(ebound).*?\?site=(.*?)"',link,  re.IGNORECASE)[0]
		cName=match[1]
		progress.update( 20, "", "Finding links..", "" )
	else:
		cName=url
	import math, random, time
	rv=str(int(5000+ math.floor(random.random()*10000)))
	currentTime=str(int(time.time()*1000))
	newURL=base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vaWZyYW1lL25ldy9tYWluUGFnZS5waHA/c3RyZWFtPQ==')+cName+  '&width=undefined&height=undefined&clip=' + cName+'&rv='+rv+'&_='+currentTime
	
	req = urllib2.Request(newURL)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	progress.update( 50, "", "Finding links..", "" )
	
#	match =re.findall('<iframe.+src=\'(.*)\' frame',link,  re.IGNORECASE)
#	print match
#	req = urllib2.Request(match[0])
#	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
#	response = urllib2.urlopen(req)
#	link=response.read()
#	response.close()
	time = 2000  #in miliseconds
	defaultStreamType=0 #0 RTMP,1 HTTP
	defaultStreamType=selfAddon.getSetting( "DefaultStreamType" ) 
#	print 'defaultStreamType',defaultStreamType
	if 1==2 and (linkType=="HTTP" or (linkType=="" and defaultStreamType=="1")): #disable http streaming for time being
#	print link
		line1 = "Playing Http Stream"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		
		match =re.findall('MM_openBrWindow\(\'(.*)\',\'ebound\'', link,  re.IGNORECASE)
			
	#	print url
	#	print match
		
		strval = match[0]
		
		#listitem = xbmcgui.ListItem(name)
		#listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		#playlist.add (strval)
		
		#xbmc.Player().play(playlist)
		listitem = xbmcgui.ListItem( label = str(cName), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=strval )
#		print "playing stream name: " + str(cName) 
		listitem.setInfo( type="video", infoLabels={ "Title": cName, "Path" : strval } )
		listitem.setInfo( type="video", infoLabels={ "Title": cName, "Plot" : cName, "TVShowTitle": cName } )
		xbmc.Player(PLAYER_CORE_AUTO).play( str(strval), listitem)
	else:
		line1 = "Playing RTMP Stream"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		progress.update( 60, "", "Finding links..", "" )
		post = {'username':'hash'}
        	post = urllib.urlencode(post)
		req = urllib2.Request(base64.b64decode('aHR0cDovL2Vib3VuZHNlcnZpY2VzLmNvbS9mbGFzaHBsYXllcmhhc2gvaW5kZXgucGhw'))
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
		response = urllib2.urlopen(req,post)
		link=response.read()
		response.close()
		

        
#		print link
		#match =re.findall("=(.*)", link)

		#print url
		#print match

		strval =link;# match[0]

		#listitem = xbmcgui.ListItem(name)
		#listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		#playlist.add (strval)

		playfile=base64.b64decode('cnRtcDovL2Nkbi5lYm91bmQudHYvdHY/d21zQXV0aFNpZ249LyVzIGFwcD10dj93bXNBdXRoU2lnbj0lcyBzd2Z1cmw9aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vbGl2ZS92Ni9qd3BsYXllci5mbGFzaC5zd2Y/ZG9tYWluPXd3dy5lYm91bmRzZXJ2aWNlcy5jb20mY2hhbm5lbD0lcyZjb3VudHJ5PUVVIHBhZ2VVcmw9aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vY2hhbm5lbC5waHA/YXBwPXR2JnN0cmVhbT0lcyB0Y1VybD1ydG1wOi8vY2RuLmVib3VuZC50di90dj93bXNBdXRoU2lnbj0lcyBsaXZlPXRydWUgdGltZW91dD0xNQ==')%(cName,strval,cName,cName,strval)
		progress.update( 100, "", "Almost done..", "" )
#		print playfile
		#xbmc.Player().play(playlist)
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
#		print "playing stream name: " + str(name) 
		#listitem.setInfo( type="video", infoLabels={ "Title": name, "Path" : playfile } )
		#listitem.setInfo( type="video", infoLabels={ "Title": name, "Plot" : name, "TVShowTitle": name } )
		xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( playfile, listitem)
		#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
	
	return


#print "i am here"
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
	mode=int(params["mode"])
except:
	pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
	linkType=args.get('linkType', '')[0]
except:
	pass


print 	mode,url,linkType

try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		Addtypes()
	elif mode==2 or mode==43:
		print "Ent url is ",name,url        
		AddEnteries(name, url)

	elif mode==3:
		print "Play url is "+url
		PlayShowLink(url)

	elif mode==4 or mode==9:
		print "Play url is "+url
		PlayLiveLink(url)
	elif mode==11:
		print "Play url is "+url
		PlayOtherUrl(url)

	elif mode==6 :
		print "Play url is "+url
		ShowSettings(url)
	elif mode==13 :
		print "Play url is "+url
		AddSports(url)
	elif mode==14 or mode==144:
		print "Play url is "+url
		AddSmartCric(url)
	elif mode==15 :
		print "Play url is "+url
		PlaySmartCric(url)
	elif mode==16 :
		print "Play url is "+url
		AddWatchCric(url)
	elif mode==17 :
		print "Play url is "+url
		PlayWatchCric(url)
	elif mode==19 :
		print "Play url is "+url
		AddWillowCric(url)
	elif mode==20:
		print "Play url is "+url
		AddWillSportsOldSeries(url)
	elif mode==21 or mode==22:
		print "Play url is "+url
		PlayWillowMatch(url)        
	elif mode==23:
		print "Play url is "+url
		AddWillowReplayParts(url)        
	elif mode==24:
		print "Play url is "+url
		AddWillSportsOldSeriesMatches(url)        

	elif mode==26 :
		print "Play url is "+url
		AddCricHD(url)
	elif mode==27 :
		print "Play url is "+url
		PlayCricHD(url)                
	elif mode==31 :
		print "Play url is "+url
		AddFlashtv(url)                
	elif mode==30 :
		print "Play url is "+url
		AddP3gSports(url)                
	elif mode==32 :
		print "Play url is "+url
		PlayFlashTv(url)                
	elif mode==33 :
		print "Play url is "+url
		PlayGen(url)                
	elif mode==34 :
		print "Play url is "+url
		GetSSSEvents(url)                
	elif mode==35 :
		print "Play url is "+url
		PlaySSSEvent(url)                
	elif mode==36 :
		print "Play url is "+url
		AddPv2Sports(url) 
	elif mode==37 :
		print "Play url is "+url
		PlayPV2Link(url) 

	elif mode==39 :
		print "Play url is "+url
		AddStreamSports(url) 
	elif mode==40 :
		print "Play url is "+url
		PlayStreamSports(url)         
	elif mode==41 :
		print "Play url is "+url
		AddCricFree(url) 
	elif mode==42 :
		print "Play url is "+url
		PlayCricFree(url) 
except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)
	

if not ( (mode==3 or mode==4 or mode==9 or mode==11 or mode==15 or mode==21 or mode==22 or mode==27 or mode==33 or mode==35 or mode==37 or mode==40 or mode==42)  )  :
	if mode==144:
		xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))