%include "typemaps.i"
%include "cstring.i"
%include "carrays.i"

/* arrays for toolkit functions wanting lists */
%array_class(int, intArray);
%array_class(double, doubleArray);

/* epanet simple python wrapper */
%module (package="epanet") toolkit
%{
#include <epanet2_2.h>
%}

/* strip the pseudo-scope from function declarations and enums*/
%rename("%(strip:[EN_])s") "";

%typemap(in,numinputs=0) EN_Project* (EN_Project temp) {
    $1 = &temp;
}

%typemap(argout) EN_Project* {
  %append_output(SWIG_NewPointerObj(*$1, SWIGTYPE_p_Project, SWIG_POINTER_NEW));
}
/*
This is the same logic applied in swmm toolkit to handle a breaking change
introduced in the version 4.3 of SWIG. Credit: karosc

See https://github.com/karosc/swmm-python/commit/1ef854ac469c1e2df29f9bb1ed718361df79cc95
*/
%header %{
SWIGINTERN PyObject*
Custom_SWIG_Python_AppendOutput(PyObject* result, PyObject* obj, int is_void) {
    if (!result) {
    result = obj;
    } else if (result == Py_None) {
    SWIG_Py_DECREF(result);
    result = obj;
    } else {
    if (!PyList_Check(result)) {
        PyObject *o2 = result;
        result = PyList_New(1);
        if (result) {
        PyList_SET_ITEM(result, 0, o2);
        } else {
        SWIG_Py_DECREF(obj);
        return o2;
        }
    }
    PyList_Append(result,obj);
    SWIG_Py_DECREF(obj);
    }
    return result;
}
#define SWIG_Python_AppendOutput Custom_SWIG_Python_AppendOutput
%}


/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}

%apply int *OUTPUT {
    int *out_count,
    int *out_version,
    int *out_units,
    int *out_qualType,
    int *out_traceNode,
    int *out_index,
    int *out_nodeType,
    int *out_type,
    int *out_demandIndex,
    int *out_numDemands,
    int *out_patIndex,
    int *out_linkType,
    int *out_node1,
    int *out_node2,
    int *out_pumpType,
    int *out_curveIndex,
    int *out_len,
    int *out_nPoints,
    int *out_nodeIndex,
    int *out_linkIndex,
    int *out_nPremises,
    int *out_nThenActions,
    int *out_nElseActions,
    int *out_logop,
    int *out_object,
    int *out_objIndex,
    int *out_variable,
    int *out_relop,
    int *out_status,
    int *out_value
};

%apply double *OUTPUT {
    double *out_value,
    double *out_x,
    double *out_y,
    double *out_baseDemand,
    double *out_pmin,
    double *out_preq,
    double *out_pexp,
    double *out_setting,
    double *out_level,
    double *out_priority
};

%apply long *OUTPUT {
    long *out_value,
    long *out_currentTime,
    long *out_tStep,
    long *out_timeLeft
};

%cstring_bounded_output(char *OUTCHAR, EN_MAXMSG);

%apply char *OUTCHAR {
    char *out_line1,
    char *out_line2,
    char *out_line3,
    char *out_comment,
    char *out_errmsg,
    char *out_chemName,
    char *out_chemUnits,
    char *out_id,
    char *out_demandName
};

%apply int *INOUT {
    int *inout_index
}

%nodefault Project;
struct Project {};
%extend Project {
  ~Project() {
    EN_deleteproject($self);
  }
};
ignore Project;

/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    $action
    if ( result > 10) {
        char errmsg[EN_MAXMSG];
        EN_geterror(result, errmsg, EN_MAXMSG);
        PyErr_SetString(PyExc_Exception, errmsg);
        SWIG_fail;
    }
    else if (result > 0) {
        PyErr_WarnEx(PyExc_Warning, "WARNING", 2);
    }
}

%feature("autodoc", "2");
%newobject EN_createproject;
%delobject EN_deleteproject;
%include <epanet2_enums.h>
%include <epanet2_2.h>
%exception;
