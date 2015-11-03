Now, you can execute python functions within regex, the format is $pyFunction.FileName.FunctionName

first parameter must be page_data, even if you dont need any page data


for example, if i want to add 2+4, i have created that function and stored in myFunctions.py file. this file should be copied in following directory which means with updates you wont lose your function file, please keep the backup of your files, just in case.
 \XBMC\userdata\addon_data\plugin.video.live.streams

def addme(page_data,a,b):
    return a+b



now, this function should be part of a regex, which then could be used anywhere, since we support regex in regex, you can pass any static of dynamic parameters.
if you need the page_data, it will also be available. the function call should result in proper python syntax.

sample call

<item>
<title>function test</title>
<link>http://$doregex[get-sum]</link>

<regex>
<name>get-sum</name>
<expres>$pyFunction:myFunctions.addme(page_data,2,4)</expres>
<page></page>
</regex>

</item>

Note, this will not run anything but if you look in the log file, 
CDVDPlayer::OpenInputStream - error opening [http://6]
which means it worked.

This will allow you to write python functions, like current date time in certain format, or do the calcualtion which otherwise is too difficult via web calls.


Another example, say if you want to call python functions, if those are simple functions then you can even call them directly, you dont have to write 
another regex or function for example

say i want to decode the base64 text, get the text via another regex (i am lazy so i hard coded it, you would want to get via dynamic regex)
but you can now write regex which contain static text, not Useful at all but useful when you have to use same big text many places.

Note that b64decode is not using page_data as parameter because it doesn't need to.


<item>
<title>function test2</title>
<link>http://$doregex[get-decode]</link>

<regex>
<name>get-decode</name>
<expres>$pyFunction:base64.b64decode("$doregex[get-enctext]")</expres>
<page></page>
</regex>

<regex>
<name>get-enctext</name>
<expres>cnRtcDovLzk1LjE0MS40My41MzoxNzM1L3JlZGlyZWN0Lz90b2tlbj1wbGF5QDE0MDI0NTUwNjIwNzQ1OQ==</expres>
<page></page>
</regex>


</item>




Also support in PAGE output of regex but not neccessary a page urls, for example,
here get-decrypted-rtmp returns a string not html page url


<regex>
<name>get-app</name>
<expres>1735\/(.*)</expres>
<page>$doregex[get-decrypted-rtmp]</page>
</regex>





External link to another file via URL
use externallink and point it to the url where the file is hosted, this supported both in Items and as well as Channels format.
For item, leave the link tag  with something dummy and enter the new tag with correct data, while in channels format there is no link.










