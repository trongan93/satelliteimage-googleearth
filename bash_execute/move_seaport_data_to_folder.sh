#cd /mnt/d/Seaport_satellite_images
#echo "$PWD"
#mkdir RGB_Only

for f in $(find /mnt/d/Seaport_satellite_images/**/**/rgb.tif);do
  echo $f;
  new_f="${f}"
#  new_ff="$new_f" | tr '/' '_'
  new_ff=${new_f////_}
  echo $new_ff

  cp $f /mnt/d/Seaport_satellite_images/RGB_Only/$new_ff
done

#find $PWD -name '*.rgb' | xargs echo