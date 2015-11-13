import numpy as np
import shapely.geometry as sh
from scipy.optimize import basinhopping


def circle_in_cutout(minimiserInput,cutout,weight):

	a = minimiserInput[0]
	b = minimiserInput[1]
	r = minimiserInput[2]**2

	circle = sh.Point(a,b).buffer(r)

	toMinimise = weight*circle.difference(cutout).area + cutout.difference(circle).area

	return toMinimise


def width_calc_minimiser(cutout,weight):

	minimizer_kwargs = {"args": (cutout,weight,), "method": 'BFGS' }
	x0 = np.array([0,0,1])

	output = basinhopping(circle_in_cutout,x0,niter=100,minimizer_kwargs=minimizer_kwargs)

	return output


def width_return(cutout,weight):
	
	output = width_calc_minimiser(cutout,weight)
	
	return output.x[2]**2 * 2


def length_calc(cutout,width):
	
	ratio = ratio_calc(cutout,width)

	length = width/ratio

	return length
	

def ratio_calc(cutout,width):
	
	perimeter = cutout.length
	area = cutout.area

	ratio = ((perimeter/area)*width)/2-1

	return ratio


def shapely_cutout(x,y):
    
    cutoutPolyList = []
    
    for i in range(len(x)):
        cutoutPolyList = cutoutPolyList + [(x[i],y[i])]

    cutout = sh.Polygon(cutoutPolyList)
    
    return cutout




