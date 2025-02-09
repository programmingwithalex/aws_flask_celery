import time
from typing import Any, Dict

from flask import flash, redirect, render_template, request, url_for

from . import create_app
from .tasks import div, requeue_example, send_async_email

flask_app = create_app("production")


@flask_app.route("/")
def hello() -> str:
    """simple route to test Flask app"""
    return "Hello, World 2!"


# will be ignored if `/flower` specified as the route in `nginx.conf`
# @flask_app.route('/flower')
# def flower_conflict():
#     return 'flower conflict!'


@flask_app.route("/celery_test_division")
def celery_test_division() -> Dict[str, float]:
    """test simple Celery task for dividing two hardcoded numbers"""
    res = div.delay(4, 5).get()

    time.sleep(2)

    return {"result": res}


@flask_app.route("/celery_test_division_fail")
def celery_test_division_fail() -> Dict[str, float]:
    """test simple Celery task for dividing two hardcoded numbers"""
    res = div.delay(4, 0).get()

    time.sleep(2)

    return {"result": res}


@flask_app.route("/celery_test_requeue_example")
def celery_test_requeue_example() -> Dict[str, float]:
    """test simple Celery task for dividing two hardcoded numbers"""
    res = requeue_example.delay().get()
    return {"result": res}


@flask_app.route("/send_email", methods=["GET", "POST"])
def send_email() -> Any:
    """send email"""
    if request.method == "GET":
        return render_template("index.html")

    email_recipient = request.form["recipient"]
    email_subject = request.form["subject"]
    email_body = request.form["body"]

    send_async_email.delay(email_recipient, email_subject, email_body)
    flash(f"Sending email to {email_recipient}!")

    return redirect(url_for("send_email"))


# ** uncomment to run locally **
# if __name__ == '__main__':
#     flask_app.run(host='0.0.0.0')
