

from kartograph import Kartograph as Kartograph
from kartograph.errors import KartographError
import shapefile
import json
import os.path
import sys

force_countries = sys.argv[1:]

map_output_dir = 'maps/'
width = 450


def get_json(f):
    return json.loads(open(f).read())


custom_bbox = get_json('custom-bbox.json')
custom_filter = get_json('custom-filter.json')
custom_country_center = get_json('custom-country-center.json')
custom_ratio = get_json('custom-ratio.json')
custom_join = get_json('custom-join.json')

# extract admin codes from shapefile, sorted by population
records = shapefile.Reader('shp/ne_50m_admin_0_countries.shp').records()
records = sorted(records, key=lambda rec: rec[23] * -1)
adm_codes = [rec[9] for rec in records]


K = Kartograph()

# also render the world map
cfg = json.loads(open('worldmap.json').read())
#print 'world'
cfg['export']['width'] = width
#K.generate(cfg, map_output_dir + 'world.svg', preview=False)

regions = get_json('region-bbox.json')

for region in regions:
    cfg = json.loads(open('continent-template.json').read())
    del cfg['proj']['id']
    cfg['bounds']['data'] = regions[region]
    cfg['export']['width'] = width
    map_filename = map_output_dir + region + '.svg'
    if not os.path.exists(map_filename):
        print region
        K.generate(cfg, map_filename, preview=True)

err = []
ignore = set(get_json('ignore-countries.json'))


# render country maps
for adm_code in adm_codes:
    if adm_code in ignore:
        continue
    map_filename = map_output_dir + adm_code + '.svg'
    l = 1
    if not os.path.exists(map_filename) or adm_code in force_countries:
        tmpl = json.loads(open('country-template.json').read())
        if os.path.exists('shp/custom/%s.shp' % adm_code):
            tmpl['layers'][l]['src'] = 'shp/custom/%s.shp' % adm_code
        tmpl['export']['width'] = width
        tmpl['layers'][l]['filter'][2] = adm_code
        if adm_code in custom_bbox:
            tmpl['bounds']['mode'] = 'bbox'
            tmpl['bounds']['data'] = custom_bbox[adm_code]
        if adm_code in custom_country_center:
            lon, lat = custom_country_center[adm_code]
            tmpl['proj']['lon0'] = lon
            tmpl['proj']['lat0'] = lat
        if adm_code in custom_ratio:
            tmpl['export']['ratio'] = custom_ratio[adm_code]
        if adm_code in custom_filter:
            tmpl['bounds']['data']['filter'] = custom_filter[adm_code]
        if adm_code in custom_join:
            tmpl['layers'][l]['join'] = custom_join[adm_code]
        try:
            # print json.dumps(tmpl)
            print adm_code
            K.generate(tmpl, map_filename, preview=False)
        except KartographError, e:
            err.append(adm_code)
            print e.message

print err
