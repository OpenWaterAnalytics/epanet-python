%include "typemaps.i"
%include "cstring.i"

/* epanet simple python wrapper */
%module (package="epanet") output
%{
#define SHARED_EXPORTS_BUILT_AS_STATIC
#include <epanet_output.h>
%}
%include <epanet_output_enums.h>

/* strip the pseudo-scope from function declarations */
%rename("%(strip:[ENR_])s") "";

%typemap(in,numinputs=0) ENR_Handle* p_handle_out (ENR_Handle temp) {
    $1 = &temp;
}

%typemap(argout) ENR_Handle* p_handle_out {
  %append_output(SWIG_NewPointerObj(SWIG_as_voidptr(retval$argnum), $1_descriptor, 0));
}

/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}


/* TYPEMAPS FOR MEMORY MANAGEMENT OF FLOAT ARRAYS */
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

%apply int *OUTPUT {
    int *int_out
};

/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    $action
    if ( result > 0) {
        PyErr_SetString(PyExc_Exception, "ERROR");
        SWIG_fail;
    }
}

%feature("autodoc", "2");
#define SHARED_EXPORTS_BUILT_AS_STATIC
%include <epanet_output.h>

%exception;
