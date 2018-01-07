from channels import Group
from django.http import HttpResponse
from channels.handler import AsgiHandler
# In consumers.py
import json
from channels.sessions import channel_session
from urllib.parse import parse_qs
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

# Connected to websocket.connect
@channel_session
def ws_connect(message, room_name):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Parse the query string
    params = parse_qs(message.content["query_string"])
    if b"username" in params:
        # Set the username in the session
        message.channel_session["username"] = params[b"username"][0].decode("utf8")
        # Add the user to the room_name group
        Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the connection.
        message.reply_channel.send({"close": True})

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("chat-%s" % message.user.username[0]).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    Group("chat-%s" % message.user.username[0]).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)


def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)
