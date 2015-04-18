#!/bin/sh

# pridat mapset do vyhledavaci cesty
g.mapsets mapset=landsat ope=add --q

# vstup
vis="LC81920252013215LGN00_B4"
nir="LC81920252013215LGN00_B5"
# vysledek
ndvi="ndvi"

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
2:plochy s minimalni vegetaci
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
r.stats -pl input=r_$ndvi

echo "Hotovo!"
