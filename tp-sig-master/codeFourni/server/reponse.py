import database as db
from drawer import Image
from random import random, randint


# Question 10
def display_like(name):
    cursor = db.execute_query("SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE '%s'" % name)
    for row in cursor: # Pour chaque ligne
        name = row[0]
        x = row[1]
        y = row[2]
        print(name + " | " + str(x) + " | " + str(y))

    cursor.close()
    db.close_connection()

# print("Entrez le nom de ce que vous recherchez : ")
# display_like(input())

# Question 11 et 14 et 15

colors = {"motorway":(0.94,0.5,0.6,1),"footway":(0.96, 0.83, 0.81, 1), "trunk":(1, 0.74, 0.64, 1), "primary":(0.99, 0.86, 0.6, 1), "residential":(0.99, 0.99, 0.99, 1), "service":(0.99, 0.99, 0.99, 1)}

cache = {}

def draw_tile(rectangle, srid, width, height, layer):
    tile = Image(width, height)
    if (layer,rectangle) in cache :
       tile = cache[(layer,rectangle)]  
    else :
        request = "SELECT ST_Transform(linestring,%d), tags->'%s' FROM ways WHERE tags ? '%s' and ST_Intersects(ST_Transform(linestring, %d), ST_MakeEnvelope(%f , %f, %f, %f,%d))"%(srid, layer, layer, srid, rectangle[0], rectangle[1], rectangle[2], rectangle[3], srid) 
        cursor = db.execute_query(request)
        for row in cursor:
            points = []
            iter_points = iter(row[0])
            for x, y in iter_points:
                x = (x - rectangle[0]) * width / (rectangle[2] - rectangle[0])
                y = height - ((y - rectangle[1]) * height / (rectangle[3] - rectangle[1]))
                points.append((x, y))
            if row[1] in colors:
                tile.draw_linestring(points, colors[row[1]])
            else : 
                colors[row[1]] = (random(), random(), random(), 1) if layer != "building" else  (0.85, 0.82, 0.79,1)
                tile.draw_linestring(points, colors[row[1]])
        cache[(layer,rectangle)] = tile
        cursor.close()
        db.close_connection()
    return tile


