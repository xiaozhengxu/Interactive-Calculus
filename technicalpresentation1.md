## Technical Review Preparation and Framing
### Matthew Beaudouin, March Saper, Judy Xu

#### Background and context

The main idea of our project is to create a interactive math app that helps students/people understand calculus. The purpose of this project is to allow the user to interact with the Fundamental Theorem of Calculus in a purely visual and geometric way, eliminating equations and allowing the user to build a geometrically intuitive understanding of the theorem. Our minimum viable product is to take a mouse-drawn function, and display its derivative graphically. Our main goal is to take a drawn function drawn in the air, convert it with openCV, display it’s derivative, and corresponding integral function. Our stretch stretch goal is to put this online.  

Currently input from user drawn curves is taken in as a list of coordinate tuples and smoothed using scipy’s interpolate. To display the various curves we are using matplotlib as a backend with pygame. The raw data from pygame graphics is therefore displayed in a pygame window. We chose this to allow for interactivity but also ease of graphing. 

At the moment we envision the UX as one window where the curve will be displayed. Interaction will take place with openCV. Users will be able to draw the curve and see it’s derivative and integral. Users may also be able to interact with the curve, finding inflection points and/or adjusting the curve by dragging points. 


#### Key questions

We would like to get input from other students about the user interaction our program will have. This does not require much technical explanation or understanding but would be very valuable to us in the design of our interactive window. In addition, input on functionality would be valuable at this stage as we have time to schedule additions.

At this stage in our code, we have three technical questions that would also be valuable to talk about. The first is on overall code architecture. We would like suggestions on how the “flow of information” should go. (This is more easily explained with visuals which we will have in our presentation.) Currently information about the mouse position goes into a controller’s update method which calls appropriate update methods for curve. We would like thoughts on this and how things should fit in the model view controller framework. Second, we would like suggestions on openCV input. OpenCV tracks pixels of a certain color, but we are trying to decide which colored pixels should be used when making our graphs. Third, we want to include a functionality where users can drag points on the graphed line to create a new curve. We have two methods for accomplishing this, which will be more fully explained in the presentation. We would like input on these or suggestions of other ways to accomplish this functionality.



#### Agenda for technical review session

Our agenda is as follows:

Background - 3 minutes

Code presentation - 3 minutes

Pseudo-Code questions - 12 minutes

UX questions - 7 minutes

We will communicate with our audience through visuals. These visuals will include pseudocode, class diagrams, and screenshots of our current progress. We hope to have productive collaborative, technical and software architecture discussions.
