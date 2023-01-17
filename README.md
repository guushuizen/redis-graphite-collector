# redis-graphite-collector

Query a Redis database indefinitely and at a regular cadence and transform data to throw at Graphite.

### Why?

I want to visualise my Redis memory store into a Graphite-backed visualisation tool (e.g. Grafana)

### How?

1. Create classes under the `collectors/` folder to define your Redis queries and transformations. (Take a peek at the `collectors/random.py` for inspiration!)
2. `mv ./config.example.py ./config.py`
3. (Optionally) `virtualenv .venv/` and `source .venv/bin/activate`
4. `pip install -r requirements.txt`
5. Setup a daemon (e.g. supervisord or systemd) to keep `python ./main.py` running indefinitely!
6. Profit \o/
