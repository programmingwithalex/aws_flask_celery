import datetime
import random
import time
from typing import Any, Union

import requests
from flask_mail import Message

from . import extensions
from .celery_app import celery_app


@celery_app.task
def test_print() -> str:
    """test task to print current time"""
    print(f"time is: {datetime.datetime.now()}")
    return f"time is: {datetime.datetime.now()}"


@celery_app.task
def add(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """add two numbers"""
    return x + y


# **example for retrying a task in case of ZeroDivisionError **
# **reference: https://docs.celeryq.dev/en/latest/userguide/tasks.html **
@celery_app.task(
    autoretry_for=(ZeroDivisionError,),
    retry_kwargs={"max_retries": 3},
    default_retry_delay=3,  # seconds
)
def div(x: Union[int, float], y: Union[int, float]) -> float:
    """divide two numbers - will retry 5 times in case of ZeroDivisionError"""
    return x / y


# ** example for task that will fail with no retry **
@celery_app.task
def div_no_retry(x: Union[int, float], y: Union[int, float]) -> float:
    """divide two numbers - no retry"""
    return x / y


# ******************************************************************** #
# ** example for chaining tasks together **
# ** reference: https://docs.celeryq.dev/en/latest/userguide/tasks.html **
@celery_app.task
def chained_func_example(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """example showing chaining of tasks"""
    # .s() -> convert a task into a Celery signature object
    # must be used for chaining
    chain = chained_subfunc_1.s(x, y) | chained_subfunc_2.s()
    return chain()


@celery_app.task()
def chained_subfunc_1(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """function 1 being called in example showing chaining of tasks"""
    time.sleep(2)
    return x + y


@celery_app.task()
def chained_subfunc_2(z: Union[int, float]) -> float:
    """function 2 being called in example showing chaining of tasks"""
    return z / 2


# ******************************************************************** #


# reference: https://docs.celeryq.dev/en/latest/userguide/calling.html
@celery_app.task
def error_handler(request: Any, exc: Exception, traceback: Any) -> None:
    """
    Can be applied to task call with:

        add.apply_async((2, 2), link_error=error_handler.s())
    """
    print(f"Task {request.id} raised exception: {exc}\n{traceback}")


# ******************************************************************** #
# ** The task may raise Reject to reject the task message using AMQPs basic_reject method **
# ** This won’t have any effect unless Task.acks_late is enabled **
#
# ** `bind` keyword allows `self` parameter to be passed to the task **
#
# ** `acks_late` - if set to True messages for this task will be acknowledged after the task has been executed, **
# ** not just before (the default behavior). **
@celery_app.task(bind=True, acks_late=True)
def task_process_notification(self: Any) -> None:
    """example for task that will fail randomly with retry"""
    try:
        # mimic random error
        if not random.choice([0, 1]):  # nosec
            raise AssertionError()

        requests.post("https://httpbin.org/delay/5", timeout=10)
    except AssertionError as e:
        print("exception raised, retry after 5 seconds")
        raise self.retry(
            exc=e,
            countdown=5,
            max_retries=10,  # default `max_retries` = 3
        )


@celery_app.task(bind=True, acks_late=True)
def requeue_example(self: Any) -> None:
    """example for task that will fail randomly with retry"""
    try:
        # mimic random error
        if datetime.datetime.now().second > 30:
            raise AssertionError()

        return f"below 30 seconds - {datetime.datetime.now().second}"
    except AssertionError as e:
        print("exception raised, retry after 5 seconds")
        raise self.retry(
            exc=e,
            countdown=5,
            max_retries=10,  # default `max_retries` = 3
        )


# ******************************************************************** #


@celery_app.task()
def send_async_email(email_recipient: str, email_subject: str, email_body: str) -> str:
    """
    send email asynchronously to verify the email sending functionality for celery

    INPUTS
    ------
    email_recipient : str : email recipient
    email_subject : str : email subject
    email_body : str : email body
    """
    from .app import flask_app

    with flask_app.app_context():
        msg = Message(
            subject=email_subject,
            sender=flask_app.config["MAIL_USERNAME"],
            recipients=[email_recipient],
            body=email_body,
        )

        extensions.mail.send(msg)

        return "Email sent"
