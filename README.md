# batman-ms-swagger

A microservice that dynamically generates and maintains **Swagger API documentation**, ensuring up-to-date API specs without manual intervention. It captures successful API interactions and updates documentation in real-time.

## Features
- **Automated API Logging**: Captures API interactions and dynamically updates Swagger documentation.
- **Swagger Documentation Generation**: Collects and organizes API endpoints, responses, and parameters into structured documentation.
- **Centralized API Specs**: Stores and manages API specs dynamically, ensuring real-time documentation updates.
- **Seamless Integration with batman-ms-logger**: Hooks into the logging service to document 2xx responses automatically.
- **RESTful API for Documentation Management**: Allows retrieval and regeneration of API specs programmatically.

## How It Works
1. **API Request Logging**: Receives structured API logs from batman-ms-logger.
2. **Swagger YAML Generation**: Processes the logged requests to dynamically generate and update Swagger documentation.
3. **Expose API Docs**: Provides a real-time `/apidocs` endpoint for viewing and interacting with the generated API documentation.
4. **Scheduled Updates**: A **cron job** ensures Swagger documentation remains current by reprocessing logs weekly.

## Endpoints

### **Log API Interaction**
```http
POST /api/v1/Api/CreateLog
```
Stores API requests and responses for documentation generation.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS api_specs (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(45) NOT NULL,
    specs JSON NOT NULL,
    outdated BOOLEAN DEFAULT 0,
    date DATETIME NOT NULL
) ENGINE=INNODB;
```

## Technologies Used
- **Python** (Flask)
- **Swagger (OpenAPI 3.0)**
- **MySQL** (for storing API logs and generated specs)
- **Docker & Kubernetes** (for microservice deployment)

## Getting Started

1. Clone the repository:
   ```sh
   git clone https://github.com/jawwadabbasi/batman-ms-swagger.git
   cd batman-ms-swagger
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the service:
   ```sh
   python app.py
   ```
4. Access Swagger documentation:
   ```sh
   http://localhost:5000/apidocs
   ```

---
**"Because even Batman needs documentation."** 🦇