/*
 *  epanet_output.i - SWIG interface description file for EPANET Output API
 * 
 *  Created:    9/20/2017
 *
 *  Author:     Michael E. Tryby
 *              US EPA - ORD/NRMRL
 *
*/ 
%module(package="epanet") output
%{
#include "epanet_output.h"

#define SWIG_FILE_WITH_INIT
%}

%include "typemaps.i"

/* DEFINE AND TYPEDEF MUST BE INCLUDED */
#define MAXMSG 53

typedef void* ENR_Handle;

typedef enum {
	ENR_node        = 1,
    ENR_link        = 2
} ENR_ElementType;

typedef enum {
    ENR_flowUnits   = 1,
    ENR_pressUnits  = 2,
    ENR_chemUnits   = 3
} ENR_Units;

typedef enum {
    ENR_CFS         = 0,
    ENR_GPM         = 1,
    ENR_MGD         = 2,
    ENR_IMGD        = 3,
    ENR_AFD         = 4,
    ENR_LPS         = 5,
    ENR_LPM         = 6,
    ENR_MLD         = 7,
    ENR_CMH         = 8,
    ENR_CMD         = 9
} ENR_FlowUnits;

typedef enum {
    ENR_PSI         = 0,
    ENR_MTR         = 1,
    ENR_KPA         = 2
} ENR_PressUnits;

typedef enum {
    ENR_NONE        = 0,
    ENR_MGL         = 1,
    ENR_UGL         = 2,
    ENR_HOURS       = 3,
    ENR_PRCNT       = 4
} ENR_ChemUnits;

/*
typedef enum {
    ENR_nodeCount   = 1,
    ENR_tankCount   = 2,
    ENR_linkCount   = 3,
    ENR_pumpCount   = 4,
    ENR_valveCount  = 5
} ENR_ElementCount;
*/

typedef enum {
    ENR_reportStart = 1,
    ENR_reportStep  = 2,
    ENR_simDuration = 3,
    ENR_numPeriods  = 4
}ENR_Time;

typedef enum {
    ENR_demand      = 1,
    ENR_head        = 2,
    ENR_pressure    = 3,
    ENR_quality     = 4
} ENR_NodeAttribute;

typedef enum {
    ENR_flow        = 1,
    ENR_velocity    = 2,
    ENR_headloss    = 3,
    ENR_avgQuality  = 4,
    ENR_status      = 5,
    ENR_setting     = 6,
    ENR_rxRate      = 7,
    ENR_frctnFctr   = 8
} ENR_LinkAttribute;

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
%typemap(in, numinputs=0) ENR_Handle* p_handle_out (ENR_Handle retval)
{
 /* OUTPUT in */
    retval = NULL;
    $1 = &retval;
}
/* used for functions that take in an opaque pointer (or NULL)
and return a (possibly) different pointer */
%typemap(argout) ENR_Handle* p_handle_out
{
 /* OUTPUT argout */
    %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
} 
/* No need for special IN typemap for opaque pointers, it works anyway */


/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}

/* TYPEMAPS FOR INT ARGUMENT AS RETURN VALUE */
%typemap(in, numinputs=0) int* int_out (int temp) {
    $1 = &temp;
}
%typemap(argout) int* int_out {
    %append_output(PyInt_FromLong(*$1));
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

/* TYPEMAPS FOR MEMORY MANAGEMNET OF FLOAT ARRAYS */
%typemap(in, numinputs=0)float** float_out (float* temp), int* int_dim (int temp){
   $1 = &temp;
}
%typemap(argout) (float** float_out, int* int_dim) {
    if (*$1) {
      PyObject *o = PyList_New(*$2);
      int i;
      float* temp = *$1;
      for(i=0; i<*$2; i++) {
        PyList_SetItem(o, i, PyFloat_FromDouble((double)temp[i]));
      }
      $result = SWIG_Python_AppendOutput($result, o);
      free(*$1);
    }
}

/* TYPEMAPS FOR MEMORY MANAGEMENT OF INT ARRAYS */
%typemap(in, numinputs=0)int** int_out (long* temp), int* int_dim (int temp){
   $1 = &temp;
}
%typemap(argout) (int** int_out, int* int_dim) {
    if (*$1) {
      PyObject *o = PyList_New(*$2);
      int i;
      long* temp = *$1;
      for(i=0; i<*$2; i++) {
        PyList_SetItem(o, i, PyInt_FromLong(temp[i]));
      }
      $result = SWIG_Python_AppendOutput($result, o);
      free(*$1);
    }
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
%apply EnumeratedType {ENR_ElementType, ENR_Units, ENR_Time, ENR_NodeAttribute, ENR_LinkAttribute}


/* RENAME FUNCTIONS PYTHON STYLE */
%rename("%(regex:/^\w+_([a-zA-Z]+)/\L\\1/)s") "";

/* GENERATES DOCUMENTATION */
%feature("autodoc", "2");


/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
	char* err_msg;
	ENR_clearError(arg1);
    $function
    if (ENR_checkError(arg1, &err_msg))
    {
        PyErr_SetString(PyExc_Exception, err_msg);
    	SWIG_fail;
    }
}
/* INSERT EXCEPTION HANDLING FOR THESE FUNCTIONS */  
int DLLEXPORT ENR_open(ENR_Handle p_handle, const char* path);

int DLLEXPORT ENR_getVersion(ENR_Handle p_handle, int* int_out);
int DLLEXPORT ENR_getNetSize(ENR_Handle p_handle, int** int_out, int* int_dim);
int DLLEXPORT ENR_getUnits(ENR_Handle p_handle, ENR_Units t_enum, int* int_out);
int DLLEXPORT ENR_getTimes(ENR_Handle p_handle, ENR_Time t_enum, int* int_out);
int DLLEXPORT ENR_getElementName(ENR_Handle p_handle, ENR_ElementType t_enum,
		int elementIndex, char** string_out, int* slen);
int DLLEXPORT ENR_getEnergyUsage(ENR_Handle p_handle, int pumpIndex,
		int* int_out, float** float_out, int* int_dim);
int DLLEXPORT ENR_getNetReacts(ENR_Handle p_handle, float** float_out, int* int_dim);


int DLLEXPORT ENR_getNodeAttribute(ENR_Handle p_handle, int periodIndex,
        ENR_NodeAttribute t_enum, float** float_out, int* int_dim);
int DLLEXPORT ENR_getLinkAttribute(ENR_Handle p_handle, int periodIndex,
        ENR_LinkAttribute t_enum, float** float_out, int* int_dim);
%exception;        

/* NO EXCEPTION HANDLING FOR THESE FUNCTIONS */        
int DLLEXPORT ENR_init(ENR_Handle* p_handle_out);        
int DLLEXPORT ENR_close(ENR_Handle* p_handle_out);
void DLLEXPORT ENR_free(void** array);

void DLLEXPORT ENR_clearError(ENR_Handle p_handle);
int DLLEXPORT ENR_checkError(ENR_Handle p_handle, char** msg_buffer);


/* CODE ADDED DIRECTLY TO SWIGGED INTERFACE MODULE */
%pythoncode%{
import enum

class ElementType(enum.Enum):
    NODE         = ENR_node
    LINK         = ENR_link

class Units(enum.Enum):
    FLOW         = ENR_flowUnits
    PRESS        = ENR_pressUnits
    CHEM         = ENR_chemUnits
    
class UnitSystem(Enum):
    US_CUST      = 0   
    SI_METRIC    = 1
            
class FlowUnits(enum.Enum):
    CFS          = ENR_CFS
    GPM          = ENR_GPM
    MGD          = ENR_MGD
    IMGD         = ENR_IMGD
    AFD          = ENR_AFD
    LPS          = ENR_LPS
    LPM          = ENR_LPM
    MLD          = ENR_MLD
    CMH          = ENR_CMH
    CMD          = ENR_CMD
            
class PressUnits(enum.Enum):
    PSI          = ENR_PSI 
    MTR          = ENR_MTR
    KPA          = ENR_KPA
        
class ConcUnits(enum.Enum):
    NONE         = ENR_NONE
    MGL          = ENR_MGL
    UGL          = ENR_UGL
    HOURS        = ENR_HOURS
    PRCNT        = ENR_PRCNT   
        
class Time(enum.Enum):
    REPORT_START = ENR_reportStart
    REPORT_STEP  = ENR_reportStep
    SIM_DURATION = ENR_simDuration
    NUM_PERIODS  = ENR_numPeriods
    
class NodeAttribute(enum.Enum):
    DEMAND       = ENR_demand
    HEAD         = ENR_head
    PRESSURE     = ENR_pressure
    QUALITY      = ENR_quality
    
class LinkAttribute(enum.Enum):
    FLOW         = ENR_flow
    VELOCITY     = ENR_velocity
    HEADLOSS     = ENR_headloss
    AVG_QUALITY  = ENR_avgQuality
    STATUS       = ENR_status
    SETTING      = ENR_setting
    RX_RATE      = ENR_rxRate
    FRCTN_FCTR   = ENR_frctnFctr
%}
