import traceback,sys
def addme(page_data,a,b):
    return a+b

def call_site(Cookie_Jar,url_to_call):
    try:
        import urllib2
        import base64
        import uuid
        req = urllib2.Request(url_to_call)

        str_guid=str(uuid.uuid1()).upper()
        str_guid=base64.b64encode(str_guid)
        req.add_header('Connection', 'Upgrade')
        req.add_header('Upgrade', 'websocket')

        req.add_header('Sec-WebSocket-Key', str_guid)
        req.add_header('Origin','http://www.streamafrik.com')
        req.add_header('Pragma','no-cache')
        req.add_header('Cache-Control','no-cache')
        req.add_header('Sec-WebSocket-Version', '13')
        req.add_header('Sec-WebSocket-Extensions', 'permessage-deflate; client_max_window_bits, x-webkit-deflate-frame')
        req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53')
        cookie_handler = urllib2.HTTPCookieProcessor(Cookie_Jar)
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
        opener = urllib2.install_opener(opener)
        from keepalive import HTTPHandler
        keepalive_handler = HTTPHandler()
        opener = urllib2.build_opener(keepalive_handler)
        urllib2.install_opener(opener)
        urllib2.urlopen(req)
        response.close()
        return ''
    except: traceback.print_exc(file=sys.stdout)
    return ''