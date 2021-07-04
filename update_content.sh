#!/bin/sh

if [ $# -lt 1 ]
  then
    echo "Uso: $0 credentials_file"
    exit 1
fi

credentials=$1
photos_dir="$HOME/in.plata/fotos" 
catalog_spreadsheet="Catalogo"
catalog_sheet_index=0
catalog_export_dir="/tmp"
catalog_exported_file="$catalog_export_dir/$catalog_spreadsheet.csv"


# download del catalogo
python3 download_spreadsheet.py $credentials $catalog_spreadsheet $catalog_sheet_index -e $catalog_export_dir

# generar contenido del sitio
python3 generate_content.py  $catalog_exported_file $photos_dir -e .

diff=`git diff *.md | wc -l`

echo "<html>"
echo "<meta http-equiv="Pragma" content="no-cache">"
echo "<meta http-equiv="Expires" content="-1">"
echo "<pre>"

if [ $diff -eq 0 ] 
then
  echo 'No hay datos modificados, no se realizó ninguna actualización' > $catalog_export_dir/index.html
else
  # Guardar los cambios en los sources para mostrar en el resultado
  git diff --color-words -U0 --src-prefix=Ficha: *.md | grep -v @@ | grep -v index | grep -v diff | grep -v -e "+++ b" > $catalog_export_dir/index.html

  # Rebuildear y deployar los cambios en el site
  ./deploy.sh > /tmp/deploy.out 2>&1 

  # Guardar los cambios en los sources
  git add .
  git commit -m "Changes"
  git push origin master
fi

cat $catalog_export_dir/index.html

echo "</pre>"
echo "</html>"

rm $catalog_export_dir/index.html
