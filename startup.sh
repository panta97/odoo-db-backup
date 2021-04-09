ZIPFILE=`ls *.zip`

# clean up
rm -f dump.sql shrank-dump.sql
rm -rf postgres-data
if [ -d 'filestore' ]; then
    rmdir 'filestore'
fi

if [ -d 'init' ]; then
    rm -rf 'init'
fi

if test -f "$ZIPFILE"; then
    echo "$ZIPFILE exists."
    unzip "$ZIPFILE"
    # shrink dump file using python
    ./env/bin/python shrinker.py
    # create init directory if not exists
    mkdir -p init
    echo "-- wrote on $(date)" > init/init.sql
    cat config.sql shrank-dump.sql >> init/init.sql
    docker-compose up
else
    echo 'zip file does not exists'
    echo 'or there is more than one zip file'
fi
