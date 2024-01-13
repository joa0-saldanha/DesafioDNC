from airflow.models import BaseOperator, Variable
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token
import json
import requests


class CallGoogleCloudFunctionsOperator(BaseOperator):

    template_fields = ('function_name', 'function_params', 'project_id')

    def _init_(
        self,
        *,
        function_name,
        function_params=None,
        project_id=Variable.get('project_id'),
        response_type='json',
        response_key=None,
        location='us-central1',
        gcp_conn_id='google_cloud_default',
        **kwargs
    ):
        super()._init_(**kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.function_name = function_name
        self.function_params = function_params
        self.response_type = response_type
        self.response_key = response_key
        self.location = location
        self.project_id = project_id

    def execute(self, context):

        url = f'https://{self.location}-{self.project_id}.cloudfunctions.net/{self.function_name}'
        id_token = fetch_id_token(Request(), url)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {id_token}'
        }
        data = json.dumps(self.function_params) if self.function_params else None
        result = requests.post(url=url, headers=headers, data=data)
        result.raise_for_status()

        if self.response_type == 'json':
            response = result.json()
            print(response)
            if self.response_key:
                return response[self.response_key]
            return response
        else:
            return result.text