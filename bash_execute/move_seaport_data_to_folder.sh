#cd /mnt/d/Seaport_satellite_images
#echo "$PWD"
#mkdir RGB_Only

for f in $(find /mnt/d/Seaport_satellite_images/**/**/rgb.tif);do
  echo $f;
  new_f="${f}"
#  new_ff="$new_f" | tr '/' '_'
  new_ff=${new_f////_}
  new_fff=${new_ff//tif/png}
  echo $new_fff

  cp $f /mnt/d/Seaport_satellite_images/RGB_Only/$new_fff
#  break
done

#find $PWD -name '*.rgb' | xargs echo