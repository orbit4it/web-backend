import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config
from helpers.others import get_greeting

async def send_verification(receiver: str, division:str, token: str):
    mail_content = f"""
    <div>Assalammualaikum, {get_greeting()}</div>
    <div>Salam hangat dari ORBIT.</div>
    <br>
    <div>Selamat!</div>
    <div>
    Anda telah diterima sebagai anggota ORBIT di divisi {division}.
    Untuk selanjutnya, silahkan verifikasi akun menggunakan link berikut:
    </div>
    <br>
    <a href="{config['CLIENT_URL']}/register/{token}">Verifikasi sekarang</a>
    <br><br>
    <div>Diharapkan untuk segera melakukan verifikasi akun.</div>
    <br>
    <div>Terima kasih.</div>
    """

    await send(mail_content=mail_content, receiver=receiver, subject="VERIFIKASI AKUN ORBIT")

async def send_group_link(receiver: str, division_name: str, division_link: str):
    mail_content = f"""
        <div>Assalammualaikum, {get_greeting()}</div>
        <div>Salam hangat dari ORBIT.</div>
        <br>

        <div>
            Selamat!
        </div>

        <div>
            Anda telah diterima sebagai anggota ORBIT di Divisi {division_name}.
            Untuk selanjutnya, silahkan join ke grup Whatsapp dengan menggunakan link berikut :
        </div>

        <br>
        <a href="{config['ORBIT_GROUP']}">{config['ORBIT_GROUP']} (Grup ORBIT)</a>
        <br>
        <a href="{division_link}">{division_link} (Grup ORBIT Divisi {division_name})</a>

        <br><br>
        <div>
            Diharapkan untuk segera masuk ke dalam grup Whatsapp,
            dikarenakan akan ada informasi penting seputar ORBIT kedepannya!
        </div>
        <br>

        <div>
            Terimakasih.
        </div>
        <br>

        <div>
            NOTE : Mohon untuk tidak menyebarkan link grup ini ke sembarang orang dan tanpa sepengetahuan kepengurusan ORBIT.
        </div>

    """

    await send(mail_content=mail_content, receiver=receiver, subject="UNDANGAN GRUP ORBIT")



async def send(mail_content:str, receiver: str, subject: str):

    sender_address = str(config["EMAIL_ADDRESS"])
    sender_pass = str(config["EMAIL_PASSWORD"])

    message = MIMEMultipart()
    message["From"] = f"Orbit <{sender_address}>"
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(mail_content, "html"))

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver, text)
    session.quit()

    print(f"Email sent to {receiver}")
