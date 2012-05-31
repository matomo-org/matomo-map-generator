#!/bin/sh
wget http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/50m-admin-0-countries.zip
unzip -d . 50m-admin-0-countries.zip
wget http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/physical/50m-lakes.zip
unzip -d . 50m-lakes.zip
wget http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/10m-admin-1-states-provinces-shp.zip
unzip -d . 10m-admin-1-states-provinces-shp.zip
