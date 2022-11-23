#--------- compile & send transaction using Goal and Python SDK ----------

import base64

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from pyteal import *
from staking_contract import *

# user declared account mnemonics
creator_mnemonic = "orphan ripple decrease all tourist feel require behind excess hazard horn congress clever park river clog basket task broken deliver leopard ready soccer able lunch"
# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = ""
HEADERS = {
    "X-API-Key": "bWGapCpvM04fLKChEQ0fW1GZk3dCyznj9Ks3r7ud"
}

# helper function to compile program source
def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key

# helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

# helper function that formats global state for printing
def format_state(state):
    print("format_state(state): state: ", state)
    formatted = {}
    for item in state:
        key = item['key']
        value = item['value']
        if len(key) < 44:
            formatted_key = base64.b64decode(key).decode('utf-8')
        else:
            formatted_key = key
        if value['type'] == 1:
            # byte string
            if formatted_key == 'voted':
                formatted_value = base64.b64decode(value['bytes']).decode('utf-8')
            else:
                formatted_value = value['bytes']
            formatted[formatted_key] = formatted_value
        else:
            # integer
            formatted[formatted_key] = value['uint']
    return formatted

# helper function to read app global state
def read_global_state(client, addr, app_id):
    results = client.account_info(addr)
    apps_created = results['created-apps']
    for app in apps_created:
        if app['id'] == app_id:
            return format_state(app['params']['global-state'])
    return {}


# create new application
def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):
    # define sender as creator
    sender = account.address_from_private_key(private_key)

    # declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = transaction.ApplicationCreateTxn(sender, params, on_complete, \
                                            approval_program, clear_program, \
                                            global_schema, local_schema)
    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id, 5)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)

    return app_id


# call application
def call_app(client, stakeholder_address, stakeholder_mnemonic, staking_amount, app_id, app_args) : 
    stakeholder_private_key = get_private_key_from_mnemonic(stakeholder_mnemonic)
    print("StakeholderPrivateKey:", stakeholder_private_key)

    app_addr = logic.get_application_address(app_id)
    # declare stakeholder
    stakeholder = account.address_from_private_key(stakeholder_private_key)
    # get node suggested parameters
    params = client.suggested_params()
    print("PaymentTxn: ", stakeholder, stakeholder_address, app_addr, staking_amount)

    # create unsigned transaction
    # create payment transaction
    paymentTxn = transaction.PaymentTxn(
        sender = stakeholder_address,
        receiver = app_addr,
        amt = staking_amount,
        sp = params,
    )
    #transaction.assign_group_id([saveStakingInfoTxn, paymentTxn])
    # sign transaction
    signedPaymentTxn = paymentTxn.sign(stakeholder_private_key)
    # send transaction
    client.send_transactions([signedPaymentTxn])
    # await confirmation
    wait_for_confirmation(client, signedPaymentTxn.get_txid(), 5)

    # app_args.append(staking_amount)
    # ----------------------------------------------------------------------------------------
    #saveStakingInfoTxn = transaction.ApplicationNoOpTxn(stakeholder, params, app_id, app_args)
    # saveStakingInfoTxn = transaction.ApplicationCallTxn(
    #     sender = stakeholder_address,
    #     index = app_id,
    #     on_complete = transaction.OnComplete.NoOpOC,
    #     app_args = app_args,
    #     # must include the previous lead bidder here to the app can refund that bidder's payment
    #     sp = params,
    # )
    # signedSaveStakingInfoTxn = saveStakingInfoTxn.sign(stakeholder_private_key)

    # tx_id = signedSaveStakingInfoTxn.transaction.get_txid()
    # # send transaction
    # client.send_transactions([signedSaveStakingInfoTxn])
    # # await confirmation
    # wait_for_confirmation(client, tx_id, 5)

    return 

def main_func() :
    # initialize an algodClient
    # algod_client = algod.AlgodClient(algod_token, algod_address)
	
    algod_client = algod.AlgodClient(
        ALGOD_TOKEN, #algod_token, 
        ALGOD_ADDRESS, #algod_address, 
        HEADERS# headers={'User-Agent': 'bWGapCpvM04fLKChEQ0fW1GZk3dCyznj9Ks3r7ud'}
    )

    # define private keys
    creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)
    print("Creator private key: ", creator_private_key)

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 2 
    global_bytes = 2
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

    # compile program to TEAL assembly
    with open("./approval.teal", "w") as f:
        approval_program_teal = approval_program()
        f.write(approval_program_teal)


    # compile program to TEAL assembly
    with open("./clear.teal", "w") as f:
        clear_state_program_teal = clear_state_program()
        f.write(clear_state_program_teal)

    # compile program to binary
    approval_program_compiled = compile_program(algod_client, approval_program_teal)

    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("--------------------------------------------")
    print("Deploying Counter application......")

    # create new application
    global app_id
    app_id = create_app(algod_client, creator_private_key, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)

    # read global state of application
    print("Global state:", read_global_state(algod_client, account.address_from_private_key(creator_private_key), app_id))
	
    return algod_client, app_id, creator_private_key

