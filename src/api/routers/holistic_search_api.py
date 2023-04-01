import logging 
import os
import pathlib
import time
import json
from typing import Dict
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Request
from google.oauth2 import service_account
from google.cloud import bigquery

from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

#bq job
current_dir = pathlib.Path(__file__).parent.absolute()

service_account_path = os.path.join(current_dir, "service_accounts", "sa.json")

router = APIRouter(
    prefix="/api/v1",
    tags=["holistic-search"],
    responses={404: {"description": "Not found"}},
)


async def bq_client(service_account_path):
    scoped_credentials =  service_account.Credentials.from_service_account_file(service_account_path).with_scopes(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    return bigquery.Client(credentials=scoped_credentials)


def bq_query_job(query_string, client):
    res = client.query(query_string).result()
    ### available methods on res: ###
    # 'api_request', 'client', 'extra_params', 'item_to_value', 'max_results', 'next_page_token', 'num_results', 'page_number', 
    # 'pages', 'path', 'schema', 'to_arrow', 'to_arrow_iterable', 'to_dataframe', 'to_dataframe_iterable', 'to_geodataframe', 'total_rows'
    return res.to_arrow(create_bqstorage_client=True).to_pandas()


# Define a Pydantic model to parse the request body JSON.
class QueryRequest(BaseModel):
    queries: Dict[str, str]


@router.post("/holistic-search", tags=["holistic-search"])
async def holistic_search(request: Request, query_request: QueryRequest):
    try:
        
        start_time = time.time()
        client = await bq_client(service_account_path)
        
        def get_dataframe(key, query):
            df = bq_query_job(query, client)
            
            # add "id" column to dataframe if it doesn't exist
            if 'id' not in df.columns:
                df['id'] = df.index
            
            # round all numbers to 2 decimal places
            df = df.round(2)
            
            return key, df.to_json(orient='records')
        
        # run all queries concurrently in a thread pool
        with ThreadPoolExecutor(max_workers=20) as executor:
            # Create a list of tasks to run concurrently
            tasks = [executor.submit(get_dataframe, key, query) for key, query in query_request.queries.items()]

            # Run all tasks concurrently and get their results
            results = [task.result() for task in tasks]

        # Combine results into the return_dict_obj
        return_dict_obj = {}
        for key, df in results:
            return_dict_obj[key] = df

        print('end_time', time.time() - start_time)
        
        # return to frontend
        return json.dumps(return_dict_obj)
    
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
