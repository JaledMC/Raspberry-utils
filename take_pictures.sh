#!/bin/bash
cont=0
while [ true ] ; do
	read -t 3 -n 1
	if [ $? = 0 ] ; then
		echo "next"
		raspistill --quality 100 -t 1 -sh 75 -co 40 -ev +8/6 -o "$cont.jpg"
		cont=$((cont+1))		
	else
	echo "waiting for the keypress"
	fi
done
