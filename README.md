# Requirements
1. OpenCV with contrib
2. numpy
3. sklearn
4. matplotlib
5. pillow
6. Python 2.7

# Part 1

Before you run p1.py, you may need to edit this file to adjust some parameters as follow:

1. sample_rect: a array of 4 elements indicating the position(x,y) and size(height,width) of simpling area. In our case, we set it to (1300,1300,100,100).
2. channel: a int specifying which channel we are dealing with. 0 for Blue, 1 for Green and 2 for Red.

Then, you can get linear regression and its plot by running p1.py.

# Part 3&4

In part 3 we generate HDR composite images with three different algorithms as required, and part 4 we make tone map images of the three outputs from three HDR composite algorithms. So we write the part 3 and part 4 in the hdr.py such that we could acquire the result of simple_linear() function to do HDR composite and then make use of HDR composite results to do tone map. 

Before you run hdr.py, you may need to madify the following paremeters if you need:

1. threshold: this is the value we use to determine whether the pixel value is sturated in the HDR composite algorithms. We tried a lot of times that the 255 is not ideal value, so we set the value to be 200 as the default value in the hdr.py, you may modify the value if you want to see different outputs image from the HDR composite algorithm.
2. gam_value: When we use the tone map function, there is a gamma correction parameter gamma need to be set, we read from the OpenCV API that the gamma is positive value of type float. Generally speaking, if gamma > 1 the function will brighten the image, if gamma < 1 the function will darken the image. The gamma value of 1.0 implies no correction, $gamma$ equal to 2.2 is suitable for most displays. We set 2.2 to be the default value in hdr.py, you may change the value if you would like to see different outputs of tone map function.

After you run hdr.py, you may find the output images in the following directories:

1. /hdr/combined: the outputs of three HDR comosite algorithms will be saved in this directory.
2. /hdr/tonemapped: the outputs of the tone map function for three HDR composite algorithms will be saved in this directory.
