import struct
import urllib2,urllib
import re
import json
import math
CRYPT_XXTEA_DELTA= 0x9E3779B9
 
class Crypt_XXTEA:
    _key=None

    def setKey(self,key):
        if isinstance(key, basestring):
            k = self._str2long(key, False);
        elif isinstance(key, list):
            k = key;
        else:
            print "The secret key must be a string or long integer array"

        if (len(k) > 4):
            print "The secret key cannot be more than 16 characters or 4 long values"
        elif (len(k) == 0):
            print "The secret key cannot be empty"
        elif (len(k) < 4):
            for i in range(len(k),4):
                k.append(0)
                #k[i] = 0;
        print k
        self._key = k;

    def encrypt(self,plaintext):

        if (self._key == None):
            print "Secret key is undefined"

        if isinstance(plaintext, basestring):
            return self._encryptString(plaintext)
        elif isinstance(plaintext, list):
            return self._encryptArray(plaintext)
        else:
            print "The plain text must be a string or long integer array"
        

    def decrypt(self,ciphertext):
        if (self._key == None):
            print "Secret key is undefined"

        if isinstance(ciphertext, basestring):
            return self._decryptString(ciphertext)
        elif isinstance(ciphertext, list):
            return self._decryptArray(ciphertext)
        else:
            print "The plain text must be a string or long integer array"

    def _encryptString(self,str):
        if (str == ''):
            return ''
        v = self._str2long(str, False);
        v = self._encryptArray(v);
        return self._long2str(v, False);

    def _encryptArray(self,v):

        n   = len(v) - 1;
        z   = v[n];
        y   = v[0];
        q   = math.floor(6 + 52 / (n + 1));
        sum = 0;
        while (0 < q):
            q-=1
    
            sum = self._int32(sum + CRYPT_XXTEA_DELTA);
            e   = sum >> 2 & 3;
            
            for p in range(0,len(p)):
                
                y  = v[p + 1];
                mx = self._int32(((z >> 5 & 0x07FFFFFF) ^ y << 2) + ((y >> 3 & 0x1FFFFFFF) ^ z << 4)) ^ self._int32((sum ^ y) + (self._key[p & 3 ^ e] ^ z));
                z  = v[p] = self._int32(v[p] + mx);

            y  = v[0];
            mx = self._int32(((z >> 5 & 0x07FFFFFF) ^ y << 2) + ((y >> 3 & 0x1FFFFFFF) ^ z << 4)) ^ self._int32((sum ^ y) + (self._key[p & 3 ^ e] ^ z));
            z  = v[n] = self._int32(v[n] + mx);
            
        return v;


    def _decryptString(self,str):
        if (str == ''):
            return '';
        v = self._str2long(str, False);
        v = self._decryptArray(v);
        return self._long2str(v, False);
        

    def _decryptArray(self,v):
        n   = len(v) - 1;
        z   = v[n];
        y   = v[0];
        q   = math.floor(6 + 52 / (n + 1));
        sum = self._int32(q * CRYPT_XXTEA_DELTA);
        while (sum != 0):
            e = sum >> 2 & 3;
            for p in range( n, 0, -1):
                
                z  = v[p - 1];
                mx = self._int32(((z >> 5 & 0x07FFFFFF) ^ y << 2) + ((y >> 3 & 0x1FFFFFFF) ^ z << 4)) ^ self._int32((sum ^ y) + (self._key[p & 3 ^ e] ^ z));
                y  = v[p] = self._int32(v[p] - mx);
                
            z   = v[n];
            mx  = self._int32(((z >> 5 & 0x07FFFFFF) ^ y << 2) + ((y >> 3 & 0x1FFFFFFF) ^ z << 4)) ^ self._int32((sum ^ y) + (self._key[p & 3 ^ e] ^ z));
            y   = v[0] = self._int32(v[0] - mx);
            sum = self._int32(sum - CRYPT_XXTEA_DELTA);
            
        return v;
        

    def _long2str(self,v, w):
     
        ln = len(v);
        s   = '';
        for i in range(0,ln):
            print v[i]
            s += struct.pack('<I', v[i]);
        if (w):
            return substr(s, 0, v[ln - 1]);
        else:
            return s;
        

    def _str2long(self,s, w):
        print 'aaaaaaaaaaaaaaa',len(s),s
        i=int(math.ceil((len(s)/4)))
        if (len(s)%4)>0 :
            i+=1
        print i
        #print  struct.unpack('<I',(s + ("\0" *( (4 - len(s) % 4) & 3))))
        v = list(struct.unpack('<'+str(i)+'I',(s + ("\0" *( (4 - len(s) % 4) & 3)))))
        print v
        if (w):
            v[0] = len(s); #prb
        return v;
        

    def _int32(self,n):
        while (n >= 2147483648):
            n -= 4294967296;
        while (n <= -2147483649):
            n += 4294967296;
        return int(n);
        
headers = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),( 'Connection','Keep-Alive')]
v=Crypt_XXTEA()
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


import time
# Retrieve channel id and primary key
timestamp = time.time();
player_id = '69T7MabZ47';
init = getUrl("http://tvplayer.playtv.fr/js/"+player_id+".js?_="+str(timestamp),headers=headers);
#print init
pat="b:(\{\"a.*\"})}"
init =re.compile(pat).findall(init)[0]
print init
init = json.loads(init);       
a =init['a'].decode("hex")#  struct.pack("<I",  a);
b = init['b'].decode("hex")
print a
print b

v.setKey("object");
params = json.loads(v.decrypt(b));
print param

