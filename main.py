import sys
import os
import urllib.request
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def fetch_ai_news():
    """Surenka naujausias AI verslo naujienas iš Google News RSS."""
    url = "https://news.google.com/rss/search?q=artificial+intelligence+business&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')[:5]
        
        news_list = []
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            news_list.append(f"- {title}\n  Nuoroda: {link}")
            
        return news_list
    except Exception as e:
        print(f"Klaida renkant naujienas: {e}")
        return ["- Nepavyko užkrauti naujienų."]

def generate_report(news):
    """Sugeneruoja verslo ataskaitą."""
    content = "=== KASDIENĖ AI VERSLO TENDENCIJŲ ATASKAITA ===\n\n"
    content += "Naujausios rasto AI naujienos ir tendencijos:\n\n"
    content += "\n\n".join(news)
    content += "\n\n--- Ataskaitą automatiškai sugeneravo AI Agentas ---"
    return content

def send_email(subject, body):
    """Išsiunčia ataskaitą el. paštu jei suvesti kintamieji."""
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_email = os.getenv("EMAIL_TO")

    if not sender_email or not sender_password or not recipient_email:
        print("Pastaba: El. pašto parametrai dar nenustatyti. Laiškas nebus siunčiamas.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Ataskaita sėkmingai išsiūsta el. paštu!")
    except Exception as e:
        print(f"Klaida siunčiant el. laišką: {e}")

if __name__ == "__main__":
    print("Agentas pradeda darbą...")
    news = fetch_ai_news()
    report = generate_report(news)
    
    # Išsaugome į failą
    with open("business_ideas.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + report + "\n")
    
    # Bandome siųsti el. paštu
    send_email("Kasdienė AI Verslo Ataskaita", report)
    print("Darbas sėkmingai baigtas!")