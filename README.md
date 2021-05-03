# FABRIQUE_PROJECT
Тестовое задание для компании "Фабрика Решений"

# Quickstart guide
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

#Документация по API

Я перечислю здесь основые запросы

Первый тип обращений это запросы GET (отдельные запросы я тестировал с помощью postman)

для обычного пользователя:

GET http://127.0.0.1:8000/polls

для админа: 

GET http://127.0.0.1:8000/admin/polls

Получение конкретного опроса:

GET http://127.0.0.1:8000/admin/polls/5 # где 5 id опроса

Работа с вопросами:

GET /admin/polls/5/questions/6 #где  номер опроса, 6 номер вопроса


Можно делать также запросы POST, PATCH, DELETE

Для облегчения тестирования был создан раздел тестов, о нем ниже

#Тесты
Необходимо при запущеном сервере перейти в папку:

cd FABRIQUE_STUDIO/FABRIQUE_TESTS
pytest

После прогона тестов, будет выведен результат об успешных/упавшших тестах. В теле теста, можно изменить json файлы
и получать различные результаты в зависимости от содержимого. 



#С наилучшими пожеланиями Маковий Ф.В.
