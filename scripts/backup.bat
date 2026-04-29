@echo off
chcp 1251 >nul
setlocal enabledelayedexpansion

set "DB_NAME=cinema_db"
set "DB_USER=postgres"
set "BACKUP_DIR=C:\Users\Dima\GitProjects\cinema-booking\backups"

if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%"
    if errorlevel 1 (
        echo Не удалось создать папку %BACKUP_DIR%
        pause
        exit /b
    )
)

set "d=%date%"
set "t=%time%"

set "dd=%d:~0,2%"
set "mm=%d:~3,2%"
set "yyyy=%d:~6,4%"

set "hh=%t:~0,2%"
set "min=%t:~3,2%"
set "ss=%t:~6,2%"

if "%hh:~0,1%"==" " set "hh=0%hh:~1,1%"

set "TS=%yyyy%-%mm%-%dd%_%hh%-%min%-%ss%"
set "BACKUP_FILE=%BACKUP_DIR%\%DB_NAME%_%TS%.sql"

echo Делаю бэкап %DB_NAME% в %BACKUP_FILE%...

pg_dump -U %DB_USER% -d %DB_NAME% -F p > "%BACKUP_FILE%" 2>nul

if errorlevel 1 (
    echo Ошибка во время создания бэкапа
    pause
    exit /b
)

echo бэкап сохранен
exit /b