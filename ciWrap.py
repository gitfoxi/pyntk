#!/usr/bin/env python

"""
Implement library calls to MCD.

"""

import sys
from ctypes import *

import os
import os.path
try:
    t1_file = os.path.dirname(__file__) + "/t1.so"
    t1=CDLL(t1_file)
except:
    t1=CDLL("./t1.so")
  

# -----------------------------------------
# ----- tpi_c.h ---------------------------
# -----------------------------------------
HpInit=t1.HpInit
HpInit.restype=None

HpTerm=t1.HpTerm
HpTerm.restype=None

HpFwTask=t1.HpFwTask
HpFwTask.restype=None

HpInit()
import atexit
atexit.register( HpTerm )

debug=0

def fw(task,anslen=4096):
  """
  Run a firmware task and return the response.
  Default is to use a 4096-byte buffer. Make it bigger if you expect a big response.
  """
  if debug:
    print "fw:",task

  ctask = create_string_buffer(task+";\n")
  cans = create_string_buffer("\000"*anslen)
  canslen = c_long(anslen)
  ctasklen = c_long(len(ctask.value))
  cret = c_long(0)

  HpFwTask( byref(ctask), \
      byref(ctasklen), \
      byref(cans), \
      byref(canslen), \
      byref(cret))

  # Maybe there's a way to handle this by increasing the buffer size
  # and calling HpFwTask again for the rest of the result?
  if canslen.value == anslen:
    print >>sys.stderr , 'Given anslen buffer was too small'
    # Need better exception definition
    raise ValueError

  # Todo: Better error messages from "MCD errors" in 93k docs
  if cret.value == -2:
    raise ValueError
  if cret.value != 0:
    print "WARNING: FW command",task,"returned",cret.value
  return cans.value

REPEAT_MODES = { 'REPEAT_ONCE':0, \
    'REPEAT_ENDLESS':1, \
    'REPEAT_UNTIL_FAIL':2 };

def SetRepeatMode(mode):
  """
  Set repeat for running a function.
  mode: REPEAT_ONCE, REPEAT_ENDLESS, REPEAT_UNTIL_FAILED
  Will throw exception if invalid repeat mode is given.
  """
  SetRepeatMode = t1.SetRepeatMode
  SetRepeatMode.restype = None
  SetRepeatMode( REPEAT_MODES[mode] )

ERRORMAP_MODES = { \
    'CYCLE_ORIENTED':0, \
    'FAILURE_ORIENTED':1 }
def SetErrorMapMode(mode):
  """
  SetErrorMapMode( 'CYCLE_ORIENTED' | 'FAILURE_ORIENTED' )
  """
  SetErrorMapMode = t1.SetErrorMapMode
  SetErrorMapMode.restype = None
  SetErrorMapMode( ERRORMAP_MODES[mode] )

def SetReportMode( window=False, printer=False, file=None ):
  """
  SetReportMode( window=False, printer=False, file=None )
  file may be a string up to 14 characters.
  """
  cwindow = c_ubyte( window and 1 or 0 )
  cprinter = c_ubyte( printer and 1 or 0 )
  cfile = file and create_string_buffer( file ) or create_string_buffer("")
  SetReportMode = t1.SetReportMode
  SetReportMode.restype = None
  SetReportMode( cwindow, cprinter, cfile )

def GetOnlineMode():
  " GetOnlineMode -- returns True if tester is online; False if offline "
  f=t1.GetOnlineMode
  f.restype = None
  cmode = c_long(0)
  f( byref(cmode) )
  mode = cmode.value
  if mode == 1   : return True 
  elif mode == 0 : return False 
  else:
    print >>sys.stderr, "GetOnlineMode returned: ",mode
    raise ValueError

# -----------------------------------------------
# ----------- libcicpi.h ------------------------
# -----------------------------------------------

def GetUserFlag( name, site=None ):
  """ 
  GetUserFlag( name, site=None )
  If site==None, return the flag for the site in focus
  Otherwise return the flag for site numbered from 1,2,3,4,...
  """
  if site is None:
    f=t1.GetUserFlag
  else:
    f=t1.GetUserFlagOfSite
  f.restype = c_long
  cvalue = c_long(0)
  if site is None:
    res=f( create_string_buffer( name ), byref(cvalue) )
  else:
    res=f( create_string_buffer( name ), c_long(site), byref(cvalue) )
  # Todo: should support name/type error when res=1 and internal error 
  #  when res=-1
  if res != 0 :
    raise ValueError

  return cvalue.value
    
def GetUserDouble( name, site=None ):
  """ 
  GetUserDouble( name, site=None )
  If site==None, return the Double for the site in focus
  Otherwise return the Double for site numbered from 1,2,3,4,...
  """
  if site is None:
    f=t1.GetUserDouble
  else:
    f=t1.GetUserDoubleOfSite
  f.restype = c_long
  cvalue = c_double(0.0)
  if site is None:
    res=f( create_string_buffer( name ), byref(cvalue) )
  else:
    res=f( create_string_buffer( name ), c_long(site), byref(cvalue) )
  # Todo: should support name/type error when res=1 and internal error 
  #  when res=-1
  if res != 0 :
    raise ValueError

  return cvalue.value
    
MAX_USER_STRING_LEN = 256 
def GetUserString ( name, site=None ):
  """ 
  GetUserString( name, site=None )
  If site==None, return the String for the site in focus
  Otherwise return the String for site numbered from 1,2,3,4,...
  """
  if site is None:
    f=t1.GetUserString
  else:
    f=t1.GetUserStringOfSite
  f.restype = c_long
  cvalue = create_string_buffer( "\000"*(MAX_USER_STRING_LEN + 1))
  if site is None:
    res=f( create_string_buffer( name ), byref(cvalue) )
  else:
    res=f( create_string_buffer( name ), c_long(site), byref(cvalue) )
  # Todo: should support name/type error when res=1 and internal error 
  #  when res=-1
  if res != 0 :
    raise ValueError

  return cvalue.value

USER_VAR_TYPES = { 0:'Flag', \
    1:'Double', \
    2:'String' }

def GetUser( name, site=None ):
  """
  Get a user flag, double or string
  If site==None, return the value for the site in focus
  Otherwise return the value for site numbered from 1,2,3,4,...
  """

  gettype = t1.GetUserType
  gettype.restype = c_long
  ct = c_long(0)
  res = gettype( create_string_buffer( name ), byref(ct))
  if res != 0 :
    raise ValueError
  fname = ''.join([ 'GetUser', USER_VAR_TYPES[ ct.value ] ])
  return globals()[ fname ]( name, site )

# I don't have to write all the different SetUser functions like I
# did with GetUser because now I realize the power of the Python.
def SetUser( name, value, site=None ):
  """
  Set a user flag, double or string
  If site==None, set the value for the site in focus
  Otherwise set the value for site numbered from 1,2,3,4,...
  """

  gettype = t1.GetUserType
  gettype.restype = c_long
  ct = c_long(0)
  res = gettype( create_string_buffer( name ), byref(ct))
  if res != 0 :
    raise ValueError
  fname = ''.join([ 'SetUser', USER_VAR_TYPES[ ct.value ], \
      site and 'OfSite' or '' ])
  f = getattr(t1,fname)
  cname = create_string_buffer(name)
  vartype = USER_VAR_TYPES[ct.value]
  if vartype == 'String':
    cvalue = create_string_buffer( value )
  elif vartype == 'Double':
    cvalue = c_double( value )
  elif vartype == 'Flag':
    cvalue = c_long( value )
  else:
    print >>sys.stderr, 'Error: GetType returned int: ',ct.value
    raise ValueError

  if site:
    res = f( cname, c_long(site), cvalue )
  else:
    res = f( cname, cvalue )
  if res != 0 :
    raise ValueError

def GetDiePosXY( site=None ):
  " (x,y) = GetDiePosXY( site=None ) "
  if site:
    f=t1.GetDiePosXYOfSite
  else:
    f=t1.GetDiePosXY
  f.restype = c_long
  cx = c_long(0)
  cy = c_long(0)
  if site:
    res = f(byref(x),byref(y))
  else:
    res = f(c_long(site),byref(x),byref(y))
  if res != 0 :
    raise ValueError
  return ( cx.value, cy.value )

def GetTemperature():
  " temperature = GetTemperature "
  f=t1.GetTemperature
  f.restype = c_long
  ctemperature = c_long(0)
  res = f( byref(ctemperature) )
  if res != 0 :
    raise ValueError
  return ctemperature.value

def GetPackageId( site=None):
  " id = GetPackageId( site=None ) "
  if site:
    f=t1.GetPackageIdOfSite
  else:
    f=t1.GetPackageId
  f.restype = c_long
  cid = c_long(0)
  if site:
    res = f( c_long(site), byref(cid) )
  else:
    res = f( byref(cid) )
  if res != 0 :
    raise ValueError
  return cid.value

def SetPackageId( id, site=None ):
  " SetPackageId( id, site=None ) "
  if site:
    f=t1.SetPackageIdOfSite
  else:
    f=t1.SetPackageId
  f.restype = c_long
  if site:
    res = f( c_long(site), byref(c_long(id)) )
  else:
    res = f( byref(c_long(id)) )
  if res != 0 :
    raise ValueError

MAX_PATH_LEN = 1027
def GetResultFile( level_name ):
  """
  result_filename = GetResultFile( level_name )

  return the file that is being used to log results for level 'level_name'
  """
  f=t1.GetResultFile
  f.restype = c_long
  cvalue = create_string_buffer( "\000"*(MAX_PATH_LEN+1))
  res = f( create_string_buffer( level_name ), cvalue )
  if res != 0 :
    raise ValueError
  return cvalue.value

def GetWaferDescriptionFile():
  """
  wafer_filename = GetWaferDescriptionFile()

  return the file that generates x and y coordinates for this wafer
  """
  f=t1.GetWaferDescriptionFile
  f.restype = c_long
  cvalue = create_string_buffer( "\000"*(MAX_PATH_LEN+1))
  res = f( cvalue )
  if res != 0 :
    raise ValueError
  return cvalue.value

def DisableErrorMessages():
  " Disable CPI error messages "
  f1=t1.DisableErrorMessages
  f.restype = c_long
  res = f()
  if res != 0 :
    raise ValueError

def EnableErrorMessages():
  " Enable CPI error messages "
  f=t1.EnableErrorMessages
  f.restype = c_long
  res = f()
  if res != 0 :
    raise ValueError

USER_MODES = { \
    'CONSOLE':1, \
    'OPERATING':2, \
    'SUPERVISING':3, \
    'ENGINEERING':4, \
    'PROTECTED':5, \
    1:'CONSOLE', \
    2:'OPERATING', \
    3:'SUPERVISING', \
    4:'ENGINEERING', \
    5:'PROTECTED', \
    }

def GetUserMode():
  """ mode = GetUserMode() 
  mode may be: CONSOLE, OPERATING, SUPERVISING, ENGINEERING, PROTECTED
  mode is a string
  """
  f=t1.GetUserMode
  f.restype = c_long
  cmode = c_long(0)
  res = f(byref(cmode))
  if res != 0:
    raise ValueError
  return USER_MODES[cmode.value]

def SetUserMode():
  """ SetUserMode( mode ) 
  mode may be: CONSOLE, OPERATING, SUPERVISING, ENGINEERING, PROTECTED
  mode is a string
  """
  f=t1.SetUserMode
  f.restype = c_long
  cmode = c_long( USER_MODES[mode] )
  res = f(cmode)
  if res != 0:
    raise ValueError

def SetOcIdleMsg( line1="", line2="" ):
  """ SetOcIdleMsg( line1="", line2="" )
  Sets message to display in Operator console.
  Only the first 20 characters of line 1 and 19 characters of line2 displayed.
  """
  f=t1.SetOcIdleMsg
  f.restype = c_long
  res = f( create_string_buffer(line1), create_string_buffer(line2) )
  if res != 0:
    raise ValueError

def ExecTestFlow( Sync=False, Mode=None):
  """
  ExecTestFlow( Sync=False, Mode=None)

  If Sync is true, wait until testflow completes before returning.
  Mode may be 'IMPORT' or 'STORE' -- which has something to do with
  hardware response data that I don't really understand.
  """
  if mode not in [None,'IMPORT','STORE']:
    raise ValueError
  func = ''.join(['ExecTestFlow', \
      Mode and Mode or '', \
      Sync and 'Sync' or '' ])
  f=getattr(t1,func)
  f.restype=c_long
  res = f()
  if res:
    # Test flow busy
    print >>sys.stderr, "Test flow is busy."
    raise BusyError

def ExecTestProgram( Sync=False, Mode=None):
  """
  ExecTestProgram( Sync=False, Mode=None)

  If Sync is true, wait until testprogram completes before returning.
  Mode may be 'IMPORT' or 'STORE' -- which has something to do with
  hardware response data that I don't really understand.
  """
  if mode not in [None,'IMPORT','STORE']:
    raise ValueError
  func = ''.join(['ExecTestProgram', \
      Mode and Mode or '', \
      Sync and 'Sync' or '' ])
  f=getattr(t1,func)
  f.restype=c_long
  res = f()
  if res:
    # Test program busy
    print >>sys.stderr, "Test flow is busy."
    raise BusyError

def GetWaferDimensions():
  """
  (minX, maxX, minY, maxY, quadrant, orientation) = \
    GetWaferDimensions()
  quadrant 1 is upper right, quadrant 2 is upper left, etc
  orientation is a bit of a mystery. It is supposed to be the "angle
  of the flatted wafer side" with angle 0 being the bottom, but I'm
  not sure what other values it might take on ...
  """
  cminX = c_long(0)
  cmaxX = c_long(0)
  cminY = c_long(0)
  cmaxX = c_long(0)
  cquadrant = c_long(0)
  corientation = c_long(0)

  f=t1.GetWaferDimensions
  f.restype = c_long
  res = f( byref(cminX), byref(cmaxX), byref(cminY), byref(cmaxY),\
      byref(cquadrant),byref(corientation ))
  if res:
    # Error occured
    raise ValueError
  return ( cminX.value, cmaxX.value, cminY.value, cmaxY.value, \
      cquadrant.value, corientation.value )

def SetWaferDimensions( minX, maxX, minY, maxY, quadrant, orientation):
  """
  SetWaferDimensions
  (minX, maxX, minY, maxY, quadrant, orientation)

  quadrant 1 is upper right, quadrant 2 is upper left, etc
  orientation is a bit of a mystery. It is supposed to be the "angle
  of the flatted wafer side" with angle 0 being the bottom, but I'm
  not sure what other values it might take on ...
  """
  f=t1.SetWaferDimensions
  f.restype = c_long
  res = f( c_long(minX), c_long(maxX), c_long(minY), c_long(maxY),\
      c_long(quadrant),c_long(orientation ))
  if res:
    # Error occured
    raise ValueError

MAX_TESTSUITE_LEN = 256
def GetTestsuiteName():
  """ testsuite = GetTestsuiteName() 
  testsuite is the one containing the user procedure that called me.
  """
  cname = create_string_buffer( "\000" * MAX_TESTSUITE_LEN )
  f=t1.GetTestsuiteName( byref(cname) )
  if res:
    raise ValueError
  return cname.value

def IsFirstInvokation():
  " True if this is the first site for which this suite is being called "
  f=t1.IsFirstInvokation
  f.restype=c_long
  cis_first = c_long(0)
  res = f( byref( cis_first ))
  if res:
    raise ValueError
  return cis_first.value and True or False

MAX_SITES = 128
def GetSitesToBeTested():
  """ sites = GetSitesToBeTested()
  sites is an array like [1,2,3,4,5,6] listing the sites to be tested
  by this call. The list is pre-sorted from lowest to highest
  """
  csites_array = (c_long*(MAX_SITES+1))()
  f=t1.GetSitesToBeTested
  f.restype = c_long
  res = f( byref( csites_array ) )
  if res:
    raise ValueError
  return filter(None,csites_array)

def Override( thing, filename ):
  """
  Override( thing, filename )
  Sets a new file to be loaded to override thing where thing is a string:
    PinConfiguration
    Levels
    Timing
    Vectors
    PinAttributes
    ChAttributes
    AnalogControl
    Waveform
    Routing
  Supposedly this function will never fail, but I have the standard
  exception code in there in case it does.
  """
  func = 'Override' + thing
  f=getattr(t1,func)
  f.restype = c_long
  res = f()
  if res:
    raise ValueError

TEST_TYPES = { 
    -1:"NoTest", 
    0:"UserProcedure", 
    1: "comment",
    2: "connect",
    3: "continuity",
    4: "disconnect",
    5: "download",
    6: "dps_connectivity",
    7: "dps_status",
    8: "dvm",
    9: "frequency",
    10: "functional",
    11: "fw_escape",
    12: "general_pmu",
    13: "get_utility_lines",
    14: "global_search",
    15: "global_search_track",
    16: "golden_device",
    17: "header",
    18: "high_z",
    19: "hold_time",
    20: "hp_ux_escape",
    21: "iddq",
    22: "inp_volt_sensitivity",
    23: "jitter",
    24: "leakage",
    25: "lock",
    26: "memory_analysis",
    27: "operating_current",
    28: "out_volt_sensitivity",
    29: "output_dc",
    30: "param_functional",
    31: "production_iddq",
    32: "propagation_delay",
    33: "redundancy_repair",
    34: "set_spec_value",
    35: "set_utility_lines",
    36: "setup_time",
    37: "shmoo_2d_track",
    38: "shmoo_2d",
    39: "shmoo_spec",
    40: "spec_search",
    41: "standby_current",
    42: "start_sequencer",
    43: "temperature",
    44: "Test_state",
    45: "unlock",
    46: "upload",
    47: "adc_capture",
    48: "adc_distortion",
    49: "adc_linearity",
    50: "analog_connect",
    51: "buffer_capture",
    52: "buffer_dist",
    53: "crosstalk",
    54: "dac_capture",
    55: "dac_distortion",
    56: "dac_linearity",
    57: "generic_TF",
    58: "analog_continuity",
    59: "time_analysis",
    60: "adc_tue_linearity",
    61: "soc_adc_linearity",
    62: "soc_adc_distortion",
    63: "soc_dac_linearity",
    64: "soc_dac_distortion",
    65: "TestMethod",
    66: "eyediagram",
    67: "hscrosstalk",
    68: "rxfunct",
    69: "rxjittol",
    70: "txfunct",
    71: "txjitgen",
    72: "txjitgen",
    73: "txjitgen",
    }

class TestsuiteDescriptor:
  def __init__(self,name,flags,ffc_count,test_type):
    self.name = name
    self.flags = flags
    self.ffc_count = ffc_count
    self.test_type = test_type

def GetModelfileString ( name ):
  """ 
  GetModelfileString( name )

  Raises ValueError if the string is not available (Ap model not running)
  """
  f=t1.GetModelfileString
  f.restype = c_long
  cvalue = create_string_buffer( "\000"*(MAX_USER_STRING_LEN + 1))
  res=f( create_string_buffer( name ), byref(cvalue) )
  # Todo: should support name/type error when res=1 and internal error 
  #  when res=-1
  if res != 0 :
    raise ValueError

  return cvalue.value

  

if __name__ == "__main__":
#  HpInit()
  print fw("ftst?;")
  try:
    print fw("rlyc? (@);",50)
  except:
    # expect exception
    pass
  else:
    print >>sys.stderr, "Ouch rlyc should have choked."
  SetRepeatMode('REPEAT_ONCE')
  try:
    SetRepeatMode('REPEAT_BLABLA')
  except:
    pass
  else:
    print >>sys.stderr, "Ouch repeatmode should have choked."

#  HpTerm()
