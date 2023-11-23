from graphics.rectangle import area as rect_area
from graphics.circle import perimeter as circle_perimeter
from graphicsd.cuboid import surface_area as cuboid_surface_area
from graphicsd.sphere import volume as sphere_volume
length=5
width=3
radius=4
height=6
print("Rectangle Area:",rect_area(length,width))
print("Circle Perimeter:",circle_perimeter(radius))
print("Cuboid Surface Area:",cuboid_surface_area(length,width,height))
print("Sphere Volume:",sphere_volume(radius))
