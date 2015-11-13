import numpy as np

import shapely.affinity as af
import shapely.geometry as sh

from scipy.optimize import basinhopping



def shapely_cutout(x,y):
    
    cutoutPolyList = []
    
    for i in range(len(x)):
        cutoutPolyList = cutoutPolyList + [(x[i],y[i])]

    cutout = sh.Polygon(cutoutPolyList)
    
    return cutout



unit_circle = sh.Point(0,0).buffer(1)


def create_ellipse(x):
    
    a = x[0]
    b = x[1]
    
    width = x[2]
    length = x[3]
    
    theta = x[4]
    
    
    ellipse = af.scale(unit_circle, xfact = width/2, yfact = length/2)
    
    ellipse = af.translate(ellipse, xoff=a, yoff=b)
    ellipse = af.rotate(ellipse, theta)

    return ellipse


def dirac_delta(t):
    
    a = 2**(-5)
    y = 1/(a*np.sqrt(np.pi)) * np.exp(-t**2/a**2)
    
    return(y)
    

def ellipse_in_cutout(minimiserInput,cutout,weight):#,maxDist):  
    
    ellipse = create_ellipse(minimiserInput)
    
    width = minimiserInput[2]
    length = minimiserInput[3]
    
    
    # A center pull is introduced in order to reduce
    # number of failures due to optimisation trying 
    # outside of the cutout
    #centerDist = np.hypot(*minimiserInput[0:2])
    
    #if (centerDist > maxDist):
        
    #    centerPull = centerDist
        
    #else:
    
    #    centerPull = 0
        
        
    
    toMinimise = (weight*ellipse.difference(cutout).area + 
                    cutout.difference(ellipse).area)# +
                    #centerPull)    

    return toMinimise



class MyTakeStep(object):
    
    def __init__(self, stepsize=0.5):
        self.stepsize = stepsize
        
    def __call__(self, x):
        s = self.stepsize
        x[0] += np.random.uniform(-3*s, 3*s)
        x[1] += np.random.uniform(-3*s, 3*s)
        x[2] += np.random.uniform(-6*s, 6*s)
        x[3] += np.random.uniform(-8*s, 8*s)
        x[4] += np.random.uniform(-90*s, 90*s)
        
        return x
    

def print_fun(x, f, accepted):

    global successCount_basinhopping
    global minVals_basinhopping
    global nSuccess_basinhopping

    a = x[0]
    b = x[1]

    w = abs(x[2])
    l = abs(x[3])

    if (l > w):
        width = w
        length = l
        theta = np.mod(x[4],180)
    else:
        width = l
        length = w
        theta = np.mod(x[4]+90,180)
    
    f = np.around(f,4)
    
    if accepted:
        
        if np.all(np.isnan(minVals_basinhopping)):
            
            minVals_basinhopping[0] = f
            successCount_basinhopping = 1
            
            print(("first local minima of %.4f at:\n"+
                "[a,b] = [%.4f, %.4f],"+
                " [width, length] = [%.4f, %.4f],"+
                " theta = %.4f\n")
                % (f,a,b,width,length,theta))
            
        elif (np.nanmin(minVals_basinhopping) == f):
        
            minVals_basinhopping[successCount_basinhopping] = f
            successCount_basinhopping += 1
            
            print(("agreeing local minima of %.4f at:\n"+
                "[a,b] = [%.4f, %.4f],"+
                " [width, length] = [%.4f, %.4f],"+
                " theta = %.4f\n")
                % (f,a,b,width,length,theta))
        
        elif (np.nanmin(minVals_basinhopping) > f):
        
            minVals_basinhopping[0] = f
            successCount_basinhopping = 1
            
            print(("new local minima of %.4f at:\n"+
                "[a,b] = [%.4f, %.4f],"+
                " [width, length] = [%.4f, %.4f],"+
                " theta = %.4f\n") 
                % (f,a,b,width,length,theta))
                
        else:
        
            print(("rejected local minima of %.4f at:\n"+
                "[a,b] = [%.4f, %.4f],"+
                " [width, length] = [%.4f, %.4f],"+
                " theta = %.4f\n") 
                % (f,a,b,width,length,theta))
            
        
    else:
        
        print(("failed to find local minima at:\n"+
            "[a,b] = [%.4f, %.4f],"+
            " [width, length] = [%.4f, %.4f],"+
            " theta = %.4f\n") 
            % (a,b,width,length,theta))
          

    if successCount_basinhopping >= nSuccess_basinhopping:
        return True



def eq_ellipse_calc(cutout,weight,userNSuccess):
    
    mytakestep = MyTakeStep()
    
    global nSuccess_basinhopping
    nSuccess_basinhopping = userNSuccess
    
    global minVals_basinhopping
    minVals_basinhopping = np.empty(nSuccess_basinhopping)
    minVals_basinhopping[:] = np.nan
    
    global successCount_basinhopping
    successCount_basinhopping = 0
    
    #maxDist = max(np.hypot(*cutout.boundary.xy))
    
    minimizer_kwargs = {"args": (cutout,weight,#maxDist,
                                 ), "method": 'BFGS' }
    x0 = np.array([0,0,1,1,0])

    output = basinhopping(ellipse_in_cutout,x0,
                          niter=1000,minimizer_kwargs=minimizer_kwargs,
                          take_step=mytakestep, callback=print_fun)

    return output
