import json
import uuid

from includes.db import Db
from includes.common import Common
from v1.handler import Handler

class Docify:

	def ApiLog(service,endpoint,request,response):

		api_data = {}
		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] = []
		api_data['ApiResult'] = []

		try:
			http_response = response['ApiHttpResponse']
			http_response = int(http_response)

		except:
			api_data['ApiHttpResponse'] = 400
			api_data['ApiMessages'] += ['INFO - Invalid HTTP response code']

			return api_data
		
		if http_response not in [200,201,202,204]:
			api_data['ApiHttpResponse'] = 200
			api_data['ApiMessages'] += ['INFO - Request processed successfully']

			return api_data

		query = """
			INSERT INTO api_logs (
				api_id, 
				service, 
				endpoint,
				request, 
				response, 
				date
			)
			VALUES (
				%s, 
				%s, 
				%s, 
				%s, 
				%s, 
				%s
			)
			ON DUPLICATE KEY UPDATE
				request = %s,
				response = %s,
				date = %s;
		"""

		inputs = (
			str(uuid.uuid4()),
			service,
			endpoint,
			json.dumps(request) if request else "",
			json.dumps(response) if response else "",
			str(Common.Datetime()),
			json.dumps(request) if request else "",
			json.dumps(response) if response else "",
			str(Common.Datetime())
		)

		if Db.ExecuteQuery(query,inputs,True):
			api_data['ApiHttpResponse'] = 201
			api_data['ApiMessages'] += ['INFO - Request processed successfully']

			return api_data

		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] += ['ERROR - Could not create record']

		return api_data
	
	def SwaggerApiDocs():

		api_data = {}
		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] = []
		api_data['ApiResult'] = []
		
		apis = Docify.FetchApiLogs()

		if not apis:
			api_data['ApiHttpResponse'] = 500
			api_data['ApiMessages'] += ['ERROR - Failed to get api logs']

			return api_data
		
		sd = Handler.GenerateSwaggerDoc(apis)

		if not sd:
			api_data['ApiHttpResponse'] = 500
			api_data['ApiMessages'] += ['ERROR - Failed to generate doc']

			return api_data

		query = """
			INSERT INTO api_specs
			SET	spec_type = %s,
				spec_yaml = %s,
				date = %s
		"""

		inputs = (
			'swagger',
			json.dumps(sd),
			str(Common.Datetime())
		)

		if Db.ExecuteQuery(query,inputs,True):
			api_data['ApiHttpResponse'] = 201
			api_data['ApiMessages'] += ['INFO - Request processed successfully']
			api_data['ApiResult'] = sd

			return api_data
		
		api_data['ApiHttpResponse'] = 500
		api_data['ApiMessages'] += ['ERROR - Could not create record']

		return api_data

	def FetchApiLogs():

		query = """
			SELECT *
			FROM api_logs
		"""

		return Db.ExecuteQuery(query,None,True)
	
	def SwaggerApiYaml():

		query = """
			SELECT spec_yaml
			FROM api_specs
			WHERE spec_type = %s
			AND outdated = %s
			LIMIT 1
		"""

		inputs = (
			'swagger',
			0
		)

		results = Db.ExecuteQuery(query,inputs,True)

		if not results:
			return False
		
		return json.loads(results[0]['spec_yaml'])