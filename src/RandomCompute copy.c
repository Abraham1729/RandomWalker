#include <stdlib.h>
#include <stdio.h>
#include <sys/resource.h>

int* compute_targets(
    int size, 
    int num_anchors) 
{
    // Allocate memory for targets
    int* targets = (int*) malloc(size * sizeof(int));
    if (targets == NULL) perror("Failed to allocate memory!");

    // Populate targets array
    for (int i = 0; i < size; i++) {
        targets[i] = rand() % num_anchors;
    }

    // Leave it to python to manage deallocation
    return targets;
}

int* compute_steps(
    int size, 
    double distFactor, 
    double startX, 
    double startY,
    int num_anchors,
    double* anchorX,
    double* anchorY,
    double* target,
    int resX,
    int resY)
{
    // Allocate memory (Release Order)
    double* stepsX = (double*) malloc(size * sizeof(double))
    double* stepsY = (double*) malloc(size * sizeof(double))
    int* pixelY = (int*) malloc(resX * sizeof(int))
    int* pixelX = (int*) malloc(resY * sizeof(int))

    if (stepsX == NULL || stepsY == NULL || pixelX == NULL || pixelY == NULL) {
        perror("Could not allocate memory!\n");
    }


    // First step initialization
    stepsX[0] = startX;
    stepsY[0] = startY;
    double minX = startX; double maxX = startX;
    double minY = startY; double maxY = startY;

    for (int i = 1; i < size; i++) {
        // Compute next step
        stepsX[i] = stepsX[i-1] + (anchorX[target[i]] - stepsX[i-1]) * distFactor;
        stepsY[i] = stepsY[i-1] + (anchorY[target[i]] - stepsY[i-1]) * distFactor;
        update_bounds(stepsX[i], stepsY[i], minX, maxX, minY, maxY);
    }

    fit_to_screen(
        stepsX, stepsY,
        pixelX, pixelY,
        resX, resY,
        minX, maxX,
        minY, maxY
        size);

    // Free memory
    free(stepsX);
    free(stepsY);

    // Create and populate screen array
    int* screen = (int*) calloc(resX * resY * sizeof(int));
    if (screen == NULL) perror("Could not allocate memory!\n");
    set_screen(screen, resX, resY, pixelX, pixelY, size);

    // Free memory -- leave screen management to python.
    free(pixelX);
    free(pixelY);
    return(screen);
}

void fit_to_screen(
    double* stepsX, 
    double* stepsY, 
    int* pixelX, 
    int* pixelY,
    int resX, 
    int resY, 
    double minX, double maxX, 
    double minY, double maxY,
    int size) 
{

    // Compute scale of original basis:
    double rangeX = maxX - minX;
    double rangeY = maxY = minY;

    // Compute scaling factor for new basis:
    double scalerX = resX / rangeX;
    double scalerY = resY / rangeY;

    // Translate min -> 0 for all points, then multiply by scaler.
    // Round to nearest pixel.
    for (int i = 0; i < size; i++) {
        pixelX[i] = (int) round((stepsX[i] + minX) * scalerX);
        pixelY[i] = (int) round((stepsX[i] + minY) * scalerY);
    }


}

void set_screen(
    int* screen, 
    int resX, 
    int resY, 
    int* pixelX, 
    int* pixelY, 
    int size) 
{
    // loop through pixelX|Y, increment 
    for (int i = 0; i < size; i++) {
        // We get the values from pixelX|Y to transform into the 1D index for screen that needs incrementing.
        screen[pixelX[i] + resX*pixelY[i]]++;
    }
}

void set_seed(int seed) 
{
    srand(seed);
}

void update_bounds(
    double x, 
    double y,
    double minX, double maxX,
    double minY, double maxY) 
{
    // Check for new X min/max
    if (x < minX) {
        minX = x;
    } else if (x > maxX) {
        maxX = x;
    }

    // Check for new Y min/max
    if (y < minY) {
        minY = y;
    } else if (y > minY) {
        maxY = y;
    }

}