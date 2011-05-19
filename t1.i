
%module t1

%{
extern int ftst();
extern void HpInit(void);
extern void HpTerm(void);
extern char* fw(char* cmd);
extern void atexit_cleanup(void);

extern char* dTsName();
extern int test_throw_error();

/* #include "TMsim.h" */
%}

%init %{
	HpInit();
	printf("HpInit() -- welcome to ntk\n");
	atexit( atexit_cleanup );
%}

extern int dErr;
extern char dErrMsg[];

extern int ftst();
extern void HpInit(void);
extern void HpTerm(void);
extern char* fw(char* cmd);

%except(python) {
  $function
  if( dErr ) {
    dErr = 0;
    PyErr_SetString( PyExc_RuntimeError, dErrMsg );
    return NULL;
  }
}

/*
extern char* dTsName();
extern int test_throw_error();

extern int TMsim_start_suite(char* testSuiteName, 
		      unsigned short lev_eq,  
		      unsigned short lev_spec,  
		      unsigned short lev_set,
		      unsigned short tim_eq,  
		      unsigned short tim_spec,  
		      unsigned short tim_set,
		      char* testFunction,
		      char* label );

extern int TMsim_log_value(char* testName,
		    double value,
		    char* PF);

extern int TMsim_end_suite(char* PF) ;
*/

