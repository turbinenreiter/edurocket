cd data
csplit LOG.CSV '/^millis,ax,ay,az,gx,gy,gz,mx,my,mz,temp,alt,pitch,yaw,roll/' '{*}'
rm LOG.CSV
cd ..

FILES=./data/*
for f in $FILES
do
    python vis.py $f
done
