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
%{
#include "epanet2.h"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"

/* DEFINE AND TYPEDEF MUST BE INCLUDED */
typedef void* EN_ProjectHandle;

typedef enum {
    EN_JUNCTION    = 0,
    EN_RESERVOIR   = 1,
    EN_TANK        = 2
} EN_NodeType;

typedef enum {
    EN_ELEVATION    = 0,
    EN_BASEDEMAND   = 1,
    EN_PATTERN      = 2,
    EN_EMITTER      = 3,
    EN_INITQUAL     = 4,
    EN_SOURCEQUAL   = 5,
    EN_SOURCEPAT    = 6,
    EN_SOURCETYPE   = 7,
    EN_TANKLEVEL    = 8,
    EN_DEMAND       = 9,
    EN_HEAD         = 10,
    EN_PRESSURE     = 11,
    EN_QUALITY      = 12,
    EN_SOURCEMASS   = 13,
    EN_INITVOLUME   = 14,
    EN_MIXMODEL     = 15,
    EN_MIXZONEVOL   = 16,
    EN_TANKDIAM     = 17,
    EN_MINVOLUME    = 18,
    EN_VOLCURVE     = 19,
    EN_MINLEVEL     = 20,
    EN_MAXLEVEL     = 21,
    EN_MIXFRACTION  = 22,
    EN_TANK_KBULK   = 23,
    EN_TANKVOLUME   = 24,
    EN_MAXVOLUME    = 25
} EN_NodeProperty;

typedef enum {
    EN_CVPIPE       = 0,
    EN_PIPE         = 1,
    EN_PUMP         = 2,
    EN_PRV          = 3,
    EN_PSV          = 4,
    EN_PBV          = 5,
    EN_FCV          = 6,
    EN_TCV          = 7,
    EN_GPV          = 8
} EN_LinkType;

typedef enum {
    EN_DIAMETER     = 0,
    EN_LENGTH       = 1,
    EN_ROUGHNESS    = 2,
    EN_MINORLOSS    = 3,
    EN_INITSTATUS   = 4,
    EN_INITSETTING  = 5,
    EN_KBULK        = 6,
    EN_KWALL        = 7,
    EN_FLOW         = 8,
    EN_VELOCITY     = 9,
    EN_HEADLOSS     = 10,
    EN_STATUS       = 11,
    EN_SETTING      = 12,
    EN_ENERGY       = 13,
    EN_LINKQUAL     = 14,
    EN_LINKPATTERN  = 15,
    EN_EFFICIENCY   = 16,
    EN_HEADCURVE    = 17,
    EN_EFFICIENCYCURVE = 18,
    EN_PRICEPATTERN = 19
} EN_LinkProperty;

typedef enum {
    EN_NODECOUNT    = 0,
    EN_TANKCOUNT    = 1,
    EN_LINKCOUNT    = 2,
    EN_PATCOUNT     = 3,
    EN_CURVECOUNT   = 4,
    EN_CONTROLCOUNT = 5,
    EN_RULECOUNT    = 6 
} EN_CountType;

typedef enum {
    EN_TRIALS       = 0,
    EN_ACCURACY     = 1,
    EN_TOLERANCE    = 2,
    EN_EMITEXPON    = 3,
    EN_DEMANDMULT   = 4,
    EN_HEADERROR    = 5,
    EN_FLOWCHANGE   = 6
} EN_Option;

typedef enum {
    EN_CFS         = 0,
    EN_GPM         = 1,
    EN_MGD         = 2,
    EN_IMGD        = 3,
    EN_AFD         = 4,
    EN_LPS         = 5,
    EN_LPM         = 6,
    EN_MLD         = 7,
    EN_CMH         = 8,
    EN_CMD         = 9
} EN_FlowUnits;

typedef enum {
    EN_DURATION     = 0,
    EN_HYDSTEP      = 1,
    EN_QUALSTEP     = 2,
    EN_PATTERNSTEP  = 3,
    EN_PATTERNSTART = 4,
    EN_REPORTSTEP   = 5,
    EN_REPORTSTART  = 6,
    EN_RULESTEP     = 7,
    EN_STATISTIC    = 8,
    EN_PERIODS      = 9,
    EN_STARTTIME    = 10,
    EN_HTIME        = 11,
    EN_QTIME        = 12,
    EN_HALTFLAG     = 13,
    EN_NEXTEVENT    = 14,
    EN_NEXTEVENTIDX = 15
} EN_TimeProperty;

typedef enum {
    EN_LOWLEVEL    = 0,
    EN_HILEVEL     = 1,
    EN_TIMER       = 2,
    EN_TIMEOFDAY   = 3
} EN_ControlType;

typedef enum {
    EN_NONE        = 0,
    EN_CHEM        = 1,
    EN_AGE         = 2,
    EN_TRACE       = 3
} EN_QualityType;

typedef enum {
  EN_NOSAVE        = 0,
  EN_SAVE          = 1,
  EN_INITFLOW      = 10,
  EN_SAVE_AND_INIT = 11
} EN_SaveOption;


#ifdef WINDOWS
  #ifdef __cplusplus
  #define DLLEXPORT __declspec(dllexport) __cdecl
  #else
  #define DLLEXPORT __declspec(dllexport) __stdcall
  #endif
#else
  #define DLLEXPORT
#endif


/* TYPEMAPS FOR OPAQUE POINTER */
/* Used for functions that output a new opaque pointer */
%typemap(in, numinputs=0) EN_ProjectHandle* ph_out (EN_ProjectHandle retval)
{
 /* OUTPUT in */
    retval = NULL;
    $1 = &retval;
}
/* used for functions that take in an opaque pointer (or NULL)
and return a (possibly) different pointer */
%typemap(argout) EN_ProjectHandle* ph_out, EN_ProjectHandle* ph_inout 
{
 /* OUTPUT argout */
    %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
} 
%typemap(in) EN_ProjectHandle* ph_inout (EN_ProjectHandle retval)
{
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


/* TYPEMAPS FOR FLOAT ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) float* float_out (float temp) {
    $1 = &temp;
}
%typemap(argout) float* float_out {
    %append_output(PyFloat_FromDouble((double)*$1));
}


/* TYPEMAP FOR MEMORY MANAGEMENT AND ENCODING OF STRINGS */
%typemap(in, numinputs=0)char** string_out (char* temp), int* slen (int temp){
   $1 = &temp;
}
%typemap(argout)(char** string_out, int* slen) {
    if (*$1) {
        PyObject* o;
        o = PyUnicode_FromStringAndSize(*$1, *$2);
        
        $result = SWIG_Python_AppendOutput($result, o);
        free(*$1);
    }
}


/* TYPEMAPS FOR INT ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) int* int_out (int temp) {
    $1 = &temp;
}
%typemap(argout) int* int_out {
    %append_output(PyInt_FromLong(*$1));
}


/* TYPEMAPS FOR LONG ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) long* long_out (long temp) {
    $1 = &temp;
}
%typemap(argout) long* long_out {
    %append_output(PyLong_FromLong(*$1));
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
%apply EnumeratedType {EN_SaveOption, EN_NodeProperty};


/* RENAME FUNCTIONS PYTHON STYLE */
%rename("%(regex:/^\w+_([a-zA-Z]+)/\L\\1/)s") "";

/* GENERATES DOCUMENTATION */
%feature("autodoc", "2");


/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    char* err_msg;
    EN_clearError(arg1);
    $function
    if (EN_checkError(arg1, &err_msg))
    {
        PyErr_SetString(PyExc_Exception, err_msg);
        free(err_msg);
        SWIG_fail;
    }
}

/* INSERT EXCEPTION HANDLING FOR THESE FUNCTIONS */
// RUNNING AN EPANET SIMULATION
int DLLEXPORT EN_runproject(EN_ProjectHandle ph, const char *f1, const char *f2, const char *f3, void (*pviewprog)(char *));

// OPENING A CLOSING THE EPANET TOOLKIT SYSTEM
int DLLEXPORT EN_open(EN_ProjectHandle ph, const char *f1, const char *f2, const char *f3);
int DLLEXPORT EN_close(EN_ProjectHandle ph);

// RETREIVING INFORMATION ABOUT NETWORK NODES
int DLLEXPORT EN_getnodeindex(EN_ProjectHandle ph, char *id, int *int_out);
int DLLEXPORT EN_getnodename(EN_ProjectHandle ph, int index, char **string_out, int *slen);
int DLLEXPORT EN_getnodetype(EN_ProjectHandle ph, int index, int *int_out);
int DLLEXPORT EN_getnodevalue(EN_ProjectHandle ph, int index, EN_NodeProperty code, float *float_out);

// RETREIVING INFORMATION ABOUT NETWORK LINKS
int DLLEXPORT EN_getlinkindex(EN_ProjectHandle ph, char *id, int *index);
int DLLEXPORT EN_getlinkid(EN_ProjectHandle ph, int index, char *id);
int DLLEXPORT EN_getlinktype(EN_ProjectHandle ph, int index, EN_LinkType *code);
int DLLEXPORT EN_getlinknodes(EN_ProjectHandle ph, int index, int *node1, int *node2);
int DLLEXPORT EN_getlinkvalue(EN_ProjectHandle ph, int index, EN_LinkProperty code, EN_API_FLOAT_TYPE *value);

// RETREIVING INFORMATION ABOUT TIME PATTERNS
int DLLEXPORT EN_getpatternid(EN_ProjectHandle ph, int index, char *id);
int DLLEXPORT EN_getpatternindex(EN_ProjectHandle ph, char *id, int *index);
int DLLEXPORT EN_getpatternlen(EN_ProjectHandle ph, int index, int *len);
int DLLEXPORT EN_getpatternvalue(EN_ProjectHandle ph, int index, int period, EN_API_FLOAT_TYPE *value);

// RETREIVING OTHER NETWORK INFORMATION
int DLLEXPORT EN_getcontrol(EN_ProjectHandle ph, int controlIndex, int *controlType, int *linkIndex, EN_API_FLOAT_TYPE *setting, int *nodeIndex, EN_API_FLOAT_TYPE *level);
int DLLEXPORT EN_getcount(EN_ProjectHandle ph, EN_CountType code, int *count);
int DLLEXPORT EN_getflowunits(EN_ProjectHandle ph, int *code);
int DLLEXPORT EN_gettimeparam(EN_ProjectHandle ph, int code, long *value);
int DLLEXPORT EN_getoption(EN_ProjectHandle ph, EN_Option opt, EN_API_FLOAT_TYPE *value);
//int DLLEXPORT EN_getversion(int *version); 

// SETTING NEW VALUES FOR NETWORK PARAMETERS
int DLLEXPORT EN_setcontrol(EN_ProjectHandle ph, int cindex, int ctype, int lindex, EN_API_FLOAT_TYPE setting, int nindex, EN_API_FLOAT_TYPE level);
int DLLEXPORT EN_setnodevalue(EN_ProjectHandle ph, int index, int code, EN_API_FLOAT_TYPE v);
int DLLEXPORT EN_setlinkvalue(EN_ProjectHandle ph, int index, int code, EN_API_FLOAT_TYPE v);
int DLLEXPORT EN_setpattern(EN_ProjectHandle ph, int index, EN_API_FLOAT_TYPE *f, int len);
int DLLEXPORT EN_setpatternvalue(EN_ProjectHandle ph, int index, int period, EN_API_FLOAT_TYPE value);
int DLLEXPORT EN_setqualtype(EN_ProjectHandle ph, int qualcode, char *chemname, char *chemunits, char *tracenode);
int DLLEXPORT EN_settimeparam(EN_ProjectHandle ph, int code, long value);
int DLLEXPORT EN_setoption(EN_ProjectHandle ph, int code, EN_API_FLOAT_TYPE v);

// SAVING AND USING HYDRAULIC ANALYSIS RESULTS FILES
int DLLEXPORT EN_savehydfile(EN_ProjectHandle ph, char *filename);
int DLLEXPORT EN_usehydfile(EN_ProjectHandle ph, char *filename);

// RUNNING A HYDRAULIC ANALYSIS
int DLLEXPORT EN_solveH(EN_ProjectHandle ph);
int DLLEXPORT EN_openH(EN_ProjectHandle ph);
int DLLEXPORT EN_initH(EN_ProjectHandle ph, EN_SaveOption flag);
int DLLEXPORT EN_runH(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_nextH(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_closeH(EN_ProjectHandle ph);

// RUNNING A WATER QUALITY ANALYSIS
int DLLEXPORT EN_solveQ(EN_ProjectHandle ph);
int DLLEXPORT EN_openQ(EN_ProjectHandle ph);
int DLLEXPORT EN_initQ(EN_ProjectHandle ph, int saveflag);
int DLLEXPORT EN_runQ(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_nextQ(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_closeQ(EN_ProjectHandle ph);

// GENERATING AN OUTPUT REPORT
int DLLEXPORT EN_saveH(EN_ProjectHandle ph);
int DLLEXPORT EN_saveinpfile(EN_ProjectHandle ph, char *filename);
int DLLEXPORT EN_report(EN_ProjectHandle ph);
int DLLEXPORT EN_resetreport(EN_ProjectHandle ph);
int DLLEXPORT EN_setreport(EN_ProjectHandle ph, char *reportFormat);
int DLLEXPORT EN_setstatusreport(EN_ProjectHandle ph, int code);
//int DLLEXPORT EN_geterror(int errcode, char *errmsg, int maxLen);

%exception;

/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */    
int DLLEXPORT EN_createproject(EN_ProjectHandle *ph_out);
int DLLEXPORT EN_deleteproject(EN_ProjectHandle *ph_inout);

int DLLEXPORT EN_getversion(int *version);

void DLLEXPORT EN_clearError(EN_ProjectHandle ph);
int DLLEXPORT EN_checkError(EN_ProjectHandle ph, char **msg_buffer);


/* CODE ADDED DIRECTLY TO SWIGGED INTERFACE MODULE */
%pythoncode%{

import enum

class NodeType(enum.Enum):
    JUNCTION        = EN_JUNCTION
    RESERVOIR       = EN_RESERVOIR
    TANK            = EN_TANK
    

class NodeProperty(enum.Enum):
    ELEVATION       = EN_ELEVATION
    BASEDEMAND      = EN_BASEDEMAND
    PATTERN         = EN_PATTERN
    EMITTER         = EN_EMITTER
    INITQUAL        = EN_INITQUAL
    SOURCEQUAL      = EN_SOURCEQUAL
    SOURCEPAT       = EN_SOURCEPAT
    SOURCETYPE      = EN_SOURCETYPE
    TANKLEVEL       = EN_TANKLEVEL
    DEMAND          = EN_DEMAND
    HEAD            = EN_HEAD
    PRESSURE        = EN_PRESSURE
    QUALITY         = EN_QUALITY
    SOURCEMASS      = EN_SOURCEMASS
    INITVOLUME      = EN_INITVOLUME
    MIXMODEL        = EN_MIXMODEL
    MIXZONEVOL      = EN_MIXZONEVOL
    TANKDIAM        = EN_TANKDIAM
    MINVOLUME       = EN_MINVOLUME
    VOLCURVE        = EN_VOLCURVE
    MINLEVEL        = EN_MINLEVEL
    MAXLEVEL        = EN_MAXLEVEL
    MIXFRACTION     = EN_MIXFRACTION
    TANK_KBULK      = EN_TANK_KBULK
    TANKVOLUME      = EN_TANKVOLUME
    MAXVOLUME       = EN_MAXVOLUME


class SaveOptions(enum.Enum):
    NOSAVE          = EN_NOSAVE
    SAVE            = EN_SAVE
    INITFLOW        = EN_INITFLOW
    SAVE_AND_INIT   = EN_SAVE_AND_INIT
  
  

%}
