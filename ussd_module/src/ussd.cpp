#include <e32std.h>
#include "Python.h"
#include "symbian_python_ext_util.h"


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
//	{"send_Òommand",	SendUssdCmd,	METH_VARARGS},
	{"send_Òommand",	(PyCFunction)SendUssdCmd,	METH_VARARGS},
    {0, 0}
};

/* module entry-point (module-initialization) function */
// Ú‡Í Í‡Í Ô‡‚ËÎ¸ÌÓ???

//PyMODINIT_FUNC initussd(void)
//{
//    /* Create the module and add the functions */
//    PyObject *m = Py_InitModule("ussd", ussd_methods);
//}

/*DL_EXPORT(void) initussd()
	{
		PyObject *module;
		module = Py_InitModule("ussd",(PyMethodDef*) ussd_methods);
	}

DL_EXPORT(void) init_ussd()
	{
		PyObject *module;
		module = Py_InitModule("ussd",(PyMethodDef*) ussd_methods);
	}*/

PyMODINIT_FUNC initussd(void)
{
    (void) Py_InitModule("ussd", (PyMethodDef*)ussd_methods);
}


/* end of file: ussd.cpp */
