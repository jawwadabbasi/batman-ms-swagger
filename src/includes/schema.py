import settings

from includes.db import Db

class Schema:

	def CreateDatabase():

		query = f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci"

		return Db.ExecuteQuery(query,None,True,True)

	def CreateTables():

		#####################################################################################################
		query = """
			CREATE TABLE IF NOT EXISTS api_logs (
				api_id VARCHAR(45) PRIMARY KEY NOT NULL,
				service VARCHAR(45) NOT NULL,
				endpoint VARCHAR(150) NOT NULL,
				request JSON DEFAULT NULL,
				response JSON NULL,
				date DATETIME NOT NULL,
				UNIQUE KEY unique_service_endpoint (service, endpoint)
			) ENGINE=INNODB;
		"""

		if not Db.ExecuteQuery(query,None,True):
			return False

		Db.ExecuteQuery("ALTER TABLE api_logs ADD INDEX service (service);",None,True)
		Db.ExecuteQuery("ALTER TABLE api_logs ADD INDEX endpoint (endpoint);",None,True)
		Db.ExecuteQuery("ALTER TABLE api_logs ADD INDEX date (date);",None,True)
		#####################################################################################################

		#####################################################################################################
		query = """
			CREATE TABLE IF NOT EXISTS api_specs (
				id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
				spec_type VARCHAR(45) NOT NULL,
				spec_yaml JSON NOT NULL,
				outdated BOOLEAN DEFAULT 0,
				date DATETIME NOT NULL
			) ENGINE=INNODB;
		"""

		if not Db.ExecuteQuery(query,None,True):
			return False

		Db.ExecuteQuery("ALTER TABLE api_specs ADD INDEX id (id);",None,True)
		Db.ExecuteQuery("ALTER TABLE api_specs ADD INDEX spec_type (spec_type);",None,True)
		Db.ExecuteQuery("ALTER TABLE api_specs ADD INDEX outdated (outdated);",None,True)
		Db.ExecuteQuery("ALTER TABLE api_specs ADD INDEX date (date);",None,True)
		#####################################################################################################

		return True