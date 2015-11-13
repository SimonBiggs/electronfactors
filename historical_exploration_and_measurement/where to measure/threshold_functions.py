import numpy as np
from scipy.interpolate import SmoothBivariateSpline


def single_angle_gap(xTest,yTest,xData,yData,xScale,yScale):
    xi = xScale * (xData - xData.min()) / xData.ptp()
    yi = yScale * (yData - yData.min()) / yData.ptp()
    
    xVal = xScale * (xTest - xData.min()) / xData.ptp()
    yVal = yScale * (yTest - yData.min()) / yData.ptp()
    
    dx = xi - xVal
    dy = yi - yVal
    
    if any((dx == 0) & (dy == 0)):
        gap = 0
        return gap
        
    theta = np.arctan(dy/dx)
    theta[dx<0] = theta[dx<0] + np.pi
    theta[(dx>0) & (dy<0)] = theta[(dx>0) & (dy<0)] + 2*np.pi
    theta[(dx==0) & (dy>0)] = np.pi/2
    theta[(dx==0) & (dy<0)] = 3*np.pi/2

    test = np.sort(theta)
    test = np.append(test,test[0] + 2*np.pi)
    gap = np.max(np.diff(test))*180/np.pi

    return gap


		
def angle_gap(xTest,yTest,xData,yData,xScale,yScale):
    
    dim = np.core.fromnumeric.shape(xTest)  
    
    if np.size(dim) == 0:
        gap = single_angle_gap(xTest,yTest,xData,yData,xScale,yScale)
        
        return gap
    
    
    gap = np.zeros(dim)
    
    
    if np.size(dim) == 1:
        for i in range(dim[0]):
            gap[i] = single_angle_gap(xTest[i],yTest[i],xData,yData,xScale,yScale)
            
        return gap
    
    
    for i in range(dim[0]):
        for j in range (dim[1]):
            gap[i,j] = single_angle_gap(xTest[i,j],yTest[i,j],xData,yData,xScale,yScale)

    return gap

		
		
def single_fit_give(xTest,yTest,xData,yData,zData,s):
    
    initialFitReturn = SmoothBivariateSpline(xData,yData,zData,s=s).ev(xTest,yTest)
    
    adjXData = np.append(xData,xTest)
    adjYData = np.append(yData,yTest)
    
    posAdjZData = np.append(zData,initialFitReturn + 1)
    negAdjZData = np.append(zData,initialFitReturn - 1)
    
    posFitReturn = SmoothBivariateSpline(adjXData,adjYData,posAdjZData,s=s).ev(xTest,yTest)
    negFitReturn = SmoothBivariateSpline(adjXData,adjYData,negAdjZData,s=s).ev(xTest,yTest)
    
    posGive = posFitReturn - initialFitReturn
    negGive = initialFitReturn - negFitReturn
    
    give = np.mean([posGive, negGive])
    
    return give
	
	

def fit_give(xTest,yTest,xData,yData,zData,s):
    
    dim = np.core.fromnumeric.shape(xTest)
    
    if np.size(dim) == 0:
        give = single_fit_give(xTest,yTest,xData,yData,zData,s)
        
        return give
    
    
    give = np.zeros(dim)
    
    
    if np.size(dim) == 1:
        for i in range(dim[0]):
            give[i] = single_fit_give(xTest[i],yTest[i],xData,yData,zData,s)
            
        return give
    
    
    for i in range(dim[0]):
        for j in range (dim[1]):
            give[i,j] = single_fit_give(xTest[i,j],yTest[i,j],xData,yData,zData,s)

    return give