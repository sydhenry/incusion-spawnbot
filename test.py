import os
import requests
import sqlite3
import uuid
from pprint import pprint

# https://github.com/dalingk/incursion-tracker/blob/master/server/update_incursions.py
INCURSION_API_URL = 'https://esi.evetech.net/latest/incursions?datasource=tranquility'
DATA_FILE = 'data.csv'  # thanks to https://wiki.eveuniversity.org/Constellation_layouts_for_Incursions

data = requests.get(INCURSION_API_URL)
data.raise_for_status()
staging_systems = {}

pprint(data)

LOOKUP = {}


class System(object):
    pass

def load_data(data):
    ret = {}
    with open(data, 'r') as file:
        for line in file:
            kingdom, rest = line.split('|')
            const, staging, vanguards, assaults, hq = rest.split('=')
            ret[staging] = {
                    'hq': hq.split('\n')[0],
                    'kingdom': kingdom,
                    'const': const,
                    'staging': staging,
                    'vanguards': vanguards.split(','),
                    'assults': assaults.split(','),
            }
    return ret



LOOKUP = load_data(DATA_FILE)
pprint(LOOKUP)

for incursion in data.json():
    staging_id = incursion['staging_solar_system_id']
    system = requests.get(
        'https://esi.evetech.net/latest/universe/systems/{}?datasource=tranquility'.format(staging_id)
    )
    system.raise_for_status()
    staging_systems[staging_id] = system.json()
    const = requests.get(
        'https://esi.evetech.net/latest/universe/constellations/{}?datasource=tranquility'.format(system.json()['constellation_id'])
    )
    const.raise_for_status()
    region_id = const['region_id']
    region = requests.get(
        'https://esi.evetech.net/latest/universe/regions/{}?datasource=tranquility'.format(region_id)
    )
    region.raise_for_status()

    system.raise_for_status()
    if system.json()['security_status'] >= .5:
        hs_sys = system.json()
        hs_region = region['name']

system_names = [staging_systems[system_id]['name'] for system_id in staging_systems]
hs = LOOKUP[hs_sys['name']]

for k, v in hs.items():
    print(f" {k}: {v}" )


"""New HS Spawn
Region: [{hs_region (https://evemaps.dotlan.net/map/{region}/)
Kingdom: {hs['kingdom'].title()
Constellation" [{hs['const']](https://evemaps.dotlan.net/map/hs_region/{hs['const']})
Headquarters: [hs['hq'].title()](https://evemaps.dotlan.net/system/{hs['hq'])
Assault { [hs['hq'].title()](https://evemaps.dotlan.net/system/{hs['hq'])
Atlangeins
Vanguard
Cat, Derririntel, Ommare
Stations in HQ
1
Is Island
False
Jumps from last HQ
14 (Route Inspection)
Suggested Dockup
Hecarrin VI - Moon 3 - Federal Navy Academy
Edencom In Spawn
None
Trigs In Spawn
None



"""

