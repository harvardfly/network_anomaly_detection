from raven import Client

dsn = ""
client = Client(dsn)

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()
