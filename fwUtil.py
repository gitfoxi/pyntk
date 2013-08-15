
import t1
import re

debug=0
debug_charlimit = 80

# todo: exception on command failure
def fw(task):
  ans = t1.fw(task)

  if debug:
    print "TASK:\t" + task[0:debug_charlimit]
    print "ANS:\t" + ans[0:debug_charlimit]

  return ans

def connect():
  fw("sqst off;rlyc cnct,off,(@);psst on;cnct on,(@);sqst brk;sqgb acff,0;")

def disconnect():
  fw("cnct off,(@);psst off;rlyc idle,off,(@);sqst brk;sqst off")

def srec_act(pins):
    fw("srec x,(@)")
    fw("srec act,(" + pins + ")")

def set_label(label):
    fw("sqsl '"+label+"'")

class ntk_save:
  def __init__(self):
    self.srestore = fw(self.query)
  def restore(self):
    fw(self.srestore)

class srec_save( ntk_save ):
    query = "srec? (@)"

class term_save( ntk_save ):
    query = "term? prm,(@)"

class etds_save( ntk_save):
    query = "etds? prm,prm,,(@)"

class drlv_save( ntk_save):
    query = "drlv? prm,(@)"

class sqsl_save( ntk_save):
    query = "sqsl?"

class uptd_save( ntk_save):
    query = "uptd? ALL"

def ntk_get_result(ans,field):
  s1 =  re.findall('^(\S+)\s+(\S.*)',ans)
  s=[s1[0][0]]
  s.extend( re.findall('("[^"]*"|\([^\)]*\)|[^"(),\s]*)(?:\s*[,]|\s*$)' ,s1[0][1]) )
  if len(s) < field:
    raise ValueError
  return s[field]

class ts_result:
  found = 0
  spec = "noTest"
  passVal = 0
  failVal = 0
  allFail = 0
  allPass = 0
  def __init__(self):
    self.found=0
    self.spec="noTest"
    self.passVal=0
    self.failVal=0
    self.allFail=0
    self.allPass=0

def tim_search(edge="r1",pin_list="@",a=0,b=10,lin_step=0.1,bin_res=0.01,
               method="L"):
  fw("edsp prm,prm,\"" + edge + "\",,,,(" + pin_list + ")")
  fw("esgb " + str(lin_step) + "," + str(bin_res) + ",")
  ans = fw("ttrs? " + str(a) + "," + str(b) + "," + method + ",("
           + pin_list+ ")");
  r = ts_result()
  value_spec = ntk_get_result(ans,1)
  if value_spec == "EQ":
    r.found=1
    r.spec= "found"
    r.passVal = float(ntk_get_result(ans,2))
    r.failVal = float(ntk_get_result(ans,3))
  elif value_spec == "LT" or value_spec == "GT":
    r.found = 0
    r.spec = "allFail"
    r.allFail = 1
  elif value_spec == "LE" or value_spec == "GE":
    r.found=0
    r.spec = "allPass"
    r.allPass = 1
  else:
    r.found = 0
    r.spec = "errNoTest"

  return r
  

class center_timing:
  def __init__(self):
    self.a = -1
    self.b = 1
    self.lin_step = 0.1
    self.bin_res = 0.01
    self.result_pins = "@"
    self.found = 0
  def go(self):
    self.high = max(self.a,self.b)
    self.low = min(self.a,self.b)

    connect()

    sr = srec_save() 

    srec_act(self.result_pins)

    found = 0
    left_start = self.a
    while( not(found) ):


      left = tim_search(pin_list=self.result_pins,
                        a=left_start, b=self.b, method="LB",
                        lin_step = self.lin_step,
                        bin_res = self.bin_res)
      if not(left.found):
        print "Error:  Left search failed with code \"" + left.spec + "\""
        raise RuntimeError
      if left.passVal > left.failVal:
        found = 1
      else:
        left_start = left.passVal + lin_step
        if left_start > self.b:
          print "Error: Left search found only pass-left region"
          raise RuntimeError
        
      

    right = tim_search(pin_list=self.result_pins,
                       a=self.b, b=self.a, method="LB",
                       lin_step = self.lin_step,
                       bin_res = self.bin_res)

    if not(right.found):
      print "Error:  Right search failed with code \"" + right.spec + "\""
      raise RuntimeError
    if( right.passVal > right.failVal ):
      print "Error: Right search found pass-region < lin_step"
      raise RuntimeError

    center = (left.passVal + right.passVal)/2

    print "Left\tRight\tCenter"
    print str(left.passVal) + "\t" + str(right.passVal) + "\t" + str(center)

    self.found = 1;
    self.left = left.passVal
    self.right = right.passVal
    self.center = center

    ## cleanup
    sr.restore()
  def set_edge(self,val=-1000):
    if( not(self.found) ):
      print "Error: center_time.set_edge can't work until go() runs"
      raise RuntimeError
    if val == -1000:
      val = self.center
    fw('etds prm,prm,,"r1:' + str(val) +'",(' + self.result_pins + ')')

def lin_search(start,stop,step,function,arg_dict={},start_test="none"):
  """Perform a linear search using an arbitrary pass-fail function

  start_test  -  may be 'pass', 'fail' or 'none'
                 sets expectation test at 'start' point
  """
  x=start

  if( not( start_test == "none" )):
    pf = function(x,**arg_dict)
    if( not(pf) and start_test == "pass" ):
      print "Error: lin_search expected starting point to pass but it failed"
      raise RuntimeError
    elif( pf and start_test == "fail"):
      print "Error: lin_search expected starting point to fail but it passed"
      raise RuntimeError
  
  while 1:
    if( function(x,**arg_dict) != pf ):
      if pf:
        return x-step
      else:
        return x
    x+=step
    if x > stop:
      print "Error: lin_search found no transition"
      raise RuntimeError

def lin_search_range(start,stop,step,function,arg_dict={}):
  left = lin_search(start,stop,step,function,arg_dict,start_test="fail")
  right = lin_search(left+step,stop,step,function,arg_dict,start_test="pass")
  return [left,right]

def bin_search(pass_val,fail_val,res,function,arg_dict={},safe=1):
  """Perform a binary search using an arbitrary pass-fail function
  """
  if safe:
    if( not(function(pass_val,**arg_dict)) ):
      print "Error: bin_search: pass_val ",pass_val," fails"
      raise RuntimeError
    if( function(fail_val,**arg_dict) ):
      print "Error: bin_search: fail_val ",fail_val," passes"
      raise RuntimeError

  while 1:
    x = (pass_val + fail_val)/2
    if( function(x,**arg_dict) ):
      pass_val = x
    else:
      fail_val = x
    if( abs(pass_val - fail_val) < res ):
      return pass_val

def linbin_search_range(start,stop,step,res,function,arg_dict={}):
  [left_lin,right_lin] = lin_search_range(start,stop,step,function,
                                          arg_dict)

  left = bin_search(left_lin, left_lin - step,
                    res, function, arg_dict)
  right = bin_search(right_lin, right_lin + step,
                     res, function, arg_dict)

  return [left,right]

def lin_search_closed_range(start,stop,step,function,arg_dict={}):
  if function( start, **arg_dict ):  # starting point passes
    start = lin_search(start,stop,step,function,arg_dict,start_test="pass") + step
  left = lin_search(start,stop,step,function,arg_dict,start_test="fail")
  right = lin_search(left+step,stop,step,function,arg_dict,start_test="pass")
  return [left,right]


def linbin_search_closed_range(start,stop,step,res,function,arg_dict={}):
  [left_lin,right_lin] = lin_search_closed_range(start,stop,step,function,
                                                 arg_dict)

  left = bin_search(left_lin, left_lin - step,
                    res, function, arg_dict)
  right = bin_search(right_lin, right_lin + step,
                     res, function, arg_dict)

  return [left,right]

def spec_center(spec,tim_or_lev="TIM",low=-2,high=2,lin_step=0.5,bin_res=0.01):
  def set_spec_ftst(value,spec):
    fw("SVLR " + tim_or_lev + ',prm,,"' + spec + '",' + `value`)
    return fw("FTST?") == "FTST P\n"

  [left,right] = linbin_search_closed_range( low, high, lin_step, bin_res,
                                             set_spec_ftst, {'spec':spec})
  center = (left+right)/2
  print "left\tright\tcenter"
  print `left`,`right`,`center`
  if not ( set_spec_ftst( center, spec ) ):
    raise RuntimeError

def set_termination(term,vth,term_mode,r_pins,d_pins):
  term_mode = term_mode.upper()
  if term_mode == "X":
    term_str = ""
    vth_str = ""
  else:
    term_str = str(term*1000)
    vth_str = str(vth*1000)    
  fw("TERM prm," + term_mode + ","+term_str+","+vth_str+",,,,("+ r_pins +")")
  fw("drlv prm,"+(str(term*1000)+",")*2+"("+d_pins+")")  



def set_r1_ftst(r1,pins):
  fw('etds prm,prm,,"r1:'+str(r1)
     + ' r2:'+str(r1)
     + ' r3:'+str(r1)
     + ' r4:'+str(r1)
     + '",('+pins+')')
  ans=fw('FTST?')
  return ans == "FTST P\n"

class center_timing_b( center_timing ):
  def go(self):
    self.high = max(self.a,self.b)
    self.low = min(self.a,self.b)

    connect()

    sr = srec_save() 

    srec_act(self.result_pins)

    found = 0

    [left,right] = linbin_search_range(start=self.low,
                                       stop=self.high,
                                       step=self.lin_step,
                                       res=self.bin_res,
                                       function=set_r1_ftst,
                                       arg_dict={"pins":self.result_pins} )

    center = (left + right)/2

    print "Left\tRight\tCenter"
    print str(left) + "\t" + str(right) + "\t" + str(center)

    self.found = 1;
    self.left = left
    self.right = right
    self.center = center

    ## cleanup
    sr.restore()
    

def stop_at_vec( vec ):
    fw("sqgb stsv," + str(vec))
    fw("ftst?")

def reset_sequencer():
  fw("sqgb acff,0")

def DC_center_threshold( pins, vec ):
  connect()
  us = uptd_save()
  stop_at_vec( vec )
  pinstr = ','.join(pins)
  slev = fw("DFVM 1,0.100000000,0.100000000,5000.000000000,-1000.000000000,1000.000000000,,,0.000000000,SPNS,(" + pinstr + ");PTST? 1,,,PVAL")
  slevL = slev.splitlines()
  levN = []
  for i in slevL:
    levN.append( float( ntk_get_result(i,3)) )

  vcom = (max(levN) + min(levN))/2
  vcom_str = str(vcom)

  fw("RCLV PRM," + vcom_str + "," + vcom_str + ",(" + pinstr + ")")
  print 'Vcom for ' + pinstr + " = " + vcom_str
  reset_sequencer()
  us.restore()
