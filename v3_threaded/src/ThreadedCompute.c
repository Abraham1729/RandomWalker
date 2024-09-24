#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/resource.h>
#include <math.h>

typedef struct {

} thread_arg_t;

static void* thread_main(void* p_arg) {
    return NULL;
}

int num_threads = 1;

int run_compute_pipeline() {
    // // need to get the num_threads from python
    // // needs to do the following
    // compute_targets()
    // - set_seed(seed)
    // - compute_target(iter, num_anchors)
    // compute_steps()
    // - set_seed(seed)
    // - compute_steps(iter, x/y anchors, dist, stepsX/Y (in AND later read out), min/max X/Y)
    // Modification: Drop the max/mins and leave that to Python? Might be a bad idea if checking 100m items...
    return 0;
}