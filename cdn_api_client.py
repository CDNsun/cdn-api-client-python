import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json

# Version 1.0.0
# This class is written to be compatible with Python 2 and Python 3

class CDNsunCdnApiClient(object):

    _URL_PREFIX = 'https://cdnsun.com/api/'
    _TIMEOUT = 60
    _username = None
    _password = None

    # The options are listed in accordance with
    # http://php.net/manual/ru/function.curl-getinfo.php
    # As the tests showed that not all of these were in a response info object
    _CURL_RESPONSE_INFO_OPTIONS = {
        'EFFECTIVE_URL': 'url', 'CONTENT_TYPE': 'content_type',
        'RESPONSE_CODE': 'http_code', 'HEADER_SIZE': 'header_size',
        'REQUEST_SIZE': 'request_size', 'INFO_FILETIME': 'filetime',
        'SSL_VERIFYRESULT': 'ssl_verify_result',
        'REDIRECT_COUNT': 'redirect_count', 'TOTAL_TIME': 'total_time',
        'NAMELOOKUP_TIME': 'namelookup_time', 'CONNECT_TIME': 'connect_time',
        'PRETRANSFER_TIME': 'pretransfer_time', 'SIZE_UPLOAD': 'size_upload',
        'SIZE_DOWNLOAD': 'size_download', 'SPEED_DOWNLOAD': 'speed_download',
        'SPEED_UPLOAD': 'speed_upload',
        'CONTENT_LENGTH_DOWNLOAD': 'download_content_length',
        'CONTENT_LENGTH_UPLOAD': 'upload_content_length',
        'STARTTRANSFER_TIME': 'starttransfer_time',
        'REDIRECT_TIME': 'redirect_time', 'INFO_CERTINFO': 'certinfo',
        'PRIMARY_IP': 'primary_ip', 'PRIMARY_PORT': 'primary_port',
        'LOCAL_IP': 'local_ip', 'LOCAL_PORT': 'local_port',
        'REDIRECT_URL': 'redirect_url'
    }

    def __init__(self, options={}):

        if not options:
            raise Exception('empty options')
        elif not 'username' in options:
            raise Exception('empty options[username]')
        elif not 'password' in options:
            raise Exception('empty options[password]')

        self._username = options['username']
        self._password = options['password']

    def get(self, options={}):

        if not options:
            raise Exception('empty options')

        options['method'] = 'GET'
        return self._request(options)

    def post(self, options={}):

        if not options:
            raise Exception('empty options')

        options['method'] = 'POST'
        return self._request(options)

    def put(self, options={}):

        if not options:
            raise Exception('empty options')

        options['method'] = 'PUT'
        return self._request(options)

    def delete(self, options={}):

        if not options:
            raise Exception('empty options')

        options['method'] = 'DELETE'
        return self._request(options)

    def _request(self, options={}):

        if not options:
            raise Exception('empty options')
        elif not 'url' in options:
            raise Exception('empty options[url]')
        elif not 'method' in options:
            raise Exception('empty options[method]')

        c = pycurl.Curl()
        method = options['method']
        url = options['url']

        if (method == 'POST' or method == 'post'):
            c.setopt(c.POST, 1)
            if 'data' in options:
                c.setopt(pycurl.POSTFIELDS, json.dumps(options['data']))
        elif (method == 'PUT' or method == 'put'):
            c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
            if 'data' in options:
                c.setopt(pycurl.POSTFIELDS, json.dumps(options['data']))
        elif (method == 'DELETE' or method == 'delete'):
            c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
            if 'data' in options:
                c.setopt(pycurl.POSTFIELDS, json.dumps(options['data']))
        elif (method == 'GET' or method == 'get'):
            if 'data' in options:
                url = ('%s?%s' % (url, urlencode(options['data'])))
        else:
            raise Exception('Unsupported method: ' + method)

        # Set headers for JSON format
        headers = [
            'Accept: application/json',
            'Content-Type: application/json'
        ]
        c.setopt(pycurl.HTTPHEADER, headers)

        # Authentication:
        c.setopt(pycurl.HTTPAUTH, c.HTTPAUTH_BASIC)
        c.setopt(pycurl.USERPWD, self._username + ':' + self._password)

        # API endpoint
        if url[:len(self._URL_PREFIX)] != self._URL_PREFIX:
            url = self._URL_PREFIX + url
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.TIMEOUT, self._TIMEOUT)

        # API call
        buffer = BytesIO()
        c.setopt(pycurl.WRITEDATA, buffer)
        response_info_str = ''
        response_error = ''
        try:
            c.perform()
        except pycurl.error:
            # If have an issue with errstr() then there is also errstr_raw()
            response_error = c.errstr()
        try:
            response_info_str = self._get_response_info_line(c)
        except pycurl.error:
            # If have an issue with errstr() then there is also errstr_raw()
            if response_error == '':
                response_error = c.errstr()
        finally:
            c.close()

        # Body is a string on Python 2 and a byte string on Python 3.
        # If we know the encoding, we can always decode the body and
        # end up with a Unicode string.
        response_body = buffer.getvalue().decode("utf-8")

        if not response_body or response_error:
            raise Exception('curl error. response_body: ' + response_body +
                            ', response_info: ' + response_info_str +
                            ', response_error: ' + response_error)

        response_body_decoded = None
        try:
            response_body_decoded = json.loads(response_body)
        except Exception:
            raise Exception('json_decode response_body error' +
                            '. response_body: ' + response_body +
                            ', response_info: ' + response_info_str +
                            ', response_error: ' + response_error)

        return response_body_decoded

    def _get_response_info_line(self, pycurl_instance):
        info_options = {}
        option_code = None
        for (curl_opt, resp_opt) in self._CURL_RESPONSE_INFO_OPTIONS.items():
            option_value = self._get_curl_info_value(pycurl_instance,
                                                     curl_opt, option_code)
            if option_value != None:
                info_options[resp_opt] = option_value
        return json.dumps(info_options)

    def _get_curl_info_value(self, pycurl_instance, curl_opt, option_code):
        option_value = None
        option_str_value = None
        try:
            option_code = getattr(pycurl_instance, curl_opt, '')
            if type(option_code) == int:
                option_value = pycurl_instance.getinfo_raw(option_code)
                option_str_value = str(option_value)
        except AttributeError:
            pass
        return option_str_value
