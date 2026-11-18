import json
import os
import smtplib
import sys
from email.message import EmailMessage

cfg = json.loads(open("config.json").read())
sid = cfg["student_id"]
status = sys.argv[1]
sha = sys.argv[2]
try:
    metrics = open("artifacts/metrics.json").read()
except FileNotFoundError:
    metrics = "metrics not available"

msg = EmailMessage()
msg["Subject"] = f"[{sid}] MIDTERM-{sid} Jenkins build {status}"
msg["From"] = os.environ["MAIL_USER"]
msg["To"] = "qasimalik@gmail.com"
msg.set_content(
    f"Student Reg No: {sid}\nBuild status: {status}\nCommit: {sha}\n\nMetrics:\n{metrics}\n"
)
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
    s.login(os.environ["MAIL_USER"], os.environ["MAIL_PASS"])
    s.send_message(msg)
print("mail sent")
