# Picture of the Day Website [![HitCount](http://hits.dwyl.io/Kelian98/Picture-of-the-Day-Website.svg)](http://hits.dwyl.io/Kelian98/Picture-of-the-Day-Website)

 A simple picture of the day website created with **Flask**, **Bootstrap** and **SQLite** by [Kelian98](https://github.com/Kelian98) and [Goswatech](https://github.com/GoswaTech)
 
## Table of contents
* [General info](#general-info)
* [Features](#features)
* [Requirements](#requirements)
* [Setup](#setup)
* [Dependencies](#dependencies)
* [Inspiration](#inspiration)

## General info
People can submit their pictures to the website. Each day a different picture is featured, along with a brief explanation written by the author itself.

## Features
- People can submit picture with description, personal webpage...
- Each day a new picture is automatically chosen

**To do**:
- When form isn't validated, fields should repopulate with previous data
- Pictures are recorded and can be reached by a unique link

## Requirements
This project is built with :
- [Python](https://www.python.org/downloads/release/) >=  3.7.4
- [Flask](https://flask.palletsprojects.com/) >=  1.1.1
- [Bootstrap](https://getbootstrap.com/) >= 4.3.1

## Setup
To run this project, install it locally, go to the main folder and run :
`$ python app.py`

## Dependencies
- `pip install flask-migrate`
- `pip install flask-script`

## Inspiration
This webapp is based on [NASA Astronomy Picture of the Day](https://apod.nasa.gov/apod/astropix.html) and [Amateur Astronomy Picture of the Day websites](http://www.aapodx2.com/).
