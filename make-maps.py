

from kartograph import Kartograph as Kartograph
import shapefile
import json
import os.path

map_output_dir = 'maps/'

custom_bbox = {
    'USA': [-121, 33, -73, 42],
    'FRA': [-5, 41, 9, 51.2],
    'JPN': [128, 30, 147, 46],
    'PRT': [-10, 37, -5, 42.3],
    'ECU': [-82, -5, -74, 2],
    'GBR': [-8.6, 49.5, 3, 59.5],
    'CHL': [-77, -57, -65, -16]
}

custom_country_center = {
    'USA': (-98.606, 39.622),
    'PRT': (-8, 39.4),
    'RUS': (98, 62),
    'AUS': (134.4, -25.1),
    'GRL': (-45, 90)
}

custom_ratio = {
    'CHL': 0.7, 'ARG': 1, 'BRA': 1, 'BOL': 1,
    'GUY': 1, 'NOR': 1, 'FIN': 1, 'NZL': 1,
    'PRT': 1, 'GBR': 1, 'IRL': 1, 'SWE': 0.8,
    'CHN': 1, 'COL': 1, 'COG': 1, 'DEU': 1,
    'FRA': 1.2, 'GHA': 1, 'GRC': 1, 'GRL': 1,
    'IND': 1.2, 'ISR': 0.8, 'ITA': 1, 'JPN': 1,
    'KEN': 1, 'KOR': 1, 'LAO': 1, 'LBN': 1,
    'LKA': 1, 'LUX': 1, 'MAR': 1, 'MDA': 1,
    'MDG': 1, 'MMR': 1, 'MNE': 1, 'MOZ': 1,
    'MWI': 1, 'OMN': 1, 'PAK': 1, 'PER': 1,
    'PHL': 1, 'SRB': 1, 'SUR': 1, 'TCD': 1,
    'TGO': 0.8, 'THA': 0.9, 'TUN': 0.8, 'TWN': 1,
    'VNM': 0.9, 'VUT': 0.9
}

# extract admin codes from shapefile, sorted by population
records = shapefile.Reader('shp/ne_50m_admin_0_countries.shp').records()
records = sorted(records, key=lambda rec: rec[23] * -1)
adm_codes = [rec[9] for rec in records]

K = Kartograph()

for adm_code in adm_codes:
    map_filename = map_output_dir + adm_code + '.svg'
    if not os.path.exists(map_filename):
        tmpl = json.loads(open('country-template.json').read())
        tmpl['layers'][1]['filter'][2] = adm_code
        if adm_code in custom_bbox:
            tmpl['bounds']['mode'] = 'bbox'
            tmpl['bounds']['data'] = custom_bbox[adm_code]
        if adm_code in custom_country_center:
            lon, lat = custom_country_center[adm_code]
            tmpl['proj']['lon0'] = lon
            tmpl['proj']['lat0'] = lat
        if adm_code in custom_ratio:
            tmpl['export']['ratio'] = custom_ratio[adm_code]
        print adm_code
        try:
            K.generate(tmpl, map_filename, preview=False)
        except:
            print 'error!'
