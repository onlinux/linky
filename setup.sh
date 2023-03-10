#/usr/bin/env bash -e

if [ ! -e "./config.ini" ]
then
    cp config.ini.default config.ini
fi

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python3`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

pip3 install -r requirements.txt

. $VENV/bin/activate



