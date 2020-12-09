import boto3
import os
import json
import pandas as pd
from urllib.error import HTTPError


def lambda_handler(event, context):
    """Retrieves data from an API and sends it to a bucket

    Parameters
    ----------
    event: dict, required
        Event Bridge Events Format

        Event doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
        200 if the update succeeds, 500 otherwise
    """
    sec = boto3.client("secretsmanager", region_name="us-east-1")
    secret = json.loads(
        sec.get_secret_value(SecretId=os.environ["SECRET_NAME"]).get("SecretString")
    )
    try:
        target_counties = pd.read_csv(
            os.environ["COUNTY_LIST"], index_col=os.environ["SEARCH_COLUMN"], usecols=[os.environ["SEARCH_COLUMN"]]
        ).index
        dtypes = {
            "country": "category",
            "state": "category",
            "level": "category",
            "metrics.testPositivityRatioDetails.source": "category",
        }
        pd.read_csv(
            f"https://api.covidactnow.org/v2/counties.csv?apiKey={secret['API_KEY']}",
            dtype=dtypes,
            index_col="fips",
        ).sort_index().reindex(target_counties).to_csv(
            os.environ["OUTPUT_FILE"]
        )
    except HTTPError as err:
        return {
            "statusCode": 500,
            "body": f"Update unsuccessful, received response {err}",
        }
    else:
        return {"statusCode": 200, "body": "Update successful!"}
