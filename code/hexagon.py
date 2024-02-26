'''
Tạo không gian lục giác 

Class Point(): Tạo 1 điểm tọa độ

create_point(hex_boundary)=>Tạo 1 điểm trong hình vuông bao quanh hình lục giác với hex_boundary là list các lng và lat của 6 đỉnh hình lục giác rồi kiểm tra xem nó có thuộc hình lục giác ko
    !!!Chú ý: Các điểm được tạo theo phân phối uniform trong hình vuông=>Nó phân bố theo phân phối uniform trong hình lục giác


''' 
import random
import folium
import h3
import pandas as pd
import matplotlib.pyplot as plt
from config import *

class Point:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
        
def create_point(hex_boundary):
    vertices = [(lat, lng) for lat,lng in hex_boundary]
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

def plot_scatter(df, metric_col, x='longitude', y='latitude', marker='.', alpha=1, figsize=(16,12), colormap='viridis'):
    df.plot.scatter(x=x, y=y, c=metric_col, title=metric_col
                    , edgecolors='none', colormap=colormap, marker=marker, alpha=alpha, figsize=figsize);
    plt.xticks([], []); plt.yticks([], [])
def aperture_downsampling(df, hex_col, metric_col, coarse_aperture_size):
    df_coarse = df.copy()
    coarse_hex_col = 'hex{}'.format(coarse_aperture_size)
    df_coarse[coarse_hex_col] = df_coarse[hex_col].apply(lambda x: h3.h3_to_parent(x,coarse_aperture_size))
    dfc = df_coarse.groupby([coarse_hex_col])[[metric_col,]].mean().reset_index()
    dfc['lat'] = dfc[coarse_hex_col].apply(lambda x: h3.h3_to_geo(x)[0])
    dfc['lng'] = dfc[coarse_hex_col].apply(lambda x: h3.h3_to_geo(x)[1])
    return dfc

def kring_smoothing(df, hex_col, metric_col, k):
    dfk = df[[hex_col]]
    dfk.index = dfk[hex_col]
    dfs =  (dfk[hex_col]
                 .apply(lambda x: pd.Series(list(h3.k_ring(x,k)))).stack()
                 .to_frame('hexk').reset_index(1, drop=True).reset_index()
                 .merge(df[[hex_col,metric_col]]).fillna(0)
                 .groupby(['hexk'])[[metric_col]].sum().divide((1 + 3 * k * (k + 1)))
                 .reset_index()
                 .rename(index=str, columns={"hexk": hex_col}))
    dfs['latitude'] = dfs[hex_col].apply(lambda x: h3.h3_to_geo(x)[0])
    dfs['longitude'] = dfs[hex_col].apply(lambda x: h3.h3_to_geo(x)[1])
    return dfs

def weighted_kring_smoothing(df, hex_col, metric_col, coef):
    # normalize the coef
    a = []
    for k, coe in enumerate(coef):
        if k == 0:
            a.append(coe)
        else:
            a.append(k * 6 * coe)
    coef = [c / sum(a) for c in coef]

    # weighted smoothing
    df_agg = df[[hex_col]]
    df_agg['hexk'] = df_agg[hex_col]
    df_agg.set_index(hex_col,inplace=True)
    temp2 = [df_agg['hexk'].reset_index()]
    temp2[-1]['k'] = 0
    K=len(coef)-1
    for k in range(1,K+1):
        temp2.append((df_agg['hexk']
                     .apply(lambda x: pd.Series(list(h3.hex_ring(x,k)))).stack()
                     .to_frame('hexk').reset_index(1, drop=True).reset_index()
                ))
        temp2[-1]['k'] = k
    df_all = pd.concat(temp2).merge(df)
    df_all[metric_col] = df_all[metric_col]*df_all.k.apply(lambda x:coef[x])
    dfs = df_all.groupby('hexk')[[metric_col]].sum().reset_index().rename(index=str, columns={"hexk": hex_col})
    dfs['lat'] = dfs[hex_col].apply(lambda x: h3.h3_to_geo(x)[0])
    dfs['lng'] = dfs[hex_col].apply(lambda x: h3.h3_to_geo(x)[1])
    return dfs
def visualize_k_ring(center_lat, center_lng, k,level):
    # Tạo một bản đồ Folium
    m = folium.Map(location=[center_lat, center_lng], zoom_start=10)

    # Tính toán mã hexagon cho điểm trung tâm
    center_h3 = h3.geo_to_h3(center_lat, center_lng, level)

    # Tạo một list chứa các mã hexagon trong k-ring
    k_ring_hexagons = h3.k_ring(center_h3, k)
    print(k_ring_hexagons)

    # Lặp qua từng mã hexagon trong k-ring và vẽ chúng trên bản đồ
    for hexagon in k_ring_hexagons:
        # Tính toán tọa độ của các đỉnh của hexagon
        vertices = h3.h3_to_geo_boundary(hexagon)

        # Tạo một list chứa tọa độ của các đỉnh của hexagon
        hexagon_vertices = [[vertex[0], vertex[1]] for vertex in vertices]

        # Vẽ hexagon lên bản đồ Folium
        folium.Polygon(
            locations=hexagon_vertices,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4
        ).add_to(m)

    # Hiển thị bản đồ
    return m

def get_surrounding_h3(h3_index, k):
    # Sử dụng hàm k_ring để lấy các ô h3 xung quanh
    surrounding_h3 = h3.k_ring(h3_index, k)
    return surrounding_h3


