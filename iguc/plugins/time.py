# iguc/plugins/time.py
from datetime import datetime

COMMAND = "time"

def handle(cl, from_user_id, args, context):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cl.direct_send(f"⏰ Current Time: {now}", [from_user_id])
