//
//  Mandelbrot.metal
//  Mandelbrot Set
//
//  Created by Sai Hemanth Bheemreddy on 26/05/20.
//  Copyright © 2020 Sai Hemanth Bheemreddy. All rights reserved.
//

#include <metal_stdlib>
using namespace metal;

struct parameters {
    float width;
    float height;
    float scaleX;
    float scaleY;
    float panX;
    float panY;
    uint maxIterations;
};

kernel void compute(texture2d<float, access::write> texture,
                    const device parameters &params,
                    uint2 gid [[thread_position_in_grid]]) {
    float x0 = (gid.x - params.panX) * params.scaleX;
    float y0 = (gid.y - params.panY) * params.scaleY;
    float x = 0, y = 0;
    uint iteration = 0;
    
    while(x*x + y*y <= 4 && iteration < params.maxIterations) {
        float xTemp = x*x - y*y + x0;
        y = 2*x*y + y0;
        x = xTemp;
        iteration++;
    }
    
    float a = 0.1, n = float(iteration);
    vec<float, 4> color = float4(0.5f * sin(a * n) + 0.5f,
                                 0.5f * sin(a * n + 2.094f) + 0.5f,
                                 0.5f * sin(a * n + 4.188f) + 0.5f,
                                 1.0);
    texture.write(color, gid);
}
