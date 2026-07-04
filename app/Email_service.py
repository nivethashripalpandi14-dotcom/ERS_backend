

# from fastapi_mail import FastMail, MessageSchema
# from pydantic import EmailStr
# from sqlalchemy import select

# from app.config import conf 


# async def send_event_registration_email(
#     email: EmailStr,
#     concert_name: str,
#     username: str,
#     concert_date: str,
# ):

#     # Fetch company name
#     company_name =  "Event Registration System"

#     # Subject
# subject = f"{company_name} - Your Concert Ticket"
# body = f"""
# <html>
# <body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:20px;">

# <div style="max-width:600px;margin:auto;background:white;padding:30px;
# border-radius:10px;">

# <h2 style="color:#2c3e50;">
#     Your Concert Ticket 🎫
# </h2>

# <p>Dear <strong>{username}</strong>,</p>

# <p>
# Your payment has been verified and your ticket has been issued successfully.
# </p>

# <hr>

# <h3>Concert Details</h3>

# <p><strong>Concert:</strong> {concert_name}</p>

# <p><strong>Date:</strong> {concert_date}</p>

# <p>
# <strong>Status:</strong>
# <span style="color:green;font-weight:bold;">
# Ticket Sent
# </span>
# </p>

# <hr>

# <p>
# Thank you for booking with <strong>{company_name}</strong>.
# </p>

# <p>
# Enjoy your concert! 🎵
# </p>

# <br>

# <p>
# Regards,<br>
# <strong>{company_name}</strong>
# </p>

# </div>

# </body>
# </html>
# """
from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr

from app.config import conf


async def send_event_registration_email(
    email: EmailStr,
    concert_name: str,
    username: str,
    concert_date: str,
):

    company_name = "Event Registration System"

    subject = f"{company_name} - Your Concert Ticket"

    body = f"""
<html>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:20px;">

<div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:10px;">

<h2 style="color:#2c3e50;">
    Your Concert Ticket 🎫
</h2>

<p>Dear <strong>{username}</strong>,</p>

<p>
Your payment has been verified and your ticket has been issued successfully.
</p>

<hr>

<h3>Concert Details</h3>

<p><strong>Concert:</strong> {concert_name}</p>

<p><strong>Date:</strong> {concert_date}</p>

<p>
<strong>Status:</strong>
<span style="color:green;font-weight:bold;">
Ticket Sent
</span>
</p>

<hr>

<p>
Thank you for booking with <strong>{company_name}</strong>.
</p>

<p>
Enjoy your concert! 🎵
</p>

<br>

<p>
Regards,<br>
<strong>{company_name}</strong>
</p>

</div>

</body>
</html>
"""

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    print(f"Ticket email sent to {email}")