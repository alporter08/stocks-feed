import json
import logging
from stocks_feed.dataloader import Stock

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # Get the length and width parameters from the event object. The
    # runtime converts the event object to a Python dictionary

    logger.info(f"Event: {event}")

    ticker = event["ticker"]
    start_date = event["start_date"]
    end_date = event["end_date"]

    s = Stock(ticker, start_date, end_date)
    data = s.get_daily_stock_prices()

    logger.info(f"CloudWatch logs group: {context.log_group_name}")

    return json.dumps(data)
