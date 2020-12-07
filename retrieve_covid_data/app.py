import boto3
from io import BytesIO
import requests
import os
import json


def lambda_handler(event, context):
    """Sample Lambda function reacting to EventBridge events

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
        The same input event file
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("bigdata2bucket")
    sec = boto3.client("secretsmanager", region_name="us-east-1")
    secret = json.loads(
        sec.get_secret_value(SecretId=os.environ["SECRET_NAME"]).get("SecretString")
    )
    with requests.get(
        "https://api.covidactnow.org/v2/states.csv",
        params={"apiKey": secret["API_KEY"]},
    ) as r, BytesIO(r.content) as payload:
        try:
            r.raise_for_status()
            if r.ok:
                bucket.upload_fileobj(payload, "covid-retrieval-test.csv")
            return {
                "statusCode": 200,
                "body": f"Update {'successful' if r.ok else 'failed'}, received status code {r.status_code}!",
            }
        except requests.exceptions.HTTPError as err:
            return {
                "statusCode": 500,
                "body": f"Update unsuccessful, received response {err}",
            }
