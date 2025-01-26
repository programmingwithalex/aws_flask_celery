import os

from celery import Celery

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]

if 'redis' in CELERY_BROKER_URL:
    CELERY_RESULT_BACKEND = os.environ["CELERY_BROKER_URL"]
else:
    CELERY_RESULT_BACKEND = 'rpc://'  # for rabbitmq

celery_app = Celery(
    "proj",
    # broker='pyamqp://guest@localhost//',  # running locally without Docker
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["proj.tasks"],
)

# ********** option to run with more than one queue ********** #
# 'tasks.add' executed in 'hipri' queue instead default queue
# task then picked up by worker subscribed to 'hipri' queue for processing
# By configuring task routing, can control distribution of tasks across different queues and workers
# based on app requirements, workload balancing, or priority management.
# celery_app.conf.update(
#     task_routes={
#         'tasks.add': {'queue': 'hipri'},
#     },
# )
# *********************************************************** #

# ** time (in seconds) for which Celery will store task results before discarding them **
celery_app.conf.update(
    result_expires=int(os.environ["CELERY_TASK_RESULT_EXPIRE_SECONDS"]),
)

# ** running periodic tasks using `celery_beat` **
celery_app.conf.beat_schedule = {
    "add-every-10-seconds": {
        "task": "proj.tasks.test_print",
        "schedule": 10.0,  # runs every 10 seconds
    },
}
celery_app.conf.timezone = "UTC"  # type: ignore


# ** uncomment to run locally **
# if __name__ == "__main__":
#     celery_app.start()
