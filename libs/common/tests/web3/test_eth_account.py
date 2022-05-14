from common.web3.eth_account import sign, verify


def test_sign_and_verify():
    msg = "I♥SF"
    address = "0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E"
    key = b"\xb2\\}\xb3\x1f\xee\xd9\x12''\xbf\t9\xdcv\x9a\x96VK-\xe4\xc4rm\x03[6\xec\xf1\xe5\xb3d"

    s = sign(msg, key)
    # print(f"\n{s}\n")
    v = verify(msg, s)
    # print(f"{v}\n")
    assert v == address
