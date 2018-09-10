# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 06:24:37 2018

@author: Acer
"""

#me trying to build a homemade version of single-linkage heirarichal clustering. 


class Point(object):
    
    def __init__(self, ID, coords):
        """coords is a np Series (array)."""
        self.coords, self.ID = coords, ID 
        
    def getID(self):
        return self.ID
    
    def getCoords(self):
        return self.coords
    
    def setID(self, ID):
        self.ID = ID
        
    def getDistanceBetween(self, pointB, minkowski = 2):
        """ return the distance between a point and another point"""
        return(sum(abs(self.coords - pointB.getCoords())**minkowski)**(1/minkowski))

    def __str__(self):
        return(str(self.ID))


class Cluster(object):
    """List of points that belong to a particular cluster, with the data about how it was built"""

    def __init__(self, ID, clusterPoints, dist, children, active):
        self.ID = ID  #incremental.  
        self.points = clusterPoints  #points in the cluster. 
        self.dist = dist  #this is the minimum distance between clusers when it was added. 
        self.children = [-1,-1]  #IDS of the clusters that created the new cluster.
        self.active = True  #very important.  old clusters that have already been joined are made inactive. 
        
    def getID(self):
        return(self.ID)
        
    def getPoints(self):
        return(self.points)
        
    def getDist(self):
        return(self.dist)

    def getChildren(self):
        return(self.children)

    def isActive(self):
        return(self.active)

    def setActive(self, a):  #a should only ever be false. 
        self.active = a

    def __str__(self):
        result = 'Cluster ' + str(self.ID) + ': '
        for p in self.points:
            result = result + str(p) + ', '
        result = result[:-2] + '\n' #removes trailing comma and space 
        print(result)
        return result




class HeirarchicalCluster(object):
    
    def __init__(self, points, sample = 0):
        """Dictionary of each cluster added sequentially, from bottom of dendo to top...immutable"""
        if sample > 0 and sample < len(points):
            points = points[0:sample]  #just takes the first points
            #points = points[random.sample(range(len(points)),sample)]
        self.clusters = {}
        #initially each point is a cluster
        for i in range(len(points)):
            self.clusters[i] = Cluster(
                    ID = i, 
                    clusterPoints = [points[i]],  #initially every point is a cluster. 
                    dist = 0, 
                    children = [],
                    active = True)  #after clusters are joined the old ones become inactive.  

    def printCluster(self):
        for i in np.arange(len(self.clusters)):
            result = 'Cluster ' + str(i) + ': '
            for p in self.clusters[i].getPoints():
                result = result + str(p.getID()) + ', '
            result = result[:-2] + '\n' #removes trailing comma and space 
            print(result)
    
    def getDist(self):
        res = []
        for c in range(len(self.clusters)):
            print(c)
            print(self.clusters[c].getDist())
            print(res)
            res = res.append(self.clusters[c].getDist())
        return res
    
    #One iteration of aglomerative clustering. Find min distance between two clusters.   
    #single linkage - minimum connection between any two points in a cluster. 
    def joinNextCluster(self):
        
        best = 100**10  #start best at an arbitrarily high value.
        toCluster = []  #this will contain the clusterIDs of the 
        #iterate through each point in each cluster
#        print(str(len(self.clusters)))
        for i in np.arange(len(self.clusters)):
            c1 = self.clusters[i]
            if not(c1.isActive()): 
                continue
 #           print('assessing cluster' + str(i))
            count1 = 0
            for p1 in c1.getPoints():
#                print('assessing point ' + str(count1) + ' in cluster ' + str(i))

                #compare it to each point in the other clusters. 
                for j in np.arange(len(self.clusters)):
#                    print('2nd loop: comparing against cluster ' + str(j))
                    c2 = self.clusters[j]
 #                   print('IS CLUSTER ' + str(j) + 'ACTIVE? ' + str(c2.isActive()))
#                    print('c2.getID = ' + str(c2.getID()) + '...c1.getID = ' + str(c1.getID()))
                    #only compare it forward and to active clusters. otherwise you make every comparison twice.  
                    if c2.isActive() and c2.getID() > c1.getID():
#                        print('continue comparison')

                        count2 = 0
                        for p2 in c2.getPoints():
#                            print('Comparing point ' + str(count1) + ' in cluster ' + str(i) + ' to point ' + str(count2) + ' in cluster ' + str(j))
                            if p2.getID() != p1.getID():  #should be unecessary
                                challenger = p1.getDistanceBetween(pointB = p2)
 #                               print('comparing ' + str(i) + '( ' + str(round(challenger,3)) + ') to ' + str(j) + ' ( ' + str(round(best,3)))

                                if challenger < best: 
                                    best = challenger
 #                                   print('updating best to ' + str(round(best,3)))
                                    toCluster = [c1,c2]  #clusters to be joined. 
                            else: 
                                print("same point is in 2 clusters!")
                                exit()
                            count2 += 1
            count1 += 1
        
        #all clusters joined. 
        if len(toCluster) == 0:
#            print("no more clusters found!")
            return None  #stupid null equivalent in python. 
        
        #deactivate the old clusters, since they can't be joined any more.  
        toCluster[0].setActive(False)
        toCluster[1].setActive(False)
        
        #create a new cluster for the joined one. 
#        print('newCluster(' + str(len(self.clusters)+1) + '):' + str(toCluster[0].getID()) + ', ' + str(toCluster[1].getID()) + '\n')
        newCluster = Cluster(
                ID = len(self.clusters)+1,
                clusterPoints = toCluster[0].getPoints() + toCluster[1].getPoints(),
                dist = best,
                children = toCluster,
                active = True
                )
        
        #add the new heirarchical cluster object. 
        self.clusters[len(self.clusters)] = newCluster
        print(self)
        self.joinNextCluster()
        


    def __str__(self):
        result = ''
        for i in np.arange(len(self.clusters)):
            result = result + 'Cluster ' + str(i) + ': '
            for p in self.clusters[i].getPoints():
                result = result + str(p.getID()) + ', '
            result = result[:-2] + ' ACTIVE: ' + str(self.clusters[i].isActive()) + '\n' #removes trailing comma and space 
#        time.sleep(1)
        return(result)


#stand alone function to read a file and create a list of points from it. 
def createPointsList(dat):
    tempList = []
    for i in np.arange(len(df)):
        tempList.append(Point(i,coords = pd.Series(df.iloc[i])))
    return tempList
        
    
#START MAIN SCRIPT

import pandas as pd
import numpy as np
import time
import random

            
df = pd.read_csv('C:/Users/ACER/Desktop/HCTest.csv')
points = createPointsList(df.iloc[:,1:3])

hc = HeirarchicalCluster(points, sample = 10)
hc.joinNextCluster()



#hc.buildWholeCluster()
#print(hc)        
        #build distance metric to all other points.  
        #keep the best.   #REALLY BAD IMPLEMENTATION. 
        

