from common.web3.eth_account import sign_msg, recover


def test_sign_and_recover():
    msg = "I♥SF"
    address = "0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E"
    key = b"\xb2\\}\xb3\x1f\xee\xd9\x12''\xbf\t9\xdcv\x9a\x96VK-\xe4\xc4rm\x03[6\xec\xf1\xe5\xb3d"

    s = sign_msg(msg, key)
    print(f"\n{s}\n")
    v = recover(msg, s, address)
    if v == "":
        raise Exception("recovered address should not be empty")
    # print(f"{v}\n")
