#include <stdlib.h>
#include <stdio.h>
#include <sys/resource.h>

void targets_and_steps(int size, int* target, double distFactor, double* stepsX, double* stepsY, int num_anchors, double* anchorX, double* anchorY) {
    // Initial step:
    target[0] = rand() % num_anchors;
    stepsX[0] = 0;  // hard coded start at (0,0)
    stepsY[0] = 0;  // hard coded start at (0,0)

    // Populate "Target" array, compute "steps" arrays
    for (int i = 1; i < size; i++)
    {
        target[i] = rand() % num_anchors;
        stepsX[i] = stepsX[i-1] + (anchorX[target[i]] - stepsX[i-1]) * distFactor;
        stepsY[i] = stepsY[i-1] + (anchorY[target[i]] - stepsY[i-1]) * distFactor;
    }
}

void compute_targets(int size, int num_anchors, int* target) {
    for (int i = 0; i < size; i++) {
        target[i] = rand() % num_anchors;
    }
}

void compute_steps(int size, int* target, double distFactor, double* stepsX, double* stepsY, int num_anchors, double* anchorX, double* anchorY) {
    stepsX[0] = 0;  // still hard coding (0,0)
    stepsY[0] = 0;
    for (int i = 1; i < size; i++) {
        stepsX[i] = stepsX[i-1] + (anchorX[target[i]] - stepsX[i-1]) * distFactor;
        stepsY[i] = stepsY[i-1] + (anchorY[target[i]] - stepsY[i-1]) * distFactor;
    }
}

void set_seed(int seed) {
    srand(seed);
}