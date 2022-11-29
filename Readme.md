# :clipboard: Описание работы
API асинхронного калькулятора математических вычислений. Доступны следующие операции:
- \+ сложение
- \- вычитание
- \* умножение
- \/ деление

API содержит в себе 3 метода:
1. Создание задачи на вычисление
2. Получание списка имеющихся задач на вычисление с их статусами
3. Получение результата вычисления задачи

Swagger API находится по адресу `/docs`

Отложенные вычисления выполняются в cron задаче, которая запускается 1 раз в минуту
# :construction_worker: Workflow
Ветка main защищена от изменений. Workflow разработки построен чере создание feature веток и pull request'ы

Каждый pull request проходит через автоматические проверки:
1. pylint - статический анализ кода. Проверка не проходит, если найдена хотя бы одна ошибка
2. mypy - проверка типизации. Проверка не проходит, если найдена хотя бы одна ошибка.
3. test - запуск тастов и проверка покрытия кода тестами. Провека не проходит, если хотя бы один тест не прошел, либо покрытие тестами ниже 99%. В случае недостающего покрытия, либо упавшего теста Github-action Bot оставит комментарий с отчетом о результатах прогона тестов и покрытию.
4. formatter - Автоматическое форматирование кода. Прогоняется isort, затем black. Запускается в том случае, если пункты 1-3 завершились успешно.

Если пункты 1-4 завершились успешно, то Github-action Bot поставит Approve к pull request'y. Это является необходимым условием для вливания feature ветки в ветку main.
# :electric_plug: Команды
## Проверки качества кода
Запуск тестов и проверка покрытия:
```
make test
```
Проверка типизации:
```
make mypy
```
Запуск статического анализатора кода:
```
make pylint
```
Запуск всех перечисленных выше проверок:
```
make all-checks
```
## Форматирование кода
```
make formatter
```
## Установка зависимостей
Установка dev зависимостей:
```
make install-deps
```
Установка конкретных групп зависимостей, объявленных в pyproject.toml:
```
make install-deps deps=[COMMA_SEPARATED_GROUPS]
```
Установка зависимостей prod окружения:
```
make install-deps deps=production
```
## Запуск приложения
Запуск приложения в production окружении:
```
make runserver
```
Запуск приложения на локальной машине (после запуска сервис будет доступен по адресу http://localhost:8000/):
```
make runserver env=dev
```
Запуск приложения с базой данных в docker контейнере (после запуска сервис будет доступен по адресу http://localhost:8000/):
```
make runserver env=container
```