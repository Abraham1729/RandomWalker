all: compute

compute: v3/src/RandomCompute.c
	mkdir -p v3/bin
	gcc -shared -o v3/bin/RandomCompute.so v3/src/RandomCompute.c

clean:
	rm -rf v3/bin