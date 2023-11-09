#include <stdlib.h>
#include <stdio.h>
#include <sys/resource.h>
#include <math.h>

void set_seed(int seed) 
{
    srand(seed);
}

void set_screen(
    int* screen, 
    int resX,  
    int* pixelX, 
    int* pixelY, 
    int size) 
{
    // Count where the steps fall on the screen
    for (int i = 0; i < size; i++) {
        printf("--------");
        printf("i=%d\n",i);
        screen[pixelX[i] + resX*pixelY[i]]++;
        printf("Value at screen[%d]: %d",pixelX[i] + resX*pixelY[i],screen[pixelX[i] + resX*pixelY[i]]);
    }
}

void fit_to_screen(
    double* stepsX, 
    double* stepsY, 
    int* pixelX, 
    int* pixelY,
    int resX, 
    int resY, 
    double minX, 
    double maxX, 
    double minY, 
    double maxY,
    int size) 
{
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    printf("*****Got here*****");
    double rangeX = maxX - minX;
    double rangeY = maxY - minY;

    // Compute scaling factor for new basis:
    // (res - 1) necessary as pixels are counted from 0, but scaling math doesn't by default.
    double scalerX = (resX - 1) / rangeX; // DIV 0 RISK
    double scalerY = (resY - 1) / rangeY; // DIV 0 RISK

    // Translate min -> 0 for all points, then multiply by scaler.
    // Round to nearest pixel.
    for (int i = 0; i < size; i++) {
        pixelX[i] = (int) round((stepsX[i] - minX) * scalerX);
        pixelY[i] = (int) round((stepsY[i] - minY) * scalerY);
    }
}

void update_bounds(
    double x, 
    double y,
    double* minX, double* maxX,
    double* minY, double* maxY) 
{
    // // Check for new X min/max
    // if (x < *minX) {
    //     *minX = x;
    // } else if (x > *maxX) {
    //     *maxX = x;
    // }

    // // Check for new Y min/max
    // if (y < *minY) {
    //     *minY = y;
    // } else if (y > *maxY) {
    //     *maxY = y;
    // }

    *minX = (*minX < x) ? *minX : x;
    *maxX = (*maxX > x) ? *maxX : x;
    *minY = (*minY < y) ? *minY : y;
    *maxY = (*maxY > y) ? *maxY : y;

}

void compute_targets(
    int size, 
    int num_anchors,
    int* targets) 
{
    // Populate targets array
    for (int i = 0; i < size; i++) {
        targets[i] = rand() % num_anchors;
    }
}

void compute_steps(
    int size, 
    double distFactor, 
    double startX, 
    double startY,
    int num_anchors,
    double* anchorX,
    double* anchorY,
    int* target,
    int resX,
    int resY,
    double* stepsX,
    double* stepsY,
    int* pixelX,
    int* pixelY,
    double minX,
    double maxX,
    double minY,
    double maxY)
{
    // First step initialization
    stepsX[0] = startX;
    stepsY[0] = startY;

    for (int i = 1; i < size; i++) {
        // Compute next step
        stepsX[i] = stepsX[i-1] + (anchorX[target[i]] - stepsX[i-1]) * distFactor;
        stepsY[i] = stepsY[i-1] + (anchorY[target[i]] - stepsY[i-1]) * distFactor;
        update_bounds(stepsX[i], stepsY[i], &minX, &maxX, &minY, &maxY);
    }

}