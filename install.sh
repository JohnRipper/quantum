#!/bin/sh
base()
{
    pip3 install --user websockets requests tomlkit;
}

extras()
{
    pip3 install --user bs4 python_anticaptcha isodate
}

webcam()
{
    pip3 install --user aioice aiortc
}

all()
{
    base && extras && webcam
}

if [ "$#" -eq 0 ];
then
    echo "Usage: ./install.sh base | extras | webcam (requires ffmpeg-devel) | all"
elif [ "$1" = "base" ] || [ "$1" = "extras" ] || [ "$1" = "webcam" ] || [ "$1" = "all" ];
then
     $1
else
    echo "Erm... $1 isn't a thing"
fi
