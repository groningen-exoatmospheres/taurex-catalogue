from .reader import CatalogueReader
import pandas as pd
import astropy.units as u

class FileReader(CatalogueReader):

    @staticmethod
    def get_target_name_tier(target_list, target_no):
        df = pd.read_csv(target_list)
        target_name = df['Planet Name'][target_no]
        target_tier = df['Tier'][target_no]
        target_method = df['Best Method'][target_no]
        return target_name, target_tier, target_method.lower()



    def __init__(self, filename=None, target_no=0, target_name=None):
        super().__init__()

        self.filename = filename

        self.debug('Reading %s', filename)
        
        self.target_no = target_no
        self.target_name = target_name

        self.star_params, self.planet_params = self.load_target_list(self.filename)



    def load_target_list(self, filename):

        import re
        df = pd.read_csv(filename)

        planet_units = []
        star_units = []
        star_values = []
        star_field = []
        planet_field = []
        planet_values = []

        for idx, c in enumerate(df.columns):
            if self.target_name is not None:
                ## update the target number from the name.
                try:
                    self.target_no = df[df['Planet Name'] == self.target_name].index[0]
                except:
                    print('PLANET NAME IS NOT RECOGNISED')
                    raise NameError
            column_value = df[c][self.target_no]    
            split = c.split()
            self.debug('split %s',split)
            self.debug('split[0] =  %s',split[0])
            if split[0].strip() in ('Planet' , 'Transit', 'Impact') :
                self.debug('IS PLANET')
                if len(split) > 3:
                    planet_field.append(" ".join(split[1:-1]))
                else:
                    planet_field.append(split[1])
                find_units = re.findall('\[.*?\]', c)
                if len(find_units) == 0:
                    planet_units.append(1)
                else:
                    unit = re.findall('\[.*?\]',c)[-1][1:-1] 
                    if unit == "Me":
                        unit = "M_earth"
                    if unit == "Re":
                        unit = "R_earth"
                    if unit == "days":
                        unit = "day"
                    planet_units.append(u.Unit(unit))
                planet_values.append(column_value)
            elif split[0].lower() == 'star':
                if len(split) > 3:
                    star_field.append(" ".join(split[1:-1]))
                else:
                    star_field.append(split[1])
                find_units = re.findall('\[.*?\]', c)
                if len(find_units) == 0:
                    star_units.append(1)
                else:
                    unit = re.findall('\[.*?\]',c)[-1][1:-1] 
                    if unit == "Ms":
                        unit = "M_sun"
                    if unit == "Rs":
                        unit = "R_sun" 
                    star_units.append(u.Unit(unit))
                star_values.append(column_value)
            
        planet_field.append('Tier')
        planet_values.append(int(df['Tier'][self.target_no]))
        planet_units.append(1)

        planet_field.append('Best Method')
        planet_values.append(df['Best Method'][self.target_no])
        planet_units.append(1)


        self.debug('Planet Field %s',planet_field)
        return zip(star_field, star_units, star_values), zip(planet_field, planet_units, planet_values)

    


    def generate_planet(self):
        from taurex.data import Planet

        planet_list = dict([ (f,(u*v)) for f,u,v in self.planet_params])
        tier = planet_list['Tier']

        best_method = planet_list['Best Method']


        self.debug('Planet list %s', planet_list)

        return planet_list['Name'],Planet(planet_mass=planet_list['Mass'].to(u.jupiterMass).value,
                      planet_radius=planet_list['Radius'].to(u.jupiterRad).value,
                      planet_distance=planet_list['Semi-major Axis'].to(u.AU).value,
                      impact_param=planet_list['Parameter'],
                      albedo=planet_list['Albedo'],
                      orbital_period=planet_list['Period'].to(u.day).value,
                      transit_time=planet_list['Duration'].to(u.s).value),tier , best_method, planet_list['Temperature'].to(u.K).value


    def generate_star(self, phoenix_path=None):
        from taurex.data.stellar import BlackbodyStar, PhoenixStar

        star_list = dict([(f, (u*v)) for f, u, v in self.star_params])

        star_dict = {
                'temperature' : star_list['Temperature'].to(u.K).value,
                'radius' : star_list['Radius'].to(u.R_sun).value,
                'distance' : star_list['Distance'].to(u.parsec).value,
                'magnitudeK' : star_list['K'],
                'mass' : star_list['Mass'].to(u.M_sun).value,
                'metallicity': star_list['Metallicity']
        }
        if phoenix_path is not None:

            return PhoenixStar(phoenix_path=phoenix_path, **star_dict
                               )
        else:
            return BlackbodyStar(**star_dict)
