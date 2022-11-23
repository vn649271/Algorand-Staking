from time import time, sleep

from algosdk import account, encoding
from algosdk.logic import get_application_address
from lib.operations import * #createStakeContract, setupStakingApp, placeStake, closeStaking
from lib.util import (
    decodeState,
    getBalances,
    getAppGlobalState,
    getLastBlockTimestamp,
)
from lib.testing.setup import getAlgodClient
from lib.testing.resources import (
    getCreatorAccount,
    getStakeholderAccount,
)

def staking_init(startTimeDelay, stakingPeriod):

    global algodClient
    global startTime, endTime, increment
    global appID

    algodClient = getAlgodClient()

    creator = getCreatorAccount(algodClient)

    startTime = int(time()) + startTimeDelay  # start time is 10 seconds in the future
    endTime = startTime + stakingPeriod  # end time is 30 seconds after start
    increment = 100_000  # 0.1 Algo

    appID = createStakeContract(
        client=algodClient,
        sender=creator,
        startTime=startTime,
        endTime=endTime,
        reserve=0,
        minStakeIncrement=increment,
    )
    
    setupStakingApp(
        client = algodClient,
        appID = appID,
        funder = creator,
    )
    appAddress = get_application_address(appID)
    return appAddress, appID


def start_staking(signed_txns):
    _, lastRoundTime = getLastBlockTimestamp(algodClient)
    if lastRoundTime < startTime + 5:
        print("lastRoundTime: ", lastRoundTime)
        sleep(startTime + 5 - lastRoundTime)
    actualAppBalancesBefore = getBalances(algodClient, get_application_address(appID))
    print("The smart contract now holds the following:", actualAppBalancesBefore)

    return placeStake(
        client = algodClient, 
        appID = appID,
        signedTxns = signed_txns
    )
    
def get_stake_info(stakeholder_address):
    globalState = getAppGlobalState(algodClient, appID)
    for e in globalState:
        if len(e) == 32 and encoding.encode_address(e) == stakeholder_address:
            return { "total": globalState[e] }
    return { "total": 0 }

def cancel_stake(stakeholderMnemonic, amount):
    stakeholder = getStakeholderAccount(algodClient, stakeholderMnemonic)
    unstaking(algodClient, appID, stakeholder, amount)

def close_staking(stakeholder):
    print("Staking closing out....")
    closeStaking(algodClient, appID, stakeholder)

    actualAppBalances = getBalances(algodClient, get_application_address(appID))
    expectedAppBalances = {0: 0}
    print("The smart contract now holds the following:", actualAppBalances)
    assert actualAppBalances == expectedAppBalances

    actualStakederBalances = getBalances(algodClient, stakeholder.getAddress())
    print("Balances after staking for ", stakeholder.getAddress(), ": ", actualStakederBalances, " Algos")
    # seller should receive the stake amount, minus the txn fee

# staking_init(60, 180)
# start_staking(
#     "wool crime limit ethics leave inmate various trouble estate sentence cage parade group oblige jar woman gravity work gadget usage mail weather rely abandon nose",
#     100000
# )