# BigQuery CORS Handler
## Overview
1.Send request to API with a dict of queries
>   e.g., `queries={"test": "select * from ___", "test2": "select * from ___", etc...}`
2. API runs the query and returns the results with the same keys + resulting data in dict format
## Testing
1. Add a service account `.json` file into`src\api\routers\service_accounts.json`
2. Install dependencies
3. Run `hypercorn main:app`
4. Navigate to http://127.0.0.1:8000/docs to view endpoints
5. Click "Try it out" on the POST `/api/v1/holistic-search` endpoint
6. Add the below into the request body:
```
{
  "queries": {
    "test": "SELECT * FROM `bigquery-public-data.samples.wikipedia` LIMIT 5000"
  }
}
```
7. Run the endpoint by clicking `Execute`
