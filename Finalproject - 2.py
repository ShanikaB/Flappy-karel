"""
File: pyramid.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random
from PIL import ImageTk
from PIL import Image


CANVAS_HEIGHT = 600
CANVAS_WIDTH = 600
OBSTACLE_WIDTH = 25


def main():
    """
     This program codes for the basic version of a game called 'Flappy bird'.
     In this game, Karel, the robot, passes through the space between the upper and lower pole. If Karel touches the
     poles, the game ends and the final score i.e. number of poles crossed successfully is displayed at the end.
    """
    count = 0
    # the position of  obstacles i.e the top and bottom pole of random size is set.
    obstacle_top_start_y = 0
    obstacle_top_end_y = random.randint(100, 450)
    obstacle_bottom_start_y = obstacle_top_end_y + 120
    obstacle_bottom_end_y = CANVAS_HEIGHT
    # the space between the top and bottom pole is 120

    # canvas is created
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'FLAPPY KAREL')

    # background of canvas is set
    img = Image.open('galaxy.png')
    pimg = ImageTk.PhotoImage(img)
    # The image on canvas will be placed at coordinates (100,200) and anchored at its northwest corner
    img_tk = canvas.create_image(0, 0, image=pimg, anchor=tkinter.NW)
    canvas.update()

    # Resize the image
    img = img.resize((600, 600))  # new width and height are (23, 32)
    pimg = ImageTk.PhotoImage(img)
    canvas.itemconfigure(img_tk, image=pimg)
    canvas.update()

    # Karel, the player, is created
    karel = create_karel(canvas)

    # opening message is displayed
    for i in range(3):
        opening_text = canvas.create_text(300, 200, font='Arial 40', text='Game begins...in ' + str(3 - i))
        canvas.update()
        canvas.move(opening_text, 1000, 0)
        time.sleep(1)

    # the top and bottom poles of olive colour are created
    obstacle_top = canvas.create_rectangle(CANVAS_WIDTH - OBSTACLE_WIDTH, obstacle_top_start_y, CANVAS_WIDTH, obstacle_top_end_y, fill="olive")
    obstacle_bottom =  canvas.create_rectangle(CANVAS_WIDTH - OBSTACLE_WIDTH, obstacle_bottom_start_y, CANVAS_WIDTH, obstacle_bottom_end_y, fill="olive")

    # the game begins
    while True:
        obstacle_top_start_y = 0
        obstacle_top_end_y = random.randint(10, 470)
        obstacle_bottom_start_y = obstacle_top_end_y + 100
        obstacle_bottom_end_y = CANVAS_HEIGHT

        #y_point = random.randint(200, 500)

        # the speed with which the poles move towards the player
        obstacle_speed = 15

        # the y position of player is moved with the mouse
        mouse_y = canvas.winfo_pointery() - 200
        canvas.moveto("karel", 0, mouse_y)

        # the obstacles start moving
        canvas.move(obstacle_top, -1 * obstacle_speed, 0)
        canvas.move(obstacle_bottom, -1 * obstacle_speed, 0)



        """
        if canvas.coords(obstacle_top)[0] > CANVAS_WIDTH / 2:
            obstacle_top = canvas.create_rectangle(CANVAS_WIDTH - OBSTACLE_WIDTH, obstacle_top_start_y, CANVAS_WIDTH, obstacle_top_end_y, fill="olive")
            obstacle_bottom = canvas.create_rectangle(CANVAS_WIDTH - OBSTACLE_WIDTH, obstacle_bottom_start_y, CANVAS_WIDTH, obstacle_bottom_end_y, fill="olive")
            canvas.move(obstacle_top, -1 * obstacle_speed, 0)
            canvas.move(obstacle_bottom, -1 * obstacle_speed, 0)
            canvas.update()
        """
        # the poles on reaching the left wall and successfully getting crossed by the player, get deleted
        if hit_left_wall(obstacle_top, canvas):
            canvas.delete(obstacle_top)
            canvas.delete(obstacle_bottom)

            #score = canvas.create_text(50, 50, font='Arial 15', text='Score:  ' + str(count))
            # the score increases by one if one obstacle is crossed successfully6
            count += 1
            # next pair of obstacle is created and run
            obstacle_top = canvas.create_rectangle(CANVAS_WIDTH - OBSTACLE_WIDTH, obstacle_top_start_y, CANVAS_WIDTH, obstacle_top_end_y, fill="olive")
            obstacle_bottom = canvas.create_rectangle(CANVAS_WIDTH - OBSTACLE_WIDTH, obstacle_bottom_start_y, CANVAS_WIDTH, obstacle_bottom_end_y, fill="olive")
            canvas.move(obstacle_top, -1 * obstacle_speed, 0)
            canvas.move(obstacle_bottom, -1 * obstacle_speed, 0)

        # player's movement is restricted to the canvas only
        if karel_hit_top('karel', canvas) or karel_hit_bottom('karel', canvas):
            if karel_hit_top('karel', canvas):
                y = 0
            if karel_hit_bottom('karel', canvas):
                y = CANVAS_HEIGHT - 70
            canvas.moveto("karel", 0, y)

        # the game stops if the player hits the poles
        if karel_hit_obstacle(obstacle_top, canvas, img_tk) or karel_hit_obstacle(obstacle_bottom, canvas, img_tk):
            canvas.delete('karel')
            text = canvas.create_text(150, 200, anchor="w", font='Arial 45', text='GAME OVER!!')
            canvas.update()
            time.sleep(1)
            canvas.delete(text)
            score = canvas.create_text(250, 200, font='Arial 40', text='Score: ' + str(count))
            canvas.update()
            time.sleep(2)
            break

        canvas.update()
        time.sleep(1/50.)


def create_karel(canvas):
    # Karel, the player, is created
    karel_outside_body = create_karel_body(canvas)
    # the inner rectangle is created
    karel_inside_body = canvas.create_rectangle(50, 540, 70, 565, tags='karel')
    # Karel limbs are created
    karel_limbs = create_karel_limbs(canvas)


def create_karel_body(canvas):
    # karel outer strokes are created
    karel_body1 = canvas.create_line(40, 530, 80, 530, tags='karel')
    karel_body2 = canvas.create_line(80, 530, 90, 540, tags='karel')
    karel_body3 = canvas.create_line(90, 540, 90, 590, tags='karel')
    karel_body4 = canvas.create_line(50, 590, 90, 590, tags='karel')
    karel_body5 = canvas.create_line(40, 580, 50, 590, tags='karel')
    karel_body6 = canvas.create_line(40, 530, 40, 580, tags='karel')

    # the horizontal line inside the outer box is created
    karel_line = canvas.create_line(60, 574, 75, 574, tags='karel')


def create_karel_limbs(canvas):
    # feet and arms are created
    left_foot_arm = canvas.create_rectangle(55, 590, 65, 595, fill="black", tags='karel')
    left_foot_feet = canvas.create_rectangle(55, 595, 75, 600, fill="black", tags='karel')
    right_foot_feet = canvas.create_rectangle(27, 565, 32, 585, fill="black", tags='karel')
    right_foot_arm = canvas.create_rectangle(32, 565, 40, 575, fill="black", tags='karel')


def karel_hit_top(object, canvas):
    # if Karel hits the top of canvas
    return canvas.coords(object)[1] <= 0


def karel_hit_bottom(object, canvas):
    # if Karel hits the bottom of canvas
    return canvas.coords(object)[3] >= CANVAS_HEIGHT


def hit_left_wall(object, canvas):
    # if karel hits the left wall
    return canvas.coords(object)[0] <= 0


def karel_hit_obstacle(object, canvas, img_tk):
    # if karel hits the poles
    object_coords = canvas.coords(object)
    x1 = object_coords[0]
    y1 = object_coords[1]
    x2 = object_coords[2]
    y2 = object_coords[3]
    results = canvas.find_overlapping(x1, y1, x2, y2)
    for item in results:
        if item == img_tk:
            # if karel overlaps with background
            return len(results) > 2
        else:
            # if karel overlaps with pole
            return len(results) > 1


def make_canvas(canvas_width, canvas_height, title):
    # canvas is created
    top = tkinter.Tk()
    top.minsize(width=canvas_width, height=canvas_height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=canvas_width + 1, height=canvas_height + 1)
    canvas.pack()
    return canvas



if __name__ == '__main__':
    main()
