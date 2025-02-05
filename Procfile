web: gunicorn --worker-class eventlet -w 1 app:app
worker: python -c 'from app import socketio, price_stream; socketio.start_background_task(price_stream)'
