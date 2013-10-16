
PYCFLAGS=$(shell pkg-config --cflags python)
PYLDFLAGS=$(shell pkg-config --libs python)

CFLAGS+=-I /opt/hp93000/soc/pws/lib/ -I /opt/hp93000/soc/mix_sgnl/include -I /opt/hp93000/soc/com/include/ -I /opt/hp93000/soc/prod_com/include/ $(PYCFLAGS)

LDFLAGS+=-L/opt/hp93000/soc/pws/sh_lib -L/opt/hp93000/soc/prod_com/sh_lib -lcicpi -lAMST -shared -Wl,-rpath,/opt/hp93000/soc/pws/sh_lib:/opt/hp93000/soc/prod_com/sh_lib $(PYLDFLAGS)

all: t1.so

t1.so: t1.c t1.i t1.h
	echo pyflag: $(PYFLAG)
	gcc $(CFLAGS) $(LDFLAGS) -o t1.so t1.c

clean:
	rm -f *.o *.so

depend:
	echo depend

