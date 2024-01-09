#!/usr/bin/env python3

# Programmer: Ruth Dohrmann
# Description: This program generates and displays the Mandelbrot set. The program allows
# the user to click on two points within the graph to generate new x and y minimum and
# maximum points which will be used to recalculate and display the plot. This process
# continues until the user decides to quit.
import matplotlib.pyplot as plt
import numpy as np

# This function returns a grid of points on the complex plane
def complex_grid(x_minimum, x_maximum, y_minimum, y_maximum, density):

    dx = x_maximum - x_minimum
    dy = y_maximum - y_minimum
    density_x = int(density)
    density_y = int(density*dy/dx)
    # test whether the change in x or the change in y is greater, calculate the density accordingly
    if (dy > dx):
        density_x = int(density*dx/dy)
        density_y = int(density)

    # xmin=start, xmax=stop, density=number of samples in the interval
    real = np.linspace(x_minimum, x_maximum, density_x)
    # ymin=start, ymax=stop, density=number of samples in the interval
    imaginary = np.linspace(y_minimum, y_maximum, density_y)

    # return 2d array of complex numbers
    # (newaxis increases the dimension of the existing array by one dimension)
    return real[np.newaxis, :] + imaginary[:, np.newaxis] * 1j

# Test whether or not the point complex(x, y) diverges in the given number of iterations
# using the equation: z = z ** 2 + c
def test_if_stable(x, y, max_num_iterations):
    z = 0
    c = complex(x, y)
    for _ in range(max_num_iterations):
        z = z ** 2 + c
        if abs(z) > 2:
            return False
    return abs(z) <= 2

count = 0
# arranged as x_minimum, y_minimum, x_maximum, y_maximum
my_list = [-2, -1.5, 0.5, 1.5]
over = False

# This function handles newly selected x and y dimensions
def on_click(event):
    global my_list
    global count

    # If the user has aready selected two new points, clear out the list and restart the process
    if len(my_list) >= 4:
        list.clear()
        count = 0

    # Check if the selected point is valid (does not equal None)
    if event.xdata and event.ydata:
        my_list.append(event.xdata)
        my_list.append(event.ydata)
        count += 1

    if count == 2:
        # Order minimum and maximum x and y values (x_minimum, y_minimum, x_maximum, y_maximum)
        if my_list[0] > my_list[2]:
            x_temp = my_list[0]
            my_list[0] = my_list[2]
            my_list[2] = x_temp
        if my_list[1] > my_list[3]:
            y_temp = my_list[1]
            my_list[1] = my_list[3]
            my_list[3] = y_temp
        # close previous figure
        plt.close()

# The user must press 'q' to end the program
# This function handles that event, closing the graph and ending the while loop
def on_key(event):
    global over
    if event.key == 'q' or event.key == 'Q':
        over = True
        plt.close()

while(not over):
    # Get the grid of complex numbers (dimension ordering: xmin, xmax, ymin, ymax)
    c = complex_grid(my_list[0], my_list[2], my_list[1], my_list[3], density=500)
    
    # Cut out the complex numbers that are unstable
    dim = c.shape
    # set up arrays of adequate size
    kept_values_x = np.zeros(dim[0]*dim[1])
    kept_values_y = np.zeros(dim[0]*dim[1])
    num_stable = 0
    # .real returns the real part and .imag the imaginary part of the complex argument
    x = c.real
    y = c.imag

    # test the x and y components for stability
    for i in range(dim[0]):
        for j in range(dim[1]):
            # if the point is stable, add it to the kept x and y values
            if test_if_stable(x[i][j], y[i][j], max_num_iterations = 20):
                kept_values_x[num_stable] = x[i][j]
                kept_values_y[num_stable] = y[i][j]
                num_stable += 1
    # resize both arrays
    kept_values_x = np.resize(kept_values_x, num_stable)
    kept_values_y = np.resize(kept_values_y, num_stable)

    # Plot the points contained in the Mandelbrot set (s = marker size)
    plt.scatter(kept_values_x, kept_values_y, color="#40BE59", marker=",", s=1)
    # gca gets the current axes and set_aspect sets the aspect ratio of the y/x-scale.
    plt.gca().set_aspect("equal")
    plt.axis("off")
    plt.title("Mandelbrot Set (press q to quit)")
    plt.connect('button_press_event', on_click)
    plt.connect('key_press_event', on_key)
    # Display scatter plot
    plt.show()
