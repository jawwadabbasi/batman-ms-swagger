import sys

from services.crons import Crons
from v1.docify import Docify

class Cron:

	def __init__(self):

		try:
			job = sys.argv[1]

		except:
			sys.exit('ERROR - No job specified')

		log_id = Crons.StartJob(job)

		if not log_id:
			sys.exit()

		if job == '':
			result = None

		elif job == 'generate-swagger-apidocs':
			result = Docify.SwaggerApiDocs()

		else:
			Crons.EndJob(log_id,'failed','ERROR - Unsupported job')
			sys.exit('ERROR - Unsupported job')

		Crons.EndJob(
			log_id,
			'success' if (result.get('ApiHttpResponse') is not None and result.get('ApiHttpResponse') != 500) else 'failed',
			result
		)

		sys.exit()

try:
	Cron()

except Exception as e:
	sys.exit(e)