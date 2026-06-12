import os
import time
from celery import Celery

# Use the Redis instance provided by a Clever Cloud Redis add-on if one is
# linked (it exposes REDIS_URL), and otherwise fall back to the local
# redis-server started by workers.sh.
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

celery_app = Celery('text_processor',
                broker=REDIS_URL,
                backend=REDIS_URL)

@celery_app.task
def process_text(text, operations=None):
    """
    Process text according to requested operations

    Available operations:
    - reverse: reverses the text
    - uppercase: converts text to uppercase
    - lowercase: converts text to lowercase
    - repeat: repeats the text (number of times specified in repeat_count)
    """
    result = text
    operations = operations or {}

    # Simulation of a time-consuming process
    time.sleep(2)

    if operations.get('reverse'):
        result = result[::-1]

    if operations.get('uppercase'):
        result = result.upper()

    if operations.get('lowercase'):
        result = result.lower()

    if operations.get('repeat'):
        repeat_count = int(operations.get('repeat_count', 2))
        result = result * repeat_count

    return result

def server(environ, start_response):
    from urllib.parse import parse_qs

    # Parse query parameters
    query_string = environ.get('QUERY_STRING', '')
    params = parse_qs(query_string)
    task_id = params.get('task_id', [''])[0]

    if task_id:
        # Retrieve task result by ID
        task = process_text.AsyncResult(task_id)
        if task.ready():
            result = task.get()
            response = f"Task {task_id} result:\n\n{result}".encode('utf-8')
        else:
            response = f"Task {task_id} is still processing...".encode('utf-8')
    else:
        # Get parameters
        text = params.get('text', ['Hello world!'])[0]
        operations = {}

        if params.get('reverse', [''])[0].lower() == 'true':
            operations['reverse'] = True

        if params.get('uppercase', [''])[0].lower() == 'true':
            operations['uppercase'] = True

        if params.get('lowercase', [''])[0].lower() == 'true':
            operations['lowercase'] = True

        if 'repeat_count' in params:
            operations['repeat'] = True
            operations['repeat_count'] = params.get('repeat_count', ['2'])[0]

        # Launch asynchronous task
        task = process_text.delay(text, operations)

        # Prepare response
        response = f"Task submitted with ID: {task.id}\n\n"
        response += f"Text to process: {text}\n"
        response += f"Operations: {', '.join(operations.keys()) if operations else 'none'}\n\n"
        response += f"To check the result, visit: /?task_id={task.id}"
        response = response.encode('utf-8')

    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(len(response)))
    ]

    start_response(status, headers)
    return [response]
