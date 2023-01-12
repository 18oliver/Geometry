#  File: Geometry.py

#  Description: Represents various geometric objects (points, cubes, cylinders, spheres)

#  Student Name: Oliver Tan

#  Student UT EID: ot2825

#  Partner Name: N/a

#  Partner UT EID: N/a

#  Course Name: CS 313E

#  Unique Number: 52530

#  Date Created: 09/12/2022

#  Date Last Modified: 09/16/2022

import math
import sys

class Point (object):
  # constructor with default values
  def __init__ (self, x = 0, y = 0, z = 0):
    self.x = x
    self.y = y
    self.z = z

  # create a string representation of a Point
  # returns a string of the form (x, y, z)
  def __str__ (self):
    return(f"({(self.x):.1f}, {(self.y):.1f}, {(self.z):.1f})")

  # get distance to another Point object
  # other is a Point object
  # returns the distance as a floating point number
  def distance (self, other):
    xDist = self.x - other.x
    yDist = self.y - other.y
    zDist = self.z - other.z
    return(math.hypot(xDist, yDist, zDist))

  # test for equality between two points
  # other is a Point object
  # returns a Boolean
  def __eq__ (self, other):
    tol = 1.0e-6
    return((abs(self.x - other.x ) < tol) and (abs(self.y - other.y ) < tol) and (abs(self.z - other.z ) < tol))

class Sphere (object):
  # constructor with default values
  def __init__ (self, x = 0, y = 0, z = 0, radius = 1):
    self.x = x
    self.y = y
    self.z = z
    self.center = Point(x, y, z)
    self.radius = radius

  # returns string representation of a Sphere of the form:
  # Center: (x, y, z), Radius: value
  def __str__ (self):
    return(f"Center: {(self.center)}, Radius: {(self.radius):.1f}")

  # compute surface area of Sphere
  # returns a floating point number
  def area (self):
    return(4 * math.pi * (self.radius**2))

  # compute volume of a Sphere
  # returns a floating point number
  def volume (self):
    return(math.pi * (self.radius**3) * (4/3))

  # determines if a Point is strictly inside the Sphere
  # p is Point object
  # returns a Boolean
  def is_inside_point (self, p):
    return(p.distance(self.center) < self.radius)

  # determine if another Sphere is strictly inside this Sphere
  # other is a Sphere object
  # returns a Boolean
  def is_inside_sphere (self, other):
    return((other.center.distance(self.center) + other.radius ) < self.radius)

  # determine if a Cube is strictly inside this Sphere
  # determine if the eight corners of the Cube are strictly 
  # inside the Sphere
  # a_cube is a Cube object
  # returns a Boolean
  def is_inside_cube (self, a_cube):
    s = a_cube.side/2
    x = a_cube.x
    y = a_cube.y
    z = a_cube.z
    corners = [Point(x+s, y+s, z+s), Point(x-s, y+s, z+s), Point(x+s, y-s, z+s), Point(x-s, y-s, z+s), Point(x+s, y+s, z-s), Point(x-s, y+s, z-s), Point(x+s, y-s, z-s), Point(x-s, y-s, z-s)]
    for corner in corners:
      if(corner.distance(self.center) >= self.radius):
        return False
    return True

  # determine if a Cylinder is strictly inside this Sphere
  # a_cyl is a Cylinder object
  # returns a Boolean
  def is_inside_cyl (self, a_cyl):
    z1 = a_cyl.z + a_cyl.height/2
    z2 = a_cyl.z - a_cyl.height/2
    if(z1 > self.z + self.radius or z2 < self.z - self.radius):
      return False
    rad1 = math.sqrt(self.radius ** 2 - (z1 - self.z)**2)
    rad2 = math.sqrt(self.radius ** 2 - (z2 - self.z)**2)
    if(math.hypot(self.x - a_cyl.x, self.y - a_cyl.y) + a_cyl.radius < min(rad1, rad2)):
      return True
    return False

  # determine if another Sphere intersects this Sphere
  # other is a Sphere object
  # two spheres intersect if they are not strictly inside
  # or not strictly outside each other
  # returns a Boolean
  def does_intersect_sphere (self, other):
    if(self.is_inside_sphere(other) or other.is_inside_sphere(self)):
      return False
    return(other.center.distance(self.center) <= (self.radius + other.radius))

  # determine if a Cube intersects this Sphere
  # the Cube and Sphere intersect if they are not
  # strictly inside or not strictly outside the other
  # a_cube is a Cube object
  # returns a Boolean
  def does_intersect_cube (self, a_cube):
    if(self.is_inside_cube(a_cube)):
      return False
    s = a_cube.side/2
    x = a_cube.x
    y = a_cube.y
    z = a_cube.z
    corners = [Point(x+s, y+s, z+s), Point(x-s, y+s, z+s), Point(x+s, y-s, z+s), Point(x-s, y-s, z+s), Point(x+s, y+s, z-s), Point(x-s, y+s, z-s), Point(x+s, y-s, z-s), Point(x-s, y-s, z-s)]
    for corner in corners:
      if(corner.distance(self.center) <= self.radius):
        return True
    return False

  # return the largest Cube object that is circumscribed
  # by this Sphere
  # all eight corners of the Cube are on the Sphere
  # returns a Cube object
  def circumscribe_cube (self):
    return(Cube(self.x, self.y, self.z, 2*(self.radius)/(math.sqrt(3))))

class Cube (object):
  # Cube is defined by its center (which is a Point object)
  # and side. The faces of the Cube are parallel to x-y, y-z,
  # and x-z planes.
  def __init__ (self, x = 0, y = 0, z = 0, side = 1):
    self.x = x
    self.y = y
    self.z = z
    self.center = Point(x,y,z)
    self.side = side

  # string representation of a Cube of the form: 
  # Center: (x, y, z), Side: value
  def __str__ (self):
    return(f"Center: {(self.center)}, Side: {(self.side):.1f}")

  # compute the total surface area of Cube (all 6 sides)
  # returns a floating point number
  def area (self):
    return(6*(self.side**2))

  # compute volume of a Cube
  # returns a floating point number
  def volume (self):
    return(self.side**3)

  # determines if a Point is strictly inside this Cube
  # p is a point object
  # returns a Boolean
  def is_inside_point (self, p):
    return(abs(p.x-self.x) < (self.side/2) and abs(p.y-self.y) < (self.side/2) and abs(p.z-self.z) < (self.side/2))

  # determine if a Sphere is strictly inside this Cube 
  # a_sphere is a Sphere object
  # returns a Boolean
  def is_inside_sphere (self, a_sphere):
    withinX = a_sphere.x + a_sphere.radius < self.x + (self.side/2) and a_sphere.x - a_sphere.radius > self.x - (self.side/2)
    withinY = a_sphere.y + a_sphere.radius < self.y + (self.side/2) and a_sphere.y - a_sphere.radius > self.y - (self.side/2)
    withinZ = a_sphere.z + a_sphere.radius < self.z + (self.side/2) and a_sphere.z - a_sphere.radius > self.z - (self.side/2)
    return(withinX and withinY and withinZ)

  # determine if another Cube is strictly inside this Cube
  # other is a Cube object
  # returns a Boolean
  def is_inside_cube (self, other):
    withinX = other.x + (other.side/2) < self.x + (self.side/2) and other.x - (other.side/2) > self.x - (self.side/2)
    withinY = other.y + (other.side/2) < self.y + (self.side/2) and other.y - (other.side/2) > self.y - (self.side/2)
    withinZ = other.z + (other.side/2) < self.z + (self.side/2) and other.z - (other.side/2) > self.z - (self.side/2)
    return(withinX and withinY and withinZ)

  # determine if a Cylinder is strictly inside this Cube
  # a_cyl is a Cylinder object
  # returns a Boolean
  def is_inside_cylinder (self, a_cyl):
    withinX = a_cyl.x + a_cyl.radius < self.x + (self.side/2) and a_cyl.x - a_cyl.radius > self.x - (self.side/2)
    withinY = a_cyl.y + a_cyl.radius < self.y + (self.side/2) and a_cyl.y - a_cyl.radius > self.y - (self.side/2)
    withinZ = a_cyl.z + (a_cyl.height/2) < self.z + (self.side/2) and a_cyl.z - (a_cyl.height/2) > self.z - (self.side/2)
    return(withinX and withinY and withinZ)

  # determine if another Cube intersects this Cube
  # two Cube objects intersect if they are not strictly
  # inside and not strictly outside each other
  # other is a Cube object
  # returns a Boolean
  def does_intersect_cube (self, other):
    if(self.is_inside_cube(other) or other.is_inside_cube(self)):
      return False
    intersectX = (abs(other.x - self.x) < ((other.side + self.side)/2))
    intersectY = (abs(other.y - self.y) < ((other.side + self.side)/2))
    intersectZ = (abs(other.z - self.z) < ((other.side + self.side)/2))
    return(intersectX and intersectY and intersectZ)

  # determine the volume of intersection if this Cube 
  # intersects with another Cube
  # other is a Cube object
  # returns a floating point number
  def intersection_volume (self, other):
    if(not self.does_intersect_cube(other)):
      return 0
    intersectX = ((other.side + self.side)/2) - abs(other.x - self.x)
    intersectY = ((other.side + self.side)/2) - abs(other.y - self.y)
    intersectZ = ((other.side + self.side)/2) - abs(other.z - self.z)
    return(intersectX * intersectY * intersectZ)

  # return the largest Sphere object that is inscribed
  # by this Cube
  # Sphere object is inside the Cube and the faces of the
  # Cube are tangential planes of the Sphere
  # returns a Sphere object
  def inscribe_sphere (self):
    return(Sphere(self.x,self.y,self.z,(self.side/2)))

class Cylinder (object):
  # Cylinder is defined by its center (which is a Point object),
  # radius and height. The main axis of the Cylinder is along the
  # z-axis and height is measured along this axis
  def __init__ (self, x = 0, y = 0, z = 0, radius = 1, height = 1):
    self.x = x
    self.y = y
    self.z = z
    self.center = Point(x, y, z)
    self.radius = radius
    self.height = height

  # returns a string representation of a Cylinder of the form: 
  # Center: (x, y, z), Radius: value, Height: value
  def __str__ (self):
    return(f"Center: {self.center}, Radius: {(self.radius):.1f}, Height: {(self.height):.1f}")

  # compute surface area of Cylinder
  # returns a floating point number
  def area (self):
    return((self.height * math.pi * self.radius*2) + (2 * math.pi * (self.radius ** 2)))

  # compute volume of a Cylinder
  # returns a floating point number
  def volume (self):
    return(math.pi * (self.radius**2) * self.height)

  # determine if a Point is strictly inside this Cylinder
  # p is a Point object
  # returns a Boolean
  def is_inside_point (self, p):
    withinXY = math.hypot((self.x - p.x), (self.y - p.y)) < self.radius
    withinZ = abs(self.z - p.z) < (self.height/2)
    return(withinXY and withinZ)

  # determine if a Sphere is strictly inside this Cylinder
  # a_sphere is a Sphere object
  # returns a Boolean
  def is_inside_sphere (self, a_sphere):
    withinZ = a_sphere.z + a_sphere.radius < self.z + (self.height)/2 and a_sphere.z - a_sphere.radius > self.z - (self.height)/2
    withinXY = math.hypot(self.x - a_sphere.x, self.y - a_sphere.y) + a_sphere.radius < self.radius
    return(withinZ and withinXY)

  # determine if a Cube is strictly inside this Cylinder
  # determine if all eight corners of the Cube are inside
  # the Cylinder
  # a_cube is a Cube object
  # returns a Boolean
  def is_inside_cube (self, a_cube):
    s = a_cube.side/2
    x = a_cube.x
    y = a_cube.y
    z = a_cube.z
    corners = [Point(x+s, y+s, z+s), Point(x-s, y+s, z+s), Point(x+s, y-s, z+s), Point(x-s, y-s, z+s), Point(x+s, y+s, z-s), Point(x-s, y+s, z-s), Point(x+s, y-s, z-s), Point(x-s, y-s, z-s)]
    for corner in corners:
      if(not self.is_inside_point(corner)):
        return False
    return True

  # determine if another Cylinder is strictly inside this Cylinder
  # other is Cylinder object
  # returns a Boolean
  def is_inside_cylinder (self, other):
    withinZ = other.z + (other.height)/2 < self.z + (self.height)/2 and other.z - (other.height)/2 > self.z - (self.height)/2
    withinXY = math.hypot(self.x - other.x, self.y - other.y) + other.radius < self.radius
    return(withinZ and withinXY)

  # determine if another Cylinder intersects this Cylinder
  # two Cylinder object intersect if they are not strictly
  # inside and not strictly outside each other
  # other is a Cylinder object
  # returns a Boolean
  def does_intersect_cylinder (self, other):
    if(self.is_inside_cylinder(other) or other.is_inside_cylinder(self)):
      return False
    withinZ = abs(self.z - other.z) < (self.height + other.height)/2
    withinXY = math.hypot(self.x - other.x, self.y - other.y) < self.radius + other.radius
    return(withinZ and withinXY)

def main():
  # read data from standard input

  # read the coordinates of the first Point p

  # create a Point object 

  # read the coordinates of the second Point q

  # create a Point object 

  # read the coordinates of the center and radius of sphereA

  # create a Sphere object 

  # read the coordinates of the center and radius of sphereB

  # create a Sphere object

  # read the coordinates of the center and side of cubeA

  # create a Cube object 

  # read the coordinates of the center and side of cubeB

  # create a Cube object 

  # read the coordinates of the center, radius and height of cylA

  # create a Cylinder object 

  # read the coordinates of the center, radius and height of cylB

  # create a Cylinder object
  pp = sys.stdin.readline()
  pp = pp.split(" ")
  p = Point(float(pp[0]),float(pp[1]),float(pp[2]))

  qq = sys.stdin.readline()
  qq = qq.split(" ")
  q = Point(float(qq[0]),float(qq[1]),float(qq[2]))

  A = sys.stdin.readline()
  A = A.split(" ")
  sphereA = Sphere(float(A[0]),float(A[1]),float(A[2]),float(A[3]))
  
  B = sys.stdin.readline()
  B = B.split(" ")
  sphereB = Sphere(float(B[0]),float(B[1]),float(B[2]),float(B[3]))
  
  A = sys.stdin.readline()
  A = A.split(" ")
  cubeA = Cube(float(A[0]),float(A[1]),float(A[2]),float(A[3]))
  
  B = sys.stdin.readline()
  B = B.split(" ")
  cubeB = Cube(float(B[0]),float(B[1]),float(B[2]),float(B[3]))
  
  A = sys.stdin.readline()
  A = A.split(" ")
  cylA = Cylinder(float(A[0]),float(A[1]),float(A[2]),float(A[3]),float(A[4]))
  
  B = sys.stdin.readline()
  B = B.split(" ")
  cylB = Cylinder(float(B[0]),float(B[1]),float(B[2]),float(B[3]),float(B[4]))
  # print if the distance of p from the origin is greater 
  # than the distance of q from the origin

  # print if Point p is inside sphereA

  # print if sphereB is inside sphereA

  # print if cubeA is inside sphereA

  # print if cylA is inside sphereA

  # print if sphereA intersects with sphereB

  # print if cubeB intersects with sphereB

  # print if the volume of the largest Cube that is circumscribed 
  # by sphereA is greater than the volume of cylA

  origin = Point(0, 0, 0)
  if(p.distance(origin) > q.distance(origin)):
    print("Distance of Point p from the origin is greater than the distance of Point q from the origin")
  else:
    print("Distance of Point p from the origin is not greater than the distance of Point q from the origin")

  if(sphereA.is_inside_point(p)):
    print("Point p is inside sphereA")
  else:
    print("Point p is not inside sphereA")

  if(sphereA.is_inside_sphere(sphereB)):
    print("sphereB is inside sphereA")
  else:
    print("sphereB is not inside sphereA")

  if(sphereA.is_inside_cube(cubeA)):
    print("cubeA is inside sphereA")
  else:
    print("cubeA is not inside sphereA")

  if(sphereA.is_inside_cyl(cylA)):
    print("cylA is inside sphereA")
  else:
    print("cylA is not inside sphereA")

  if(sphereB.does_intersect_sphere(sphereA)):
    print("sphereA does intersect sphereB")
  else:
    print("sphereA does not intersect sphereB")

  if(sphereB.does_intersect_cube(cubeB)):
    print("cubeB does intersect sphereB")
  else:
    print("cubeB does not intersect sphereB")

  if(sphereA.circumscribe_cube().volume() > cylA.volume()):
    print("Volume of the largest Cube that is circumscribed by sphereA is greater than the volume of cylA")
  else:
    print("Volume of the largest Cube that is circumscribed by sphereA is not greater than the volume of cylA")

#  print()
  # print if Point p is inside cubeA

  # print if sphereA is inside cubeA

  # print if cubeB is inside cubeA

  # print if cylA is inside cubeA

  # print if cubeA intersects with cubeB

  # print if the intersection volume of cubeA and cubeB
  # is greater than the volume of sphereA

  # print if the surface area of the largest Sphere object inscribed 
  # by cubeA is greater than the surface area of cylA
  if(cubeA.is_inside_point(p)):
    print("Point p is inside cubeA")
  else:
    print("Point p is not inside cubeA")

  if(cubeA.is_inside_sphere(sphereA)):
    print("sphereA is inside cubeA")
  else:
    print("sphereA is not inside cubeA")

  if(cubeA.is_inside_cube(cubeB)):
    print("cubeB is inside cubeA")
  else:
    print("cubeB is not inside cubeA")

  if(cubeA.is_inside_cylinder(cylA)):
    print("cylA is inside cubeA")
  else:
    print("cylA is not inside cubeA")

  if(cubeA.does_intersect_cube(cubeB)):
    print("cubeA does intersect cubeB")
  else:
    print("cubeA does not intersect cubeB")

  if(cubeA.intersection_volume(cubeB) > sphereA.volume()):
    print("Intersection volume of cubeA and cubeB is greater than the volume of sphereA")
  else:
    print("Intersection volume of cubeA and cubeB is not greater than the volume of sphereA")

  if(cubeA.inscribe_sphere().area() > cylA.area()):
    print("Surface area of the largest Sphere object inscribed by cubeA is greater than the surface area of cylA")
  else:
    print("Surface area of the largest Sphere object inscribed by cubeA is not greater than the surface area of cylA")

#  print()

  # print if Point p is inside cylA

  # print if sphereA is inside cylA

  # print if cubeA is inside cylA

  # print if cylB is inside cylA

  # print if cylB intersects with cylA
  if(cylA.is_inside_point(p)):
    print("Point p is inside cylA")
  else:
    print("Point p is not inside cylA")

  if(cylA.is_inside_sphere(sphereA)):
    print("sphereA is inside cylA")
  else:
    print("sphereA is not inside cylA")

  if(cylA.is_inside_cube(cubeA)):
    print("cubeA is inside cylA")
  else:
    print("cubeA is not inside cylA")

  if(cylA.is_inside_cylinder(cylB)):
    print("cylB is inside cylA")
  else:
    print("cylB is not inside cylA")

  if(cylA.does_intersect_cylinder(cylB)):
    print("cylB does intersect cylA")
  else:
    print("cylB does not intersect cylA")

if __name__ == "__main__":
  main()