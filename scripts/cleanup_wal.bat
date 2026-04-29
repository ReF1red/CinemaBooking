@echo off
chcp 1251 >nul

set "WAL_ARCHIVE_DIR=C:\pg_wal_archive"
set "DAYS_TO_KEEP=7"

if not exist "%WAL_ARCHIVE_DIR%" (
    echo Папка с архивами не найдена.
    pause
    exit /b
)

echo Удаляем файлы старше %DAYS_TO_KEEP% дней...
forfiles /p "%WAL_ARCHIVE_DIR%" /s /m *.* /d -%DAYS_TO_KEEP% /c "cmd /c del /q @path" 2>nul

if errorlevel 1 (
    echo Нет файлов для удаления.
) else (
    echo Очистка завершена.
)

pause