aaa=base64.b64decode('Qw1KSDguKGJBMEUcTVF3bCliVTRDFFFOa2R0IU8lTFZTV3RoYnwNNBhKXQw3ODUgRiVEA1tWLzM3PhN5RgkK')

min_js_string = getUrl('http://www.muchmovies.org/js/jquery.min.js', mobile=True).result

import jsunpackMM
sUnpacked = jsunpackMM.unpack(min_js_string,1,2) #2nd level encryption , encrypted 3 times	


variables=re.compile('d1\(atob\(.*?,(.*?),(.*?)\)').findall(sUnpacked)[0]

cf_var=variables[0].split('"')[1]
e_var=variables[1].split('"')[1]
cf_var=base64.b64decode(base64.b64decode(cf_var))
e_var=base64.b64decode(base64.b64decode(e_var))
print decryptMe(aaa, cf_var, e_var)	#movie link
