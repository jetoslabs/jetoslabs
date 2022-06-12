import ipfshttpclient


def new_ipfs_client():
    client = ipfshttpclient.connect(timeout=10)
    return client


def close_ipfs_client(client: ipfshttpclient.Client):
    return client.close()


def ipfs_add(client: ipfshttpclient.Client, file_path: str):
    # client = ipfshttpclient.connect()
    # res = client.add("test copy.txt")
    res = client.add(file_path)
    return res


def ipfs_add_bytes(client: ipfshttpclient.Client, data: bytes):
    res = client.add_bytes(data)
    return res


def ipfs_cat(client: ipfshttpclient.Client, content_hash: str):
    # client = ipfshttpclient.connect()
    content = client.cat(content_hash)
    return content
