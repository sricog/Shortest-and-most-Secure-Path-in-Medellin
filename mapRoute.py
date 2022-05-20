import gmplot
import pandas as pd
import webbrowser
apikey = 'AIzaSyBFSjXTLiGgLYvA_-SrCaoUWfBAouEgEUo'
def createPolygon():
    lngs = []
    lats = []
    area = pd.read_csv('poligono_de_medellin.csv',sep=';')
    polygon = str(area['geometry'].to_list()[0])[9:-2].split(',')
    for coord in polygon:
        long,lat = list(map(float,coord[1:].split(' ')))
        lngs.append(long)
        lats.append(lat)
    return lats,lngs 
def organizeCoordinates(path):
    lat = []
    long = []
    for coord in path:
        longg,latt = list(map(float,coord[1:-1].split(',')))
        long.append(longg)
        lat.append(latt)
    return lat,long

def createMap1(path1,path3):
    latLimit, longLimit = createPolygon()
    lat,long = organizeCoordinates(path1)
    # lat2,long2 = organizeCoordinates(path2)
    lat3,long3 = organizeCoordinates(path3)
    gmapone = gmplot.GoogleMapPlotter(
    6.267203842477565, -75.579710387, 12,
    apikey=apikey,)
    gmapone.polygon(latLimit,longLimit,face_color='white',
                    face_alpha = 0.4, edge_color='black', edge_width=10)
    gmapone.scatter(lat,long,'green',size = 3,marker = False)
    gmapone.plot(lat,long,'green',edge_width = 4)
    # gmapone.scatter(lat2,long2,'blue',size = 3,marker = False)
    # gmapone.plot(lat2,long2,'blue',edge_width = 5)
    gmapone.scatter(lat3,long3,'red',size = 3,marker = False)
    gmapone.plot(lat3,long3,'red',edge_width = 6)
    gmapone.marker(lat[0],long[0],label = 'A',title='Punto Inicio')
    gmapone.marker(lat[-1],long[-1],label = 'B')
    gmapone.draw('map.html')
    webbrowser.open_new_tab('map.html')

def createMap2(path):
    latLimit, longLimit = createPolygon()
    lat,long = organizeCoordinates(path)
    gmapone = gmplot.GoogleMapPlotter(
    6.267203842477565, -75.579710387, 12,
    apikey=apikey,)
    gmapone.polygon(latLimit,longLimit,face_color='white',
                    face_alpha = 0.4, edge_color='black', edge_width=10)
    gmapone.scatter(lat,long,'green',size = 3,marker = False)
    gmapone.plot(lat,long,'green',edge_width = 4)
    gmapone.marker(lat[0],long[0],label = 'A',title='Punto Inicio')
    gmapone.marker(lat[-1],long[-1],label = 'B')
    gmapone.draw('map.html')
    webbrowser.open_new_tab('map.html')