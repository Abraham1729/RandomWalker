all: compute

compute: v2/src/RandomCompute.c
	mkdir -p v2/bin
	gcc -shared -o v2/bin/RandomCompute.so v2/src/RandomCompute.c

clean:
	rm -rf v2/bin