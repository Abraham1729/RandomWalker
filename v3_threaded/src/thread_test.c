#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// int NUM_THREADS = 10;
#define NUM_THREADS 10

// You'll need a custom object to pass thread arguments (single values *or* pointers)
typedef struct {
    int id;
    int* result_array;
} thread_arg_t;

static void* thread_main(void* p_arg) {
    // cast void* to thread_arg_t*
    thread_arg_t *my_arg = (thread_arg_t *) p_arg;

    // Trivial computation since we're doing POC: just update the result array for validation
    int id = my_arg->id;
    int* res_array = my_arg->result_array;
    res_array[id] = id;

    return NULL;
}

int main() {
    // Generate thread + args arrays
    pthread_t threads[NUM_THREADS];
    thread_arg_t thread_args[NUM_THREADS];
    int res_array[NUM_THREADS];

    // - Create threads and store in array
    int rc; // return caputre to validate thread creation
    for (int i = 0; i < NUM_THREADS; i++) {
        // set arguments for this thread
        thread_args[i].id = i;
        thread_args[i].result_array = res_array;
        // thread_args[i].result_rray = &res_array[0];  // This is an equivalent statement to just assigning res_array's name.

        // create thread
        rc = pthread_create(&threads[i], NULL, thread_main, &thread_args[i]);
        if (rc) { // handle case where thread creation fails (rc != 0)
            printf("pthread_create() failed for thread %d.\n",i);
            exit(-1);
        }
    }

    // - Join threads
    for (int i = 0; i < NUM_THREADS; i++)  {
        rc = pthread_join(threads[i], NULL);
        if (rc) { // handle case where thread creation fails (rc != 0)
            printf("pthread_join() failed for thread %d.\n",i);
            exit(-1);
        }
    }  
    
    // - Validate output
    for (int i = 0; i < NUM_THREADS; i++) {
        printf("res_array[%d]:\t%d\n", i, res_array[i]);
    }

    return 0;
}