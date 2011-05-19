HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3

PYTHON_ROOT=/home/m/opt
#
# Agilent 93000 Makefile
#
HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
# Avoid influences from user's shell startup file
ENV=

# Name of makefile
MAKEFILE=Makefile

# Base for target name
NAME=libcifset

# destination base path for libraries and programs
DEST=.

#
#
GENERATED_HEADERS=

# $(SRCS) is the list of source files used.
# $(SRCS) is given as argument to makedepend to create the dependency information
SRCS=$(filter-out ~%, $(wildcard *.c *.C *.cpp))

# List of object files to be created
# Usually, OBJS contains one file for each file in SRCS
# Assuming that SRCS contains only .c, .C, .cpp, .l and .y files,
# OBJS can be obtained from SRCS as follows.
# But it is also possible to define OBJS explicitely if you wish
# to have object files in OBJS whose sources are not in SRCS.
# Since SRCS is only used for makedepend, these object files
# would also be built, but makedepend would create no dependency
# rules for them.
OBJS_L=$(SRCS:.l=.o)
OBJS_Y=$(OBJS_L:.y=.o)
OBJS_C=$(OBJS_Y:.C=.o)
OBJS_CPP=$(OBJS_C:.cpp=.o)
OBJS=$(sort $(OBJS_CPP:.c=.o))

# archive libraries to be linked to target
LIBS=

# shared libraries to be linked to target
SH_LIBS= -Wl,-rpath,: 

# system libraries to be linked to target, like -lm -lX11 etc.
SYSLIBS=-lm -lpython2.7 -L$(PYTHON_ROOT)/lib -lpthread -lutil -ldl

# External object files required to build target
EXTERNAL_OBJS=

# dependency directories to build libraries and objects
ifeq ($(HP83000_ROOT),/opt/hp93000/soc)
        BUILD_DIRS=
else
        BUILD_DIRS= 
endif
# 
# Compilers to be used.
# If the scripts CC_hp83000 and CCP_hp83000 are used, they may
# have options to enable support of purify, purecover, insure or dmalloc.
# These options are specified as purify=[yes|no|<debug tool config file>].
# The default configuration files for the debug tools are located in $(HP83000_ROOT)/com/lbin
CC=/usr/bin/gcc
CXX=/usr/bin/g++

# Compile flags to be used
CFLAGS=-fpic -I $(PYTHON_ROOT)/include -I $(HP83000_ROOT)/pws/lib -I$(HP83000_ROOT)/prod_com/include -I$(HP83000_ROOT)/com/include -I$(HP83000_ROOT)/mix_sgnl/include -I $(HP83000_ROOT)/pws/include -O -D_EXTENDED_ANSI -DHP83000_ROOT=\"/opt/hp93000/soc\" -DHP83000_REVISION=\"5.4.3\" -DWIZARD_ESCAN=0 -DNDEBUG -DHP93_SOC -DHP83_F330 -DWIZARD_NYI=1 -DX11R5 -Didnumber=domainname -DOS_LINUX -D_GNU_SOURCE -DHP_UX_10 -DJDK_13 -Wall
CFLAGS_DEBUG=-g -fpic -I $(PYTHON_ROOT)/include -I $(HP83000_ROOT)/pws/lib -I$(HP83000_ROOT)/prod_com/include -I$(HP83000_ROOT)/com/include -I$(HP83000_ROOT)/mix_sgnl/include -I $(HP83000_ROOT)/pws/include -O -D_EXTENDED_ANSI -DHP83000_ROOT=\"/opt/hp93000/soc\" -DHP83000_REVISION=\"5.4.3\" -DWIZARD_ESCAN=0 -DNDEBUG -DHP93_SOC -DHP83_F330 -DWIZARD_NYI=1 -DX11R5 -Didnumber=domainname -DOS_LINUX -D_GNU_SOURCE -DHP_UX_10 -DJDK_13 -Wall
CXXFLAGS=-I $(HP83000_ROOT)/pws/lib -I$(HP83000_ROOT)/prod_com/include -I$(HP83000_ROOT)/com/include -I$(HP83000_ROOT)/mix_sgnl/include -I $(HP83000_ROOT)/pws/include -O -D_EXTENDED_ANSI -DHP83000_ROOT=\"/opt/hp93000/soc\" -DHP83000_REVISION=\"5.4.3\" -DWIZARD_ESCAN=0 -DNDEBUG -DHP93_SOC -DHP83_F330 -DWIZARD_NYI=1 -DX11R5 -Didnumber=domainname -DOS_LINUX -D_GNU_SOURCE -DHP_UX_10 -DJDK_13 -DStd=std -DUSING_NAMESPACE_STD=using\ namespace\ std\; -Wall
CXXFLAGS_DEBUG=-g -I $(HP83000_ROOT)/pws/lib -I$(HP83000_ROOT)/prod_com/include -I$(HP83000_ROOT)/com/include -I$(HP83000_ROOT)/mix_sgnl/include -I $(HP83000_ROOT)/pws/include -O -D_EXTENDED_ANSI -DHP83000_ROOT=\"/opt/hp93000/soc\" -DHP83000_REVISION=\"5.4.3\" -DWIZARD_ESCAN=0 -DNDEBUG -DHP93_SOC -DHP83_F330 -DWIZARD_NYI=1 -DX11R5 -Didnumber=domainname -DOS_LINUX -D_GNU_SOURCE -DHP_UX_10 -DJDK_13 -DStd=std -DUSING_NAMESPACE_STD=using\ namespace\ std\; -Wall

LD=/usr/bin/gcc
LDFLAGS=-L/usr/X11R6/lib

YACC=/usr/bin/bison
YFLAGS=-d

LEX=/usr/bin/flex
LFLAGS=

PATH=/bin:/usr/bin:/usr/atria/bin:/opt/aCC/bin:/opt/langtools/bin
SHELL=/bin/ksh

# Files to remove in make clean or make clobber
CLEAN_FILES=$(OBJS) core *~
HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
CLOBBER_FILES=$(SHARED_LIBRARY) $(CI) Makefile.bak makefile.Template

CI_BIN_SOURCE="${HP83000_ROOT}/prod_env/bin"
CI_TARGET =  .
CI = Ci

GEN_CI_SCRIPT = $(HP83000_ROOT)/prod_env/lbin/gen_ci_script_ddd
GEN_CI_SCRIPT_GDB = $(HP83000_ROOT)/prod_env/lbin/gen_ci_script_gdb
GEN_CI_SCRIPT_DDD = $(HP83000_ROOT)/prod_env/lbin/gen_ci_script_ddd

SHARED_LIBRARY=$(DEST)/$(NAME).so

all:	$(SHARED_LIBRARY)
	@rm -f $(CI_TARGET)/$(CI).d
	@rm -f $(CI_TARGET)/$(CI)
	@ln -s $(CI_BIN_SOURCE)/ci_function $(CI_TARGET)/$(CI)

debug symbol:
	$(MAKE) -f $(MAKEFILE) debugddd

debugxdb:
	$(MAKE) -f $(MAKEFILE) CFLAGS="$(CFLAGS_DEBUG)" CXXFLAGS="$(CXXFLAGS_DEBUG)" $(SHARED_LIBRARY)
	@rm -f $(CI_TARGET)/$(CI).d
	@ln -s $(CI_BIN_SOURCE)/ci_function.d $(CI_TARGET)/$(CI).d
	@rm -f $(CI_TARGET)/$(CI)
	@$(GEN_CI_SCRIPT_GDB)
	@chmod +x $(CI_TARGET)/$(CI)

debuggdb:
	$(MAKE) -f $(MAKEFILE) CFLAGS="$(CFLAGS_DEBUG)" CXXFLAGS="$(CXXFLAGS_DEBUG)" $(SHARED_LIBRARY)
	@rm -f $(CI_TARGET)/$(CI).d
	@ln -s $(CI_BIN_SOURCE)/ci_function.d $(CI_TARGET)/$(CI).d
	@rm -f $(CI_TARGET)/$(CI)
	@$(GEN_CI_SCRIPT_GDB)
	@chmod +x $(CI_TARGET)/$(CI)

debugddd:
	$(MAKE) -f $(MAKEFILE) CFLAGS="$(CFLAGS_DEBUG)" CXXFLAGS="$(CXXFLAGS_DEBUG)" $(SHARED_LIBRARY)
	@rm -f $(CI_TARGET)/$(CI).d
	@ln -s $(CI_BIN_SOURCE)/ci_function.d $(CI_TARGET)/$(CI).d
	@rm -f $(CI_TARGET)/$(CI)
	@$(GEN_CI_SCRIPT_DDD)
	@chmod +x $(CI_TARGET)/$(CI)

SRCS=$(filter-out ~%, $(wildcard *.c *.C *.cpp))

HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
# Build shared library
$(SHARED_LIBRARY):     $(OBJS) $(BUILD_DIRS) $(EXTERNAL_OBJS) $(LIBS) 
	$(LD) -shared -Wl,-Bdynamic $(LDFLAGS) $(SH_LIBS) \
	      $(OBJS) $(EXTERNAL_OBJS) $(LIBS) $(SYSLIBS) \
	      -o $(SHARED_LIBRARY)

HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3
HP83000_ROOT=/opt/hp93000/soc
HP83000_REVISION=5.4.3

clean:
	rm -f $(CLEAN_FILES)

clobber:
	rm -f $(CLEAN_FILES) $(CLOBBER_FILES)

# create 'makefile' out of 'Makefile' with added dependencies
# The command `echo $(CC) | cut -d ' ' -f1` below returns the first word
# of $(CC). $(CC) might contain addidional options (e.g. for purify support).
# makedepend needs to know, which compiler is used, because if a script like
# CC_hp83000 or CCP_hp83000 is used, makedepend needs to know, which options
# (include paths etc.) are set in the compiler script. makedepend then
# calls the compile script with the option -queryCompileFlags and expects the
# script to output the the options it uses for the compiler to stdout.
# Also add rules for building $(BUILD_DIRS) that create libraries and
# objects that are linked into the executable.
depend:
	@$(HP83000_ROOT)/com/lbin/makedepend -f $(MAKEFILE) \
	                -c `echo $(CC) | cut -d ' ' -f1` \
	                -C `echo $(CXX) | cut -d ' ' -f1` \
	                -- -CFLAGS $(CFLAGS) \
	                   -CXXFLAGS $(CXXFLAGS) \
	                   -BUILD_DIRS $(BUILD_DIRS) \
	                -- \
	                $(SRCS)

# install nothing (target used for compatibility only)
install:
	@echo "nothing to be installed"

$(OBJS): $(GENERATED_HEADERS)
MTMS =  
MTTS =  
# DO NOT DELETE THIS LINE -- make depend depends on it.

# AUTOMATICALLY GENERATED WITH "make depend"
# DO NOT CHANGE

# Dependencies of files generated with /usr/bin/g++
#    use CXXFLAGS:  -I /opt/hp93000/soc/pws/lib -I/opt/hp93000/soc/prod_com/include -I/opt/hp93000/soc/com/include -I/opt/hp93000/soc/mix_sgnl/include -I /opt/hp93000/soc/pws/include -O -D_EXTENDED_ANSI -DHP83000_ROOT="/opt/hp93000/soc" -DHP83000_REVISION="5.4.3" -DWIZARD_ESCAN=0 -DNDEBUG -DHP93_SOC -DHP83_F330 -DWIZARD_NYI=1 -DX11R5 -Didnumber=domainname -DOS_LINUX -D_GNU_SOURCE -DHP_UX_10 -DJDK_13 -DStd=std -DUSING_NAMESPACE_STD=using namespace std; -Wall
###

# Dependencies of files generated with /usr/bin/gcc:
#    use CFLAGS:  -fpic -I /opt/hp93000/soc/pws/lib -I/opt/hp93000/soc/prod_com/include -I/opt/hp93000/soc/com/include -I/opt/hp93000/soc/mix_sgnl/include -I /opt/hp93000/soc/pws/include -O -D_EXTENDED_ANSI -DHP83000_ROOT="/opt/hp93000/soc" -DHP83000_REVISION="5.4.3" -DWIZARD_ESCAN=0 -DNDEBUG -DHP93_SOC -DHP83_F330 -DWIZARD_NYI=1 -DX11R5 -Didnumber=domainname -DOS_LINUX -D_GNU_SOURCE -DHP_UX_10 -DJDK_13 -Wall
### 
fn_templ.o: fn_templ.c /opt/hp93000/soc/pws/lib/tpi_c.h \
  /opt/hp93000/soc/com/include/machine.h \
  /opt/hp93000/soc/com/include/largefile.h \
  /opt/hp93000/soc/com/include/luna_endian.h \
  /opt/hp93000/soc/mix_sgnl/include/adiUserI.h \
  /opt/hp93000/soc/mix_sgnl/include/adi.h \
  /opt/hp93000/soc/com/include/ci_types.h \
  /opt/hp93000/soc/prod_com/include/libcicpi.h
pyproc.o: pyproc.c /opt/hp93000/soc/pws/lib/tpi_c.h \
  /opt/hp93000/soc/com/include/machine.h \
  /opt/hp93000/soc/com/include/largefile.h \
  /opt/hp93000/soc/com/include/luna_endian.h \
  /opt/hp93000/soc/mix_sgnl/include/adiUserI.h \
  /opt/hp93000/soc/mix_sgnl/include/adi.h \
  /opt/hp93000/soc/com/include/ci_types.h \
  /opt/hp93000/soc/prod_com/include/libcicpi.h
