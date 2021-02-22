import requests
import sched
import time


def post_request_update_holds():
    # Set up scheduler
    s = sched.scheduler(time.time, time.sleep)

    delay = 10 * 60  # Delay 10 minutes
    priority = 1

    def send_request(sc):
        response = requests.post('http://credit-service:8000/api/update/holds')

        s.enter(delay, priority, send_request, (sc, ))

    s.enter(delay, priority, send_request, (s, ))
    s.run()