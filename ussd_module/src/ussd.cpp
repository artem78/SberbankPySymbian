#include "Python.h"
#include <e32base.h>
#include <e32std.h>
#include <c32comm.h>
#include "symbian_python_ext_util.h"
#if __WINS__
	#include <f32file.h>
#endif

// docs:
//	https://docs.python.org/release/2.5.4/ext/intro.html
//	https://people.csail.mit.edu/rudolph/PythonExtension.pdf


void SendUssdCmdL(const TDesC8 &aCommand)
	{	
	_LIT(KCsyName,"DATAPORT");
	_LIT(KDataPort,"DATAPORT::1");// this works with CUSD
	_LIT8(KAtCmdFmt, "AT+CUSD=1,\"%S\",15\r\n");
	
	TBuf8<64> atCmd;
	atCmd.Format(KAtCmdFmt, &aCommand);
	
#if __WINS__
	RFs fs;
	User::LeaveIfError(fs.Connect());
	CleanupClosePushL(fs);
	
	RFile file;
	_LIT(KFileName, "c:\\__ussd_cmds.log");
	User::LeaveIfError(file.Replace(fs, KFileName, EFileWrite));
	CleanupClosePushL(file);
	
	{
	TBuf8<128> buf;
	buf.Copy(aCommand);
	buf.Append('\r');
	buf.Append('\n');
	buf.Append(atCmd);
	buf.Append('\r');
	buf.Append('\n');
	User::LeaveIfError(file.Write(buf));
	}
	
	CleanupStack::PopAndDestroy(2, &fs);
#endif
	
	
	//////////
	//return;
	//////////
	
	User::LeaveIfError(StartC32());
	//console->Printf(_L("server started\n"));
	
	RCommServ server;	
	server.Connect();
	TInt ret=server.LoadCommModule(KCsyName());
	User::LeaveIfError(ret);
	//console->Printf(_L("module loaded\n"));
	
	RComm commPort;
	ret=commPort.Open(server,KDataPort,/*ECommExclusive*/ ECommShared);
	User::LeaveIfError(ret);
	//console->Printf(_L("port opened\n"));
	
	TRequestStatus status;
	commPort.Write(status,/*KTimeOut,*/atCmd);
	//console->Printf(_L("write\n"));
	TBuf8<256> buf;
	buf.Zero();
	User::WaitForRequest(status);
	User::LeaveIfError(status.Int());
	//console->Printf(_L("write end\n"));
	
	//Issue Request for more Information
	commPort.ReadOneOrMore(status, buf);
	//console->Printf(_L("read\n"));
	//SetActive();
	User::WaitForRequest(status);
	User::LeaveIfError(status.Int());
	//console->Printf(_L("read end\n"));
	
	TBuf<256> buf16;
	buf16.Copy(buf);
	//console->Printf(_L("response: \"%S\""), &buf16);
	
	commPort.Close();
	server.Close();
	
	
	
	//console->Printf(_L("MainL end\n"));
	}


static PyObject* SendUssdCmd_py(PyObject* /*self*/, PyObject *args)
{
	char* _cmd_arg;
	
	if (!PyArg_ParseTuple(args, "s", &_cmd_arg))
		return NULL;
	
	TBuf8<64> cmd;
	cmd.Copy((TUint8*)_cmd_arg);
	
	TRAPD(leaveCode, SendUssdCmdL(cmd));
	if (leaveCode != KErrNone)
		{
		return SPyErr_SetFromSymbianOSErr(leaveCode);
		}
	
	Py_RETURN_NONE;
}

static const PyMethodDef ussd_methods[] = {
	{"send_command",	(PyCFunction)SendUssdCmd_py,	METH_VARARGS},
    {0, 0}
};

PyMODINIT_FUNC initussd(void)
{
    (void) Py_InitModule("ussd", (PyMethodDef*)ussd_methods);
}

/* end of file: ussd.cpp */
