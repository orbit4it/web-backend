import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import config


async def send(receiver: str, division: str, token: str):
    mail_content = f"""
    <div>Assalammualaikum</div>
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

    sender_address = str(config["EMAIL_ADDRESS"])
    sender_pass = str(config["EMAIL_PASSWORD"])

    message = MIMEMultipart()
    message["From"] = f"Orbit <{sender_address}>"
    message["To"] = receiver
    message["Subject"] = "VERIFIKASI AKUN ORBIT"
    message.attach(MIMEText(mail_content, "html"))

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver, text)
    session.quit()

    print(f"Email sent to {receiver}")
