#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour récupérer TOUS les devoirs Pronote et envoyer un email.
Version manuelle : envoie TOUS les devoirs (sans tracking).
Avec traductions en anglais et formatage amélioré.
"""

import os, smtplib, io, email.generator
from datetime import datetime, date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from pathlib import Path

try:
from pronotepy import Client
from googletrans import Translator

translator = Translator()

# Identifiants configurés
PRONOTE_URL = "https://2170001x.index-education.net/pronote/eleve.html"
PRONOTE_USERNAME = "ALY"
PRONOTE_PASSWORD = "Pronote2604!"

EMAIL_GMAIL = "Dadaaugalop@gmail.com"
EMAIL_APP_PASSWORD = "xpsu dobo tehp bsre"


def get_homework(client):
    """Récupère TOUS les devoirs des 7 derniers jours et les 30 prochains jours."""
    try:
        homework_list = client.homework(
            date_from=date.today() - timedelta(days=7),
            date_to=date.today() + timedelta(days=30)
        )
        return homework_list
    except Exception as e:
        print(f"Erreur lors de la récupération des devoirs: {e}")
        return []


def format_text_for_email(text):
    """Ajoute des retours à la ligne avant ・ et ★."""
    text = text.replace("・", "<br/>・")
    text = text.replace("★", "<br/>★")
    return text


def translate_text(text, target_lang):
    """Traduit le texte dans la langue cible."""
    try:
        result = translator.translate(text, src_lang='ja', dest_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"Erreur de traduction: {e}")
        return "[Traduction indisponible]"


def format_homework_email(homework_list):
    """Formate TOUS les devoirs avec traductions en anglais."""
    if not homework_list:
        return None
    
    homework_list.sort(key=lambda x: x.date if x.date else date.max)
    
    content = "<h2>Tous les devoirs d'Arthur / すべての宿題 / All Homework</h2>\n<ul>\n"
    
    for hw in homework_list:
        due_date = hw.date.strftime("%d/%m/%Y") if hw.date else "Date non définie"
        
        # Formatage avec retours à la ligne
        formatted_original = format_text_for_email(hw.description)
        
        # Traduction anglaise
        translated_en = translate_text(hw.description, 'en')
        formatted_en = format_text_for_email(translated_en)
        
        content += f"<li><strong>{hw.subject.name}</strong> - <span style=\"font-size: 1.5em;\">À faire pour le {due_date} / 期限: {due_date}</span><br/><br/>"
        content += f"<strong>🇯🇵 日本語 (Original):</strong><br/>{formatted_original}<br/><br/>"
        content += f"<strong>🇬🇧 English:</strong><br/>{formatted_en}<br/><br/>"
        content += f"</li>\n"
    
    content += "</ul>"
    
    return content


def send_email(subject, html_content, gmail_user, app_password):
    """Envoie un email via Gmail."""
    if not app_password:
        print("Erreur: EMAIL_APP_PASSWORD non configuré correctement")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = gmail_user
        msg['To'] = gmail_user
        
        part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part)
        
        buffer = io.BytesIO()
        g = email.generator.BytesGenerator(buffer, mangle_from_=False)
        g.flatten(msg)
        message_bytes = buffer.getvalue()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, app_password)
            server.sendmail(gmail_user, gmail_user, message_bytes)
        
        print(f"Email envoyé avec succès à {gmail_user}")
        return True
    
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False


def main():
    """Fonction principale."""
    try:
        print(f"[{datetime.now()}] Connexion à Pronote...")
        
        client = Client(PRONOTE_URL, PRONOTE_USERNAME, PRONOTE_PASSWORD)
        
        print("Récupération de TOUS les devoirs...")
        homework_list = get_homework(client)
        
        if not homework_list:
            print("Aucun devoir trouvé.")
            return
        
        print(f"Nombre de devoirs trouvés: {len(homework_list)}")
        
        email_content = format_homework_email(homework_list)
        
        if email_content:
            subject = f"Tous les devoirs - {datetime.now().strftime('%d/%m/%Y')} (TOUS) / すべての宿題"
            
            if send_email(subject, email_content, EMAIL_GMAIL, EMAIL_APP_PASSWORD):
                print("Devoirs envoyés avec succès.")
            else:
                print("L'email n'a pas pu être envoyé.")
        else:
            print("Aucun devoir à signaler.")
    
    except Exception as e:
        print(f"Erreur critique: {e}")
        error_msg = f"<p>Erreur lors de la vérification des devoirs Pronote:</p><p>{str(e)}</p>"
        send_email(
            "ERREUR: Vérification devoirs Pronote",
            error_msg,
            EMAIL_GMAIL,
            EMAIL_APP_PASSWORD
        )


if __name__ == "__main__":
    main()
