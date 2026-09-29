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
        if backend not in ('ollama', 'openai-compatible'):
            raise ValueError('Choose ollama or openai-compatible as the local backend.')
        parsed = urlparse(endpoint)
        if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1', 'localhost', '::1') or parsed.username:
            raise ValueError('V0 only connects to a local model server.')
        self.model, self.endpoint, self.backend = model, endpoint.rstrip('/'), backend

    def installed_models(self):
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
        if self.backend == 'openai-compatible':
            with opener.open(self.endpoint+'/v1/models',timeout=5) as response:
                payload = response.read(1_000_001)
            if len(payload) > 1_000_000:
                raise ValueError('Local model list exceeds the response limit.')
            data = json.loads(payload)
            rows = data.get('data') if isinstance(data, dict) else None
            if not isinstance(rows, list) or any(not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id'].strip() for row in rows):
                raise ValueError('Local model list must contain a data list of model IDs.')
            return [{'name': row['id']} for row in rows]
        with opener.open(self.endpoint+'/api/tags',timeout=5) as response:
            models=json.loads(response.read(1_000_000)).get('models',[])
        with opener.open(self.endpoint+'/api/ps',timeout=5) as response:
            loaded=json.loads(response.read(1_000_000)).get('models',[])
        for model in models:
            model['loaded_vram']=sum(item.get('size_vram',0) for item in loaded if item.get('name')==model.get('name'))
        return models

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
