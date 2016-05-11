### Visual Calculus

#### Description
This project aims to help individuals understand and interact with the Fundamental Theorem of Calculus in a purely visual and geometric way. We hope to help learners build an intuition for the relationships among a line and its corresponding derivative and integral through an interactive window where users begin by drawing an input curve. Afer the curve is drawn, it's corresponding integral and derivative are displayed and users may adjust these lines and observe how they change in relation to one another. Users may also view corresponding tangent lines and areas to connect the functions of derivatives and integrals to their properties as lines. We hope this module will act as a supplement to traditional textbook explanations and will be a userful tool for both teachers and learners.

#### Getting started
This module requires scipy, numpy, OpenCV, and pygame. 

To install these in a linux system use:

 ` sudo apt-get install python-numpy python-scipy python-pygame python-opencv`
 
To install these in other operating systems visit:

Pygame:
http://www.pygame.org/download.shtml

OpenCV:
http://docs.opencv.org/3.1.0/d5/de5/tutorial_py_setup_in_windows.html#gsc.tab=0

Scipy and numpy:
http://www.numpy.org/

#### Usage
To use the program, run main.py.

`  python main.py`

Toggle on the draw button in the bottom left corner to begin. Click once to begin drawing and again to stop. From there, use the buttons to view tangent lines, critical points and more. Toggle on the camera button to draw a curve using webcam. (A tennis ball works well).

#####Keyboard shortcuts 

't': Turn on/off show tangents
 
'a': Turn on/off show area under curve

'c': Turn on/off show critical points

'h': Turn on/off legend

'g': Turn on/off grid

Space: draw with open CV and stop drawing

Right click: clear screen

's': Save the current screen as a image. run main.py from terminal or other interactive python, and you will be prompted to enter your prefered filename ex.(screen.png)

##### Open CV drawing colors
The current two colors are bright\_green and bright\_pink. bright\_green works with a tennis ball and any light green colored sticky notes. bright\_pink works well with bright pink sticky notes. To change the drawing color, modify color = 'bright_pink' in Control.py (line 20). 

To add a drawing color for open CV, find a color range for the given color at http://colorizer.org/. Color range is in HSV and open CV has the following HSV range: H: 0-180, S: 0 -255, V: 0-255. Convert the values if necessary. In Control.py add the color range and the color name to the dictionary *colors* on top of the page. 

##### Changing screen size
The current screen size is 800 by 800 pixels. To change it, modify line 21 in view.py : screen_size = (x,y).

##### Changing mode of moving curve in code
There are two ways to move the curve around. The default is 'Handle'. To experiment with the other mode 'Curve', change line 23 in Control.py to pull_mode = 'Curve'. Save the script and run again.

##### Known Bugs
Open CV calibration does not work.

#### Authors
[Matthew Beaudouin-Lafon](https://github.com/MatthewBeaudouinLafon), [March Saper](https://github.com/mesrumpled), [Xiaoxheng Xu](https://github.com/xiaozhengxu) 

Attribution to http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/ for Open CV object tracking.

#### License
Refer to  GNU GENERAL PUBLIC LICENSE
Copyright (c) [2016] [Contributors above]
