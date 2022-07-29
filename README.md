# ko_logging

## Пример использования 

`Dockerfile` - устанавливаю ko_logging из git

<details>
  <summary>Dockerfile</summary>

```BASH
RUN pip install --upgrade pip &&\
    pip install git+https://github.com/Shk337/ko_logging#egg=ko_logging &&\
    pip install -r requirements.txt
```

</details>

`example.py`  - импортирую get_logger

<details>
  <summary>example.py</summary>

```python
from ko_logging import get_logger

logger = get_logger()

logger.warning(f'log message')
```

</details>

`requirements.txt` - название и версия

<details>
  <summary>requirements.txt</summary>

```txt
ko_logging>=0.0.1
```

</details>

---

## get_logger


`logger_name` - имя логгера (logger_name: str = 'logger')</br>
`logger_level` - уровень логгера (logger_level=logging.DEBUG)</br>
`format_handler` - формат хендлера (format_handler: str = "[%(name)s] [%(process)s] [%(levelname)s] [%(pathname)s:%(lineno)d]: %(message)s")</br>
`color` - определяет, нужен ли цвет логам: True/False (color: bool = False), может неправильно отображаться, например, в Grafana </br>
`set_handlers_format` - определяет, менять ли все остальные хендлеры, можно передать список с названиями: "all"/[list](set_handlers_format: str = "all")</br>

<details>
  <summary>пример 1</summary>

```python
from ko_logging import get_logger

logger = get_logger()

logger.warning(f'log message')
```
`log` </br>

[logger] [37] [WARNING] [/app/./example.py:12]: log message
</details>

<details>
  <summary>пример 2</summary>

```python
from ko_logging import get_logger

logger = get_logger(name='example123', handler_format="%(asctime)-8s %(processName)s  %(message)s", colorize=True)

logger.warning(f'log message')
```
`log` </br>

<p><span style="color:#F4FA58">2022-07-28 11:30:07,120 SpawnProcess-1  log message</span>.</p>
</details>