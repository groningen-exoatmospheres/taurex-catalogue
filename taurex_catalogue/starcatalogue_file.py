from taurex.mixin import StarMixin
from .cataloguereader import FileReader
## this is required for aq.
import astropy.units as u
#import exoatlas as ea
import numpy as np
from taurex.constants import RSOL, MSOL

class StarCatalogueFile(StarMixin):

    def __init_mixin__(self, planet_name=None, temperature=None, 
                       radius=None, distance=None, magnitudeK=None, metallicity=None,
                       mass=None, ld_method='unique',
                 ldc=[0.38606363, 0.58637444, -0.19471546, -0.00559748], catalogue_path = None, planet_no = None):

        self._planet_name = planet_name
        self._planet_no = planet_no
        self._catalogue_path = catalogue_path

        if self._catalogue_path is None:
            raise TypeError('The catalogue file is None') 
        else:
            reader = FileReader(filename=catalogue_path, target_no=self._planet_no, target_name=self._planet_name)

        self._star_params = dict([(f, (u*v)) for f, u, v in reader.star_params])
        self._planet_params = dict([(f, (u*v)) for f, u, v in reader.planet_params])

        
        ##star_distance = 1/star_data['gaia_parallax']*1e3


        if radius is None:
            self._radius = self._star_params['Radius'].to(u.Rsun).value*RSOL
        
        if distance is None:
            self.distance = self._star_params['Distance'].to(u.pc).value

        if magnitudeK is None:
            self.magnitudeK = self._star_params['K']

        if metallicity is None:
            ### TO BE UPDATED
            #self._metallicity = 0.0
            self._metallicity = self._star_params['Metallicity']
        if mass is None:
            self._mass= self._star_params['Mass'].to(u.Msun).value*MSOL
        
        if temperature is None:
            ## self.temperature NEEDS TO BE CALLED LAST AS IT ALSO recompute_spectrum()
            self.temperature = self._star_params['Temperature'].to(u.K).value
        else:
            self.temperature = self.temperature
        
        self.info('STAR CATALOGUE PARAMETERS')
        self.info('planet name: '+str(self._planet_name))
        self.info('star radius: '+str(self._radius/RSOL))
        self.info('star mass: '+str(self._mass/MSOL))
        self.info('star temperature: '+str(self._temperature))
        self.info('star metallicity: '+str(self._metallicity))
        self.info('star distance: '+str(self.distance))
        self.info('star magK: '+str(self.magnitudeK))

    @classmethod
    def input_keywords(self):
        return ['cataloguefile', 'edwards' ]