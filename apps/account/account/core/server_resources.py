from common.server_resources.server_resources import ServerResources


def create_server_resources():
    server_resources = ServerResources()
    return server_resources


# Note: Create server here and not in main
# Creating server will cause import cycle issues (as server being used everywhere will import from main file)
server_resources = create_server_resources()
