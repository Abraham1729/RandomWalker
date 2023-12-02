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
    int num_anchors,
    int size)
{
    int maxScore = 0;
    // Count where the steps fall on the screen
    for (int i = 0; i < size; i++) {
        screen[pixelX[i] + resX*pixelY[i]]++;
        if (screen[pixelX[i] + resX*pixelY[i]] > maxScore) maxScore++;
    }

    // I'll be adding a loop of size num_anchors for setting the score of anchor pixels.
    // for (int i = size; i < (size + num_anchors); i++) {
    //     // I'll need to have been computing the maximum value on the screen array in the above loop
    //     // I'll be using this to determine what objective score to set for these pixels.
    //     screen[pixelX[i] + resX*pixelY[i]] = maxScore;
    // }
}

void fit_to_screen(
    int size,
    double* stepsX,
    double* stepsY,
    int show_anchors,
    int num_anchors,
    double* anchorX,
    double* anchorY,
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
    double scalerX = (resX - 1) / rangeX; // DIV 0 RISK??
    double scalerY = (resY - 1) / rangeY; // DIV 0 RISK??

    // Translate min -> 0 for all points, then multiply by scaler.
    // Round to nearest pixel.
    for (int i = 0; i < size; i++) {
        pixelX[i] = (int) round((stepsX[i] - minX) * scalerX);
        pixelY[i] = (int) round((stepsY[i] - minY) * scalerY);
    }

    // if (show_anchors) {
    //     for (int i = 0; i < num_anchors; i++) {
    //         pixelX[size + i] = (int) round((anchorX[i] - minX) * scalerX);
    //         pixelY[size + i] = (int) round((anchorX[i] - minY) * scalerY);
    //     }
    // }
}

void update_bounds(
    double x, 
    double y,
    double* minX, double* maxX,
    double* minY, double* maxY) 
{
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
    int iter, 
    int show_anchors,
    int num_anchors,
    double* anchorX,
    double* anchorY,
    int* target,
    double distFactor, 
    double* stepsX,
    double* stepsY,
    double* minX,
    double* maxX,
    double* minY,
    double* maxY)
{
    for (int i = 1; i < iter; i++) {
        // Compute next step
        stepsX[i] = stepsX[i-1] + (anchorX[target[i]] - stepsX[i-1]) * distFactor;
        stepsY[i] = stepsY[i-1] + (anchorY[target[i]] - stepsY[i-1]) * distFactor;
        update_bounds(stepsX[i], stepsY[i], minX, maxX, minY, maxY);
    }

    // If we're showing anchors we'll have to update bounds for them too.
    // if (show_anchors) {
    //     for (int i = 0; i < num_anchors; i++) { 
    //         update_bounds(anchorX[i], anchorY[i], minX, maxX, minY, maxY);
    //     }
    // }
}