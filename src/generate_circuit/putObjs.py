import golly as g

objs = open("objs.txt", "r")
log = open("log.txt", "w+")
draw = list(eval(open("draw.txt", "r").readline()))

objects = []

for i in range(22):
    objects.append(eval(objs.readline()))

for i in range(len(draw)):
    for j in range(len(draw[i])):
        posx = 270*i - 270*j
        posy = 270*j + 270*i

        g.putcells(objects[draw[i][j]], posx, posy)

        