from flask import (
    Blueprint, redirect, current_app, request
)
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import json
import socket

from webapp.kafka import KafkaSingleton

from .middlewares.authenticated import authenticated
from ..session_wrapper import session_wrapper
from ..category_flash import flash_action_success

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.post('/login')
def login():
    group = request.form.get('group').strip()
    user = request.form.get('user').strip()

    session_wrapper.group = group
    session_wrapper.user = user

    current_app.logger.info(f'Logged in as {group}:{user}')

    kafka_topic = f'devprin.{group}.task.result'
    current_app.logger.info(f'Changing kafka consumer: must subscribe to topic {kafka_topic}')
    kafka_instance = KafkaSingleton()
    kafka_instance.init_consumer(kafka_topic)
    current_app.logger.info('Kafka consumer changed')

    flash_action_success('Login avvenuto con successo')

    return redirect(request.referrer)


@bp.post('/logout')
@authenticated
def logout():
    current_app.logger.info(f'User {session_wrapper.group}:{session_wrapper.user} has logged out')
    session_wrapper.clear()

    flash_action_success('Logout avvenuto con successo')

    return redirect(request.referrer)