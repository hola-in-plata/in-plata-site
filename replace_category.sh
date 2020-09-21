#!/bin/sh

if [ $# -lt 2 ]
  then
    echo "Uso: $0 path category"
    exit 1
fi

path=$1
category=$2

for i in $(ls $path) 
do 
  new_name=$(echo $i | sed "s/\([[:digit:]]\{2\}-\)\([[:digit:]]\{2\}\)\(-.*\)/\1$category\3/g")
  mv $i $new_name
done

