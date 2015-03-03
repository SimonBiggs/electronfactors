import numpy as np

from finding_centre import FindCentre
from straightening import Straighten
from ellipse_fitting import FitEllipse


class EquivalentEllipse(object):
    """Returns an equivalent ellipse. Requires the input of cutout X and Y coords along with the centre_fit function.
    """
    def __init__(self, **kwargs):       
        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.circle_fit = kwargs['circle_fit']

        self._FoundCentre = FindCentre(x=self.cutoutXCoords, y=self.cutoutYCoords, circle_fit=self.circle_fit)
        self.centre = self._FoundCentre.centre
        
        self._Straightened = Straighten(x=self.cutoutXCoords, y=self.cutoutYCoords, centre = self.centre)
        
        self._FittedEllipse = FitEllipse(x=self._Straightened.straightenedXCoords, 
                                         y=self._Straightened.straightenedYCoords)
        
        self.inputCutout = self._Straightened.cutout
        self.centredCutout = self._Straightened.centredCutout
        self.straightenedCutout = self._Straightened.straightenedCutout
        
        self.eqEllipse = self._FittedEllipse.ellipse
        self.eqEllipseXCoords = self._FittedEllipse.ellipseXCoords
        self.eqEllipseYCoords = self._FittedEllipse.ellipseYCoords
        
        self.width = self._FittedEllipse.width
        self.length = self._FittedEllipse.length
