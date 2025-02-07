import inspect
import json

from services.logger import Logger

class Handler:

	def GenerateSwaggerDoc(data):

		doc = {
			"swagger": "2.0",
			"info": {
				"title": "Batman API Documentation",
				"description": "Automatically generated API documentation for Batman microservices.",
				"version": "1.0.0"
			},
			"host": "batman-ms-swagger",
			"schemes": ["http"],
			"paths": {}
		}

		for x in data:
			endpoint = f"/api/v1/{x['service']}/{x['endpoint'].strip('/')}"
			response_body = json.loads(x['response']) if x['response'] else {}

			if endpoint not in doc["paths"]:
				doc["paths"][endpoint] = {}

			doc["paths"][endpoint]["post"] = {
				"summary": f"API for {x['service']}",
				"description": f"Documentation for {x['service']} of endpoint {x['endpoint']}",
				"tags": [x['service']],
				"parameters": [
					{
						"in": "body",
						"name": "request_body",
						"required": True,
						"schema": Handler.Schema(json.loads(x['request']) if x['request'] else {})
					}
				],
				"responses": {
					f"{response_body.get('ApiHttpResponse', 200)}": {
						"description": "Success",
						"schema": Handler.Schema(response_body)
					},
					"400": {
						"description": "Bad Request",
						"schema": {
							"type": "object",
							"properties": {
								"ApiHttpResponse": {
									"type": "integer",
									"example": 400
								},
								"ApiMessages": {
									"type": "array",
									"items": {
										"type": "string",
										"example": [
											"ERROR - Missing required parameters", 
											"ERROR - Invalid arguments", 
											"ERROR - Invalid meta",
											"ERROR - No records found"
										]
									}
								},
							}
						}
					},
                    "500": {
						"description": "Internal Server Error",
						"schema": {
							"type": "object",
							"properties": {
								"ApiHttpResponse": {
									"type": "integer",
									"example": 500
								},
								"ApiMessages": {
									"type": "array",
									"items": {
										"type": "string",
										"example": [
											"ERROR - Unexpected server issue", 
											"ERROR - Database connection failed"
										]
									}
								},
							}
						}
					},
				}
			}
		
		return doc

	def Schema(data={}):

		schema = {
				"type": "object",
				"properties": {}
			}
		
		try:
			schema["properties"] = {
				key: {
					"type": Handler.SwaggerDataType(type(value)), 
					"example": value
				} for key, value in data.items()
			}

		except Exception as e:
			Logger.CreateExceptionLog(inspect.stack()[0][3],str(e),json.dumps(data))

			return schema

		return schema
	
	def SwaggerDataType(type):

		types = {
			str: "string",
			int: "integer",
			float: "number",
			bool: "boolean",
			list: "array",
			dict: "object"
		}

		return types.get(type, "string")