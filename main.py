import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from duckduckgo_search import DDGS

def ieskoti_naujienu():
    ddgs = DDGS()
    query = 'artificial intelligence business trends'
    rezultatai = []
    try:
        results = ddgs.news(keywords=query, region='wt-wt', max_results=5)
        for r in results:
            rezultatai.append({
                'title': r.get('title', ''),
                'link': r.get('url', ''),
                'snippet': r.get('body', '')
            })
    except Exception as e:
        print(f"Naujienų paieškos klaida: {e}")
    return rezultatai

def ieskoti_darbu():
    ddgs = DDGS()
    queries = [
        'site:cvbankas.lt "Palanga" "pusė etato" -valytojas -valytoja -valymas',
        'site:cvonline.lt "Palanga" "pusė etato" -valytojas -valytoja -valymas',
        'site:cvmarket.lt "Palanga" "pusė etato" -valytojas -valytoja -valymas',
        'site:skelbiu.lt/skelbimai/darbas "Palanga" "pusė etato" -valytojas -valytoja -valymas',
        'site:linkedin.com/jobs "Palanga" "part-time" -cleaner'
    ]
    
    rezultatai = []
    matytos_nuorodos = set()
    draudziami_zodziai = ['valytoj', 'valym', 'cleaner', 'tvarkytoj']

    for q in queries:
        try:
            results = ddgs.text(keywords=q, region='lt-lt', max_results=4)
            for r in results:
                link = r.get('href', '')
                title = r.get('title', '')
                body = r.get('body', '')
                
                tekstas_patikrinimui = (title + " " + body).lower()
                ar_yra_draudziamu = any(zodis in tekstas_patikrinimui for zodis in draudziami_zodziai)

                if link and link not in matytos_nuorodos and not ar_yra_draudziamu:
                    matytos_nuorodos.add(link)
                    rezultatai.append({
                        'title': title,
                        'link': link,
                        'snippet': body
                    })
        except Exception as e:
            print(f"Darbo paieškos klaida su užklausa '{q}': {e}")
            
    return rezultatai

def siusti_laiska(naujienos, darbai):
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not email_user or not email_password or not email_to:
        print("Trūksta el. pašto kintamųjų (Secrets).")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Kasdienė ataskaita: AI Verslo tendencijos IR Darbo skelbimai"
    msg['From'] = email_user
    msg['To'] = email_to

    html_body = "<div style='font-family: Arial, sans-serif; max-width: 600px; margin: auto;'>"
    
    # 1 SEKTORIUS: AI VERSLO TENDENCIJOS
    html_body += "<h2 style='color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px;'>🚀 AI ir Verslo tendencijos</h2>"
    if not naujienos:
        html_body += "<p>Šiandien naujų AI verslo naujienų nerasta.</p>"
    else:
        html_body += "<ul style='padding-left: 20px;'>"
        for n in naujienos:
            html_body += f"""
            <li style="margin-bottom: 12px;">
                <a href="{n['link']}" style="font-weight: bold; color: #2980b9; text-decoration: none;">{n['title']}</a><br>
                <span style="color: #555; font-size: 13px;">{n['snippet']}</span>
            </li>
            """
        html_body += "</ul>"

    # 2 SEKTORIUS: DARBO SKELBIMAI PALANGOJE
    html_body += "<h2 style='color: #2c3e50; border-bottom: 2px solid #2ecc71; padding-bottom: 5px; margin-top: 30px;'>💼 Pusės etato darbai Palangoje</h2>"
    if not darbai:
        html_body += "<p>Šiandien naujų pusės etato skelbimų Palangoje nerasta.</p>"
    else:
        html_body += "<ul style='padding-left: 20px;'>"
        for d in darbai:
            html_body += f"""
            <li style="margin-bottom: 12px;">
                <a href="{d['link']}" style="font-weight: bold; color: #27ae60; text-decoration: none;">{d['title']}</a><br>
                <span style="color: #555; font-size: 13px;">{d['snippet']}</span>
            </li>
            """
        html_body += "</ul>"
        
    html_body += "</div>"

    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_password)
            server.sendmail(email_user, email_to, msg.as_string())
        print("Laiškas sėkmingai išsiųstas!")
    except Exception as e:
        print(f"Klaida siunčiant laišką: {e}")

if __name__ == "__main__":
    rasta_naujienu = ieskoti_naujienu()
    rasti_darbai = ieskoti_darbu()
    siusti_laiska(rasta_naujienu, rasti_darbai)
