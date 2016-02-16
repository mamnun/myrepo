import re
def tr(param1 , param2 , param3):
    _loc4_ = 0;
    _loc5_= "";
    _loc6_ = None
    if( ord(param1[- 2]) == param2 and ord(param1[2]) == param3):
        _loc5_ = "";
        _loc4_ = len(param1)- 1;
        while(_loc4_ >= 0):
            _loc5_ = _loc5_ + param1[_loc4_]
            _loc4_-=1;
        param1 = _loc5_;
        _loc6_ = int(param1[-2:]);
        print 'xx',_loc6_
        param1 = param1[2:];
        param1 = param1[0:-3];
        _loc6_ = _loc6_ / 2;
        if(_loc6_ < len(param1)):
            _loc4_ = _loc6_;
        while(_loc4_ < len(param1)):
            param1 = param1[0:_loc4_]+ param1[_loc4_ + 1:]
            _loc4_ = _loc4_ + _loc6_ * 1;

        param1 = param1 + "!";

    return param1;

def swapme(st, fromstr , tostr):
    st=st.replace(tostr,"___")
    st=st.replace(fromstr,tostr)
    st=st.replace("___", fromstr)
    return st

     
def decode(encstring):
    encstring=tr(encstring ,114,65)
    mc_from="MD7cXIZxt5B61RHbN8dovGzW3C"
    mc_to="myilk4UpJfYLgn0u9eQwsVaT2="
    if 1==2:#encstring.endswith("!"):
        encstring=encstring[:-1]
        mc_from="ngU08IuldVHosTmZz9kYL2bayE"
        mc_to="v7ec41D6GpBtXx3QJRiN5WwMf="

    st=encstring
    for i in range(0,len(mc_from)):
        st=swapme(st, mc_from[i], mc_to[i])
    print st
    return st.decode("base64")
    
