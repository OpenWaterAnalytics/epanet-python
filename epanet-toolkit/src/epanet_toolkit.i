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

%module epanet_toolkit
%{
#include "epanet2.h"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"

/* DEFINE AND TYPEDEF MUST BE INCLUDED */
typedef void* EN_ProjectHandle;


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

/* TYPEMAPS FOR LONG ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) long* long_out (long temp) {
    $1 = &temp;
}
%typemap(argout) long* long_out {
    %append_output(PyLong_FromLong(*$1));
}

/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    char* err_msg;
    EN_clearError(arg1);
    $function
    if (EN_checkError(arg1, &err_msg))
    {
        PyErr_SetString(PyExc_Exception, err_msg);
        SWIG_fail;
    }
}

/* INSERT EXCEPTION HANDLING FOR THESE FUNCTIONS */  
int DLLEXPORT EN_open(EN_ProjectHandle ph, const char *f1, const char *f2, const char *f3);
int DLLEXPORT EN_close(EN_ProjectHandle ph);

int DLLEXPORT EN_getnodeindex(EN_ProjectHandle ph, char *id, int *index);
int DLLEXPORT EN_getnodeid(EN_ProjectHandle ph, int index, char *id);
int DLLEXPORT EN_getnodetype(EN_ProjectHandle ph, int index, int *code);
int DLLEXPORT EN_getnodevalue(EN_ProjectHandle ph, int index, int code, EN_API_FLOAT_TYPE *value);

int DLLEXPORT EN_getlinkindex(EN_ProjectHandle ph, char *id, int *index);
int DLLEXPORT EN_getlinkid(EN_ProjectHandle ph, int index, char *id);
int DLLEXPORT EN_getlinktype(EN_ProjectHandle ph, int index, EN_LinkType *code);
int DLLEXPORT EN_getlinknodes(EN_ProjectHandle ph, int index, int *node1, int *node2);
int DLLEXPORT EN_getlinkvalue(EN_ProjectHandle ph, int index, EN_LinkProperty code, EN_API_FLOAT_TYPE *value);

int DLLEXPORT EN_getpatternid(EN_ProjectHandle ph, int index, char *id);
int DLLEXPORT EN_getpatternindex(EN_ProjectHandle ph, char *id, int *index);
int DLLEXPORT EN_getpatternlen(EN_ProjectHandle ph, int index, int *len);
int DLLEXPORT EN_getpatternvalue(EN_ProjectHandle ph, int index, int period, EN_API_FLOAT_TYPE *value);

int DLLEXPORT EN_getcontrol(EN_ProjectHandle ph, int controlIndex, int *controlType, int *linkIndex, EN_API_FLOAT_TYPE *setting, int *nodeIndex, EN_API_FLOAT_TYPE *level);
int DLLEXPORT EN_getcount(EN_ProjectHandle ph, EN_CountType code, int *count);
int DLLEXPORT EN_getflowunits(EN_ProjectHandle ph, int *code);
int DLLEXPORT EN_gettimeparam(EN_ProjectHandle ph, int code, long *value);
int DLLEXPORT EN_getoption(EN_ProjectHandle ph, EN_Option opt, EN_API_FLOAT_TYPE *value);
int DLLEXPORT EN_getversion(int *version);

int DLLEXPORT EN_setcontrol(EN_ProjectHandle ph, int cindex, int ctype, int lindex, EN_API_FLOAT_TYPE setting, int nindex, EN_API_FLOAT_TYPE level);
int DLLEXPORT EN_setnodevalue(EN_ProjectHandle ph, int index, int code, EN_API_FLOAT_TYPE v);
int DLLEXPORT EN_setlinkvalue(EN_ProjectHandle ph, int index, int code, EN_API_FLOAT_TYPE v);
int DLLEXPORT EN_setpattern(EN_ProjectHandle ph, int index, EN_API_FLOAT_TYPE *f, int len);
int DLLEXPORT EN_setpatternvalue(EN_ProjectHandle ph, int index, int period, EN_API_FLOAT_TYPE value);
int DLLEXPORT EN_setqualtype(EN_ProjectHandle ph, int qualcode, char *chemname, char *chemunits, char *tracenode);
int DLLEXPORT EN_settimeparam(EN_ProjectHandle ph, int code, long value);
int DLLEXPORT EN_setoption(EN_ProjectHandle ph, int code, EN_API_FLOAT_TYPE v);

int DLLEXPORT EN_savehydfile(EN_ProjectHandle ph, char *filename);
int DLLEXPORT EN_usehydfile(EN_ProjectHandle ph, char *filename);

int DLLEXPORT EN_solveH(EN_ProjectHandle ph);
int DLLEXPORT EN_openH(EN_ProjectHandle ph);
int DLLEXPORT EN_initH(EN_ProjectHandle ph, int flag);
int DLLEXPORT EN_runH(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_nextH(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_closeH(EN_ProjectHandle ph);

int DLLEXPORT EN_solveQ(EN_ProjectHandle ph);
int DLLEXPORT EN_openQ(EN_ProjectHandle ph);
int DLLEXPORT EN_initQ(EN_ProjectHandle ph, int saveflag);
int DLLEXPORT EN_runQ(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_nextQ(EN_ProjectHandle ph, long* long_out);
int DLLEXPORT EN_closeQ(EN_ProjectHandle ph);

int DLLEXPORT EN_saveH(EN_ProjectHandle ph);
int DLLEXPORT EN_saveinpfile(EN_ProjectHandle ph, char *filename);
int DLLEXPORT EN_report(EN_ProjectHandle ph);
int DLLEXPORT EN_resetreport(EN_ProjectHandle ph);
int DLLEXPORT EN_setreport(EN_ProjectHandle ph, char *reportFormat);
int DLLEXPORT EN_setstatusreport(int code);
int DLLEXPORT EN_geterror(int errcode, char *errmsg, int maxLen);


/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */    
int DLLEXPORT EN_alloc(EN_ProjectHandle* ph_out);
int DLLEXPORT EN_free(EN_ProjectHandle* ph_out);

