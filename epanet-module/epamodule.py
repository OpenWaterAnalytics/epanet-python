"""Python EpanetToolkit interface

added function ENsimtime"""


import ctypes
import platform
import datetime

_plat= platform.system()
if _plat=='Linux':
  _lib = ctypes.CDLL("libepanet2.so.2")
elif _plat=='Windows':
  try:
    # if epanet2.dll compiled with __cdecl (as in OpenWaterAnalytics)
    _lib = ctypes.CDLL("epamodule\epanet2.dll")
    _lib.ENgetversion(ctypes.byref(ctypes.c_int()))
  except ValueError:
     # if epanet2.dll compiled with __stdcall (as in EPA original DLL)
     try:
       _lib = ctypes.windll.epanet2
       _lib.ENgetversion(ctypes.byref(ctypes.c_int()))
     except ValueError:
       raise Exception("epanet2.dll not suitable")

else:
  Exception('Platform '+ _plat +' unsupported (not yet)')


_current_simulation_time=  ctypes.c_long()

_max_label_len= 32
_err_max_char= 80
  




def ENepanet(nomeinp, nomerpt='', nomebin='', vfunc=None):
    """Runs a complete EPANET simulation.

    Arguments:
    nomeinp: name of the input file
    nomerpt: name of an output report file
    nomebin: name of an optional binary output file
    vfunc  : pointer to a user-supplied function which accepts a character string as its argument."""  
    if vfunc is not None:
        CFUNC = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_char_p)
        callback= CFUNC(vfunc)
    else:
        callback= None
    ierr= _lib.ENepanet(ctypes.c_char_p(nomeinp.encode()), 
                        ctypes.c_char_p(nomerpt.encode()), 
                        ctypes.c_char_p(nomebin.encode()), 
                        callback)
    if ierr!=0: raise ENtoolkitError(ierr)


def ENopen(nomeinp, nomerpt='', nomebin=''):
    """Opens the Toolkit to analyze a particular distribution system

    Arguments:
    nomeinp: name of the input file
    nomerpt: name of an output report file
    nomebin: name of an optional binary output file
    """
    ierr= _lib.ENopen(ctypes.c_char_p(nomeinp.encode()), 
                      ctypes.c_char_p(nomerpt.encode()), 
                      ctypes.c_char_p(nomebin.encode()))
    if ierr!=0: 
      raise ENtoolkitError(ierr)


def ENclose():
  """Closes down the Toolkit system (including all files being processed)"""
  ierr= _lib.ENclose()
  if ierr!=0: raise ENtoolkitError(ierr)


def ENgetnodeindex(nodeid):
    """Retrieves the index of a node with a specified ID.

    Arguments:
    nodeid: node ID label"""
    j= ctypes.c_int()
    ierr= _lib.ENgetnodeindex(ctypes.c_char_p(nodeid.encode()), ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetnodeid(index):
    """Retrieves the ID label of a node with a specified index.

    Arguments:
    index: node index"""    
    label = ctypes.create_string_buffer(_max_label_len)
    ierr= _lib.ENgetnodeid(index, ctypes.byref(label))
    if ierr!=0: raise ENtoolkitError(ierr)
    return label.value


def ENgetnodetype(index):
    """Retrieves the node-type code for a specific node.

    Arguments:
    index: node index"""
    j= ctypes.c_int()
    ierr= _lib.ENgetnodetype(index, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetnodevalue(index, paramcode):
    """Retrieves the value of a specific node parameter.

    Arguments:
    index:     node index
    paramcode: Node parameter codes consist of the following constants:
                  EN_ELEVATION  Elevation
                  EN_BASEDEMAND ** Base demand
                  EN_PATTERN    ** Demand pattern index
                  EN_EMITTER    Emitter coeff.
                  EN_INITQUAL   Initial quality
                  EN_SOURCEQUAL Source quality
                  EN_SOURCEPAT  Source pattern index
                  EN_SOURCETYPE Source type (See note below)
                  EN_TANKLEVEL  Initial water level in tank
                  EN_DEMAND     * Actual demand
                  EN_HEAD       * Hydraulic head
                  EN_PRESSURE   * Pressure
                  EN_QUALITY    * Actual quality
                  EN_SOURCEMASS * Mass flow rate per minute of a chemical source
                    * computed values)
                   ** primary demand category is last on demand list

               The following parameter codes apply only to storage tank nodes:
                  EN_INITVOLUME  Initial water volume
                  EN_MIXMODEL    Mixing model code (see below)
                  EN_MIXZONEVOL  Inlet/Outlet zone volume in a 2-compartment tank
                  EN_TANKDIAM    Tank diameter
                  EN_MINVOLUME   Minimum water volume
                  EN_VOLCURVE    Index of volume versus depth curve (0 if none assigned)
                  EN_MINLEVEL    Minimum water level
                  EN_MAXLEVEL    Maximum water level
                  EN_MIXFRACTION Fraction of total volume occupied by the inlet/outlet zone in a 2-compartment tank
                  EN_TANK_KBULK  Bulk reaction rate coefficient"""
    j= ctypes.c_float()
    ierr= _lib.ENgetnodevalue(index, paramcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


##------
def ENgetlinkindex(linkid):
    """Retrieves the index of a link with a specified ID.

    Arguments:
    linkid: link ID label"""
    j= ctypes.c_int()
    ierr= _lib.ENgetlinkindex(ctypes.c_char_p(linkid.encode()), ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetlinkid(index):
    """Retrieves the ID label of a link with a specified index.

    Arguments:
    index: link index"""
    label = ctypes.create_string_buffer(_max_label_len)
    ierr= _lib.ENgetlinkid(index, ctypes.byref(label))
    if ierr!=0: raise ENtoolkitError(ierr)
    return label.value


def ENgetlinktype(index):
    """Retrieves the link-type code for a specific link.

    Arguments:
    index: link index"""
    j= ctypes.c_int()
    ierr= _lib.ENgetlinktype(index, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetlinknodes(index):
    """Retrieves the indexes of the end nodes of a specified link.

    Arguments:
    index: link index"""
    j1= ctypes.c_int()
    j2= ctypes.c_int()
    ierr= _lib.ENgetlinknodes(index,ctypes.byref(j1),ctypes.byref(j2))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j1.value,j2.value

def ENgetlinkvalue(index, paramcode):
    """Retrieves the value of a specific link parameter.

    Arguments:
    index:     link index
    paramcode: Link parameter codes consist of the following constants:
                 EN_DIAMETER     Diameter
                 EN_LENGTH       Length
                 EN_ROUGHNESS    Roughness coeff.
                 EN_MINORLOSS    Minor loss coeff.
                 EN_INITSTATUS   Initial link status (0 = closed, 1 = open)
                 EN_INITSETTING  Roughness for pipes, initial speed for pumps, initial setting for valves
                 EN_KBULK        Bulk reaction coeff.
                 EN_KWALL        Wall reaction coeff.
                 EN_FLOW         * Flow rate
                 EN_VELOCITY     * Flow velocity
                 EN_HEADLOSS     * Head loss
                 EN_STATUS       * Actual link status (0 = closed, 1 = open)
                 EN_SETTING      * Roughness for pipes, actual speed for pumps, actual setting for valves
                 EN_ENERGY       * Energy expended in kwatts
                   * computed values"""
    j= ctypes.c_float()
    ierr= _lib.ENgetlinkvalue(index, paramcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value
#------

def ENgetpatternid(index):
    """Retrieves the ID label of a particular time pattern.

    Arguments:
    index: pattern index"""
    label = ctypes.create_string_buffer(_max_label_len)
    ierr= _lib.ENgetpatternid(index, ctypes.byref(label))
    if ierr!=0: raise ENtoolkitError(ierr)
    return label.value

def ENgetpatternindex(patternid):
    """Retrieves the index of a particular time pattern.

    Arguments:
    id: pattern ID label"""
    j= ctypes.c_int()
    ierr= _lib.ENgetpatternindex(ctypes.c_char_p(patternid.encode()), ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetpatternlen(index):
    """Retrieves the number of time periods in a specific time pattern.

    Arguments:
    index:pattern index"""
    j= ctypes.c_int()
    ierr= _lib.ENgetpatternlen(index, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetpatternvalue( index, period):
    """Retrieves the multiplier factor for a specific time period in a time pattern.

    Arguments:
    index:  time pattern index
    period: period within time pattern"""
    j= ctypes.c_float()
    ierr= _lib.ENgetpatternvalue(index, period, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value



def ENgetcount(countcode):
    """Retrieves the number of network components of a specified type.

    Arguments:
    countcode: component code EN_NODECOUNT
                              EN_TANKCOUNT
                              EN_LINKCOUNT
                              EN_PATCOUNT
                              EN_CURVECOUNT
                              EN_CONTROLCOUNT"""
    j= ctypes.c_int()
    ierr= _lib.ENgetcount(countcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetflowunits():
    """Retrieves a code number indicating the units used to express all flow rates."""
    j= ctypes.c_int()
    ierr= _lib.ENgetflowunits(ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value    


def ENgettimeparam(paramcode):
    """Retrieves the value of a specific analysis time parameter.
    Arguments:
    paramcode: EN_DURATION     
               EN_HYDSTEP
               EN_QUALSTEP
               EN_PATTERNSTEP
               EN_PATTERNSTART
               EN_REPORTSTEP
               EN_REPORTSTART
               EN_RULESTEP
               EN_STATISTIC
               EN_PERIODS"""
    j= ctypes.c_int()
    ierr= _lib.ENgettimeparam(paramcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value
    
def  ENgetqualtype():
    """Retrieves the type of water quality analysis called for
    returns  qualcode: Water quality analysis codes are as follows:
                       EN_NONE	0 No quality analysis
                       EN_CHEM	1 Chemical analysis
                       EN_AGE 	2 Water age analysis
                       EN_TRACE	3 Source tracing
             tracenode:	index of node traced in a source tracing
	                analysis  (value will be 0 when qualcode
			is not EN_TRACE)"""
    qualcode= ctypes.c_int()
    tracenode= ctypes.c_int()
    ierr= _lib.ENgetqualtype(ctypes.byref(qualcode),
                             ctypes.byref(tracenode))
    if ierr!=0: raise ENtoolkitError(ierr)
    return qualcode.value, tracenode.value



#-------Retrieving other network information--------
def ENgetcontrol(cindex):
    """Retrieves the parameters of a simple control statement.
    Arguments:
       cindex:  control statement index
       ctype:   control type code EN_LOWLEVEL   (Low Level Control)
                                  EN_HILEVEL    (High Level Control)
                                  EN_TIMER      (Timer Control)       
                                  EN_TIMEOFDAY  (Time-of-Day Control)
       lindex:  index of link being controlled
       setting: value of the control setting
       nindex:  index of controlling node
       level:   value of controlling water level or pressure for level controls 
                or of time of control action (in seconds) for time-based controls"""
    #int ENgetcontrol(int cindex, int* ctype, int* lindex, float* setting, int* nindex, float* level )
    ctype = ctypes.c_int()
    lindex = ctypes.c_int()
    setting = ctypes.c_float()
    nindex = ctypes.c_int()
    level = ctypes.c_float()

    ierr= _lib.ENgetcontrol(ctypes.c_int(cindex), ctypes.byref(ctype),
                            ctypes.byref(lindex), ctypes.byref(setting),
                            ctypes.byref(nindex), ctypes.byref(level) )
    if ierr!=0: raise ENtoolkitError(ierr)
    return ctype.value, lindex.value, setting.value, nindex.value, level.value


def ENgetoption(optioncode):
    """Retrieves the value of a particular analysis option.

    Arguments:
    optioncode: EN_TRIALS       
                EN_ACCURACY 
                EN_TOLERANCE 
                EN_EMITEXPON 
                EN_DEMANDMULT""" 
    j= ctypes.c_int()
    ierr= _lib.ENgetoption(optioncode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value

def ENgetversion():
    """Retrieves the current version number of the Toolkit."""
    j= ctypes.c_int()
    ierr= _lib.ENgetversion(ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value



#---------Setting new values for network parameters-------------
def ENsetcontrol(cindex, ctype, lindex, setting, nindex, level ):
    """Sets the parameters of a simple control statement.
    Arguments:
       cindex:  control statement index
       ctype:   control type code  EN_LOWLEVEL   (Low Level Control)
                                   EN_HILEVEL    (High Level Control)  
                                   EN_TIMER      (Timer Control)       
                                   EN_TIMEOFDAY  (Time-of-Day Control)
       lindex:  index of link being controlled
       setting: value of the control setting
       nindex:  index of controlling node
       level:   value of controlling water level or pressure for level controls
                or of time of control action (in seconds) for time-based controls"""
    #int ENsetcontrol(int cindex, int* ctype, int* lindex, float* setting, int* nindex, float* level )
    ierr= _lib.ENsetcontrol(ctypes.c_int(cindex), ctypes.c_int(ctype),
                            ctypes.c_int(lindex), ctypes.c_float(setting), 
                            ctypes.c_int(nindex), ctypes.c_float(level) )
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetnodevalue(index, paramcode, value):
    """Sets the value of a parameter for a specific node.
    Arguments:
    index:  node index
    paramcode: Node parameter codes consist of the following constants:
                  EN_ELEVATION  Elevation
                  EN_BASEDEMAND ** Base demand
                  EN_PATTERN    ** Demand pattern index
                  EN_EMITTER    Emitter coeff.
                  EN_INITQUAL   Initial quality
                  EN_SOURCEQUAL Source quality
                  EN_SOURCEPAT  Source pattern index
                  EN_SOURCETYPE Source type (See note below)
                  EN_TANKLEVEL  Initial water level in tank
                       ** primary demand category is last on demand list
               The following parameter codes apply only to storage tank nodes
                  EN_TANKDIAM      Tank diameter
                  EN_MINVOLUME     Minimum water volume
                  EN_MINLEVEL      Minimum water level
                  EN_MAXLEVEL      Maximum water level
                  EN_MIXMODEL      Mixing model code
                  EN_MIXFRACTION   Fraction of total volume occupied by the inlet/outlet
                  EN_TANK_KBULK    Bulk reaction rate coefficient
    value:parameter value"""
    ierr= _lib.ENsetnodevalue(ctypes.c_int(index), ctypes.c_int(paramcode), ctypes.c_float(value))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetlinkvalue(index, paramcode, value):
    """Sets the value of a parameter for a specific link.
    Arguments:
    index:  link index
    paramcode: Link parameter codes consist of the following constants:
                 EN_DIAMETER     Diameter
                 EN_LENGTH       Length
                 EN_ROUGHNESS    Roughness coeff.
                 EN_MINORLOSS    Minor loss coeff.
                 EN_INITSTATUS   * Initial link status (0 = closed, 1 = open)
                 EN_INITSETTING  * Roughness for pipes, initial speed for pumps, initial setting for valves
                 EN_KBULK        Bulk reaction coeff.
                 EN_KWALL        Wall reaction coeff.
                 EN_STATUS       * Actual link status (0 = closed, 1 = open)
                 EN_SETTING      * Roughness for pipes, actual speed for pumps, actual setting for valves
                 * Use EN_INITSTATUS and EN_INITSETTING to set the design value for a link's status or setting that 
                   exists prior to the start of a simulation. Use EN_STATUS and EN_SETTING to change these values while 
                   a simulation is being run (within the ENrunH - ENnextH loop).

    value:parameter value"""
    ierr= _lib.ENsetlinkvalue(ctypes.c_int(index), 
                              ctypes.c_int(paramcode), 
			      ctypes.c_float(value))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENaddpattern(patternid):
    """Adds a new time pattern to the network.
    Arguments:
      id: ID label of pattern"""
    ierr= _lib.ENaddpattern(ctypes.c_char_p(patternid.encode()))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetpattern(index, factors):
    """Sets all of the multiplier factors for a specific time pattern.
    Arguments:
    index:    time pattern index
    factors:  multiplier factors list for the entire pattern"""
    # int ENsetpattern( int index, float* factors, int nfactors )
    nfactors= len(factors)
    cfactors_type= ctypes.c_float* nfactors
    cfactors= cfactors_type()
    for i in range(nfactors):
       cfactors[i]= float(factors[i] )
    ierr= _lib.ENsetpattern(ctypes.c_int(index), cfactors, ctypes.c_int(nfactors) )
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetpatternvalue( index, period, value):
    """Sets the multiplier factor for a specific period within a time pattern.
    Arguments:
       index: time pattern index
       period: period within time pattern
       value:  multiplier factor for the period"""
    #int ENsetpatternvalue( int index, int period, float value )
    ierr= _lib.ENsetpatternvalue( ctypes.c_int(index), 
                                  ctypes.c_int(period), 
				  ctypes.c_float(value) )
    if ierr!=0: raise ENtoolkitError(ierr)
 
 

def ENsetqualtype(qualcode, chemname, chemunits, tracenode):
    """Sets the type of water quality analysis called for.
    Arguments:
         qualcode:	water quality analysis code
         chemname:	name of the chemical being analyzed
         chemunits:	units that the chemical is measured in
         tracenode:	ID of node traced in a source tracing analysis """
    ierr= _lib.ENsetqualtype( ctypes.c_int(qualcode),
                              ctypes.c_char_p(chemname.encode()),
			      ctypes.c_char_p(chemunits.encode()),
                              ctypes.c_char_p(tracenode.encode()))
    if ierr!=0: raise ENtoolkitError(ierr)


def  ENsettimeparam(paramcode, timevalue):
    """Sets the value of a time parameter.
    Arguments:
      paramcode: time parameter code EN_DURATION
                                     EN_HYDSTEP
                                     EN_QUALSTEP
                                     EN_PATTERNSTEP
                                     EN_PATTERNSTART
                                     EN_REPORTSTEP
                                     EN_REPORTSTART
                                     EN_RULESTEP
                                     EN_STATISTIC
                                     EN_PERIODS
      timevalue: value of time parameter in seconds
                      The codes for EN_STATISTIC are:
                      EN_NONE     none
                      EN_AVERAGE  averaged
                      EN_MINIMUM  minimums
                      EN_MAXIMUM  maximums
                      EN_RANGE    ranges"""
    ierr= _lib.ENsettimeparam(ctypes.c_int(paramcode), ctypes.c_int(timevalue))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetoption( optioncode, value):
    """Sets the value of a particular analysis option.

    Arguments:
      optioncode: option code EN_TRIALS
                              EN_ACCURACY  
                              EN_TOLERANCE 
                              EN_EMITEXPON 
                              EN_DEMANDMULT
      value:  option value"""
    ierr= _lib.ENsetoption(ctypes.c_int(optioncode), ctypes.c_float(value))
    if ierr!=0: raise ENtoolkitError(ierr)


#----- Saving and using hydraulic analysis results files -------
def ENsavehydfile(fname):
    """Saves the current contents of the binary hydraulics file to a file."""
    ierr= _lib.ENsavehydfile(ctypes.c_char_p(fname.encode()))
    if ierr!=0: raise ENtoolkitError(ierr)

def  ENusehydfile(fname):
    """Uses the contents of the specified file as the current binary hydraulics file"""
    ierr= _lib.ENusehydfile(ctypes.c_char_p(fname.encode()))
    if ierr!=0: raise ENtoolkitError(ierr)



#----------Running a hydraulic analysis --------------------------
def ENsolveH():
    """Runs a complete hydraulic simulation with results 
    for all time periods written to the binary Hydraulics file."""
    ierr= _lib.ENsolveH()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENopenH(): 
    """Opens the hydraulics analysis system"""
    ierr= _lib.ENopenH()


def ENinitH(flag=None):
    """Initializes storage tank levels, link status and settings, 
    and the simulation clock time prior
to running a hydraulic analysis.

    flag  EN_NOSAVE [+EN_SAVE] [+EN_INITFLOW] """
    ierr= _lib.ENinitH(flag)
    if ierr!=0: raise ENtoolkitError(ierr)


def ENrunH():
    """Runs a single period hydraulic analysis, 
    retrieving the current simulation clock time t"""
    ierr= _lib.ENrunH(ctypes.byref(_current_simulation_time))
    if ierr>=100: 
      raise ENtoolkitError(ierr)
    elif ierr>0:
      return ENgeterror(ierr)


def ENsimtime():
    """retrieves the current simulation time t as datetime.timedelta instance"""
    return datetime.timedelta(seconds= _current_simulation_time.value )

def ENnextH():
    """Determines the length of time until the next hydraulic event occurs in an extended period
       simulation."""
    _deltat= ctypes.c_long()
    ierr= _lib.ENnextH(ctypes.byref(_deltat))
    if ierr!=0: raise ENtoolkitError(ierr)
    return _deltat.value


def ENcloseH():
    """Closes the hydraulic analysis system, freeing all allocated memory."""
    ierr= _lib.ENcloseH()
    if ierr!=0: raise ENtoolkitError(ierr)

#--------------------------------------------

#----------Running a quality analysis --------------------------
def ENsolveQ():
    """Runs a complete water quality simulation with results 
    at uniform reporting intervals written to EPANET's binary Output file."""
    ierr= _lib.ENsolveQ()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENopenQ():
    """Opens the water quality analysis system"""
    ierr= _lib.ENopenQ()


def ENinitQ(flag=None):
    """Initializes water quality and the simulation clock 
    time prior to running a water quality analysis.

    flag  EN_NOSAVE | EN_SAVE """
    ierr= _lib.ENinitQ(flag)
    if ierr!=0: raise ENtoolkitError(ierr)

def ENrunQ():
    """Makes available the hydraulic and water quality results
    that occur at the start of the next time period of a water quality analysis, 
    where the start of the period is returned in t."""
    ierr= _lib.ENrunQ(ctypes.byref(_current_simulation_time))
    if ierr>=100: 
      raise ENtoolkitError(ierr)
    elif ierr>0:
      return ENgeterror(ierr)

def ENnextQ():
    """Advances the water quality simulation 
    to the start of the next hydraulic time period."""
    _deltat= ctypes.c_long()
    ierr= _lib.ENnextQ(ctypes.byref(_deltat))
    if ierr!=0: raise ENtoolkitError(ierr)
    return _deltat.value
    
    
def ENstepQ():
    """Advances the water quality simulation one water quality time step. 
    The time remaining in the overall simulation is returned in tleft."""
    tleft= ctypes.c_long()
    ierr= _lib.ENnextQ(ctypes.byref(tleft))
    if ierr!=0: raise ENtoolkitError(ierr)
    return tleft.value

def ENcloseQ():
    """Closes the water quality analysis system, 
    freeing all allocated memory."""
    ierr= _lib.ENcloseQ()
    if ierr!=0: raise ENtoolkitError(ierr)
#--------------------------------------------





def ENsaveH():
    """Transfers results of a hydraulic simulation 
    from the binary Hydraulics file to the binary
    Output file, where results are only reported at 
    uniform reporting intervals."""
    ierr= _lib.ENsaveH()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsaveinpfile(fname):
    """Writes all current network input data to a file 
    using the format of an EPANET input file."""
    ierr= _lib.ENsaveinpfile( ctypes.c_char_p(fname.encode()))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENreport():
    """Writes a formatted text report on simulation results 
    to the Report file."""
    ierr= _lib.ENreport()
    if ierr!=0: raise ENtoolkitError(ierr)

def ENresetreport():
    """Clears any report formatting commands 
    
    that either appeared in the [REPORT] section of the 
    EPANET Input file or were issued with the 
    ENsetreport function"""
    ierr= _lib.ENresetreport()
    if ierr!=0: raise ENtoolkitError(ierr)
    
def ENsetreport(command):
    """Issues a report formatting command. 
    
    Formatting commands are the same as used in the 
    [REPORT] section of the EPANET Input file."""
    ierr= _lib.ENsetreport(ctypes.c_char_p(command.encode()))
    if ierr!=0: raise ENtoolkitError(ierr)

def ENsetstatusreport(statuslevel):
    """Sets the level of hydraulic status reporting. 
    
    statuslevel:  level of status reporting  
                  0 - no status reporting
                  1 - normal reporting
                  2 - full status reporting"""
    ierr= _lib.ENsetstatusreport(ctypes.c_int(statuslevel))
    if ierr!=0: raise ENtoolkitError(ierr)

def ENgeterror(errcode):
    """Retrieves the text of the message associated with a particular error or warning code."""
    errmsg= ctypes.create_string_buffer(_err_max_char)
    _lib.ENgeterror( errcode,ctypes.byref(errmsg), _err_max_char )
    return errmsg.value.decode()

def ENwriteline(line ):
    """Writes a line of text to the EPANET report file."""
    ierr= _lib.ENwriteline(ctypes.c_char_p(line.encode() ))
    if ierr!=0: raise ENtoolkitError(ierr)


class ENtoolkitError(Exception):
    def __init__(self, ierr):
      self.warning= ierr < 100
      self.args= (ierr,)
      self.message= ENgeterror(ierr)
      if self.message=='' and ierr!=0:
         self.message='ENtoolkit Undocumented Error '+str(ierr)+': look at text.h in epanet sources'
    def __str__(self):
      return self.message
      
      
#------ functions added from OpenWaterAnalytics ----------------------------------
# functions not present in original Epanet2 toolkit from US EPA
# it may change in future versions
#----------------------------------------------------------------------------------
if hasattr(_lib,"ENgetcurve"):
   def ENgetcurve(curveIndex):
       curveid = ctypes.create_string_buffer(_max_label_len)
       nValues = ctypes.c_int()
       xValues= ctypes.POINTER(ctypes.c_float)()
       yValues= ctypes.POINTER(ctypes.c_float)()
       ierr= _lib.ENgetcurve(curveIndex,
                             ctypes.byref(curveid),
	     	             ctypes.byref(nValues),
	     	             ctypes.byref(xValues),
	     	             ctypes.byref(yValues)
		             )
       # strange behavior of ENgetcurve: it returns also curveID
       # better split in two distinct functions ....
       if ierr!=0: raise ENtoolkitError(ierr)
       curve= []
       for i in range(nValues.value):
          curve.append( (xValues[i],yValues[i]) )
       return curve

   def ENgetcurveid(curveIndex):
       curveid = ctypes.create_string_buffer(_max_label_len)
       nValues = ctypes.c_int()
       xValues= ctypes.POINTER(ctypes.c_float)()
       yValues= ctypes.POINTER(ctypes.c_float)()
       ierr= _lib.ENgetcurve(curveIndex,
                             ctypes.byref(curveid),
	     	             ctypes.byref(nValues),
	     	             ctypes.byref(xValues),
	     	             ctypes.byref(yValues)
		             )
       # strange behavior of ENgetcurve: it returns also curveID
       # better split in two distinct functions ....
       if ierr!=0: raise ENtoolkitError(ierr)
       return curveid.value

#-----end of functions added from OpenWaterAnalytics ----------------------------------


EN_ELEVATION     = 0      # /* Node parameters */
EN_BASEDEMAND    = 1
EN_PATTERN       = 2
EN_EMITTER       = 3
EN_INITQUAL      = 4
EN_SOURCEQUAL    = 5
EN_SOURCEPAT     = 6
EN_SOURCETYPE    = 7
EN_TANKLEVEL     = 8
EN_DEMAND        = 9
EN_HEAD          = 10
EN_PRESSURE      = 11
EN_QUALITY       = 12
EN_SOURCEMASS    = 13
EN_INITVOLUME    = 14
EN_MIXMODEL      = 15
EN_MIXZONEVOL    = 16

EN_TANKDIAM      = 17
EN_MINVOLUME     = 18
EN_VOLCURVE      = 19
EN_MINLEVEL      = 20
EN_MAXLEVEL      = 21
EN_MIXFRACTION   = 22
EN_TANK_KBULK    = 23

EN_DIAMETER      = 0      # /* Link parameters */
EN_LENGTH        = 1
EN_ROUGHNESS     = 2
EN_MINORLOSS     = 3
EN_INITSTATUS    = 4
EN_INITSETTING   = 5
EN_KBULK         = 6
EN_KWALL         = 7
EN_FLOW          = 8
EN_VELOCITY      = 9
EN_HEADLOSS      = 10
EN_STATUS        = 11
EN_SETTING       = 12
EN_ENERGY        = 13

EN_DURATION      = 0      # /* Time parameters */
EN_HYDSTEP       = 1
EN_QUALSTEP      = 2
EN_PATTERNSTEP   = 3
EN_PATTERNSTART  = 4
EN_REPORTSTEP    = 5
EN_REPORTSTART   = 6
EN_RULESTEP      = 7
EN_STATISTIC     = 8
EN_PERIODS       = 9

EN_NODECOUNT     = 0      # /* Component counts */
EN_TANKCOUNT     = 1
EN_LINKCOUNT     = 2
EN_PATCOUNT      = 3
EN_CURVECOUNT    = 4
EN_CONTROLCOUNT  = 5

EN_JUNCTION      = 0      # /* Node types */
EN_RESERVOIR     = 1
EN_TANK          = 2

EN_CVPIPE        = 0      # /* Link types */
EN_PIPE          = 1
EN_PUMP          = 2
EN_PRV           = 3
EN_PSV           = 4
EN_PBV           = 5
EN_FCV           = 6
EN_TCV           = 7
EN_GPV           = 8

EN_NONE          = 0      # /* Quality analysis types */
EN_CHEM          = 1
EN_AGE           = 2
EN_TRACE         = 3

EN_CONCEN        = 0      # /* Source quality types */
EN_MASS          = 1
EN_SETPOINT      = 2
EN_FLOWPACED     = 3

EN_CFS           = 0      # /* Flow units types */
EN_GPM           = 1
EN_MGD           = 2
EN_IMGD          = 3
EN_AFD           = 4
EN_LPS           = 5
EN_LPM           = 6
EN_MLD           = 7
EN_CMH           = 8
EN_CMD           = 9

EN_TRIALS        = 0      # /* Misc. options */
EN_ACCURACY      = 1
EN_TOLERANCE     = 2
EN_EMITEXPON     = 3
EN_DEMANDMULT    = 4

EN_LOWLEVEL      = 0      # /* Control types */
EN_HILEVEL       = 1
EN_TIMER         = 2
EN_TIMEOFDAY     = 3

EN_AVERAGE       = 1      # /* Time statistic types.    */
EN_MINIMUM       = 2
EN_MAXIMUM       = 3
EN_RANGE         = 4

EN_MIX1          = 0      # /* Tank mixing models */
EN_MIX2          = 1
EN_FIFO          = 2
EN_LIFO          = 3

EN_NOSAVE        = 0      # /* Save-results-to-file flag */
EN_SAVE          = 1
EN_INITFLOW      = 10     # /* Re-initialize flow flag   */



FlowUnits= { EN_CFS :"cfs"   ,
             EN_GPM :"gpm"   ,
             EN_MGD :"a-f/d" ,
             EN_IMGD:"mgd"   ,
             EN_AFD :"Imgd"  ,
             EN_LPS :"L/s"   ,
             EN_LPM :"Lpm"   ,
             EN_MLD :"m3/h"  ,
             EN_CMH :"m3/d"  ,
             EN_CMD :"ML/d"  }
