

Проект — простой блог с возможностью регистрации пользователей и функционалом для создания и взаимодействия с постами.

Основные возможности
Регистрация и аутентификация пользователей
Пользователи могут зарегистрироваться, войти в систему и выйти из неё.
Сброс пароля по электронной почте
Восстановление доступа через отправку письма со ссылкой для сброса пароля.
Добавление и редактирование постов 
Авторизованные пользователи могут создавать, редактировать и удалять свои посты.
Отображение постов
Все пользователи могут просматривать опубликованные посты с пагинацией.
Лайки и комментарии
Возможность ставить лайки и оставлять комментарии к постам.
Поиск по постам 
Удобный поиск по заголовкам и содержимому постов.
Использование PostgreSQL
База данных PostgreSQL обеспечивает надежное хранение данных.

Технологии
Python 3.x  
Django  
PostgreSQL  
HTML, CSS (с кастомной стилизацией)  

Установка и запуск

Клонируйте репозиторий:

   git clone https://github.com/kira111dfg/blog.git
   cd blog
Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Установите зависимости:
pip install -r requirements.txt
Настройте подключение к базе PostgreSQL в settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
Примените миграции:
python manage.py migrate
Создайте суперпользователя:
python manage.py createsuperuser
Запустите сервер разработки:
python manage.py runserver
Откройте в браузере: http://127.0.0.1:8000
Конфигурация отправки почты для сброса пароля
В settings.py добавьте настройки SMTP, например для Gmail:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
