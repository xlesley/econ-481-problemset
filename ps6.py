"""
Lesley Xu
ECON 481

Implements the functions for PS6.
"""


def github() -> str:
    """
    Takes no arguments and returns a link to my solutions on GitHub.
    """

    return "https://github.com/xlesley/econ-481-problemset/blob/main/ps6.py"


def std() -> str:
    """
    Generates a SQL query to calculate the standard deviation of bids for each
    item in the auctions database.

    Returns:
        str: SQL query string.
    """

    query = """
            SELECT
                b.itemid,
                SQRT(SUM(POW((b.bidAmount - mean_bid), 2)) / (COUNT(*) - 1)) AS bidStd
            FROM
                bids b
            LEFT JOIN
                (SELECT itemid, AVG(bidAmount) AS mean_bid FROM bids GROUP BY itemid) AS means
            ON
                b.itemid = means.itemid
            GROUP BY
                b.itemid
            HAVING COUNT(*) > 1
            """
    return query


def bidder_spend_frac() -> str:
    """
    Generates a SQL query to calculate the total spend, total bids, and spend
    fraction for each bidder in the auctions database.

    Returns:
        str: SQL query string.
    """

    query = """
            SELECT
                bidderName,
                SUM(CASE WHEN highBidderName = bidderName THEN bidamount ELSE 0 END) AS total_spend,
                SUM(bidamount) AS total_bids,
                CAST(SUM(CASE WHEN highBidderName = bidderName THEN bidamount ELSE 0 END) AS REAL) / CAST(SUM(bidamount) AS REAL) AS spend_frac
            FROM (
                SELECT
                    bidderName,
                    bidamount,
                    highBidderName,
                    ROW_NUMBER() OVER (PARTITION BY itemId, bidderName ORDER BY bidamount DESC) AS row_num
                FROM bids) AS ranked_bids
            WHERE row_num = 1
            GROUP BY bidderName
            """

    return query


def min_increment_freq() -> str:
    """
    Generates a SQL query to calculate the frequency of bids that are exactly
    the minimum bid increment above the previous high bid, excluding items
    where isBuyNowUsed=1.

    Returns:
        str: SQL query string.
    """

    query = """
            SELECT
            SUM(CASE WHEN b2.bidAmount = b1.bidAmount + i.bidIncrement THEN 1
                ELSE 0
                END) * 1.0 / COUNT(b2.bidAmount) AS freq
            FROM bids b1
            JOIN bids b2 ON b1.itemId = b2.itemId AND b1.bidAmount < b2.bidAmount
            JOIN items i ON i.itemId = b1.itemId
            WHERE i.isBuyNowUsed = 0
            GROUP BY b1.itemId
            """

    return query


def win_perc_by_timestamp() -> str:
    """
    Generates a SQL query to calculate the win percentage by timestamp bin for
    bids placed in the auctions database.

    Returns:
        str: SQL query string.
    """

    query = """
            WITH AuctionTimes AS (
            SELECT
                itemId,
                MIN(bidTime) AS auctionStartTime,
                MAX(bidTime) AS auctionEndTime
            FROM
                bids
            GROUP BY
                itemId
        ),
            BinnedBids AS (
                SELECT
                    b.itemId,
                    b.bidderName,
                    b.bidAmount,
                    b.bidTime,
                    a.auctionStartTime,
                    a.auctionEndTime,
                    julianday(b.bidTime) AS bid_julianday,
                    julianday(a.auctionStartTime) AS start_julianday,
                    julianday(a.auctionEndTime) AS end_julianday,
                    (julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                    (julianday(a.auctionEndTime) - julianday(a.auctionStartTime)) AS normalized_time,
                    (julianday(b.bidTime) - julianday(a.auctionStartTime)) / 
                    (julianday(a.auctionEndTime) - julianday(a.auctionStartTime)) AS timestamp_bin,
                    MAX(b.bidAmount) AS winningBidAmount
                FROM
                    bids b
                JOIN
                    AuctionTimes a ON b.itemId = a.itemId
                GROUP BY
                    b.itemId,
                    b.bidderName,
                    b.bidAmount,
                    b.bidTime,
                    a.auctionStartTime,
                    a.auctionEndTime
            )
            SELECT
                timestamp_bin,
                COUNT(CASE WHEN bidAmount = winningBidAmount THEN 1 END) * 1.0 / COUNT(*) AS win_perc
            FROM
                BinnedBids
            GROUP BY
                timestamp_bin
    """

    return query
