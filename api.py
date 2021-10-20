import sudoku
import logging
from pathlib import Path
import json
from threading import Thread
import time
import flask
import copy

import os

app = flask.Flask(__name__, static_url_path='', static_folder='./html/')


if os.getenv('SUDOKU_DEBUG'):
    app.config["DEBUG"] = True
config = None # global config object
generate_t = None

# a simple struct like object
# just holds some variables
class Config:
    def __init__(self):
        # TODO allow user configuratiuon!
        self.port = 8089
        self.grid_len = 100
        self.difficulty = 40
        self.grids = {'grid_array': []}

def init():
    config = Config()
    load_grids(config)
    return config

def load_grids(config):
    # create config path
    Path('./config/').mkdir(parents=True, exist_ok=True)
    config_path = Path('./config/grids.json')
    if not Path.exists(config_path):
        return

    contents = Path(config_path).read_text()
    config.grids = json.loads(contents)


def gen_grid(config):
    logging.info('{}/{} grids. Generating new grid...'.format(len(config.grids['grid_array']), config.grid_len))
    new_grid = sudoku.generate(0, config.difficulty)
    config.grids['grid_array'].append(new_grid)
    with open('./config/grids.json', 'w') as fp:
        json.dump(config.grids, fp)
    logging.info('Grid with seed ' + str(new_grid[1]) + ' created')

def helper(config):
    while True:
        if len(config.grids['grid_array']) < config.grid_len:
            gen_grid(config)

        time.sleep(1)

@app.route('/getall', methods=['GET'])
def get_all():
    return flask.jsonify(config.grids)

@app.route('/next', methods=['GET'])
def next():
    if len(config.grids['grid_array']) >= 1:
            config.grids['current'] = config.grids['grid_array'][0]
            del config.grids['grid_array'][0]
            return flask.jsonify('ok')
    return flask.jsonify('no_grid'), 404

@app.route('/current', methods=['GET'])
def current():
    return flask.jsonify(config.grids['current'])

@app.route('/cheat', methods=['GET'])
def cheat():
    solved = copy.deepcopy(config.grids['current'][0])
    sudoku.solve(solved)
    return flask.jsonify((solved, config.grids['current'][1]))

@app.route('/put', methods=['GET'])
def put():
    try:
        x = int(flask.request.args.get('x'))
        y = int(flask.request.args.get('y'))
        n = int(flask.request.args.get('n'))
    except Exception:
        x = None
        y = None
        n = None

    if x is None or y is None or n is None or x > 9 or y > 9 or n > 9 or x < 0 or y < 0 or n < 0:
        return flask.jsonify('bad_request'), 400

    if sudoku.is_possible(config.grids['current'][0], y, x, n) and config.grids['current'][0][y][x] == 0:
        config.grids['current'][0][y][x] = n
        if sudoku.solve(copy.deepcopy(config.grids['current'][0])):
            with open('./config/grids.json', 'w') as fp:
                json.dump(config.grids, fp)
            return flask.jsonify('ok')
        config.grids['current'][0][y][x] = 0

    return flask.jsonify('bad_input')

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

def run():
    global config
    global generate_t
    logging.basicConfig(level=logging.DEBUG)
    config = init()

    urls = {
            '/': index
            }

    generate_t = Thread(target=helper, args=[config])
    generate_t.start()

def start_app():
    global config
    app.run(port=config.port)

