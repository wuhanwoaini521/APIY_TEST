

class AssertException(Exception):
    def __init__(self, expect, actual):
        self.expect = expect
        self.actual = actual
        print('Expect value: {} and Actual value: {} are not equal'.format(self.expect, self.actual))


class MethodException(Exception):
    def __init__(self, method):
        self.method = method
        print('Request method error, not support {} method, please choose ["GET", "POST","PUT","DELETE"]'.format(method))


class RequestException(Exception):
    def __init__(self):
        print('RequestException')


class ResponseException(Exception):
    def __init__(self):
        print('ResponseException')


class FileException(Exception):
    def __init__(self):
        print('FileException')


class StatusException(Exception):
    def __init__(self):
        print('StatusException')
