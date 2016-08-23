import urllib2

def copy(connection, from_path, to_path):
    # connection: a swift client object
    # from_path: path to file to copy e.g "container/file.txt"
    # to_path: path to copy to e.g "container/file2.txt"
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    req = urllib2.Request("%s/%s" % (connection.url, from_path))
    req.add_header("X-Auth-Token", connection.token)
    req.get_method = lambda: "COPY"
    req.add_header("Destination", to_path)
    url = opener.open(req)
