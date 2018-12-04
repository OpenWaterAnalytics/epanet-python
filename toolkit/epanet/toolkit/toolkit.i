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
#include "epanet_py.h"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"


#ifndef EN_API_FLOAT_TYPE
  #define EN_API_FLOAT_TYPE float
#endif

// Opaque pointer to project
typedef void *Handle;

%include "epanet2_enums.h"


/* TYPEMAPS FOR OPAQUE POINTER */
/* Used for functions that output a new opaque pointer */
%typemap(in, numinputs=0) Handle *ph_out (Handle retval)
{
 /* OUTPUT in */
    retval = NULL;
    $1 = &retval;
}
/* used for functions that take in an opaque pointer (or NULL)
and return a (possibly) different pointer */
%typemap(argout) Handle *ph_out, Handle *ph_inout 
{
 /* OUTPUT argout */
    %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
} 
%typemap(in) Handle *ph_inout (Handle retval)
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


/* TYPEMAPS FOR INT ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) int* int_out (int temp) {
    $1 = &temp;
}
%typemap(argout) int* int_out {
    %append_output(PyInt_FromLong(*$1));
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
%apply EnumeratedType {EN_FlowUnits, EN_HeadLossType, EN_SaveOption, EN_StatusReport, EN_TimeProperty, EN_QualityType};


/* GENERATES DOCUMENTATION */
%feature("autodoc", "2");


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


int hyd_solve(Handle ph);
int hyd_save(Handle ph);
int hyd_open(Handle ph);
int hyd_init(Handle ph, EN_SaveOption saveFlag);
int hyd_run(Handle ph, long *long_out);
int hyd_next(Handle ph, long *long_out);
int hyd_close(Handle ph);
int hyd_savefile(Handle ph, char *filename);
int hyd_usefile(Handle ph, char *filename);


int qual_solve(Handle ph);
int qual_open(Handle ph);
int qual_init(Handle ph, EN_SaveOption saveFlag);
int qual_run(Handle ph, long *long_out);
int qual_next(Handle ph, long *long_out);
int qual_step(Handle ph, long *long_out);
int qual_close(Handle ph);


int rpt_writeline(Handle ph, char *line);
int rpt_writeresults(Handle ph);
int rpt_reset(Handle ph);
int rpt_set(Handle ph, char *reportCommand);
int rpt_setlevel(Handle ph, EN_StatusReport code);
int rpt_getcount(Handle ph, EN_CountType code, int *int_out);
int rpt_anlysstats(Handle ph, EN_AnalysisStatistic code, EN_API_FLOAT_TYPE *float_out );


int anlys_getoption(Handle ph, EN_Option code, EN_API_FLOAT_TYPE *value);
int anlys_setoption(Handle ph, EN_Option code, EN_API_FLOAT_TYPE value);
int anlys_getflowunits(Handle ph, EN_FlowUnits *code);
int anlys_setflowunits(Handle ph, EN_FlowUnits code);
int anlys_gettimeparam(Handle ph, EN_TimeProperty code, long *value);
int anlys_settimeparam(Handle ph, EN_TimeProperty code, long value);
int anlys_getqualinfo(Handle ph, EN_QualityType *qualcode, char *chemname, char *chemunits, int *tracenode);
int anlys_getqualtype(Handle ph, EN_QualityType *qualcode, int *tracenode);
int anlys_setqualtype(Handle ph, EN_QualityType qualcode, char *chemname, char *chemunits, char *tracenode);


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

class HeadLossType(enum.Enum):
    HW = EN_HW
    DW = EN_DW
    CM = EN_CM

class FlowUnits(enum.Enum):
    CFS = EN_CFS
    GPM = EN_GPM
    MGD = EN_MGD
    IMGD = EN_IMGD
    AFD = EN_AFD
    LPS = EN_LPS
    LPM = EN_LPM
    MLD = EN_MLD
    CMH = EN_CMH
    CMD = EN_CMD

class SaveOption(enum.Enum):
    NOSAVE        = EN_NOSAVE 
    SAVE          = EN_SAVE
    INITFLOW      = EN_INITFLOW
    SAVE_AND_INIT = EN_SAVE_AND_INIT

class StatusReport(enum.Enum):
    NONE   = EN_NO_REPORT
    NORMAL = EN_NORMAL_REPORT
    FULL   = EN_FULL_REPORT
  
class AnalysisStatistic(enum.Enum):
    ITERATIONS    = EN_ITERATIONS
    RELERROR      = EN_RELATIVEERROR
    MAXHEADERROR  = EN_MAXHEADERROR
    MAXFLOWCHANGE = EN_MAXFLOWCHANGE
    MASSBALANCE   = EN_MASSBALANCE
    
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

class QualityType(enum.Enum):
    NONE  = EN_NONE
    CHEM  = EN_CHEM
    AGE   = EN_AGE
    TRACE = EN_TRACE


%}
