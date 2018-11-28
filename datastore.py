# datastore.py
# Key-Value Cache
# Created  23-11-2018
# Aaron McConnell

import json    # Library for json file read/write
from flask import Flask, request, jsonify # use Flask web framework
from threading import Lock
import fcntl   #Library for file locking
import ast

lock = Lock()           # Create a lock to handle concurrent access
cache = dict()          # Key/Values Cache
app = Flask(__name__)

@app.route('/get/<key>', methods=['POST'])
def get(key):
    with app.app_context():
        # Return a value list from cache
        global cache
        with lock: 
            # Check that an actual key has been received
            if isinstance(key, str):
                # Check if the key is already in the cache
                if key in cache:
                    return json.dumps(cache[key])
                else:
                    return jsonify("Key is not in cache")
            else:
                return jsonify("Key is not a string")

@app.route('/set/<key>/<values>', methods=['POST'])
def set(key,values):
    with app.app_context():
        global cache
        with lock:
            # Convert to a list from the values string
            values = ast.literal_eval(values)
            cache.update({key: values})
            _fileWrite()
        return jsonify("Cache updated")


@app.route('/append/<key>/<value>', methods=['POST'])
def append(key,value):
    global cache
    with lock:
        if key in cache:
            if value in cache[key]:
                return "Key-Value already exists"
            else:
                cache[key].append(value)
                _fileWrite()
                return "Key exists. Value added"
        else:
            cache.update({key: [value]})
            _fileWrite()
            return "New key and value added"



@app.route('/prepend/<key>/<value>', methods=['POST'])
def prepend(key, value):
    # Prepend cache with new key-value
    global cache
    with lock:
        if key in cache:
            if value in cache[key]:
                return "Key-Value already exists"
            else:
                cache[key].insert(0, value)
                _fileWrite()
                return "Key exists. Value added"
        else:
            cache.update({key: [value]})
            _fileWrite()
            return "New key and value added"


def _fileWrite():
    global cache
    # Write cache to file for persistance
    f = open("cache.json", "w")

    # Lock the file to prevent multiple, concurrent  writes    
    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    f.write(json.dumps(cache))
    # Unlock and close the file
    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()

def _fileRead():
    global cache
    try:
        # Read cache from file
        # No need to lock file as this only happens at process boot
        with open("cache.json") as f_in:
            return (json.load(f_in))
    except:
        # If file doesn't exist, return empty dict braces
        # file will be created on next _fileWrite()
        return(json.loads("{}"))
                                                              
if __name__ == '__main__':
    cache = dict(_fileRead())    #read keys/values from file at boot
    app.run(threaded=True, debug=True)

# endfile
