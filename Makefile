all: compute

compute: src/RandomCompute.c
	mkdir -p bin
	gcc -shared -o bin/RandomCompute.so src/RandomCompute.c

clean:
	rm -rf ./bin/RandomCompute.so
