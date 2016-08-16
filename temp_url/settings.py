import getpass
import os
import sys

# Auth settings
# Looks for OpenStack credentials in environment
# Defaults to second option if not found in environment

username = os.getenv("OS_USERNAME") or ""
if username == "":
    print("No username specified in settings or user environment")
    sys.exit()
password = os.getenv("OS_PASSWORD") or getpass.getpass("OpenStack password (%s): " % username)
auth_url = os.getenv("OS_AUTH_URL") or ""
tenant_name = os.getenv("OS_TENANT_NAME") or ""

if "OS_USERNAME" in os.environ:
    print("Using account '%s' from environment" % username)

