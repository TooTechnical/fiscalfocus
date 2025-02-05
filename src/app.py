# src/app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from models.trades import Trade
from utils.database import SessionLocal, engine
import os
import eventlet
import requests

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

def price_stream():
    while True:
        try:
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={'ids': 'bitcoin,ethereum', 'vs_currencies': 'usd'},
                timeout=5
            )
            data = response.json()
            socketio.emit('price_update', {
                'btc': data['bitcoin']['usd'],
                'eth': data['ethereum']['usd']
            })
        except Exception as e:
            print(f"Price stream error: {str(e)}")
        finally:
            socketio.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('execute_trade')
def handle_trade(data):
    try:
        db = SessionLocal()
        new_trade = Trade(
            pair=data['pair'],
            amount=data['amount'],
            price=data['price']
        )
        db.add(new_trade)
        db.commit()
        socketio.emit('trade_confirmation', {'status': 'success', 'trade_id': new_trade.id})
    except Exception as e:
        socketio.emit('trade_confirmation', {'status': 'error', 'message': str(e)})
    finally:
        db.close()

if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    socketio.run(app)
