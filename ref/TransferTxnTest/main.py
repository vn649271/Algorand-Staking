from txn2 import test_send_algo_txn 

sender_prv_key = 'uXtnKHY74recz4Y1HIiYI51bgCMIqT0JZufw9Q/eoA33fntH01+J2s5XhUZn1pychnewrXuni6rxjjUQu4SWVQ=='
sender = '657HWR6TL6E5VTSXQVDGPVU4TSDHPMFNPOTYXKXRRY2RBO4ESZK467J7MI'
receiver = 'IXY7TNLQ75CBIB3UKLHK5GQBLITR5FFWD3MYJOOCXAILJ36VM344YVQAS4'

test_send_algo_txn(sender_prv_key, sender, receiver, 7)
