from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("\n---------------------------------------------------------------------------------------")
    print("address: {}".format(address))
    print("private key: {}".format(private_key))
    print("passphrase: {}".format(mnemonic.from_private_key(private_key)))
generate_algorand_keypair()
