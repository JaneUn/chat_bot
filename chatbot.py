from db import init_db, get_current_session, write_session, close_session, write_message
import signal
import random
import datetime
import threading
import time
import sys


joy = ("\U0001F600", "\U0001F603", "\U0001F604", "\U0001F601", "\U0001F606", "\U0001F602", "\U0001F60A", "\U0001F973", "\U0001F929")

sad = ("\U0001F612", "\U0001F614", "\U0001F61E", "\U0001F61F", "\U0001F641", "\U0001F615", "\U0001F629", "\U0001F62B", "\U0001F613")

angry = ("\U0001F47F", "\U0001F62C", "\U0001F624", "\U0001F621", "\U0001F47A", "\U0001F480", "\U0001F620", "\U0001F92F", "\U0001F928")

SESSION_TIME = 3
prev_state = 'neutral'
current_state = 'neutral'
session = -1

latest_message_time = None


def answer_with_error():
    print("Я тебя не понимаю")
    clear_state()


def form_answer():
    global prev_state, current_state
    answer = ""

    if prev_state == 'neutral' and current_state == 'joy_state':
        answer = "Привет! Здорово, что у тебя хорошее настроение!"
    elif prev_state == 'neutral' and current_state == 'sad_state':
        answer = "Привет. Не грусти."
    elif prev_state == 'neutral' and current_state == 'angry_state':
        answer = "Привет. Ты очень зол."
    elif prev_state == 'joy_state' and current_state == 'joy_state':
        answer = "Ты очень рад!"
    elif prev_state == 'sad_state' and current_state == 'sad_state':
        answer = "Тебе все еще грустно."
    elif prev_state == 'angry_state' and current_state == 'angry_state':
        answer = "Ты все еще зол."
    elif prev_state == 'joy_state' and current_state == 'sad_state':
        answer = "Ты загрустил."
    elif prev_state == 'joy_state' and current_state == 'angry_state':
        answer = "Ты разозлился."
    elif prev_state == 'sad_state' and current_state == 'joy_state':
        answer = "Рад, что тебе лучше!"
    elif prev_state == 'sad_state' and current_state == 'angry_state':
        answer = "Кажется, тебе стало ещё хуже."
    elif prev_state == 'angry_state' and current_state == 'joy_state':
        answer = "Рад, что ты снова в хорошем настроении!"
    elif prev_state == 'angry_state' and current_state == 'sad_state':
        answer = "Ты был зол, а теперь загрустил."
    else:
        answer_with_error()

    prev_state = current_state
    return answer


def is_long_message(message):
    return len(message) > 1 or len(message) < 1


def clear_state():
    prev_state = 'neutral'
    current_state = 'neutral'


def send_message(message):
    print(message)


def parse_emotional_state(message):
    global current_state
    if message in joy:
        current_state = 'joy_state'
    elif message in sad:
        current_state = 'sad_state'
    elif message in angry:
        current_state = 'angry_state'
    else:
        clear_state()


def answer_message(message, session, client):
    global latest_message_time

    write_message(datetime.datetime.now(), session, message, client)

    if is_long_message(message):
        answer_with_error()
        return

    latest_message_time = time.time()
    parse_emotional_state(message)
    answer = form_answer()
    send_message(answer)


def break_session():
    close_session(session, datetime.datetime.now())
    sys.exit()


if __name__ == "__main__":
    init_db()
    write_session(datetime.datetime.now())
    session = get_current_session()
    client = random.randint(10000, 99999)
    latest_message_time = time.time()

    while time.time() - latest_message_time < SESSION_TIME:
        message = input()
        answer_message(message, session, client)

    break_session()
