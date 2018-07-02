/*
 *  epanet_toolkit.i - SWIG interface description file for EPANET toolkit
 * 
 *  Created:    11/27/2017
 *  Author:     Michael E. Tryby
 *              US EPA - ORD/NRMRL
 *  
 *  Build command: 
 *    $ swig -I../../../include -python epanet_toolkit.i
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

/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */    
int DLLEXPORT EN_alloc(EN_ProjectHandle* ph_out);
int DLLEXPORT EN_free(EN_ProjectHandle* ph_out);

