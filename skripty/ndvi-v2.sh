#!/bin/sh

#%module
#% description: Vypocet reklasifikovaneho NDVI
#%end
#%option G_OPT_M_MAPSET
#% required: yes
#% answer: landsat
#%end
#%option
#% key: output_postfix
#% type: string
#% description: Postfix pro vystupni vrstvu (vychozi: ndvi)
#% answer: ndvi
#%end 

if [ "$1" != "@ARGS_PARSED@" ] ; then
    exec g.parser "$0" "$@"
fi

mapset=$GIS_OPT_MAPSET

# pridat mapset do vyhledavaci cesty
g.mapsets mapset=$mapset ope=add --q

# vstup
vis=`g.list type=raster mapset=$mapset pattern='*B4$'`
nir=`g.list type=raster mapset=$mapset pattern='*B5$'`
# vysledek
ndvi=$GIS_OPT_OUTPUT_POSTFIX

# vypocet NDIV
echo "VIS: $vis ; NIR: $nir"
r.mapcalc exp="$ndvi = float($nir - $vis) / ($nir + $vis)" --o

# reklasifikace (1,2,3)
echo "Reklasifikuji..."
# r.reclass umi reklasifikovat pouze celociselne rastry, proto pouzime
# r.recode
r.recode input=$ndvi output=r_$ndvi rules=- --o <<EOF
 -1:0.05:1 
 0.05:0.35:2 
 0.35:1:3
EOF

# popisky
r.category map=r_$ndvi sep=':' rules=- <<EOF
1:bez vegetace, vodni plochy
2:plochy pokryte vegetaci
3:plochy pokryte vegetaci
EOF

# tabulka barev
r.colors map=r_$ndvi rules=- --q <<EOF
 1 red
 2 yellow
 3 0 136 26
EOF

# vypsat vysledek
echo "Generuji report..."
r.report map=r_$ndvi units=h

echo "Hotovo!"
