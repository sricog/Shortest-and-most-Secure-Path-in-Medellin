import pandas as pd
import JsonApi
import mapRoute
import graphAlgorithms
import time

data = pd.read_csv('calles_de_medellin_con_acoso.csv', sep = ';',)
data.harassmentRisk = data.harassmentRisk.fillna(data.harassmentRisk.mean())
graph= {}
unique_origins = data.origin.unique()

# The graph is represented as a dict of dicts
# Keys are the origins and at first their values are empty dicts.
for i in range(len(unique_origins)):
    graph[unique_origins[i]] = {}

# The values are filled.
# The keys are the destinations and the values are the distance, and
# harassment risk for each destination.
for i in data.index:
    if data["oneway"][i]==False:
        graph[data["origin"][i]][data["destination"][i]]=(data["length"][i],data["harassmentRisk"][i])
    else:
        graph[data["origin"][i]][data["destination"][i]]=(data["length"][i],data["harassmentRisk"][i])
        try:
            graph[data["destination"][i]][data["origin"][i]]=(data["length"][i],data["harassmentRisk"][i])
        except KeyError:#  This error happens when 'oneway' is True and the destination must be as a key in the dict as a origin.
                        # In some cases, this coordinates where not presented as a origin in the dataframe.
            graph[data['destination'][i]]={data["origin"][i]:(data["length"][i],data["harassmentRisk"][i])}


def main():
    first_menu()
    print("-------------------------")

def first_menu():
    print("---Welcome to our proyect---\nPlease enter your origin location. Be as specific as possible.\nExample: \"Universidad Nacional medellin porteria peatonal\"")
    origin = graphAlgorithms.nearestOrigin(JsonApi.strToCoordinates(input()),data)
    origin = str((origin[1],origin[0]))
    print("Great! Now enter your destination. Be as specific as possible")
    destination = graphAlgorithms.nearestDestination(JsonApi.strToCoordinates(input()),data)
    destination = str((destination[1],destination[0]))
    print("Great! We offer you different routes depending on your needs.\nEnter 1 if you want to know the shortest and the safest path.")
    print("Enter 2 if you want to know the shortest path without exceeding a harassmernt risk.\nEnter 3 if you want to know the safest path without exceeding a distance.")
    print("Enter other option to exit the program.")
    choice = int(input())
    if choice == 1:
        first_choice_menu(origin,destination)
    elif choice == 2:
        second_choice_menu(origin,destination)
    elif choice == 3:
        third_choice_menu(origin,destination)
        
 
def first_choice_menu(origin,destination):
    t1 = time.time()
    safest_path,total_distance,risk = graphAlgorithms.safest_path(origin,destination,graph) 
    # balanced_path,total_distance1,risk1 = graphAlgorithms.shortest_and_safest_path(origin,destination,graph) 
    shortest_path, total_distance2,risk2 = graphAlgorithms.shortest_path(origin,destination,graph)
    if float('infinity') in [total_distance,total_distance2,risk,risk2]: 
        print("There's no path.")
        exit() 
    mapRoute.createMap1(safest_path,shortest_path)
    tf = time.time() - t1
    print(f"Great. The algorithm took {tf} seconds.")
    print(f"The green path is the safest path. It's total distance is: {total_distance} meters. The risk is: {risk}")
    # print(f"The blue path is the balanced path. It's total distance is: {total_distance1} meters. The risk is: {risk1}")
    print(f"The red path is the shortest path. It's total distance is: {total_distance2} meters. The risk is: {risk2}")
    
def second_choice_menu(origin,destination):
    max_risk = float(input("What is the maximum risk?"))
    t1 = time.time()
    path, distance,risk = graphAlgorithms.no_exceed_risk(origin,destination,graph,max_risk)
    if float('infinity') in [distance,risk]: 
        print("There's no path.")
        exit()
    mapRoute.createMap2(path)
    tf = time.time() - t1
    print(f"Great. The algorithm took {tf} seconds.")
    print(f"Average risk: {risk}\nTotal distance: {distance}")
    
def third_choice_menu(origin,destination):
    max_distance = float(input("What is the maximum distance?"))
    t1 = time.time()
    path,distance,risk = graphAlgorithms.no_exceed_distance(origin,destination,graph,max_distance)
    if float('infinity') in [distance,risk]: 
        print("There's no path.")
        exit()
    mapRoute.createMap2(path)
    tf = time.time() - t1
    print(f"Great. The algorithm took {tf} seconds.")
    print(f"Average risk: {risk}\nTotal distance: {distance}")

main()
