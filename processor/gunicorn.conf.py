import multiprocessing

bind = "0.0.0.0:9000"
workers = multiprocessing.cpu_count() * 2 + 1
raw_env = ["PYTHONUNBUFFERED=1",
           "PYGEOAPI_CONFIG=pygeoapi-config.yml",
           "KC_CLIENT_ID=kommonitor-processor",
           "KC_CLIENT_SECRET=jZV9arebN6KOpez8gBW2cr2yS0OAu7nh"]
