from taurex.mixin import PlanetMixin
## this is required for aq.
import astropy.units as u
import numpy as np
from taurex.constants import G, RJUP, MJUP, RSOL, MSOL, AU
from taurex.data.fittable import fitparam, Fittable, derivedparam
import requests

class PlanetCatalogueExomast(PlanetMixin):

    def __init_mixin__(self, planet_name=None, planet_mass=None, planet_radius=None,
                 planet_distance=None,
                 impact_param=None, orbital_period=None, albedo=None,
                 transit_time=None, eccentricity= None, pericentre_long = None, 
                 pericentre_time = None, ascending_node_long = None, mid_time = None, 
                 inclination = None, planet_no = None):

        ## estimated_transit_dur for actual calculation of the transit duration in hours
        self._planet_name = planet_name
        self._planet_no = planet_no
        self._user_params = [planet_mass, planet_radius, 
            planet_distance, impact_param, orbital_period, 
            albedo, transit_time, eccentricity, pericentre_long, 
            pericentre_time, ascending_node_long, mid_time]
        
        x = requests.get("https://exo.mast.stsci.edu/api/v0.1/exoplanets/identifiers/", params={'name': planet_name})
        name = x.text.split(':')[1].split(',')[0].split('"')[1]
        x = requests.get('https://exo.mast.stsci.edu/api/v0.1/exoplanets/'+name+'/properties', params={'format':'json', 'flatten_response':False})
        self._dicoX = x.json()[0]

        self._canonical_planet_name = self._dicoX['canonical_name']

        if planet_mass is None:
            planet_mass = self._dicoX['Mp']

        if planet_radius is None:
            planet_radius = self._dicoX['Rp']
        
        if planet_distance is None:
            planet_distance = self._dicoX['orbital_distance']

        if impact_param is None:
            ### TO BE UPDATED
            impact_param = self._dicoX['impact_parameter']
        
        if orbital_period is None:
            orbital_period = self._dicoX['orbital_period']

        if albedo is None:
            albedo = 0.3

        if eccentricity is None:
            #### TO BE UPDATED
            eccentricity = self._dicoX['eccentricity']

        if pericentre_long is None:
            #### TO BE UPDATED
            pericentre_long = self._dicoX['omega']

        if mid_time is None:
            mid_time = self._dicoX['transit_time']

        if pericentre_time is None:
            pericentre_time = 0.0
        if ascending_node_long is None:
            ascending_node_long = 0.0
        
        if transit_time is None:
            ## given in days and converted to seconds
            transit_time = self._dicoX['transit_duration']*24*60*60

        #self._mass = planet_mass*MJUP
        self.set_planet_mass(planet_mass, unit='Mjup')
        #self._radius = planet_radius*RJUP
        self.set_planet_radius(planet_radius, unit='Rjup')
        #self._distance = planet_distance*AU
        self.set_planet_semimajoraxis(planet_distance, unit='AU')

        if inclination == 'from_impact' :
            self.info('Inclination was not provided. Setting this as default value!')
            star_radius = self._dicoX['Rs']*RSOL
            inclination = np.arccos(star_radius * impact_param / self.get_planet_semimajoraxis(unit='m'))*180/np.pi
        elif inclination is None:
            inclination = self._dicoX['inclination']

        self._impact = impact_param
        self._inclination = inclination
        self._orbit_period = orbital_period
        self._albedo = albedo
        self._transit_time = transit_time
        self._mid_time = mid_time
        self._pericentre_long = pericentre_long
        self._eccentricity = eccentricity
        self.pericentre_time = pericentre_time
        self.ascending_node_long = ascending_node_long

        self.info('PLANET CATALOGUE PARAMETERS')
        self.info('planet name: '+str(self._canonical_planet_name))
        self.info('planet radius: '+str(planet_radius))
        self.info('planet mass: '+str(planet_mass))
        self.info('planet sma: '+str(planet_distance))
        self.info('planet impact: '+str(self._impact))
        self.info('planet inclination: '+str(self._inclination))
        self.info('planet period: '+str(self._orbit_period))
        self.info('planet transit time: '+str(self._transit_time))
        self.info('planet mid time: '+str(self._mid_time))
        self.info('planet pericentre: '+str(self._pericentre_long))
        self.info('planet eccentricity: '+str(self._eccentricity))

    @fitparam(param_name='orbital_period', param_latex='$P_{orb}$',
              default_fit=False, default_bounds=[0.5, 1.5])
    def orbitalPeriod(self):
        """
        Orbital period in days
        """
        return self._orbit_period
    
    @orbitalPeriod.setter
    def orbitalPeriod(self, value):
        self._orbit_period = value

    @fitparam(param_name='mid_time', param_latex='$T_{mid}$',
              default_fit=False, default_bounds=[0.5, 1.5])
    def midTime(self):
        """
        Mid time in days
        """
        return self._mid_time
    
    @midTime.setter
    def midTime(self, value):
        self._mid_time = value

    @fitparam(param_name='pericentre_long', param_latex='$Perictr$',
              default_fit=False, default_bounds=[0, 180])
    def pericentre(self):
        """
        Pericentre Longiture in degrees
        """
        return self._pericentre_long
    @pericentre.setter
    def pericentre(self, value):
        self._pericentre_long = value
    
    @fitparam(param_name='impact_param', param_latex='$Impact$',
              default_fit=False, default_bounds=[0, 180])
    def impact(self):
        """
        Pericentre Longiture in degrees
        """
        return self._impact
    @impact.setter
    def impact(self, value):
        self._impact = value

    @fitparam(param_name='inclination', param_latex='$Inclination$',
              default_fit=False, default_bounds=[0, 180])
    def inclination(self):
        """
        Pericentre Longiture in degrees
        """
        return self._inclination
    @inclination.setter
    def inclination(self, value):
        self._inclination = value

    @classmethod
    def input_keywords(self):
        return ['exomast']


