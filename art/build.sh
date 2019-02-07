mkdir -p build/candelabrus build/fons build/dejure build/nietz build/darwin build/mereokratos
inkscape -z candelabrus.svg -l build/candelabrus/icon.svg
inkscape -z candelabrus.svg -e build/candelabrus/icon.png -w 256 -h 256
inkscape -z fons.svg -l build/fons/icon.svg
inkscape -z fons.svg -e build/fons/icon.png -w 256 -h 256
inkscape -z nietz.svg -l build/nietz/icon.svg
inkscape -z nietz.svg -e build/nietz/icon.png -w 256 -h 256
inkscape -z dejure.svg -l build/dejure/icon.svg
inkscape -z dejure.svg -e build/dejure/icon.png -w 256 -h 256
inkscape -z darwin.svg -l build/darwin/icon.svg
inkscape -z darwin.svg -e build/darwin/icon.png -w 256 -h 256
inkscape -z mereokratos.svg -l build/mereokratos/icon.svg
inkscape -z mereokratos.svg -e build/mereokratos/icon.png -w 256 -h 256

cp -r build/* ../source/static/
rm -r build
