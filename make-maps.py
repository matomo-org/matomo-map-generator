

from kartograph import Kartograph as Kartograph
import shapefile
import json
import os.path

map_output_dir = 'maps/'

country_min_area = {
    'JPN': .1,
    'AUS': .01,
    'CAN': .05,
    'ALA': .1,
    'FRA': .2,
    'DNK': .1,
    'ITA': .05,
    'GBR': .165,
    'ESP': .165
}

custom_country_center = {
    'USA': (-98.606, 39.622)
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
        print adm_code
        try:
            K.generate(tmpl, map_filename, preview=False)
        except:
            print 'error!'
