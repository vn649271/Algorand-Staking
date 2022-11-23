from flask import Flask, request
from flask_restful import Resource, Api
from main_module import *
global algod_client, creator_private_key, app_id

app = Flask(__name__)
api = Api(app)

stake = {}

algod_client, app_id, creator_private_key = main_func()

def create_stake(stakeholder_address, stakeholder_mnemonic, amount):
    print("--------------------------------------------")
    amountInMicroAlgo = int(float(amount) * 1000000)
    stakedAmount = call_app(algod_client, creator_private_key, stakeholder_address, stakeholder_mnemonic, amountInMicroAlgo, app_id)
    return stakedAmount / 1000000

class Stake(Resource):
    def get(self, address):
        return {address: stake[address]}

    def post(self, address):
        params = request.form
        print(params)

        staked_amount = create_stake(
            address,
            params['mnemonic'], 
            float(params['amount'])
        )
        stake['address'] = address
        stake['amount'] = staked_amount

        return {'stake': stake}

api.add_resource(Stake, '/stake/<string:address>')


