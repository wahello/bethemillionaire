import pymysql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver):
    fr = "support@bethemillionaire.com"
    to = receiver

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Important Notice From BeTheMillionaire"
    msg['From'] = 'support@bethemillionaire.com'
    msg['To'] = "no-reply@bethemillionaire.com"

    html = """\
    <html>
      <head></head>
      <body>
        
        hi,<br>
        
        welcome to BeTheMillionaire.<br>
        
        BeTheMillionaire is update profile section for you.<br>
        
        you can change your profile information, account password, add your affiliate link and change your password.<br>
        
        you can simply login to BeTheMillionaire by following the link:<br>
        
        https://www.bethemillionaire.com/account/login/<br>
        
        then you click "my profile setting" under menu "my account".<br>
        
        or click here after login:
        <br>
        https://www.bethemillionaire.com/account/membership-account/profile/
        <br><br>
        
        
        thanks<br>
        BeTheMillionaire Team<br>       
                  
                
      </body>
    </html>
    """

    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fr, "menaKP00")
    s.sendmail(fr, to, msg.as_string())
    s.quit()




def fetch_db():
    db = pymysql.connect(user="root",passwd="Nstu12345678~!",host="46.101.14.199",db="be_themillionaire")
    cursor = db.cursor()
    cursor.execute("SELECT email from account_userprofile")
    data=cursor.fetchall()
    email_list = []

    for row in data :
        #email_list.append(row[0])
        send_email(row[0])
        print('email sent to : %s' %row[0])
    db.close()


fetch_db()
