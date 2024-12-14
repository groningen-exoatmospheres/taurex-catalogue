# taurex-catalogue
Provides automatic parameters for TauREx planet and star objects

Can be used as Mixin to avoid typing manually the parameters. Below is an example.

Loading the necessary classes:
```
from taurex_catalogue import PlanetCatalogueExomast, StarCatalogueExomast
from taurex.planet import Planet
from taurex.stellar import BlackbodyStar
from taurex.mixin import enhance_class
```
Creating an enhanced planet and star with automated parameters:

```
pl = enhance_class(Planet, PlanetCatalogueExomast, planet_name = 'WASP-121 b')
st = enhance_class(BlackbodyStar, StarCatalogueExomast, planet_name= 'WASP-121 b')
```
