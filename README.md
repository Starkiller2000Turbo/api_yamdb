### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Starkiller2000Turbo/api_yamdb.git

cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env

source env/bin/activate
```

Установить зависимости из файла 'requirements.txt':

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

Импортировать базу данных из файлов:

```
make imports
```

Выполнить миграции и запустить проект:

```
make
```