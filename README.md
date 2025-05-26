# grafana-aaa-2025

## Запуск

```bash
docker-compose up --build
```

Затем открываем в браузере:
ML сервис : http://localhost:5001
Prometheus : http://localhost:9090
Grafana : http://localhost:3000 (admin / admin)

Пример запроса к сервису:
```bash
curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"x": 5, "gender": "male"}'
```

## Метрики

Доступны по адресу: http://localhost:5001/metrics

Список метрик:

request_latency_seconds
inference_latency_seconds
errors_total
requests_total
model_type
gender_distribution

## Grafana Dashboard + json импорт файл

Заходим в Grafana: http://localhost:3000
Логин: admin, пароль: admin

Файл (```New dashboard-1748263555716.json```) можно подгрузить в UI.
