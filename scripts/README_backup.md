# Настройка резервного копирования БД

Запустить cmd как администратор и выполнить:

```bash
# Остановить PostgreSQL
net stop postgresql-x64-18

# Создайте папку для WAL архива
# Например:
mkdir C:\pg_wal_archive

# Найди файл postgresql.conf, который расположен в C:\Program Files\PostgreSQL\18\data

# Найдите и замените эти строки в postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'copy "%p" "C:\\pg_wal_archive\\%f"'

# Запустить PostgreSQL
net start postgresql-x64-18

# Проверка работы архивации
psql -U postgres -c "SHOW archive_mode;"
psql -U postgres -c "SHOW archive_command;"
# Должно выдать on и copy ...

# Ручной запуск 
# Расположены в cinema-booking\scripts
# backup.bat - для создания backup в папке backups
# cleanup_wal.bat - для очистки WAL архива

# Автоматически бэкап создается ежедневно, а WAL архив очищается еженедельно

# Восстановление

psql -U postgres -d cinema_db < путь_к_бэкапу.sql