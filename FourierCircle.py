import math, random, numpy

#Circle class to hold all properties of a circle in the fourier series
class FourierCircle:
    def __init__(self, radius, frequency, radians):
        self.radius=radius
        self.frequency=frequency
        self.radians=radians
    def setTip(self,tip):
        self.tip=tip
    def setCenter(self,center):
        self.center=center
    def tick(self, timeUnit):
        self.radians+=self.frequency*timeUnit

#A collection of circles and the methods necessary to but a fourier series drawing in motion
class FourierSeries:
    def __init__(self, size):
        #start in the center of screen
        self.startX = 500
        self.startY = 500
        self.size=size+1
        self.circles = []
        
        #random forier circle generator
        maxRad=150
        ratio=1-(1/size)
        #create first circle (freq. 0)
        rad=random.randint(1,maxRad)
        ang=random.uniform(0,6.28)        
        self.circles.append(FourierCircle(rad,0,ang))
        #create the rest of circles 2 at a time, one with positive and on negative freq.
        for freq in range(1,size+1):
            #maxRad(ius)  and ratio are used to create smaller and smaller radius circles
            ratio-=(1/size)
            maxRad=int(maxRad*ratio)+1
            #positive freq
            rad=random.randint(1,maxRad)
            ang=random.uniform(0,6.28)
            self.circles.append(FourierCircle(rad,freq,ang))
            #negative freq
            rad=random.randint(1,maxRad)
            ang=random.uniform(0,6.28)            
            self.circles.append(FourierCircle(rad,-freq,ang))
            
    #CREATE FOURIER CIRCLES BASED OFF OF AN ORDERED SET OF COORDINATES
    def loadOrderedSet(self, orderedSet):
        
        if len(orderedSet) < 2:
            return -1
        #Divide the amt of points in half until there are less than 500
        while len(orderedSet) > 500:
            newPoints = []
            for ind in range(0,len(orderedSet),2):
                newPoints.append(orderedSet[ind])
            orderedSet = newPoints        
        #Narrow down points that are too close and too far apart
        temp=[]
        for ind in range(1,len(orderedSet)):
            distance = math.pow((orderedSet[ind][0]-orderedSet[ind-1][0]),2) + math.pow((orderedSet[ind][1]-orderedSet[ind-1][1]),2)
            if distance < 100 or distance > 25:
                temp.append(orderedSet[ind])
        orderedSet = temp        
        
                
        
        #if orderedSet's length is odd delete last entry to prevent error
        if len(orderedSet) % 2 == 1:
            orderedSet.pop()
            
        #average x and y points in the ordered set to find the center of the volume
        sumX=0
        sumY=0
        for point in orderedSet:
            sumX+=point[0]
            sumY+=point[1]
        self.startX=int(sumX/len(orderedSet))
        self.startY=int(sumY/len(orderedSet))
        
        for ind in range(0,len(orderedSet)):
            orderedSet[ind]=(orderedSet[ind][0]-self.startX,orderedSet[ind][1]-self.startY)
        
        #create circles using fourier series
        transform = []
        amtEpicycles = len(orderedSet)
        self.size=amtEpicycles
        for i in range(int(-amtEpicycles/2),int(amtEpicycles/2)):
            complexSum=Complex(0,0) #(real,imag)
            #summation of the product of the complex polar and linear coordinates
            for j in range(int(-amtEpicycles/2),int(amtEpicycles/2)):
                theta = (2 * math.pi * i * j) / amtEpicycles;
                cons=Complex(math.cos(theta),-1*math.sin(theta))
                xy=Complex(orderedSet[j][0],orderedSet[j][1])
                complexSum=complexSum.add(xy.mult(cons))
            #divide complexSum by amt of epicycles to average
            complexSum.real = complexSum.real / amtEpicycles
            complexSum.imag = complexSum.imag / amtEpicycles
            #evaluate circle properties based on complex number in fourier series
            freq = i
            amp = math.sqrt(complexSum.real*complexSum.real + complexSum.imag*complexSum.imag)
            phase = math.atan2(complexSum.imag, complexSum.real)
            transform.append((amp,freq,phase))
        
        #reorder the fourier transform series in order of amplitude
        def amp(val): 
            return val[0]
        transform.sort(key = amp, reverse=True) 
        
        #create list of FourierCircles using the fourier transform
        self.circles = []
        for epi in transform:
            self.circles.append(FourierCircle(epi[0],epi[1],epi[2]))
        
    #TICK EACH FOURIER CIRCLE IN 'CIRCLES'
    def tick(self, timeUnit):
        for ind in range(0,len(self.circles)):
            self.circles[ind].tick(timeUnit)
    
    #SETS CIRCLE CENTER TO THE TIP OF THE PREVIOUS CIRCLE
    def getCenter(self, circleInd):
        if circleInd == 0: #the first circle's center is startX and startY (recursive basecase)
            self.circles[circleInd].setCenter((self.startX,self.startY))
            return (self.startX,self.startY)
        else:
            tip=self.getTip(circleInd-1) #call to getTip()
            self.circles[circleInd].setCenter(tip)
            return tip
    
    #SETS CIRCLE TIP TO THE (center + radius*cos(theta),center + radius*sin(theta))
    def getTip(self, circleInd=None):
        if circleInd == None:
            circleInd=len(self.circles)-1        
        center = self.getCenter(circleInd) #call to getCenter()
        tipX = center[0] + self.circles[circleInd].radius * math.cos(self.circles[circleInd].radians)
        tipY = center[1] + self.circles[circleInd].radius * math.sin(self.circles[circleInd].radians)
        self.circles[circleInd].setTip((tipX,tipY))
        return (tipX,tipY)
    
    #RETURN CIRCLE AT THE INDEX
    def getCircle(self, ind):
        return self.circles[ind]

#A class that holds an imaginary and real number (both floats) and does simple calculations 
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
    #add two complex numbers
    def add(self, complexNum):
        return Complex( self.real+complexNum.real,  self.imag+complexNum.imag)
    #multiply two complex numbers
    def mult(self, complexNum):
        re= self.real*complexNum.real- self.imag*complexNum.imag
        im= self.real*complexNum.imag+ self.imag*complexNum.real
        return Complex(re,im)
    
    
    
        
    
        
        