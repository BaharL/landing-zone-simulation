# -*- coding: utf-8 -*-
'''
The Caponians, an alien strain coming from an unspecified planet in
the galaxy, have been planning for quite a while the invasion of the
planet Earth. To do this, they have created and installed in various
points of the planet "mind bending machines". This machinery reduces
the intelligence of humans through the telephone network [1].

Once the phase of reducing human intelligence is over, the next
step towards the conquest of the Earth will be the landing on our
planet, which will happen as soon as the Caponians will find some
areas where they can land with their spaceships.

A spaceship (seen from above) can be represented as a rectangle of
dimensions W (width) and H (height). When considering the necessary
space for landing, a spaceship will open hatches on the 4 sides of
the rectangle. These gates are one per side.

The areas protrude by the same amount D, in order to allow to open on
each side a landing hatch. Each hatch is therefore as wide as the side
of the spaceship on which it is located and long as D, whatever side
it is on.

The Caponians would like to land with their spaceships in some of our
cities by looking at the city map. A city can be represented as a black
rectangular image, in which every building is represented as a colored
rectangle (each building has a color that uniquely identifies it).

In order to define the final details of the landing plan, the Caponians
need an algorithm which, given a map of a city and a
list of spaceships, confirms or not if
each spaceship has enough space to land in that city.
To land, a spaceship has to open its 4 hatches. Spaceships do not land
in the city at the same time, so they must be evaluated separately
from each other.

(1) So, given a black image (city) filled with solid colored
rectangles (buildings), where each building has its own unique color,
it is necessary:

- determine position, size and color of each rectangle
- save in a text file one rectangle per line
- in the file, each rectangle is represented with a sequence of 7 values:
     x, y, w, h, r, g, b
  separated by commas, in order of decreasing y-coordinate (the row
  nunber). In case of equal y, in order of increasing x (row-pixel number).

(2) Next, we are given a text file containing N triple of
integers. Each triple is separated internally and from the other
triples by a variable number of spaces, tabs or carriage returns. Each
triple represents width W, height H and minimum distance D (see below)
of a spaceship that you would like to land in a city at step (1):

- So we have to return a list of N Boolean values: the i-th value in
the list is True if there is enough space in the image to
insert the i-th spaceship.

- a rectangle can be inserted in the image if there exists at least
one position in the image where there is enough space (i.e., an area
consisting entirely of black pixels) to hold the i-th spaceship.
A spaceship can land if contains the rectangle itself, plus the 4
"extensions" of the rectangle, i.e. the 4 hatches of the spaceship.

For example, if a spaceship has 2 pixels of width and 3 of height and
D = 2, we will have to look for an area in the image to contain the
following figure:

                              **
                              **
                            **++**
                            **++**
                            **++**
                              **
                              **

where the + symbols are the pixels of the 2x3 rectangle/spaceship and the *
are the pixels of the 4 extensions/hatches.

Example:
Given the following image represented with one character for each
pixel, where "." is a black pixel and characters other than "." are
colored pixels (*=red, +=green):

**....
**....
......
......
....++
....++

The file with the found rectangles  must contain the lines:
4,4,2,2,0,255,0
0,0,2,2,255,0,0

and given the following spaceships:

(3, 3, 0)
(2, 2, 4)
(1, 1, 3)
(4, 2, 1)
(2, 4, 1)

the returned list will be: [True, False, False, False, False].
In fact only the first spaceship can land for example in the zone marked by
'X' (it has no doors, in fact D = 0)

**.XXX
**.XXX
...XXX
......
....++
....++

while the others don't enter in the map because, even if they have a point
in which they can land, they cannot open all the hatches.


[1] https://en.wikipedia.org/wiki/Zak_McKracken_and_the_Alien_Mindbenders)
'''
from pngmatrix import load_png8

def parse_numbers_from_file(file_txt):
    with open(file_txt) as f:
        numbers = []
        for line in f:
            line = line.strip().replace('\t', ' ').replace('\n', ' ')
            numbers += [int(num) for num in line.split()]
        return [tuple(numbers[i:i+3]) for i in range(0, len(numbers), 3)]

def extract_rectangles(image):
    width = len(image[0])
    height = len(image)
    dizionario = {}
    rectangles = []
    for y in range(height):
        for x in range(width):
            color = image[y][x]
            if color != (0, 0, 0):
                if color not in dizionario:
                    dizionario[color] = {'x_start': x, 'x_end': x, 'y_start': y, 'y_end': y}
                else:
                    dizionario[color]['x_end'] = max(dizionario[color]['x_end'], x)
                    dizionario[color]['y_end'] = max(dizionario[color]['y_end'], y)
                    
    for color, coords in dizionario.items():
        rectangles.append((coords['x_start'], coords['y_start'], coords['x_end'] - coords['x_start'] + 1, coords['y_end'] - coords['y_start'] + 1, color[0], color[1], color[2]))
        
    rectangles.sort(key=lambda x: (-x[1], x[0]))
    return rectangles

def create_spaceship_matrix(w, h, d):
    matrix = []
    ht = h + 2 * d
    wt = w + 2 * d
    for i in range(ht):
        row = []
        for j in range(wt):
            if d <= j < wt - d:
                row.append((0, 0, 0))
            else:
                if d <= i < ht - d:
                    row.append((0, 0, 0))                   
                else:
                    row.append((255, 255, 255))               
        matrix.append(row)
    return matrix

def find_free_space_in_image(image, matrix):
    for row in range(len(image) - len(matrix) + 1):
        for col in range(len(image[0]) - len(matrix[0]) + 1):
            match = True
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] == (0, 0, 0) and image[row + i][col + j] != (0, 0, 0):
                        match = False
                        break
                if not match:
                    break
            if match:
                return True
    return False

def ex(file_png, file_txt, file_out):
    image = load_png8(file_png)
    
    
    
    with open(file_out, "w") as f:
        for tuple in extract_rectangles(image):
            numbers_str = ",".join(str(num) for num in tuple)
            f.write(numbers_str + "\n")

    astronave = parse_numbers_from_file(file_txt)
    print(astronave)
    result=[]
    for ast in astronave:
        width, height, extension_length = ast
        matrix = create_spaceship_matrix(width, height, extension_length)

        result.append(find_free_space_in_image(image, matrix))    

    return result
    pass

if __name__ == "__main__":
    #print(ex('image7.png','rectangles7.txt','astronave7.txt'))
    #print(extract_rectangles('image0.png'))
    #print(parse_numbers_from_file('example.txt'))
    pass

