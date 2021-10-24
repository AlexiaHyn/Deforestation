from PIL import Image
import numpy
import math

compare = (147, 204, 147)

def calculate_average(start_h, start_w, length_h, length_w, rgb_im, width, height):
    sum = 0
    count = 0
    for i in range(start_h, start_h + length_h):
        for j in range(start_w, start_w + length_w):
            if (i < height  and j < width ):
                r, g, b = rgb_im.getpixel((j, i))
                count += 1
                sum += abs(math.sqrt((r-compare[0])**2+(g-compare[1])**2+(b-compare[2])**2))
    return sum/count

def processing(path, grid):
    grid = 10
    im = Image.open(path)
    rgb_im = im.convert('RGB')
    width, height = im.size
    color_avg = []
    for i in range(1, grid + 1):
        color_avg.append([])
        for j in range(1, grid + 1):
            color_avg[i-1].append(calculate_average((i-1) * math.floor(height/10), (j-1)*math.floor(width/10), math.floor(height/10), math.floor(width/10), rgb_im, width, height))

    #Total average
    total = 0
    for list in color_avg:
        for num in list:
            total += num
    total_average = total/(grid*grid)

    #Total variance
    sum = 0
    for list in color_avg:
        for num in list:
            sum += (num-total_average)**2
    variance = sum/(grid*grid)

    return total_average, variance

test_path1 = "D:/Desktop/t1.jpg"
test_path2 = "D:/Desktop/t2.jpg"
total_avg1, var1 = processing(test_path1, 10)
total_avg2, var2 = processing(test_path2, 10)
print("Deforestation: ", total_avg2 - total_avg1)