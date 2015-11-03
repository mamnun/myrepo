# -*- coding: utf-8 -*-

'''
    Shani_08 resolver for muchmovies.
    jsunpack code is based on jsunpack code by t0mm0.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,time,base64

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result


class jsunpack:
    def unpack(self, sJavascript,iteration=1, totaliterations=2):
        #print 'iteration',iteration
        if sJavascript.startswith('var _0xcb8a='):
            aSplit=sJavascript.split('var _0xcb8a=')
            ss="myarray="+aSplit[1].split("eval(")[0]
            exec(ss)
            a1=62
            c1=int(aSplit[1].split(",62,")[1].split(',')[0])
            p1=myarray[0]
            k1=myarray[3]
            with open('temp file'+str(iteration)+'.js', "wb") as filewriter:
                filewriter.write(str(k1))
            #aa=1/0
        else:

            aSplit = sJavascript.split("rn p}('")
            
            p1,a1,c1,k1=('','0','0','')
         
            ss="p1,a1,c1,k1=('"+aSplit[1].split(".spli")[0]+')' 
            exec(ss)
        k1=k1.split('|')
        aSplit = aSplit[1].split("))'")
    #    print ' p array is ',len(aSplit)
    #   print len(aSplit )

        #p=str(aSplit[0]+'))')#.replace("\\","")#.replace('\\\\','\\')

        #print aSplit[1]
        #aSplit = aSplit[1].split(",")
        #print aSplit[0] 
        #a = int(aSplit[1])
        #c = int(aSplit[2])
        #k = aSplit[3].split(".")[0].replace("'", '').split('|')
        #a=int(a)
        #c=int(c)
        
        #p=p.replace('\\', '')
    #    print 'p val is ',p[0:100],'............',p[-100:],len(p)
    #    print 'p1 val is ',p1[0:100],'............',p1[-100:],len(p1)
        
        #print a,a1
        #print c,a1
        #print 'k val is ',k[-10:],len(k)
    #    print 'k1 val is ',k1[-10:],len(k1)
        e = ''
        d = ''#32823

        #sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        sUnpacked1 = str(self.__unpack(p1, a1, c1, k1, e, d,iteration))
        
        #print sUnpacked[:200]+'....'+sUnpacked[-100:], len(sUnpacked)
    #    print sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
        
        #exec('sUnpacked1="'+sUnpacked1+'"')
        if iteration>=totaliterations:
    #        print 'final res',sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
            return sUnpacked1#.replace('\\\\', '\\')
        else:
    #        print 'final res for this iteration is',iteration
            return self.unpack(sUnpacked1,iteration+1)#.replace('\\', ''),iteration)#.replace('\\', '');#self.unpack(sUnpacked.replace('\\', ''))

    def __unpack(self, p, a, c, k, e, d, iteration):

        with open('before file'+str(iteration)+'.js', "wb") as filewriter:
            filewriter.write(str(p))
        while (c > 1):
            c = c -1
            if (k[c]):
                aa=str(self.__itoaNew(c, a))
                #re.sub('\\b' + aa +'\\b', k[c], p) THIS IS Bloody slow!
                p=self.findAndReplaceWord(p,aa,k[c])

                
        with open('after file'+str(iteration)+'.js', "wb") as filewriter:
            filewriter.write(str(p))
        return p

    def findAndReplaceWord(self, source_str, word_to_find,replace_with):
        #function equalavent to re.sub('\\b' + aa +'\\b', k[c], p)
        splits=None
        splits=source_str.split(word_to_find)
        if len(splits)>1:
            new_string=[]
            current_index=0
            for current_split in splits:
                #print 'here',i
                new_string.append(current_split)
                val=word_to_find#by default assume it was wrong to split

                #if its first one and item is blank then check next item is valid or not
                if current_index==len(splits)-1:
                    val='' # last one nothing to append normally
                else:
                    if len(current_split)==0: #if blank check next one with current split value
                        if ( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_'):# first just just check next
                            val=replace_with
                    #not blank, then check current endvalue and next first value
                    else:
                        if (splits[current_index][-1].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') and (( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_')):# first just just check next
                            val=replace_with
                            
                new_string.append(val)
                current_index+=1
            #aaaa=1/0
            source_str=''.join(new_string)
        return source_str        

    def __itoa(self, num, radix):
    #    print 'num red',num, radix
        result = ""
        if num==0: return '0'
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result

    def __itoaNew(self, cc, a):
        aa="" if cc < a else self.__itoaNew(int(cc / a),a) 
        cc = (cc % a)
        bb=chr(cc + 29) if cc> 35 else str(self.__itoa(cc,36))
        return aa+bb


def decryptMe(cj, cf, e):
    ci = ""
    ch = ""
    cg = 0
    lenofcf=len(cf)
    lenOfE=len(e)
    for cg in range(0,len(cj)):
        ci += chr(ord(cj[cg])^ord(cf[cg %lenofcf]))

    for cg in range(0,len(ci)):
        ch += chr(ord(ci[cg])^ord(e[cg %lenOfE]))
    return ch


def resolve(url):
    try:
        result = getUrl(url, mobile=True).result
        cj = re.compile('gsm = "(.+?)"').findall(result)[-1]
        cj = base64.b64decode(cj)


        min_js_string = getUrl('http://www.muchmovies.org/js/jquery.min.js', mobile=True).result


        sUnpacked = jsunpack().unpack(min_js_string,1,2) #2nd level encryption , encrypted 3 times	


        variables = re.compile('d1\(atob\(.*?,(.*?),(.*?)\)').findall(sUnpacked)[0]

        cf_var = variables[0]
        cf = re.compile('[\'|\"](.+?)[\'|\"]').findall(cf_var)[0]
        for i in range(0, cf_var.count('atob')): cf = base64.b64decode(cf)

        e_var = variables[1]
        e = re.compile('[\'|\"](.+?)[\'|\"]').findall(e_var)[0]
        for i in range(0, e_var.count('atob')): e = base64.b64decode(e)

        print cf, e

        url = decryptMe(cj, cf, e)
        return url
    except:
        return


#print resolve('http://www.muchmovies.org/movies/300-rise-of-an-empire-2014')
