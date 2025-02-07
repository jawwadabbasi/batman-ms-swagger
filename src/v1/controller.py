import inspect

from v1.docify import Docify

class Ctrl_v1:

	def Response(endpoint, request_data=None, api_data=None, log=True):

		return api_data

	def BadRequest(endpoint, request_data=None):

		api_data = {}
		api_data['ApiHttpResponse'] = 400
		api_data['ApiMessages'] = ['ERROR - Missing required parameters']
		api_data['ApiResult'] = []

		return api_data
	
	def ApiLog(request_data):

		if (not request_data.get('Service')
			or not request_data.get('Endpoint')
			or not request_data.get('Request')
			or not request_data.get('Response')
		):
			return Ctrl_v1.BadRequest(inspect.stack()[0][3],request_data)

		api_data = Docify.ApiLog(
			request_data.get('Service'),
			request_data.get('Endpoint'),
			request_data.get('Request'),
			request_data.get('Response')
		)

		return Ctrl_v1.Response(inspect.stack()[0][3],request_data,api_data)