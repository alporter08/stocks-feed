import json
import logging
from stocks_feed.dataloader import Stock

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    # Get the length and width parameters from the event object. The
    # runtime converts the event object to a Python dictionary

    ticker = event["ticker"]
    start_date = event["width"]
    end_date = event["end_date"]

    s = Stock(ticker, start_date, end_date)
    data = s.get_daily_stock_prices()

    logger.info(f"CloudWatch logs group: {context.log_group_name}")

    # return the calculated area as a JSON string
    # data = {"area": area}
    return json.dumps(data)
