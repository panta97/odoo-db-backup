ZIPFILE=`ls *.zip`

rm -f "$ZIPFILE"
rm -f dump.sql shrank-dump.sql
rm -rf postgres-data
if [ -d 'filestore' ]; then
    rmdir 'filestore'
fi

if [ -d 'init' ]; then
    rm -rf 'init'
fi
