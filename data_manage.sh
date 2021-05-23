#!/usr/bin/env bash

arg1=$(echo $1 | tr [[:upper:]] [[:lower:]])
arg2=$2

SCRIPT_PATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 || exit 1 ; pwd -P )"
BACKUP_DIR_NAME=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="backups"
DB_NAME="insys"
MEDIA_DIR="media"
ARCHIVE_DEPTH=7


backup(){
  # создание резервной копии базы даннных и файлов из каталога media
  cd $SCRIPT_PATH
  sudo -u postgres pg_dump -Fc org > ${DB_NAME}.db.dump
  tar cf $BACKUP_DIR/$BACKUP_DIR_NAME.tar $MEDIA_DIR
  tar rf $BACKUP_DIR/$BACKUP_DIR_NAME.tar ${DB_NAME}.db.dump
  gzip $BACKUP_DIR/$BACKUP_DIR_NAME.tar
  rm ${DB_NAME}.db.dump
  # удаление архивов старше n-дней указанных в переменной ARCHIVE_DEPTH
  find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$ARCHIVE_DEPTH -delete
}

restore(){
  # восстановление базы данных и файлов каталога media из резервной копии
  if [[ -n $arg2 ]]; then
    if [[ -e $arg2  ]]; then
      if [[ $arg2 == *.tar.gz ]]; then
        sudo -u postgres psql -c 'DROP DATABASE insys_old;'
        sudo -u postgres psql -c 'ALTER DATABASE insys RENAME TO insys_old;'
        sudo -u postgres psql -c 'CREATE DATABASE insys WITH ENCODING='UTF8' OWNER=django;'
        # восстановление базы данных
        tar zxf $arg2 ${DB_NAME}.db.dump
        pg_restore -U postgres -W -h localhost -d insys ${DB_NAME}.db.dump
        rm ${DB_NAME}.db.dump
        # восстановление файлов в каталоге media
        rm -R $SCRIPT_PATH/$MEDIA_DIR
        tar zxf $arg2 -C $SCRIPT_PATH $MEDIA_DIR
      else
        echo "Укажите архив формата '.tar.gz'"
      fi
    else
      echo "Архив по данному пути не существует"
    fi
  else
    echo "Не указан путь до архива для восстановления"
  fi
}


case "$arg1" in
	backup)
	  backup
	;;
	restore)
	  restore
	;;
	*)
	  echo "backup            - создание резервной копии базы даннных и файлов из каталога media"
	  echo "restore path_arch - восстановление базы данных и файлов каталога media из резервной копии"
	;;
esac
