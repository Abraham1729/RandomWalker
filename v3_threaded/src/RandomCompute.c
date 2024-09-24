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
    int maxScore = 0;
    // Count where the steps fall on the screen
    for (int i = 0; i < size; i++) {
        screen[pixelX[i] + resX*pixelY[i]]++;
        if (screen[pixelX[i] + resX*pixelY[i]] > maxScore) maxScore++;
    }
}

void fit_to_screen(
    int size,
    double* stepsX,
    double* stepsY,
    double minX, 
    double maxX, 
    double minY, 
    double maxY,
    int resX,
    int resY,
    int* pixelX,
    int* pixelY)
{
    double rangeX = maxX - minX;
    double rangeY = maxY - minY;

    // Compute scaling factor for new basis:
    double scalerX = (resX - 1) / rangeX;
    double scalerY = (resY - 1) / rangeY;

    // Translate min -> 0 for all points, then multiply by scaler.
    // Round to nearest pixel.
    for (int i = 0; i < size; i++) {
        pixelX[i] = (int) round((stepsX[i] - minX) * scalerX);
        pixelY[i] = (int) round((stepsY[i] - minY) * scalerY);
    }
}

void compute_bounds (
    double* minX, double* maxX,
    double* minY, double* maxY,
    double* stepsX,
    double* stepsY,
    int length)  
{
    for (int i = 0; i < length; i++) {
        *minX = (*minX < stepsX[i]) ? *minX : stepsX[i];
        *maxX = (*maxX > stepsX[i]) ? *maxX : stepsX[i];
        *minY = (*minY < stepsY[i]) ? *minY : stepsY[i];
        *maxY = (*maxY > stepsY[i]) ? *maxY : stepsY[i];
    }
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
    int iter, 
    double* anchorX,
    double* anchorY,
    int* target,
    double distFactor, 
    double* stepsX,
    double* stepsY)
{
    for (int i = 1; i < iter; i++) {
        // Compute next step
        stepsX[i] = stepsX[i-1] + (anchorX[target[i]] - stepsX[i-1]) * distFactor;
        stepsY[i] = stepsY[i-1] + (anchorY[target[i]] - stepsY[i-1]) * distFactor;
    }
}