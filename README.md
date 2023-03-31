# BigQuery CORS Handler
## Overview
> Send request to API with a dict of queries
>   e.g., `queries={"test": "select * from ___", "test2": "select * from ___", etc...}`
> API runs the query and returns the results with the same keys + resulting data in dict format
## Testing
> Add a service account `.json` file into`src\api\routers\service_accounts.json`
> Install dependencies
> Run `hypercorn main:app`
> Navigate to http://127.0.0.1:8000/docs to view endpoints
> Click "Try it out" on the POST `/api/v1/holistic-search` endpoint
> Add the below into the request body:
```
{
  "queries": {
    "test": "SELECT * FROM `bigquery-public-data.samples.wikipedia` LIMIT 5000"
  }
}
```
> Run the endpoint by clicking `Execute`