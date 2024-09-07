# /run.py
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from threading import Timer
from src.app import create_app
import webbrowser
env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)



def open_browser():
      port = os.getenv('FLASK_PORT')
      webbrowser.open_new("http://127.0.0.1:" + port)

if __name__ == '__main__':
  port = os.getenv('FLASK_PORT')
  app.run(debug=True, use_reloader=False,host='0.0.0.0', port=port)
