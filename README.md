# FABRIQUE_PROJECT
Тестовое задание для компании "Фабрика Решений"

# Необходимые действия перед началом
cd fabrique_studio
pip install -r project_package.txt

cd FABRIQUE_PROJECT
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Создаём супер-юзера с именем admin и паролем admin. 
Можно использовать другое имя но тогда в файле FABRIQUE_TESTS/settings.py нужно также изменить их 
(по умолчанию стоит admin/admin)

#Запуск сервера
cd fabrique_studio/FABRIQUE_PROJECT
python manage.py runserver


#Тесты
Необходимо запустить сервер python manage.py runserver

cd FABRIQUE_STUDIO/FABRIQUE_TESTS
pytest

После прогона тестов, будет выведен результат об успешных/упавшших тестах. В теле теста, можно изменить json файлы
и получать различные результаты в зависимости от содержимого. 


#С наилучшими пожеланиями Маковий Ф.В.