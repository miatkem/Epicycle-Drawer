from PIL import Image
import math

#A class that reads a pictures and creates a path for the fourier circles to follow
class ImageTrace:
    #Contructor that takes an image
    def __init__(self,image):
        self.image=image
        self.points=[]
        width, height = image.size
        pixImg = self.image.load()
        #add all black pixels locations to points
        for x in range(width):
            for y in range(height):
                color = self.image.getpixel((x,y))
                #grayscale pictures
                if type(color) == int:
                    if color == 1:
                        self.points.append((x,y))
                #rgb pictures
                elif color[0]+color[1]+color[2]==0:
                    self.points.append((x,y))
        
        #put the points into order using the closest points method
        self.orderedPoints=[self.points[0]]
        while len(self.points)>0:
            ind=self.closestPoint(self.orderedPoints[len(self.orderedPoints)-1])
            self.orderedPoints.append(self.points.pop(ind))
        
    #calculates distance between two xy points        
    def distance(self,pointA,pointB):
        return (math.pow((pointA[0]-pointB[0]),2) + math.pow((pointA[1]-pointB[1]),2))
    
    #finds next closest point in list of points to the parameter point
    def closestPoint(self,point):
        closestInd = 0
        minDistance = self.distance(self.points[0],point)
        for ind in range(1,len(self.points)):
            nextDist = self.distance(self.points[ind],point)
            if nextDist < minDistance:
                minDistance=nextDist
                closestInd = ind
        return closestInd
    
        