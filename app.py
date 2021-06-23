import pandas as pd
import json
import uuid
import geopandas
from shapely.geometry import Point, Polygon, LineString

intersection_=pd.read_csv('/Users/macbook/PycharmProjects/intersections/IntersectionsParis1.csv',sep=';')
intersection_[['X']] =intersection_['X_a_inters'].apply(lambda x: float(x.split()[0].replace(',', '.')))
intersection_[['Y']] =intersection_['Y_a_inters'].apply(lambda x: float(x.split()[0].replace(',', '.')))
print(intersection_.head(2))
print(intersection_.columns)
#########################préparation du fichier Json################################
with open("/Users/macbook/PycharmProjects/intersections/itinéraire_inters.json", encoding='utf-8', errors='ignore') as json_data:
    data = json.load(json_data, strict=False)
    data = data[0]['legs'][0]['steps']
#print(data)

intersection = []

all_lines = []

liste_des_largeurs = []

index_of_line_in_request = 0
points_json = []
current_request_uuid = str(uuid.uuid1())
for location in data:
    # LOOP dans chaque intersection pour récup toutes les locations
    for coordinate in location['intersections']:
        # Nous crééons l'objet largeur
        coordinate['intersectiondu_segment'] = 0.0
        # Si l'array a une longueur de 2 (0: pt1 et 1: pt2), on lance la requete et on vide l'array
        intersection.append(coordinate['location'])
        if len(intersection) == 2:
            index_of_line_in_request += 1
            # construction des deux points, extrêmité de la ligne droite

            point1 = 'POINT( ' + str(intersection[0][0]) + " " + str(intersection[0][1]) + ' )'
            print(point1)
            # print(type(point1))
            x1 = int(intersection[0][0])
            y1 = int(intersection[0][1])

            point2 = 'POINT( ' + str(intersection[1][0]) + " " + str(intersection[1][1]) + ' )'
            print(point2)
            x2 = int(intersection[1][0])
            y2 = int(intersection[1][1])
            current_line = (current_request_uuid, index_of_line_in_request, point1, point2)
            curr = (point1, point2)
            all_lines.append(current_line)
            points_json.append(curr)
            print(all_lines)
            print("points_json", points_json)


            intersection = []

            intersection.append(coordinate['location'])
            print("intersections:", intersection)

            liste_des_largeurs.append(None)

            print('liste des largeurs :', liste_des_largeurs)

print("points_json", points_json)
######################préparation d'un dataframe avec les points json extrait de l'itinéraire###################@
points_json_=pd.DataFrame(points_json, columns=['X','Y'])
points=points_json_.copy()
points[['lat1']]=points['X'].apply(lambda x : x[6:-11])
points[['lon1']]=points['X'].apply(lambda x : x[15:-1])
points[['lat2']]=points['Y'].apply(lambda x : x[6:-11])
points[['lon2']]=points['Y'].apply(lambda x : x[15:-1])
points=points.drop(['X'],axis=1)
points=points.drop(['Y'],axis=1)
points['lat1']=points['lat1'].astype(float)
points['lon1']=points['lon1'].astype(float)
points['lat2']=points['lat2'].astype(float)
points['lon2']=points['lon2'].astype(float)
############################utilisation de la base de données pour affichet les infos des intersections#############@
# Exemple à partir des deux premiers points Json
for i in range(intersection_.shape[0]):
    for j in range(points.shape[0]):

        point1 = Point(points['lat1'][j] - 1, points['lon1'][j] - 1)
        point2 = Point(points['lat2'][j], points['lon2'][j])
        # on trace une ligne entre les deux points pour définir le premier segment
        # line = LineString([point1, point2])
        # on définit notre buffer Y

        Y = point2.buffer(0.0001)  # buffer de diamètre 10 mètres

        # coord sont les coordonnées des points sur le fichier csv
        coord = Point(intersection_['X'][i], intersection_['Y'][i])

        # if points['lat2'][j]<=intersection['X_a_inters'][i] and points['lon2'][j]<=intersection['Y_a_inters'][i]:
        # on rajoute une condition pour vérifier si les points du fichier csv appartiennent bien au buffer Y et on affiche tous ces points
        if Y.contains(coord) == True:
            x = intersection_['osm_id'][i], intersection_['Street'][i], intersection_['ID_interse'][i], intersection_['X_a_inters'][i], \
                intersection_['Y_a_inters'][i]

            print(x)

# print(points)
# print(coord)
# points.append(coord)
# print(Y.contains(coord)) 
