
# Overview
A product I made for myself to create custom resume and cover letters. I was tired of needing to keep multiple copies of my resume so I put everything is csv files and created a flask app to display print-to-PDF friendly resume and cover letters. It's still not usable without a bit of reading in my mind and Python skills, but it's getting closer. 

# How to use

## To setup:
1. Install Python
2. Open a terminal and type pip install Flask
3. Change the folder name from "models" to "data" and populate it
4. The parameters.py file lets you choose settings for your resume. 

## To run file: 
open a terminal and then copy and paste: 
export FLASK_DEBUG=1
flask run

# What is new 
## Added on last commit:
Refactored filtering functions in app.py
Created a new simple resume format using paged.js and rebranded old css to "funky.css"
Changed dict keys for all csv data to uniformise in english
Created a new format for FRQ grants
Splitted relevant experiences and generic experiences as two distinct resume sections.
Refactored dates formatting and gender-neutral text formatting in the filter function.