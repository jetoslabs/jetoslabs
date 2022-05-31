
def send_eth(w3_provider, from_address: str, from_key: str, to_address: str, ether: float):
    # get the nonce.  Prevents one from sending the transaction twice
    nonce = w3_provider.eth.getTransactionCount(from_address)

    # creating transaction TODO: move it up the code chain
    value = w3_provider.toWei(ether * 1, 'ether')
    transaction = {
        'to': to_address,
        'value': value,
        'gas': 2000000,
        'nonce': nonce,
        # 'chainId': 5777,
        'gasPrice': w3_provider.toWei('50', 'gwei'),
    }

    # sign the transaction
    signed = w3_provider.eth.account.sign_transaction(transaction, from_key)

    # send transaction
    tx_hash = w3_provider.eth.send_raw_transaction(signed.rawTransaction)

    # return transaction hash
    return w3_provider.toHex(tx_hash)
