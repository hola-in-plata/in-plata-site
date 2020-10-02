#!/bin/sh

if [ $# -lt 1 ]
  then
    echo "Uso: $0 path"
    exit 1
fi

path=$1

for i in $(ls $path) 
do 
  code=in.plata-$(echo $i | sed "s/\([[:digit:]]\{2\}-\)\([[:digit:]]\{2\}-\)\([[:digit:]]\{4\}\)\(-.*\)/\1\2\3/g")
  convert $path/$i -gravity South -pointsize 20 -fill grey -annotate +300+10 $code $path/out/$i 
done

