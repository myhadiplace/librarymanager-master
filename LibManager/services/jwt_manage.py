import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_jwt_token(user_id,valid_time):
    info = {'user_id':user_id, "exp":datetime.utcnow() + timedelta(seconds=valid_time)
            }
    token = jwt.encode(info,'f$920#)flcpam4v23n',algorithm="HS256")
    return token

def decode_jwt_token(token):
    try:
        decoded_token = jwt.decode(token,'f$920#)flcpam4v23n',algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print('jwt error: this token has expired!')
        return None
    except jwt.DecodeError:
        print('jwt error: invalid token!')
        return None


