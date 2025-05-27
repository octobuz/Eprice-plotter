This is a simple program to save a PNG image of Nord Pool electricity prices. There are 48 values in the plot, one for each hour. The prices are updated at 14:00 o'clock, if there are no delays. The prices are from: https://porssisahko.net/api.

To build and run this program you need to do:

  
1. $ docker build -t ummagamma/eprice-plotter .

2. $ docker run -v $(pwd):/app ummagamma/eprice-plotter

...DONE!
 
The image is saved to your working directory. 
The image is overwritten on each run.