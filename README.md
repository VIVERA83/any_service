# Mem Center 

___
<span id="0"></span>

### <span id="1">1. </span><span style="color:purple">Описание</span>

 В этом сервисе можно сгенерировать «быстрый мем», создать картинку на основе готовых шаблонов или загрузить свою.

### <span id="2">2. </span><span style="color:purple">Служебные команды для запуска</span> 


Запуск приложения в docker контейнере
```bash
docker compose up --build
```

```bash
cd meme_center 
alembic init -t async alembic
```
```bash
cd meme_center 
alembic revision --autogenerate -m "Initial tables"
```
```bash
cd meme_center
alembic upgrade head
```