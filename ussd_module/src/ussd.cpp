#include <e32std.h>
#include "Python.h"
#include "symbian_python_ext_util.h"

// docs: https://docs.python.org/release/2.5.4/ext/intro.html


static PyObject* SendUssdCmd(PyObject* , PyObject *args)
{
	const char *command;
	
	if (!PyArg_ParseTuple(args, "s", &command))
		return NULL;
	
	// todo: implement this
	
	Py_INCREF(Py_None);
	return Py_None;

}

static const PyMethodDef ussd_methods[] = {
	{"send_command",	(PyCFunction)SendUssdCmd,	METH_VARARGS},
    {0, 0}
};

PyMODINIT_FUNC initussd(void)
{
    (void) Py_InitModule("ussd", (PyMethodDef*)ussd_methods);
}

/* end of file: ussd.cpp */
