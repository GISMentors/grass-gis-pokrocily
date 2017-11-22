#!/bin/sh

# gsutil cp -n -r gs://earthengine-public/landsat/L5/191/026 .

cd 026
for f in *.tar.bz; do
    tar xvjf $f
done
cd ..

exit 0