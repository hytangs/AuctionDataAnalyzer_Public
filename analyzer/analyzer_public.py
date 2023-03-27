import pandas as pd
from datetime import datetime


def parse_auction(filename):
    print(filename)
    data = pd.read_excel(filename, index_col=0)
    auction_data = []
    for i in data.itertuples():
        if pd.isnull(i[1]):
            continue
        print(i[0])
        records_count = len(i)
        item_index = i[0]
        item_name = i[1]
        item_start_bid = i[2]

        timestamp = str(i[3])
        date = datetime.strptime(timestamp[:10], '%Y-%m-%d').date()
        item_close_time = datetime.combine(date, datetime.strptime(timestamp[11:], '%H:%M:%S').time())
        item_bids = []

        stop_sign = False
        n = 0
        item_overtime_count = 0
        bidder_dict = {}
        item_bidder_count = 0
        while not stop_sign:
            if 4 + n * 3 >= records_count:
                stop_sign = True
            elif pd.isnull(i[4 + n * 3]):
                n += 1
                continue
            else:
                bidder = i[4 + n * 3]
                if bidder in bidder_dict:
                    bid_bidder = bidder_dict[bidder]
                else:
                    bidder_dict[bidder] = item_bidder_count
                    bid_bidder = item_bidder_count
                    item_bidder_count += 1
                bid_price = i[5 + n * 3]
                bid_time = datetime.combine(date, datetime.strptime(str(int(i[6 + n * 3])), '%H%M%S').time())
                item_bids.append([bid_bidder, bid_price, bid_time])
                if bid_time > item_close_time:
                    item_overtime_count += 1
                n += 1
        auction_data.append([item_index, item_name, item_start_bid, item_close_time, item_overtime_count,
                             item_bidder_count, item_bids])
    return auction_data

