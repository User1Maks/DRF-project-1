# DRF-project-1

Регистрация новых пользователей происходит после подтверждения почтового ящика.

В проекте есть фикстуры с данными:

- data.json - данные всего проекта
- education.json - данные приложения education 
- users.json - данные приложения users
- groups.json - данные о группах

----------------------------------------------------------------
Данные для запроса в Postman:

Вывод списка пользователей с историей платежей:
http://localhost:8000/users/list/

Порядок сортировки по дате, по убыванию:
http://localhost:8000/users/payments/?ordering=-payment_date

Фильтрация по оплате картой:
http://localhost:8000/users/payments/?payment_by_card=True

Фильтрация по оплате наличными:
http://localhost:8000/users/payments?cash_payment=1

Фильтрация по курсу с id=1
http://localhost:8000/users/payments/?paid_course=1

Фильтрация по уроку с id=1
http://localhost:8000/users/payments/?paid_lesson=1

Порядок сортировки по дате, по убыванию и фильтрация по курсу id=3:
http://localhost:8000/users/payments/?ordering=-payment_date&paid_course=3

----------------------------------------------------------------
### Использование

Для заполнения БД начальными данными введите команды:
```commandline
python manage.py migrate
```
```commandline
python manage.py loaddata data.json
```

Чтобы создать суперпользователя, используйте команду:
```commandline
python manage.py csu
```
