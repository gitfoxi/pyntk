/*%Z%**********************************************************************
 *%Z%
 *%Z%                     MODULE  : fn_templ.c
 *%Z%
 *%Z%---------------------------------------------------------------------
 *%Z%
 *%Z%        (c) Copyright Agilent Technologies GmbH, Boeblingen 1993
 *%Z%
 *%Z%---------------------------------------------------------------------
 *%Z%
 *%Z%  AUTHOR  : Eric Furmanek, SSTD-R&D
 *%Z%
 *%Z%  DATE    : 17.09.93
 *%Z%
 *%Z%---------------------------------------------------------------------
 *%Z%
 *%Z%  CONTENTS: Template for user written functions.
 *%Z%
 *%Z%
 *%Z%  Instructions:
 *%Z%
 *%Z%  1) Copy this template to as many .c files as you require
 *%Z%
 *%Z%  2) Use the command 'make depend' to make visible the new
 *%Z%     source files to the makefile utility
 *%Z%
 *%Z%  3) Use the command 'make' to generate libcifset.sl - the
 *%Z%     shared library needed for the command interface.
 *%Z%
 *%Z%
 *%Z%*********************************************************************/

/*
 *-- system includes ------------------------------------------------------
 */
#include <python2.7/Python.h>
#include <stdio.h>

/*
 *-- module include -------------------------------------------------------
 */

#include "tpi_c.h"
#include "adiUserI.h"
#include "ci_types.h"
#include "libcicpi.h"

/*
 *-- external functions ---------------------------------------------------
 */

/*
 *-- external variables ---------------------------------------------------
 */

/*
 *-- defines --------------------------------------------------------------
 */


/*
 *-- typedefs -------------------------------------------------------------
 */

/*
 *-- globals variables ----------------------------------------------------
 */

/*
 *-- functions ------------------------------------------------------------
 */

/*%Z%***********************************************************************
 *%Z%
 *%Z%  FUNCTION NAME: reversi
 *%Z%
 *%Z%  DESCRIPTION:
 *%Z%
 *%Z%  This routine is an example of how a CommandSet call as specified in
 *%Z%  the application model file can be realized as a user function. The
 *%Z%  function itself is a trivial example of string manipulation, but it
 *%Z%  does demonstrate usage of all the input and output parameters
 *%Z%  and their string length limitations.
 *%Z%
 *%Z%  ---------------------------------------------------------------------
 *%Z%
 *%Z%  Valid Return Codes:
 *%Z%
 *%Z%  CI_CALL_PASS    = 0  function completed successfully
 *%Z%  CI_TEST_PASS    = 0  test passed 
 *%Z%  CI_TEST_FAIL    = 1  test failed
 *%Z%  CI_CALL_ERROR   = 2  function call failed
 *%Z%  CI_CALL_BREAKD  = 3  break
 *%Z%
 *%Z%  Constants used:
 *%Z%
 *%Z%  CI_CI_MAX_COMMENT_LEN = 45000 bytes
 *%Z%
 *%Z%  ---------------------------------------------------------------------
 *%Z%  Reverses the input parameter string and returns the result as the
 *%Z%  value to be assigned to the application model file variable
 *%Z%
 *%Z%  Function Call:
 *%Z%
 *%Z%  *val = EXEC_INP(reversi abc);
 *%Z%
 *%Z%  Result: *val is assigned the value "cba")
 *%Z%
 *%Z%  ----------------------------------------------------------------------
 *%Z%
 *%Z%  Very Important: always restrict the length of comment_out. If strncat
 *%Z%  is used then a terminating '\0' is automatically  placed at the end
 *%Z%  of the string, even if the full CI_MAX_COMMENT_LEN bytes are written
 *%Z%
 *%Z%  ----------------------------------------------------------------------
 *%Z%  INPUTS:  char *parm_list_input   input parameter string pointer
 *%Z%           int   parmcount         No. of tokens in *parm_list_input
 *%Z%
 *%Z%  OUTPUTS: char *comment_out       output/result buffer
 *%Z%           int  *comlen            length (in bytes) of comment data 
 *%Z%           int  *state_out         success state of the function call
 *%Z%
 *%Z%=======================================================================
 *==========================================================================
 *
 *  WRITTEN BY:  Eric Furmanek, SSTD-R&D    DATE: 1993
 *
 *  CHANGES   : 
 *
 ***************************************************************************/

#include <stdio.h>
#include <unistd.h>


int firstcall = 1;
// Change me to python location or use a system call to set me like "which python"
static char *pyprog = "/home/m/opt/bin/python";
void py (
        char  *parm_list_input,
        int    parmcount,
        char  *comment_out, 
        int   *comlen,
        int   *state_out
    )
{
  int pyret;
  char buf[65535];
  getcwd(buf,65535);
  static PyObject *px, *global_dict, *main_module, *x_str_obj;
  char *x_str;
  char *waste;
  char *tmp;
  char *progname;
  char *py_argv[2];

  printf("py running: %s\nfrom directory: %s\n\n",parm_list_input,buf);
  tmp=buf;
  waste=buf;
  while( (tmp = strstr(tmp+1,"waste")) !=NULL ) waste=tmp;
  sprintf( waste, "py/main.py" );
  py_argv[0]="";
  py_argv[1]=0;

  if( firstcall ) {
    firstcall=0;
    Py_SetProgramName(pyprog);
  }

  

 

  // If 'db' is the first word in the string or it is preceeded only by whitespace
  // and if db is followed by whitespace, then strip db and the whitespace
  // from the string and reload all python modules.
  char *tmp_pli, *first_tok;
  tmp_pli = strdup(parm_list_input);  

  first_tok = strsep(&tmp_pli," \t\r\n");
  if( first_tok != NULL ) {
    if( strcasecmp( first_tok, "db" ) == 0 ) {
      parm_list_input = parm_list_input + 1 + strlen(first_tok);
      printf("Found \'db\' at start of command string.  Reloading python modules.\n");
      if( Py_IsInitialized() ) {
	Py_Finalize();
      }
    }
  }
  free(first_tok);

  if( !Py_IsInitialized() ) {
    Py_Initialize();
    // buf now contains a path to main.py

    PySys_SetArgv(1,py_argv);
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('../py')");
    PyRun_SimpleString("sys.path.append('../py/contrib')");
//    PyRun_SimpleString("from ci_util import *");
    PyRun_SimpleString("from main import *");
    PyRun_SimpleString("print sys.version");
    
    main_module = PyImport_AddModule("__main__");
    global_dict = PyModule_GetDict(main_module);
    
  }

  PyRun_SimpleString("x=\'\'");
  sprintf(buf, "x=%s",parm_list_input);
  pyret = PyRun_SimpleString(buf);
  
  px = PyDict_GetItemString(global_dict,"x");
  x_str_obj = PyObject_Str( px );
  x_str = PyString_AsString( x_str_obj);
  
  strcpy(comment_out,x_str);
  *comlen = strlen(comment_out);
  

  if( pyret != 0  ) {
    *state_out = CI_TEST_FAIL;
  } else {
    *state_out = CI_TEST_PASS;
  }
}

