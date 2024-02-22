'''
Tạo không gian lục giác 

Class Point(): Tạo 1 điểm tọa độ

create_point(hex_boundary)=>Tạo 1 điểm trong hình vuông bao quanh hình lục giác với hex_boundary là list các lng và lat của 6 đỉnh hình lục giác rồi kiểm tra xem nó có thuộc hình lục giác ko
    !!!Chú ý: Các điểm được tạo theo phân phối uniform trong hình vuông=>Nó phân bố theo phân phối uniform trong hình lục giác


''' 
import random
import folium
import h3

class Point:
    def __init__(self, lng, lat):
        self.x = lng
        self.y = lat
def create_point(hex_boundary):
    vertices = [(lon, lat) for lon,lat in hex_boundary]
    # Tìm tọa độ x và y tối đa, tối thiểu của hình lục giác
    min_x = min(vertices, key=lambda p: p[0])[0]
    max_x = max(vertices, key=lambda p: p[0])[0]
    min_y = min(vertices, key=lambda p: p[1])[1]
    max_y = max(vertices, key=lambda p: p[1])[1]

    while True:
        # Tạo một điểm ngẫu nhiên trong hình vuông bao quanh hình lục giác
        random_point = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))

        # Kiểm tra xem điểm này có nằm trong hình lục giác không
        if is_inside_hexagon(random_point, vertices):
            return Point(random_point[0],random_point[1])

def is_inside_hexagon(point, vertices):
    """Kiểm tra xem một điểm có nằm trong hình lục giác không."""
    # Sử dụng phương pháp Ray Casting để kiểm tra
    count = 0
    n = len(vertices)
    for i in range(n):
        j = (i + 1) % n
        if ((vertices[i][1] > point[1]) != (vertices[j][1] > point[1])) and \
           (point[0] < (vertices[j][0] - vertices[i][0]) * (point[1] - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) + vertices[i][0]):
            count += 1
    return count % 2 == 1

# 2 hàm visualize của H3
def visualize_hexagons(hexagons, color="red", folium_map=None):
    """
    hexagons is a list of hexcluster. Each hexcluster is a list of hexagons. 
    eg. [[hex1, hex2], [hex3, hex4]]
    """
    polylines = []
    lat = []
    lng = []
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        # flatten polygons into loops.
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        lat.extend(map(lambda v:v[0],polyline))
        lng.extend(map(lambda v:v[1],polyline))
        polylines.append(polyline)
    
    if folium_map is None:
        m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=13, tiles='cartodbpositron')
    else:
        m = folium_map
    for polyline in polylines:
        my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color=color)
        m.add_child(my_PolyLine)
    return m
    

def visualize_polygon(polyline, color):
    polyline.append(polyline[0])
    lat = [p[0] for p in polyline]
    lng = [p[1] for p in polyline]
    m = folium.Map(location=[sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=13, tiles='cartodbpositron')
    my_PolyLine=folium.PolyLine(locations=polyline,weight=8,color=color)
    m.add_child(my_PolyLine)
    return m