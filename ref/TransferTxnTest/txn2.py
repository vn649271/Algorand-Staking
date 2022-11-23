# Example of accesing a remote API with a custom token key.
# (from contribution to: https://github.com/algorand/py-algorand-sdk)
# In this case, the API is expecting the key "X-API-Key" instead of the
# default "X-Algo-API-Token". This is done by using a dict with our custom
# key, instead of a string, as the token.

import json
import base64
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn

# algod_address = "https://testnet-algorand.api.purestake.io/ps2"
# algod_token = ""
# headers = {
#     # "X-API-Key": "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab",
#     "X-API-Key": "bWGapCpvM04fLKChEQ0fW1GZk3dCyznj9Ks3r7ud"
# }

# algod_client = algod.AlgodClient(algod_token, algod_address, headers)

# try:
#     status = algod_client.status()
#     print("Status: " + json.dumps(status, indent=2, sort_keys=True))
# except Exception as e:
#     print("Failed to get algod status: {}".format(e))

# # Retrieve latest block information                                                                                                                                               
# last_round = status.get("last-round")
# print("####################")
# try:
#     block = algod_client.block_info(last_round)
#     print("Latest block: " + json.dumps(block, indent=2, sort_keys=True))
# except Exception as e:
#     print("Failed to get algod status: {}".format(e))

def test_send_algo_txn(private_key, sender, receiver, amount):

    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = ""
    headers = {
        # "X-API-Key": "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab",
        "X-API-Key": "bWGapCpvM04fLKChEQ0fW1GZk3dCyznj9Ks3r7ud"
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers)

    try:
        status = algod_client.status()
        print("Status: " + json.dumps(status, indent=2, sort_keys=True))
    except Exception as e:
        print("Failed to get algod status: {}".format(e))

    # print("My address: {}".format(sender))
    account_info = algod_client.account_info(sender)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000
    note = "Hello World".encode()
    amountInMicroAlgo = int(amount * 1000000)
    unsigned_txn = PaymentTxn(sender, params, receiver, amountInMicroAlgo, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    account_info = algod_client.account_info(sender)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print('Waiting for confirmation')
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print('Transaction confirmed in round', txinfo.get('confirmed-round'))
    return txinfo


# private_key = 'uXtnKHY74recz4Y1HIiYI51bgCMIqT0JZufw9Q/eoA33fntH01+J2s5XhUZn1pychnewrXuni6rxjjUQu4SWVQ=='
# sender = '657HWR6TL6E5VTSXQVDGPVU4TSDHPMFNPOTYXKXRRY2RBO4ESZK467J7MI'
# receiver = 'IXY7TNLQ75CBIB3UKLHK5GQBLITR5FFWD3MYJOOCXAILJ36VM344YVQAS4'

# #replace private_key and sender with your private key and your address
# test_send_algo_txn(private_key, sender, receiver)
