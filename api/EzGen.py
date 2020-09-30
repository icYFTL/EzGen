from source.api.api import *
from core import config

app.run(host=config['host'], port=config['port'], debug=False)