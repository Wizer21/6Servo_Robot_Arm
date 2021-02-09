# 6 Servomotor Arm 🤖
This project is a 6-axis arm, controlled on a Raspberry Pi.

The arm can be managed from an Xbox controller. :video_game:  
By using the calculation method below, I can create vertical or horizontal movements. If, for example, I want to claw to be lowered, I set this new position and calculate from this one, witch should be the new motors postions.

Come see it on [youtube](https://www.youtube.com/watch?v=-BNIDh299wI&feature=youtu.be) ! :clapper:

## Components
- [Raspberry Pi 4B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/), 4Gb  
- The [Grab-It](https://joy-it.net/de/products/Robot02) arm from [Joy_it](https://joy-it.net/en/)  
- 16 pwm pin card, [PCA9685](https://www.amazon.fr/gp/product/B07V72VBJ4/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)

## Programmatical part :wrench:
- Python  
- [Qt](https://www.qt.io/) for the GUI  
- [Pigpio](http://abyz.me.uk/rpi/pigpio/examples.html) for the pin control  

<img width="800" alt="Failure to load image, open there" src="https://drive.google.com/uc?export=view&id=1lsptWAeE1047xdFiftxcgOpJheJEhI9M">
<img width="800" alt="Failure to load image, open there" src="https://drive.google.com/uc?export=view&id=1kcNa3WQNZCbU3FKjx-0OkFhBEvRXbJol">

## To do :memo:
- [X] Make the arm fully managed through an Xbox controller 
- [ ] Create a pattern movement builder
- [ ] Connect to arm to a Node.Js api, allowing remote control
- [ ] Insert a 3D viewer in the application

<img width="600" alt="Failure to load image, open there" src="https://drive.google.com/uc?export=view&id=1G144SaH336PP6PAeimX-bxtZagvuSLau">
