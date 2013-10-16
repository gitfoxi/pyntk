
/* 
#include "Python.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <assert.h>
#include "tpi_c.h"
#include "adiUserI.h"
#include "ci_types.h"
#include "libcicpi.h"

#define BUF_LEN 65536

char buf1[ BUF_LEN ];
char buf2[ BUF_LEN ];
INT32 fw_ret;


#include "t1.h"

// A simple interface to firmware commands that don't return any crazy
// huge binary strings or anything:
// 
// returns pointer to answer on success ( buf2 )
// returns 0 on failure
// places return code in global fw_ret
//
//
// WARNING: Will die horribly if buffers overflow.
//
/*
char* fw(char* cmd) {
  INT32 cmd_len,ans_len;

  //TODO: dynamic reallocation in case of buffer too small
  // or split a large command into many small ones.
  assert( strlen(cmd) < BUF_LEN );

  strcpy(buf1,cmd);
  cmd_len = strlen(buf1);
  strcpy((buf1+cmd_len),"\n");
  cmd_len++;

  ans_len = BUF_LEN-1;
  HpFwTask(buf1, &cmd_len, buf2, &ans_len, &fw_ret);

  buf2[ans_len]=0;
  return buf2;
  
}

// Returns 1 on pass, 0 on fail, -1 on error
int ftst() {
  char* r;

  r = fw("FTST?");

  if( !r ) {
    printf("ftst() error number %d\n",(int)fw_ret);
    return -1;
  }

  if(*(r+5) == 'P') {
    return 1;
  }

  return 0;
}

void atexit_cleanup(void) {
  HpTerm();
  printf("HpTerm() -- byebye 93k\n");
}



int dErr;
char dErrMsg[ BUF_LEN ];

void throw_error(char* s) {
  dErr = 1;
  strcpy(dErrMsg,s);
  printf("Throwing error: %s\n",dErrMsg);
}

char* dTsName() {
  int status;
  status = GetTestsuiteName( buf1 );

  if( status != 0 ) {
    throw_error("Internal error in GetTestsuiteName");
    strcpy( buf1, "NoNameLoaded" );
  }

  return buf1;
}

int test_throw_error() {
  throw_error("test_throw_error succeeded.");
  return 1;
}
*/
