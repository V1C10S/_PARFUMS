# Parfums API

O backend usa FastAPI e persiste cada catálogo diretamente em `data/*.json`.

## Execução

```bash
python -m pip install -r requirements.txt
python app.py
```

A API fica disponível em `http://localhost:5500` e a documentação interativa,
em `http://localhost:5500/docs`.

## Endpoints

Os catálogos estão disponíveis nestas bases:

- `/parfurm/featured`
- `/parfurm/seasons/spring`
- `/parfurm/seasons/summer`
- `/parfurm/seasons/fall`
- `/parfurm/seasons/winter`

Cada base aceita `GET` e `POST`. Para um item específico, acrescente `/{id}` e
use `GET`, `PUT`, `PATCH` ou `DELETE`. As alterações feitas pela API são salvas
no arquivo JSON correspondente.
