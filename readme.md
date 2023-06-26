# Cow API

## Quick start

A recent version of docker desktop which includes docker compose should be installed.

Note this was developped on a MacAir M1.

```bash
make start
#  to stop: make stop
```

## API UI documentation

Open api docs can be found with two flavours of UI:
  - [swwagger](http://localhost:8000/docs)
  - [redoc](http://localhost:8000/redoc)


## API CLI documentation

Here is a brief overview of what can be executed. Please refer to the APU UI section
for a better user experience and with the API possibly more up to date.


## cow create


```bash
curl -X POST -H "content-type: application/json" -d '{
    "name": "betty",
    "sex": "male",
    "birthdate": "2019-02-11T03:21:00.000000",
    "condition": "healthy",
    "weight": {
        "mass_kg": 1100,
        "last_measured": "2022-11-02T11:15:00.000000"
    },
    "feeding": {
        "amount_kg": 5,
        "cron_schedule": "0 */6 * * *",
        "last_measured": "2022-11-02T11:00:00.000000"
    },
    "milk_production": {
        "last_milk": "2022-11-02T09:00:00.000000",
        "cron_schedule": "0 8,12,16,20 * * *",
        "amount_l": 5
    },
    "has_calves": true
}' http://localhost:8000/cows

```

### cow update

```bash
curl -X PUT -H "content-type: application/json" -d '{
    "name": "jane",
    "weight": {
        "mass_kg": 100,
        "last_measured": "2023-11-02T11:15:00.000000"
    }
}' http://localhost:8000/cows/1

```

### cow filter

```bash
curl -X PUT -H "content-type: application/json" http://localhost:8000/cows?sex=Female

```

## Scaling to all cows in EU

The number of cows in Europe is monitored by Eurostat.

For context in 2022, there were 74.8 Million cows.

To improve something you need to measure it. So to open a conversation about scalability
it is helpful to define the ability of the current solution.

We provide some initial load testing with `k6`.

Please ensure `k6` is installed. On Mac:

```bash
brew install k6
```

Run an experiment with 100 (vus in `k6` terminology) machines trying to update the API concurrently (1 per cow):

```bash
k6 run --vus 100 --duration 30s loadtest.js
```

Here is an example output report. It was produced on a M1 macbook air with the app running within docker.

```
     data_received..................: 107 MB 3.0 MB/s
     data_sent......................: 349 kB 9.8 kB/s
     http_req_blocked...............: avg=263.26µs min=1µs     med=4µs   max=5.56ms p(90)=9µs    p(95)=2.55ms
     http_req_connecting............: avg=184.06µs min=0s      med=0s    max=2.71ms p(90)=0s     p(95)=2.2ms
     http_req_duration..............: avg=2.49s    min=14.17ms med=2.55s max=7.92s  p(90)=3.98s  p(95)=4.46s
       { expected_response:true }...: avg=2.49s    min=14.17ms med=2.55s max=7.92s  p(90)=3.98s  p(95)=4.46s
     http_req_failed................: 0.00%  ✓ 0         ✗ 1132
     http_req_receiving.............: avg=694.21µs min=10µs    med=321µs max=6.45ms p(90)=1.73ms p(95)=2ms
     http_req_sending...............: avg=21.86µs  min=2µs     med=23µs  max=524µs  p(90)=28.9µs p(95)=33µs
     http_req_tls_handshaking.......: avg=0s       min=0s      med=0s    max=0s     p(90)=0s     p(95)=0s
     http_req_waiting...............: avg=2.49s    min=14.13ms med=2.55s max=7.91s  p(90)=3.97s  p(95)=4.46s
     http_reqs......................: 1132   31.672633/s
     iteration_duration.............: avg=6s       min=1.78s   med=5.89s max=13.36s p(90)=8.35s  p(95)=9.38s
     iterations.....................: 566    15.836316/s
     vus............................: 51     min=51      max=100
     vus_max........................: 100    min=100     max=100

```

The scenario implemented run run over 31 requests per second.
This would be the equivalent to 30 * 60 * 60 * 24 = 2592000 requests a day.

During these tests it was clear that the web app was the bottleneck in that the CPU usage was maxed out.
The Postgres instance didn't see much CPU usage peaking at 5%.

Further investigation is needed to see if performance can be improved further.
Note there is nothing stopping us from running multiple instances of the app to scale out.


sources:
    - overview [eurostat](https://ec.europa.eu/eurostat/web/products-eurostat-news/-/ddn-20220517-2)
    - bovine [eurostat](https://ec.europa.eu/eurostat/databrowser/view/APRO_MT_LSCATL/default/table?lang=en)


## Dev

### API running on host

Start the server on devevelopers' machine:

```bash
uvicorn cows.main:app --reload

```

### with docker compose

see `makefile` for full list of commands.

Please ensure the docker daemon is already running on your dev pc.

```bash
make start

```

### code qa

A variety of code quality checks are implemented using `pre-commit`.

Do ensure you have it installed and initiated before development work.

You only need to do the following once:

```
pip install pre-commit
pre-commit install

```
Once installed you can run all the checks outside of making a commit with:

```
pre-commit run -a
```

Note for `Pyright` to run within `pre-commit` requires configuration that is specific
to how the dev manages their virtual environments.
Specify the path to your environment in the `pyrightconfig.json` file.

For this reason the check is commented out in `.pre-commit-config.yaml`.

### tests

TODO
