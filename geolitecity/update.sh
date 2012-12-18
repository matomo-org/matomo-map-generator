date=20121204
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity_$date.tar.xz
xzdec GeoLiteCity_$date.tar.xz > GeoLiteCity.tar
tar xf GeoLiteCity.tar
rm GeoLiteCity.tar
mv GeoLiteCity_20121204/GeoLiteCity-Location.csv location.csv
mysql -u root geoip < db-setup.sql
mysqlimport -u root --ignore-lines=2 --fields-terminated-by=, --fields-optionally-enclosed-by='"' --local geoip location.csv

