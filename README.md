This is the first part of the project for Knowledge Technologies


It uses an exact and an approximate string matching to map the reviews to a title.

- You will need a python interpreter either 2.7 or 2.6 (Tested on 2.7.10 and 2.6.6)

- Access to the UNIX commands wc, grep and agrep. 

To run in command line use: python Project2x.py

The project is written in python 2.7. However as dimefox current version of python is 2.6.6 

I provided two versions of my program Project27 and Project26 


IMPORTANT The Project26 version uses a patched function called check_output() to simulate the
subprocess.check_output() introduced in python 2.7, it seems to work well on dimefox but only use it if necesary. 
This is no my code all rights belongs to the creator
source: https://gist.github.com/edufelipe/1027906 


The file Project2x.py must be in the same directory as the file film_titles.txt that contains all titles

and a folder called revs that contains all the reviews.

It will generate a file called results.txt where the output will be in the next format:

filename.txt -> title

Where title is the best fit for the review in filename.txt 

Andres Landeta(alandeta) 631427



