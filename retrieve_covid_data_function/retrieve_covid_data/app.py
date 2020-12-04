from schema.aws.events.scheduledjson import Marshaller
from schema.aws.events.scheduledjson import AWSEvent
from schema.aws.events.scheduledjson import ScheduledEvent
import boto3
from io import BytesIO
import requests
import os


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

    # Deserialize event into strongly typed object
    awsEvent: AWSEvent = Marshaller.unmarshall(event, AWSEvent)
    detail: ScheduledEvent = awsEvent.detail

    # Execute business logic
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("bigdata2bucket")
    print(f"Api key: {os.getenv('API_KEY')}")
    with requests.get(
        "https://api.covidactnow.org/v2/states.json",
        params={"apiKey": os.getenv("API_KEY")},
    ) as r, BytesIO(r.content) as payload:
        if r.status_code == 200:
            bucket.upload_fileobj(payload, "covid-retrieval-test.json")

    # Make updates to event payload, if desired
    awsEvent.detail_type = "HelloWorldFunction updated event of " + awsEvent.detail_type

    # Return event for further processing
    return Marshaller.marshall(awsEvent)
