import functools

from flask import session, has_request_context

from webapp.kafka import Kafka

def request_context_validated(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not has_request_context():
            raise Exception('Cannot access the flask.session object without a request context')
        return fn(*args, **kwargs)
    return wrapper

class SessionWrapper:
    @property
    @request_context_validated
    def user(self) -> str:
        return session.get('user', None)

    @user.setter
    @request_context_validated
    def user(self, value: str):
        session['user'] = value

    @property
    @request_context_validated
    def group(self) -> str:
        return session.get('group', None)

    @group.setter
    @request_context_validated
    def group(self, value: str):
        session['group'] = value

    @property
    @request_context_validated
    def kafka_instance(self) -> Kafka:
        return session.get('kafka_instance', None)

    @kafka_instance.setter
    @request_context_validated
    def kafka_instance(self, value: Kafka):
        session['kafka_instance'] = value

    def clear(self):
        session.clear()

session_wrapper = SessionWrapper()