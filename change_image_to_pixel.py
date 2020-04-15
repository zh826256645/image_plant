# -*- coding:utf-8 -*-
""" 将图片转化为像素图片 """
import os
from PIL import Image
import numpy as np


def model_one(img_url, width_step, height_step):
    """ 模式 1 """
    filepath, filename = os.path.split(img_url)
    img = Image.open(img_url)
    img = change_image_to_pixel(img, width_step, height_step)
    img.save(os.path.join(filepath, "pixel_" + filename))


def model_two(img_url, width_step, height_step, times=1):
    """ 模式 2 """
    filepath, filename = os.path.split(img_url)
    img = Image.open(img_url)
    for i in range(times):
        img = change_image_to_pixel(img, width_step * pow(2, i), height_step * pow(2, i))
    img.save(os.path.join(filepath, "pixel_" + filename))


def model_three(img_url, width_step, height_step, times=1):
    """ 模式 3 """
    filepath, filename = os.path.split(img_url)
    img = Image.open(img_url)
    for i in range(times):
        img = change_image_to_pixel(img, width_step + (width_step * i), height_step + (height_step * i))
    img.save(os.path.join(filepath, "pixel_" + filename))


def change_image_to_pixel(img, width_step, height_step):
    width, height = img.size
    width_num = width // width_step
    height_num = height // height_step

    x_list = list()
    for x in range(0, width+1, width_step):
        x_list.append(x)

    y_list = list()
    for y in range(0, height+1, height_step):
        y_list.append(y)

    x_np = np.array(x_list)
    y_np = np.array(y_list)

    blocks = list()
    X, Y = np.meshgrid(x_np, y_np)
    for i in range(len(y_list) - 1):
        for j in range(len(x_list) - 1):
            blocks.append([(X[i][j], Y[i][j]),
                           (X[i][j+1], Y[i][j+1]),
                           (X[i+1][j], Y[i+1][j]),
                           (X[i+1][j+1], Y[i+1][j+1])])

    blocks_colors = list()
    for l_d, r_d, l_u, r_u in blocks:
        colors = list()
        for i in range(r_u[0] - l_u[0]):
            for j in range(r_u[1] - r_d[1]):
                color = img.getpixel((int(l_d[0] + i), int(l_d[1] + j)))
                colors.append(color)

        blocks_colors.append(max(colors, key=colors.count))

    new_img = Image.new('RGB', (width_step * width_num, height_step * height_num), (255, 255, 255))
    for index, (l_d, r_d, l_u, r_u) in enumerate(blocks):
        color = blocks_colors[index]
        for i in range(r_u[0] - l_u[0]):
            for j in range(r_u[1] - r_d[1]):
                new_img.putpixel((int(l_d[0] + i), int(l_d[1] + j)), color)

    return new_img


if __name__ == '__main__':
    input_img = 'files/wx_tx.png'
    model_two(input_img, 2, 2, 4)
