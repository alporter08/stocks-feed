import os
import json
import logging
from stocks_feed.dataloader import Stock
from stocks_feed.aws_utils import get_secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # Get the length and width parameters from the event object. The
    # runtime converts the event object to a Python dictionary

    logger.info(f"Event: {event}")

    if "POLYGON_API_KEY" not in os.environ:
        logger.info("Setting POLYGON_API_KEY env variable.")
        os.environ["POLYGON_API_KEY"] = get_secret()

    ticker = event["ticker"]
    start_date = event["start_date"]
    end_date = event["end_date"]

    s = Stock(ticker, start_date, end_date)
    data = s.get_daily_stock_prices()

    logger.info(f"CloudWatch logs group: {context.log_group_name}")

    return json.dumps(data)
