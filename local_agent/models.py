import json
import urllib.request
from typing import Protocol
from urllib.parse import urlparse


class Model(Protocol):
    def generate(self, messages: list, config: dict) -> dict: ...


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Local model redirects are disabled.')


class LocalModel:
    def __init__(self, model, endpoint='http://127.0.0.1:11434', backend='ollama'):
        parsed = urlparse(endpoint)
        if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1', 'localhost', '::1') or parsed.username:
            raise ValueError('V0 only connects to a local model server.')
        self.model, self.endpoint, self.backend = model, endpoint.rstrip('/'), backend

    def installed_models(self):
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
        with opener.open(self.endpoint+'/api/tags',timeout=5) as response:
            return json.loads(response.read(1_000_000)).get('models',[])

    def generate(self, messages, config):
        if self.backend == 'ollama':
            path = '/api/chat'
            payload = dict(model=self.model, messages=messages, stream=False, format=config.get('response_schema','json'), options={**{k:v for k,v in config.items() if k in ('num_thread','num_ctx')},'num_predict':4096,'temperature':0})
        else:
            path = '/v1/chat/completions'
            payload = dict(model=self.model, messages=messages, stream=False, temperature=0.1, max_tokens=4096, response_format={'type':'json_object'})
        request = urllib.request.Request(self.endpoint + path, json.dumps(payload).encode(), {'Content-Type':'application/json'})
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
        with opener.open(request, timeout=120) as response:
            data = json.loads(response.read(4 * 1024 * 1024))
        content = data['message']['content'] if self.backend == 'ollama' else data['choices'][0]['message']['content']
        result = json.loads(content)
        if not isinstance(result, dict):
            raise ValueError('Model response must be a JSON object.')
        return result
