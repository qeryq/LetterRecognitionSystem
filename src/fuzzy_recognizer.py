import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from PIL import Image as image


def horizontal(x):
    val = [0, 0, 0, 0, 0]
    weight = [0, 0, 0, 0, 0]

    if x in range(0, 301):
        val[0] = 1

        if x < 200:
            weight[0] = 1
        else:
            weight[0] = (-x + 300) / 100

    if x in range(200, 451):
        val[1] = 1

        if x < 325:
            weight[1] = (x - 200) / 125
        else:
            weight[1] = 1 - (x - 325) / 125

    if x in range(400, 601):
        val[2] = 1

        if x <= 450:
            weight[2] = (x - 400) / 50
        elif x in range(450, 550):
            weight[2] = 1
        else:
            weight[2] = 1 - (x - 550) / 50

    if x in range(550, 801):
        val[3] = 1

        if x < 675:
            weight[3] = (x - 550) / 125
        else:
            weight[3] = 1 - (x - 675) / 125

    if x in range(700, 1001):
        val[4] = 1

        if x > 800:
            weight[4] = 1
        else:
            weight[4] = (x - 700) / 100

    return val, weight


def vertical(x):
    val = [0, 0, 0]
    weight = [0, 0, 0]

    if x in range(0, 401):
        val[0] = 1

        if x < 200:
            weight[0] = 1
        else:
            weight[0] = (-x + 400) / 200

    if x in range(300, 701):
        val[1] = 1

        if x <= 450:
            weight[1] = (x - 300) / 150
        elif x in range(450, 550):
            weight[1] = 1
        else:
            weight[1] = 1 - (x - 550) / 150

    if x in range(600, 1001):
        val[2] = 1

        if x > 800:
            weight[2] = 1
        else:
            weight[2] = (x - 600) / 200

    return val, weight


def generate_vertical_data():
    top = []
    middle = []
    bottom = []

    for i in range(1001):
        val, weight = vertical(i)
        top.append(weight[0])
        middle.append(weight[1])
        bottom.append(weight[2])

    data = pd.DataFrame({'Top': top,
                         'Middle': middle,
                         'Bottom': bottom, })

    return data


def generate_horizontal_data():
    left = []
    center_left = []
    center = []
    center_right = []
    right = []

    for i in range(1001):
        val, weight = horizontal(i)
        left.append(weight[0])
        center_left.append(weight[1])
        center.append(weight[2])
        center_right.append(weight[3])
        right.append(weight[4])

    data = pd.DataFrame({'left': left,
                         'center_left': center_left,
                         'center': center,
                         'center_right': center_right,
                         'right': right})

    return data


data = generate_vertical_data()
data.plot(figsize=(10,5))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.7), prop={'size': 15})
plt.title('Vertical', color='black', size = 20)

plt.savefig("static/vertical.png", bbox_inches="tight")

data = generate_horizontal_data()
data.plot(figsize=(10,5))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.7), prop={'size': 15})
plt.title('Horizontal', color='black', size = 20)

plt.savefig("static/horizontal.png", bbox_inches="tight")


def horizontal_orientation(x):
    val = 0
    weight = 0

    if x in range(0, 301):
        val = 1

        if x < 200:
            weight = 1
        else:
            weight = (-x + 300) / 100

    if x in range(200, 451):
        val = 2

        if x < 325:
            weight = (x - 200) / 125
        else:
            weight = 1 - (x - 325) / 125

    if x in range(400, 601):
        val = 3

        if x <= 450:
            weight = (x - 400) / 50
        elif x in range(450, 550):
            weight = 1
        else:
            weight = 1 - (x - 550) / 50

    if x in range(550, 801):
        val = 4

        if x < 675:
            weight = (x - 550) / 125
        else:
            weight = 1 - (x - 675) / 125

    if x in range(700, 1001):
        val = 5

        if x > 800:
            weight = 1
        else:
            weight = (x - 700) / 100

    return val, weight


def vertical_orientation(x):
    val = 0
    weight = 0

    if x in range(0, 401):
        val = 1

        if x < 200:
            weight = 1
        else:
            weight = (-x + 400) / 200

    if x in range(300, 701):
        val = 2

        if x <= 450:
            weight = (x - 300) / 150
        elif x in range(450, 550):
            weight = 1
        else:
            weight = 1 - (x - 550) / 150

    if x in range(600, 1001):
        val = 3

        if x > 800:
            weight = 1
        else:
            weight = (x - 600) / 200

    return val, weight


def black_orientation(img):
    letter = img.convert('RGB').resize((1000, 1000))
    pix = letter.load()

    width = letter.size[0]
    height = letter.size[1]

    dictrion = []

    for i in range(height):
        for j in range(width):
            if pix[i, j] != (255, 255, 255):
                dictionary = [0, 0, 0, 0, 0, 0]
                dictionary[0] = i
                dictionary[1] = j
                dictionary[2], dictionary[4] = horizontal_orientation(i)
                dictionary[3], dictionary[5] = vertical_orientation(j)
                dictrion.append(dictionary)

    return np.array(dictrion)


def check_if_black_pixel_in_section(d, h, v):
    return np.any(np.logical_and(d[:, 2] == h, d[:, 3] == v))


def check_if_black_pixel_in_section_with_weigh(d, h, v, wh, wv):
    return np.any(
        np.logical_and(np.logical_and(d[:, 2] == h, d[:, 3] == v), np.logical_and(d[:, 4] >= wh, d[:, 5] >= wv)))


def count_if_black_pixel_in_section_with_weigh(d, h, v, wh, wv):
    return np.count_nonzero(
        np.logical_and(np.logical_and(d[:, 2] == h, d[:, 3] == v), np.logical_and(d[:, 4] >= wh, d[:, 5] >= wv)))


def recognize_letter(letter_data):
    # recognize 'A' 

    if (not check_if_black_pixel_in_section_with_weigh(letter_data, 5, 1, 1, 1) and
            not check_if_black_pixel_in_section_with_weigh(letter_data, 1, 1, 1, 1) and
            count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) == 0 and
            count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0 and
            count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) == 0 and
            count_if_black_pixel_in_section_with_weigh(letter_data, 3, 2, 1, 1) == 0):
        return 'A'

    # B   
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 2) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) < 150 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) < 100 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) < 150):
        return 'B'

    # C
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) == 0 and not
          check_if_black_pixel_in_section(letter_data, 3, 2)):
        return 'C'

    # D 
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and not
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 2) and
          (count_if_black_pixel_in_section_with_weigh(letter_data, 1, 1, 1, 1) > 10000) and
          (count_if_black_pixel_in_section_with_weigh(letter_data, 1, 3, 1, 1) > 10000) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 3, 1, 1) < 1000):
        return 'D'

    # E    
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 2) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) > 155 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) > 100 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) > 150):
        return 'E'

    # F
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and not
          check_if_black_pixel_in_section(letter_data, 3, 3) and not
          check_if_black_pixel_in_section(letter_data, 4, 3)):
        return 'F'

    # G
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 1, 1, 1) > 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) > 0 and not
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) > 0 and
          check_if_black_pixel_in_section(letter_data, 3, 2)):
        return 'G'

    # H    
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 4, 2) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 1, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 1, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0):
        return 'H'

    # I    
    elif (check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and not
          check_if_black_pixel_in_section(letter_data, 1, 1) and not
          check_if_black_pixel_in_section(letter_data, 1, 2) and not
          check_if_black_pixel_in_section(letter_data, 1, 3) and not
          check_if_black_pixel_in_section(letter_data, 5, 1) and not
          check_if_black_pixel_in_section(letter_data, 5, 2) and not
          check_if_black_pixel_in_section(letter_data, 5, 3)):
        return 'I'

    # J
    elif (check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and not
          check_if_black_pixel_in_section(letter_data, 1, 1) and not
          check_if_black_pixel_in_section(letter_data, 1, 2) and not
          check_if_black_pixel_in_section(letter_data, 2, 1) and not
          check_if_black_pixel_in_section(letter_data, 2, 2)):
        return 'J'

    # K
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and
          check_if_black_pixel_in_section(letter_data, 4, 2) and not
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) and not
          check_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1)):
        return 'K'

    # L
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 2) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          check_if_black_pixel_in_section(letter_data, 4, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and not
          check_if_black_pixel_in_section(letter_data, 3, 1) and not
          check_if_black_pixel_in_section(letter_data, 3, 2) and not
          check_if_black_pixel_in_section(letter_data, 4, 1) and not
          check_if_black_pixel_in_section(letter_data, 5, 1) and not
          check_if_black_pixel_in_section(letter_data, 4, 2) and not
          check_if_black_pixel_in_section(letter_data, 5, 2)):
        return 'L'

    # M
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 2) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and not
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 1, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) == 0):
        return 'M'

    # N
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 2) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and not
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 1, 1, 1) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 2, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) == 0):
        return 'N'

    # O    
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          check_if_black_pixel_in_section(letter_data, 4, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 3, 1, 1) < 5000 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) != 0 and
          (count_if_black_pixel_in_section_with_weigh(letter_data, 1, 1, 1, 1) < 10000) and
          (count_if_black_pixel_in_section_with_weigh(letter_data, 1, 3, 1, 1) < 10000)):
        return 'O'


    # P
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and  #
          check_if_black_pixel_in_section(letter_data, 1, 2) and  #
          check_if_black_pixel_in_section(letter_data, 1, 3) and  #
          check_if_black_pixel_in_section(letter_data, 2, 1) and  #
          check_if_black_pixel_in_section(letter_data, 2, 2) and  #
          check_if_black_pixel_in_section(letter_data, 2, 3) and  #
          check_if_black_pixel_in_section(letter_data, 3, 1) and  #
          check_if_black_pixel_in_section(letter_data, 3, 2) and  #
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0 and  #
          check_if_black_pixel_in_section(letter_data, 4, 1) and  #
          check_if_black_pixel_in_section(letter_data, 4, 2) and not  #
          check_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) and  #
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 1, 1, 1) and  #
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 3, 1, 1) == 0):
        return 'P'

    # Q
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          check_if_black_pixel_in_section(letter_data, 4, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 3, 1, 1) > 5000 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) != 0 and
          (count_if_black_pixel_in_section_with_weigh(letter_data, 1, 1, 1, 1) < 10000) and
          (count_if_black_pixel_in_section_with_weigh(letter_data, 1, 3, 1, 1) < 10000)):
        return 'Q'

    # R
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and  #
          check_if_black_pixel_in_section(letter_data, 1, 2) and  #
          check_if_black_pixel_in_section(letter_data, 1, 3) and  #
          check_if_black_pixel_in_section(letter_data, 2, 1) and  #
          check_if_black_pixel_in_section(letter_data, 2, 2) and  #
          check_if_black_pixel_in_section(letter_data, 3, 1) and  #
          check_if_black_pixel_in_section(letter_data, 3, 2) and  #
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0 and  #
          check_if_black_pixel_in_section(letter_data, 4, 1) and  #
          check_if_black_pixel_in_section(letter_data, 4, 2) and  #
          check_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) and  #
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 1, 1, 1) and  #
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 3, 1, 1) != 0):
        return 'R'

    # S 
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 1, 2, 1, 1) < 100 and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 2) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) < 100 and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) != 0 and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 1, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 1, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 1, 1, 1) < 500 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 1, 1, 1) != 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) < 500 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) != 0):
        return 'S'

    # T
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and not
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) == 0 and not
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) == 0 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) == 0 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) == 0 and not
          check_if_black_pixel_in_section(letter_data, 5, 2) and not
          check_if_black_pixel_in_section(letter_data, 5, 3)):
        return 'T'

    # U   
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 2) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and not
          check_if_black_pixel_in_section(letter_data, 3, 1) and not
          check_if_black_pixel_in_section(letter_data, 3, 2)):
        return 'U'
    # V
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and not
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 1) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 1, 2, 1, 1) < 100 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 1, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 3, 1, 1) == 0):
        return 'V'

    # W
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 2) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 2) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 1, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) != 0):
        return 'W'

    # X
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 1, 2, 1, 1) == 0 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) == 0 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 1, 1, 1) == 0 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) == 0 and
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) == 0):
        return 'X'

    # Y
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 1, 2, 1, 1) == 0 and not
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and not
          check_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) and not
          check_if_black_pixel_in_section(letter_data, 5, 3) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 1, 1, 1) == 0 and
          check_if_black_pixel_in_section(letter_data, 3, 2) and
          check_if_black_pixel_in_section(letter_data, 3, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 1, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 3, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 1, 1, 1) < 200 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 2, 3, 1, 1) == 0):
        return 'Y'

    # Z
    elif (check_if_black_pixel_in_section(letter_data, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 2, 1) and
          check_if_black_pixel_in_section(letter_data, 3, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 1) and
          check_if_black_pixel_in_section(letter_data, 5, 1) and
          check_if_black_pixel_in_section(letter_data, 1, 3) and
          check_if_black_pixel_in_section(letter_data, 2, 3) and
          check_if_black_pixel_in_section_with_weigh(letter_data, 3, 3, 1, 1) and
          check_if_black_pixel_in_section(letter_data, 4, 3) and
          check_if_black_pixel_in_section(letter_data, 5, 3) and
          count_if_black_pixel_in_section_with_weigh(letter_data, 1, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 4, 2, 1, 1) == 0 and
          count_if_black_pixel_in_section_with_weigh(letter_data, 5, 2, 1, 1) == 0):
        return 'Z'

    else:
        return None

