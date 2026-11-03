# Development notes

## Run tests

```bash
python -m unittest -v
```

## Run the example

```bash
python tinyrag.py index docs/
python tinyrag.py ask "how does retrieval rank passages?" -k 3
```

The tests use deterministic inputs where practical. They check core behavior and
edge handling; they are not a benchmark or a production readiness certification.
