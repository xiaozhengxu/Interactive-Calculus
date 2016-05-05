---
title: Welcome to Visual Calculus
layout: template
filename: index
--- 

### Visual Calculus?

Yes, visual calculus! This project aims to help individuals understand and interact with the Fundamental Theorem of Calculus in a purely visual and geometric way. We hope to help learners build and intuition for the relationships among a line and its corresponding derivative and integral through an interactive window where users begin by drawing an input curve. After the curve is drawn, it’s corresponding integral and derivative are displayed and users may adjust these lines and observe how they change in relation to one another. Users may also view corresponding tangent lines and areas to connect the functions of derivatives and integrals to their properties as lines. We hope this modules will act as a supplement to traditional textbook explanations and will be a useful too for both teachers and learners. See below for a visual and how to get started using our module!

![Visual Calculus](https://github.com/xiaozhengxu/Interactive-Calculus/blob/gh-pages/viscalcexample.png)

### Using Visual Calculus

#### Requirements

Our project can be cloned from [github](https://github.com/xiaozhengxu/Interactive-Calculus) or directly downloaded from the buttons above.

This module requires scipy, numpy, OpenCV, and pygame. 

To install these in a linux system use:

 ` sudo apt-get install python-numpy python-scipy python-pygame python-opencv`
 
To install these in other operating systems visit:

[Pygame](http://www.pygame.org/download.shtml), [OpenCV](http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0), [Scipy and Numpy](http://www.numpy.org/)

#### Usage
To use the program, run main.py.

`  python main.py`

Toggle on the draw button in the bottom left corner to begin. Click once to begin drawing and again to stop. From there, use the buttons to view tangent lines, critical points and more. Toggle on the camera button to draw a curve using webcam. (A tennis ball will work best.) 
