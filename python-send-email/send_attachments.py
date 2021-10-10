import smtplib
import os
import time
import mimetypes
from pyfiglet import Figlet
from tqdm import tqdm
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

def send_email(text=None, template=None):
    # sender = "your_email"
    sender = "rowi.xyz@gmail.com"
    # your password = "your password"
    password = "k46VONHerZ13k"
    # password = os.getenv("EMAIL_PASSWORD")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        with open(template) as file:
            template = file.read()
    except IOError:
        # return "The template file doesn't found!"
        template = None

    try:
        server.login(sender, password)
        # msg = MIMEText(template, "html")
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = sender
        msg["Subject"] = "С Днем Рождения! Только сегодня скидка по промокоду до 90%!"

        if text: 
            msg.attach(MIMEText(text))

        if template:
            msg.attach(MIMEText(template, "html"))

        print("Прикрепление файлов...")
        for file in tqdm(os.listdir("attachments")):
            time.sleep(0.2)
            filename = os.path.basename(file)
            ftype, encoding = mimetypes.guess_type(file)
            file_type, subtype = ftype.split("/")
            
            if file_type == "text":
                with open(f"attachments/{file}") as f:
                    file = MIMEText(f.read())
            elif file_type == "image":
                with open(f"attachments/{file}", "rb") as f:
                    file = MIMEImage(f.read(), subtype)
            elif file_type == "audio":
                with open(f"attachments/{file}", "rb") as f:
                    file = MIMEAudio(f.read(), subtype)
            elif file_type == "application":
                with open(f"attachments/{file}", "rb") as f:
                    file = MIMEApplication(f.read(), subtype)
            else:
                with open(f"attachments/{file}", "rb") as f:
                    file = MIMEBase(f.read(), subtype)
                    file.set_payload(f.read())
                    encoders.encode_base64(file)

            # with open(f"attachments/{file}", "rb") as f:
            #     file = MIMEBase(f.read(), subtype)
            #     file.set_payload(f.read())
            #     encoders.encode_base64(file)

            file.add_header("content-disposition", "attachment", filename=filename)
            msg.attach(file)

        print("Отправка email...")
        server.sendmail(sender, sender, msg.as_string())

        return "Сообщение успешно отправлено!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


def main():
    font_text = Figlet(font="slant")
    print(font_text.renderText("send email"))
    text = input("Введите ваш текст или нажмите Enter: ")
    template = input("Введите название шаблона или нажмите Enter: ")
    print(send_email(text=text, template=template))


if __name__ == "__main__":
    main()