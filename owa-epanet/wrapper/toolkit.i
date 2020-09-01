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

/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}

%apply int *OUTPUT {
    int *count,
    int *version,
    int *units,
    int *qualType,
    int *traceNode,
    int *index,
    int *nodeType,
    int *type,
    int *demandIndex,
    int *numDemands,
    int *patIndex,
    int *linkType,
    int *node1,
    int *node2,
    int *pumpType,
    int *curveIndex,
    int *len,
    int *nPoints,
    int *nodeIndex,
    int *linkIndex,
    int *nPremises,
    int *nThenActions,
    int *nElseActions,
    int *logop,
    int *object,
    int *objIndex,
    int *variable,
    int *relop,
    int *status
};

%apply double *OUTPUT {
    double *value,
    double *baseDemand,
    double *pmin,
    double *preq,
    double *pexp,
    double *setting,
    double *level,
    double *priority,
    double *out_x,
    double *out_y
};

%apply double *INPUT {
    double *x,
    double *y,
    double *xValues,
    double *yValues
};

%apply long *OUTPUT {
    long *value,
    long *currentTime,
    long *tStep,
    long *timeLeft
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
