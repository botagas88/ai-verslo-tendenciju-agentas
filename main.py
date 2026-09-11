import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from duckduckgo_search import DDGS

def ieskoti_darbu():
    ddgs = DDGS()
    
    # Paieškos užklausos, orientuotos į aptarnavimą, pardavimus ir pagalbinius darbus (be valytojų)
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
            results = ddgs.text(keywords=q, region='lt-lt', max_results=5)
            for r in results:
                link = r.get('href', '')
                title = r.get('title', '')
                body = r.get('body', '')
                
                # Papildomas patikrinimas, kad tikrai nepatektų valymo darbai
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
            print(f"Paieškos klaida su užklausa '{q}': {e}")
            
    return rezultatai

def siusti_laiska(darbai):
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not email_user or not email_password or not email_to:
        print("Trūksta el. pašto kintamųjų (Secrets).")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Darbo skelbimai Palangoje (Pusė etato)"
    msg['From'] = email_user
    msg['To'] = email_to

    if not darbai:
        html_body = "<h3>Šiandien naujų pusės etato skelbimų Palangoje (išskyrus valymo darbus) nerasta.</h3>"
    else:
        html_body = "<h2>Naujausi pusės etato darbo skelbimai Palangoje:</h2><ul>"
        for d in darbai:
            html_body += f"""
            <li style="margin-bottom: 15px;">
                <a href="{d['link']}" style="font-weight: bold; font-size: 16px; color: #1a73e8;">{d['title']}</a><br>
                <span style="color: #555;">{d['snippet']}</span>
            </li>
            """
        html_body += "</ul>"

    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_password)
            server.sendmail(email_user, email_to, msg.as_string())
        print("Laiškas sėkmingai išsiųstas!")
    except Exception as e:
        print(f"Klaida siunčiant laišką: {e}")

if __name__ == "__main__":
    rasti_darbai = ieskoti_darbu()
    siusti_laiska(rasti_darbai)
