# client.py
# Key-Value Cache
# Created  23-11-2018
# Aaron McConnell

import json
import requests
import ast


### Client to test API of cache server

### Change option variable to appropriate int value
### in order to select correct API call

### 1: append
### 2. setvals
### 3. get
### 4. prepend

option = 1

def append():
    # Append key-value
    key = "append_test"
    value = "app0"

    # Send data to append method of server address via URL
    obj = requests.post("http://127.0.0.1:5000/append/" + key + "/" + value)
    print (obj.text)


def setvals():
    # Set key-value
    
    key = "setValSet0"
    valueList = ["set0", "set1", "set2"]
    obj = requests.post("http://127.0.0.1:5000/set/" + key + "/" + str(valueList))
    print (obj.text)


def get():
    # get key-value

    # specify the key we want the value for. 
    key = "append_test"
    # send the key in the URL and get the response object
    obj = requests.post('http://127.0.0.1:5000/get/' + key)
    # get the text from the response and convert it to list/string 
    value = ast.literal_eval(obj.text)
    # check if a list of values or an error message is returned
    if isinstance(value, str) and value.startswith("Key is not"):
        print (value)
    else:
        print ("Values for key: " + key)
        for v in value: print (v)


def prepend():
    # prepend cache
    key = "prepend_test"
    value = "pre0"
    obj = requests.post("http://127.0.0.1:5000/prepend/" + key + "/" + value)
    print (obj.text)


options = {1 : append,
           2 : setvals,
           3 : get,
           4 : prepend,
           }

options[option]()

# endfile
