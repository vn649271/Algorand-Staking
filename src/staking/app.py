from flask import Flask, request
from flask_restful import Resource, Api
from main_module import *

app = Flask(__name__)
api = Api(app)

appAddress = staking_init(startTimeDelay = 60, stakingPeriod = 3600)


class Stake(Resource):
    def get(self, address):
        stake_info = get_stake_info(address)
        return { 'address': stake_info }

    # Staking
    def post(self, address):
        params = request.form
        print(params)

        ret = start_staking(
            params['signed_txns'], 
        )

        return {'stake': ret}
    
    # Unstaking
    def delete(self, address):
        params = request.form
        print(params)

        ret = cancel_stake(
            params['signed_txns'], 
        )

        return {'unstake': ret}
 

api.add_resource(Stake, '/stake/<string:address>')

class ContractInfo(Resource):
    def get(self):
        return { 'address': appAddress }

api.add_resource(ContractInfo, '/contract')
