import pytest

from datastore import append, prepend, get, set, _fileWrite, _fileRead, exit_handler

def test_append():
    assert( append("append0", "value0"))

def test_prepend():
    assert( prepend("pre0", "pval0"))

def test_get():
    assert(get("testVal"))

def test_set():
    assert(set("setVal", str(["s0", "s1", "s2"])))

def test__fileWrite():
    _fileWrite()

def test_fileRead():
    _fileRead()

def test_exit_handler():
    exit_handler()
