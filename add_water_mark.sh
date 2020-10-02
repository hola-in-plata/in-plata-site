#!/bin/sh

if [ $# -lt 1 ]
  then
    echo "Uso: $0 path"
    exit 1
fi

path=$1
outdir=watermark
color=LightSlateGrey
#color=grey
pointsize=40

cd $path

mkdir -p $outdir

for i in $(ls *.*) 
do 
  code=in.plata-$(echo $i | sed "s/\([[:digit:]]\{2\}-\)\([[:digit:]]\{2\}-\)\([[:digit:]]\{4\}\)\(-.*\)/\1\2\3/g")
  convert $i -gravity South -pointsize $pointsize -fill $color -annotate +200+10 $code ../$i 
done

