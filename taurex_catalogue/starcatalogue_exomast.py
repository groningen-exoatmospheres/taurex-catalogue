from taurex.mixin import StarMixin
## this is required for aq.
import astropy.units as u
#import exoatlas as ea
import numpy as np
from taurex.constants import RSOL, MSOL
import requests

class StarCatalogueExomast(StarMixin):

    def __init_mixin__(self, planet_name=None, temperature=None, 
                       radius=None, distance=None, magnitudeK=None, metallicity=None,
                       mass=None, ld_method='unique',
                 ldc=[0.38606363, 0.58637444, -0.19471546, -0.00559748], planet_no = None):

        self._planet_name = planet_name
        self._planet_no = planet_no

        x = requests.get("https://exo.mast.stsci.edu/api/v0.1/exoplanets/identifiers/", params={'name': planet_name})
        name = x.text.split(':')[1].split(',')[0].split('"')[1]
        x = requests.get('https://exo.mast.stsci.edu/api/v0.1/exoplanets/'+name+'/properties', params={'format':'json', 'flatten_response':False})
        self._dicoX = x.json()[0]

        self._canonical_planet_name = self._dicoX['canonical_name']

        if radius is None:
            self._radius = self._dicoX['Rs']*RSOL
        
        if distance is None:
            self.distance = self._dicoX['distance']

        if magnitudeK is None:
            self.magnitudeK = self._dicoX['Kmag']

        if metallicity is None:
            ### TO BE UPDATED
            #self._metallicity = 0.0
            self._metallicity = self._dicoX['Fe/H']
        if mass is None:
            self._mass= self._dicoX['Ms']*MSOL
        
        if temperature is None:
            ## self.temperature NEEDS TO BE CALLED LAST AS IT ALSO recompute_spectrum()
            self.temperature = self._dicoX['Teff']
        else:
            self.temperature = self.temperature
        
        self.info('STAR CATALOGUE PARAMETERS')
        self.info('planet name: '+str(self._planet_name))
        self.info('star radius: '+str(self._radius/RSOL))
        self.info('star mass: '+str(self._mass/MSOL))
        self.info('star temperature: '+str(self.temperature))
        self.info('star metallicity: '+str(self._metallicity))
        self.info('star distance: '+str(self.distance))
        self.info('star magK: '+str(self.magnitudeK))

    @classmethod
    def input_keywords(self):
        return ['exomast' ]