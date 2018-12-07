/*
 *  epanet_toolkit.i - SWIG interface description file for EPANET toolkit
 * 
 *  Created:    11/27/2017
 *  Author:     Michael E. Tryby
 *              US EPA - ORD/NRMRL
 *  
 *  Build command: 
 *    $ swig -I../include -python -py3 epanet_toolkit.i
 *
*/ 

%module(package="epanet") toolkit


%include "typemaps.i"
%include "cstring.i"
              
              
%{
#include "epanet_py.h"

#define SWIG_FILE_WITH_INIT
%}


#ifndef EN_API_FLOAT_TYPE
  #define EN_API_FLOAT_TYPE float
#endif

// Opaque pointer to project
typedef void *Handle;


%include "epanet2_enums.h"


/* TYPEMAPS FOR OPAQUE POINTER */
/* Used for functions that output a new opaque pointer */
%typemap(in, numinputs=0) Handle *ph_out (Handle retval) {
 /* OUTPUT in */
    retval = NULL;
    $1 = &retval;
}
/* used for functions that take in an opaque pointer (or NULL)
and return a (possibly) different pointer */
%typemap(argout) Handle *ph_out, Handle *ph_inout {
 /* OUTPUT argout */
    %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
} 
%typemap(in) Handle *ph_inout (Handle retval) {
   /* INOUT in */
   SWIG_ConvertPtr(obj0,SWIG_as_voidptrptr(&retval), 0, 0);
    $1 = &retval;
}
/* No need for special IN typemap for opaque pointers, it works anyway */


/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}


/* TYPEMAP FOR ENUMERATED TYPES */
%typemap(in) EnumeratedType (int val, int ecode = 0) {
    if (PyObject_HasAttrString($input,"value")) {
        PyObject* o;
        o = PyObject_GetAttrString($input, "value");
        ecode = SWIG_AsVal_int(o, &val); 
    }   
    else {
        SWIG_exception_fail(SWIG_ArgError(ecode), "in method '" "$symname" "', argument " "$argnum"" of type '" "$ltype""'"); 
    }   
    
    $1 = ($1_type)(val);
}
%apply EnumeratedType {EN_NodeProperty, EN_LinkProperty, EN_TimeProperty, 
    EN_AnalysisStatistic, EN_CountType, EN_NodeType, EN_LinkType, EN_QualityType,
    EN_SourceType, EN_HeadLossType, EN_FlowUnits, EN_DemandModel, EN_Option, 
    EN_ControlType, EN_StatisticType, EN_MixingModel, EN_SaveOption, EN_PumpType,
    EN_CurveType, EN_ActionCodeType, EN_RuleObject, EN_RuleVariable, 
    EN_RuleOperator, EN_RuleStatus, EN_StatusReport};


/* MARK FUNCTIONS AS ALLOCATING AND DEALLOCATING MEMORY */ 
%newobject proj_create;
%delobject proj_delete;


/* GENERATES DOCUMENTATION */
%feature("autodoc", "2");


/* MACRO FOR RETURNING A BOUNDED LENGTH STRING */
%cstring_bounded_output(char *id_out, EN_MAXID);


/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    char* err_msg;
    
    err_clear(arg1);
    
    $function
    if (err_check(arg1, &err_msg))
    {
        PyErr_SetString(PyExc_Exception, err_msg);
        toolkit_free((void **)&err_msg);
        SWIG_fail;
    }
}


/* INSERT EXCEPTION HANDLING FOR THESE FUNCTIONS */

int proj_run(Handle ph, const char *input_path, const char *report_path, const char *output_path);
int proj_init(Handle ph, const char *rptFile, const char *outFile, EN_FlowUnits unitsType, EN_HeadLossType headLossType);
int proj_open(Handle ph, const char *inpFile, const char *rptFile, const char *binOutFile);
int proj_savefile(Handle ph, const char *filename);
int proj_close(Handle ph);


int hydr_solve(Handle ph);
int hydr_save(Handle ph);
int hydr_open(Handle ph);
int hydr_init(Handle ph, EN_SaveOption saveFlag);
int hydr_run(Handle ph, long *OUTPUT);
int hydr_next(Handle ph, long *OUTPUT);
int hydr_close(Handle ph);
int hydr_savefile(Handle ph, char *filename);
int hydr_usefile(Handle ph, char *filename);


int qual_solve(Handle ph);
int qual_open(Handle ph);
int qual_init(Handle ph, EN_SaveOption saveFlag);
int qual_run(Handle ph, long *OUTPUT);
int qual_next(Handle ph, long *OUTPUT);
int qual_step(Handle ph, long *OUTPUT);
int qual_close(Handle ph);


int rprt_writeline(Handle ph, char *line);
int rprt_writeresults(Handle ph);
int rprt_reset(Handle ph);
int rprt_set(Handle ph, char *reportCommand);
int rprt_setlevel(Handle ph, EN_StatusReport code);
int rprt_getcount(Handle ph, EN_CountType code, int *OUTPUT);
int rprt_anlysstats(Handle ph, EN_AnalysisStatistic code, EN_API_FLOAT_TYPE *OUTPUT );


int anlys_getoption(Handle ph, EN_Option code, EN_API_FLOAT_TYPE *OUTPUT);
int anlys_setoption(Handle ph, EN_Option code, EN_API_FLOAT_TYPE value);
int anlys_getflowunits(Handle ph, int *OUTPUT);
int anlys_setflowunits(Handle ph, EN_FlowUnits code);
int anlys_gettimeparam(Handle ph, EN_TimeProperty code, long *OUTPUT);
int anlys_settimeparam(Handle ph, EN_TimeProperty code, long value);
int anlys_getqualinfo(Handle ph, EN_QualityType *qualcode, char *chemname, char *chemunits, int *tracenode);
int anlys_getqualtype(Handle ph, EN_QualityType *qualcode, int *tracenode);
int anlys_setqualtype(Handle ph, EN_QualityType qualcode, char *chemname, char *chemunits, char *tracenode);


int node_add(Handle ph, char *id, EN_NodeType nodeType);
int node_delete(Handle ph, int index, int actionCode);
int node_getindex(Handle ph, char *id, int *OUTPUT);
int node_getid(Handle ph, int index, char *id_out);
int node_setid(Handle ph, int index, char *newid);
int node_gettype(Handle ph, int index, int *OUTPUT);
int node_getvalue(Handle ph, int index, int code, EN_API_FLOAT_TYPE *OUTPUT);
int node_setvalue(Handle ph, int index, int code, EN_API_FLOAT_TYPE value);
int node_getcoord(Handle ph, int index, EN_API_FLOAT_TYPE *OUTPUT, EN_API_FLOAT_TYPE *OUTPUT);
int node_setcoord(Handle ph, int index, EN_API_FLOAT_TYPE x, EN_API_FLOAT_TYPE y);


int dmnd_getmodel(Handle ph, int *type, EN_API_FLOAT_TYPE *pmin, EN_API_FLOAT_TYPE *preq, EN_API_FLOAT_TYPE *pexp);
int dmnd_setmodel(Handle ph, int type, EN_API_FLOAT_TYPE pmin, EN_API_FLOAT_TYPE preq, EN_API_FLOAT_TYPE pexp);
int dmnd_getcount(Handle ph, int nodeIndex, int *OUTPUT);
int dmnd_getbase(Handle ph, int nodeIndex, int demandIndex, EN_API_FLOAT_TYPE *OUTPUT);
int dmnd_setbase(Handle ph, int nodeIndex, int demandIndex, EN_API_FLOAT_TYPE baseDemand);
int dmnd_getpattern(Handle ph, int nodeIndex, int demandIndex, int *OUTPUT);
int dmnd_setpattern(Handle ph, int nodeIndex, int demandIndex, int patIndex);
int dmnd_getname(Handle ph, int nodeIndex, int demandIdx, char *demandName);
int dmnd_setname(Handle ph, int nodeIndex, int demandIdx, char *demandName);


int link_add(Handle ph, char *id, EN_LinkType linkType, char *fromNode, char *toNode);
int link_delete(Handle ph, int index, int actionCode);
int link_getindex(Handle ph, char *id, int *OUTPUT);
int link_getid(Handle ph, int index, char *id_out);
int link_setid(Handle ph, int index, char *newid);
int link_gettype(Handle ph, int index, int *OUTPUT);
int link_settype(Handle ph, int *index, EN_LinkType type, int actionCode);
int link_getnodes(Handle ph, int index, int *OUTPUT, int *OUTPUT);
int link_setnodes(Handle ph, int index, int node1, int node2);
int link_getvalue(Handle ph, int index, EN_LinkProperty code, EN_API_FLOAT_TYPE *OUTPUT);
int link_setvalue(Handle ph, int index, int code, EN_API_FLOAT_TYPE value);


int pump_gettype(Handle ph, int linkIndex, int *OUTPUT);
int pump_getheadcurveindex(Handle ph, int pumpIndex, int *OUTPUT);
int pump_setheadcurveindex(Handle ph, int pumpIndex, int curveIndex);


int ptrn_add(Handle ph, char *id);
int ptrn_getindex(Handle ph, char *id, int *OUTPUT);
int ptrn_getid(Handle ph, int index, char *id);
int ptrn_getlength(Handle ph, int index, int *OUTPUT);
int ptrn_getvalue(Handle ph, int index, int period, EN_API_FLOAT_TYPE *OUTPUT);
int ptrn_setvalue(Handle ph, int index, int period, EN_API_FLOAT_TYPE value);
int ptrn_getavgvalue(Handle ph, int index, EN_API_FLOAT_TYPE *OUTPUT);
int ptrn_set(Handle ph, int index, EN_API_FLOAT_TYPE *values, int len);


int curv_add(Handle ph, char *id);
int curv_getindex(Handle ph, char *id, int *OUTPUT);
int curv_getid(Handle ph, int index, char *id);
int curv_getlength(Handle ph, int index, int *OUTPUT);
int curv_gettype(Handle ph, int curveIndex, int *OUTPUT);
int curv_getvalue(Handle ph, int curveIndex, int pointIndex, EN_API_FLOAT_TYPE *OUTPUT, EN_API_FLOAT_TYPE *OUTPUT);
int curv_setvalue(Handle ph, int curveIndex, int pointIndex, EN_API_FLOAT_TYPE x, EN_API_FLOAT_TYPE y);
int curv_get(Handle ph, int curveIndex, char* id, int *nValues, EN_API_FLOAT_TYPE **xValues, EN_API_FLOAT_TYPE **yValues);
int curv_set(Handle ph, int index, EN_API_FLOAT_TYPE *x, EN_API_FLOAT_TYPE *y, int len);


int toolkit_getversion(int *int_out);


%exception;

/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */    

int  proj_create(Handle *ph_out);
int  proj_delete(Handle *ph_inout);

void err_clear(Handle ph);
int  err_check(Handle ph, char** msg_buffer);
void toolkit_free(void **memory);


/* CODE ADDED DIRECTLY TO SWIGGED INTERFACE MODULE */
%pythoncode%{

import enum

class NodeProperty(enum.Enum):
    ELEVATION   = EN_ELEVATION
    BASEDEMAND  = EN_BASEDEMAND
    PATTERN     = EN_PATTERN
    EMITTER     = EN_EMITTER
    INITQUAL    = EN_INITQUAL
    SOURCEQUAL  = EN_SOURCEQUAL
    SOURCEPAT   = EN_SOURCEPAT
    SOURCETYPE  = EN_SOURCETYPE
    TANKLEVEL   = EN_TANKLEVEL
    DEMAND      = EN_DEMAND
    HEAD        = EN_HEAD
    PRESSURE    = EN_PRESSURE
    QUALITY     = EN_QUALITY
    SOURCEMASS  = EN_SOURCEMASS
    INITVOLUME  = EN_INITVOLUME
    MIXMODEL    = EN_MIXMODEL
    MIXZONEVOL  = EN_MIXZONEVOL
    TANKDIAM    = EN_TANKDIAM
    MINVOLUME   = EN_MINVOLUME
    VOLCURVE    = EN_VOLCURVE
    MINLEVEL    = EN_MINLEVEL
    MAXLEVEL    = EN_MAXLEVEL
    MIXFRACTION = EN_MIXFRACTION
    TANK_KBULK  = EN_TANK_KBULK
    TANKVOLUME  = EN_TANKVOLUME
    MAXVOLUME   = EN_MAXVOLUME


class LinkProperty(enum.Enum):
    DIAMETER        = EN_DIAMETER
    LENGTH          = EN_LENGTH
    ROUGHNESS       = EN_ROUGHNESS
    MINORLOSS       = EN_MINORLOSS
    INITSTATUS      = EN_INITSTATUS
    INITSETTING     = EN_INITSETTING
    KBULK           = EN_KBULK
    KWALL           = EN_KWALL
    FLOW            = EN_FLOW
    VELOCITY        = EN_VELOCITY
    HEADLOSS        = EN_HEADLOSS
    STATUS          = EN_STATUS
    SETTING         = EN_SETTING
    ENERGY          = EN_ENERGY
    LINKQUAL        = EN_LINKQUAL
    LINKPATTERN     = EN_LINKPATTERN
    EFFICIENCY      = EN_EFFICIENCY
    HEADCURVE       = EN_HEADCURVE
    EFFICIENCYCURVE = EN_EFFICIENCYCURVE
    PRICEPATTERN    = EN_PRICEPATTERN
    STATE           = EN_STATE
    CONST_POWER     = EN_CONST_POWER
    SPEED           = EN_SPEED


class TimeProperty(enum.Enum):
    DURATION     = EN_DURATION
    HYDSTEP      = EN_HYDSTEP
    QUALSTEP     = EN_QUALSTEP
    PATTERNSTEP  = EN_PATTERNSTEP
    PATTERNSTART = EN_PATTERNSTART
    REPORTSTEP   = EN_REPORTSTEP
    REPORTSTART  = EN_REPORTSTART
    RULESTEP     = EN_RULESTEP
    STATISTIC    = EN_STATISTIC
    PERIODS      = EN_PERIODS
    STARTTIME    = EN_STARTTIME
    HTIME        = EN_HTIME
    QTIME        = EN_QTIME
    HALTFLAG     = EN_HALTFLAG
    NEXTEVENT    = EN_NEXTEVENT
    NEXTEVENTIDX = EN_NEXTEVENTIDX


class AnalysisStatistic(enum.Enum):
    ITERATIONS    = EN_ITERATIONS
    RELATIVEERROR = EN_RELATIVEERROR
    MAXHEADERROR  = EN_MAXHEADERROR
    MAXFLOWCHANGE = EN_MAXFLOWCHANGE
    MASSBALANCE   = EN_MASSBALANCE
  

class CountType(enum.Enum):
    NODES         = EN_NODECOUNT
    TANKS         = EN_TANKCOUNT
    LINKS         = EN_LINKCOUNT
    PTRNS         = EN_PATCOUNT
    CURVS         = EN_CURVECOUNT
    CTRLS         = EN_CONTROLCOUNT
    RULES         = EN_RULECOUNT


class NodeType(enum.Enum):
    JUNCTION    = EN_JUNCTION
    RESERVOIR   = EN_RESERVOIR
    TANK        = EN_TANK


class LinkType(enum.Enum):
    CVPIPE       = EN_CVPIPE
    PIPE         = EN_PIPE
    PUMP         = EN_PUMP
    PRV          = EN_PRV
    PSV          = EN_PSV
    PBV          = EN_PBV
    FCV          = EN_FCV
    TCV          = EN_TCV
    GPV          = EN_GPV


class QualityType(enum.Enum):
    NONE        = EN_NONE
    CHEM        = EN_CHEM
    AGE         = EN_AGE
    TRACE       = EN_TRACE


class SourceType(enum.Enum):
    CONCEN      = EN_CONCEN
    MASS        = EN_MASS
    SETPOINT    = EN_SETPOINT
    FLOWPACED   = EN_FLOWPACED


class HeadLossType(enum.Enum):
    HW          = EN_HW
    DW          = EN_DW
    CM          = EN_CM


class FlowUnits(enum.Enum):
    CFS         = EN_CFS
    GPM         = EN_GPM
    MGD         = EN_MGD
    IMGD        = EN_IMGD
    AFD         = EN_AFD
    LPS         = EN_LPS
    LPM         = EN_LPM
    MLD         = EN_MLD
    CMH         = EN_CMH
    CMD         = EN_CMD


class DemandModel(enum.Enum):
    DDA         = EN_DDA
    PDA         = EN_PDA


class Option(enum.Enum):
    TRIALS       = EN_TRIALS
    ACCURACY     = EN_ACCURACY
    TOLERANCE    = EN_TOLERANCE
    EMITEXPON    = EN_EMITEXPON
    DEMANDMULT   = EN_DEMANDMULT
    HEADERROR    = EN_HEADERROR
    FLOWCHANGE   = EN_FLOWCHANGE
    DEMANDDEFPAT = EN_DEMANDDEFPAT
    HEADLOSSFORM = EN_HEADLOSSFORM


class ControlType(enum.Enum):
    LOWLEVEL    = EN_LOWLEVEL
    HILEVEL     = EN_HILEVEL
    TIMER       = EN_TIMER
    TIMEOFDAY   = EN_TIMEOFDAY


class StatisticType(enum.Enum):
    AVERAGE     = EN_AVERAGE
    MINIMUM     = EN_MINIMUM
    MAXIMUM     = EN_MAXIMUM
    RANGE       = EN_RANGE


class MixingModel(enum.Enum):
    MIX1        = EN_MIX1
    MIX2        = EN_MIX2
    FIFO        = EN_FIFO
    LIFO        = EN_LIFO



class SaveOption(enum.Enum):
    NOSAVE        = EN_NOSAVE
    SAVE          = EN_SAVE
    INITFLOW      = EN_INITFLOW
    SAVE_AND_INIT = EN_SAVE_AND_INIT


class PumpType(enum.Enum):
    CONST_HP    = EN_CONST_HP
    POWER_FUNC  = EN_POWER_FUNC
    CUSTOM      = EN_CUSTOM
    NOCURVE     = EN_NOCURVE


class CurveType(enum.Enum):
    VOL         = EN_V_CURVE
    CHAR        = EN_P_CURVE
    EFF         = EN_E_CURVE
    HL          = EN_H_CURVE
    GEN         = EN_G_CURVE


class ActionCode(enum.Enum):
    UNCOND      = EN_UNCONDITIONAL
    COND        = EN_CONDITIONAL


class RuleObject(enum.Enum):
    R_NODE      = EN_R_NODE 
    R_LINK      = EN_R_LINK
    R_SYSTEM    = EN_R_SYSTEM


class RuleVariable(enum.Enum):
    R_DEMAND    = EN_R_DEMAND
    R_HEAD      = EN_R_HEAD
    R_GRADE     = EN_R_GRADE
    R_LEVEL     = EN_R_LEVEL
    R_PRESSURE  = EN_R_PRESSURE
    R_FLOW      = EN_R_FLOW
    R_STATUS    = EN_R_STATUS
    R_SETTING   = EN_R_SETTING 
    R_POWER     = EN_R_POWER
    R_TIME      = EN_R_TIME 
    R_CLOCKTIME = EN_R_CLOCKTIME
    R_FILLTIME  = EN_R_FILLTIME
    R_DRAINTIME = EN_R_DRAINTIME


class RuleOperator(enum.Enum):
    R_EQ        = EN_R_EQ
    R_NE        = EN_R_NE
    R_LE        = EN_R_LE
    R_GE        = EN_R_GE
    R_LT        = EN_R_LT 
    R_GT        = EN_R_GT
    R_IS        = EN_R_IS
    R_NOT       = EN_R_NOT
    R_BELOW     = EN_R_BELOW
    R_ABOVE     = EN_R_ABOVE


class RuleStatus(enum.Enum):
    R_IS_OPEN   = EN_R_IS_OPEN
    R_IS_CLOSED = EN_R_IS_CLOSED
    R_IS_ACTIVE = EN_R_IS_ACTIVE


class StatusReport(enum.Enum):
    NO_REPORT     = EN_NO_REPORT
    NORMAL_REPORT = EN_NORMAL_REPORT
    FULL_REPORT   = EN_FULL_REPORT

%}
