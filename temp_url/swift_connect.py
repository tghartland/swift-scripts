import settings
import sys
import swiftclient

def swift_connect():
    """
    Gets and returns a connection to the
    OpenStack host specified in settings.py
    """
    connection = swiftclient.client.Connection(user=settings.username,
                     key=settings.password,
                     tenant_name=settings.tenant_name,
                     auth_version="2.0",
                     authurl=settings.auth_url)
    
    try:
        c = connection.get_auth()
    except swiftclient.exceptions.ClientException, e:
        print("Connection failed.")
        print(e)
        sys.exit()
    return connection

if __name__ == "__main__":
    # test connection
    connection = swift_connect()
    print("Success")
