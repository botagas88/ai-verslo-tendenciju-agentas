import os
import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bs4
import requests


def gauti_rss_rezultatus(uzklausa, max_rez = 5):
    encoded_query = urllib.parse.quote(uzklausa)
    url = f'https://news.google.com/rss/search?q={encoded_query}&hl=lt&gl=LT&ceid=LT:lt'
    rezultatai = []
    try:
        response = requests.get(url, timeout=10)
        soup = bs4.BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:max_rez]
        for item in items:
            title = item.title.text if item.title else ''
            link = item.link.text if item.link else ''
            snippet = item.description.text if item.description else ''
            # Išvalome HTML žymes iš aprašymo
            clean_snippet = bs4.BeautifulSoup(snippet, 'html.parser').get_text()
            rezultatai.append(
                {'title': title, 'link': link, 'snippet': clean_snippet}
            )
    except Exception as e:
        print(f'Klaida ieškant RSS ("{uzklausa}"): {e}')
    return rezultatai


def ieskoti_naujienu():
    # Paieška tarptautinėms AI ir verslo naujienoms
    url = 'https://news.google.com/rss/search?q=artificial+intelligence+business&hl=en-US&gl=US&ceid=US:en'
    rezultatai = []
    try:
        response = requests.get(url, timeout=10)
        soup = bs4.BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:5]
        for item in items:
            title = item.title.text if item.title else ''
            link = item.link.text if item.link else ''
            snippet = item.description.text if item.description else ''
            clean_snippet = bs4.BeautifulSoup(snippet, 'html.parser').get_text()
            rezultatai.append(
                {'title': title, 'link': link, 'snippet': clean_snippet}
            )
    except Exception as e:
        print(f'Naujienų paieškos klaida: {e}')
    return rezultatai


def ieskoti_darbu():
    # Tikslios Google RSS užklausos lietuviškiems portalams
    darbo_uzklausos = [
        'site:cvbankas.lt Palanga',
        'site:cv.lt Palanga',
        'site:skelbiu.lt Palanga darbas',
    ]

    rezultatai = []
    matytos_nuorodos = set()
    draudziami = ['valytoj', 'valym', 'tvarkytoj', 'cleaner']

    for u in darbo_uzklausos:
        rasti = gauti_rss_rezultatus(u, max_rez=5)
        for r in rasti:
            title_lower = r['title'].lower()
            snippet_lower = r['snippet'].lower()

            # Tikriname ar nėra valymo darbų
            yra_draudziamas = any(
                z in title_lower or z in snippet_lower for z in draudziami
            )

            if r['link'] not in matytos_nuorodos and not yra_draudziamas:
                matytos_nuorodos.add(r['link'])
                rezultatai.append(r)

    return rezultatai


def siusti_laiska(naujienos, darbai):
    email_user = os.environ.get('EMAIL_USER')
    email_password = os.environ.get('EMAIL_PASSWORD')
    email_to = os.environ.get('EMAIL_TO')

    if not email_user or not email_password or not email_to:
        print('Trūksta el. pašto kintamųjų.')
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Kasdienė ataskaita: Verslo AI naujienos ir Darbai Palangoje'
    msg['From'] = email_user
    msg['To'] = email_to

    html_body = "<div style='font-family: Arial, sans-serif; max-width: 650px; margin: auto;'>"

    # 1. AI VERSLO TENDENCIJOS
    html_body += "<h2 style='color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 5px;'>🚀 AI ir Verslo tendencijos</h2>"
    if not naujienos:
        html_body += '<p>Šiandien naujų AI verslo naujienų nerasta.</p>'
    else:
        html_body += "<ul style='padding-left: 20px;'>"
        for n in naujienos:
            html_body += f"""
            <li style="margin-bottom: 12px;">
                <a href="{n['link']}" style="font-weight: bold; color: #1a73e8; text-decoration: none;">{n['title']}</a><br>
                <span style="color: #555; font-size: 13px;">{n['snippet']}</span>
            </li>
            """
        html_body += '</ul>'

    # 2. DARBO SKELBIMAI PALANGOJE
    html_body += "<h2 style='color: #2e7d32; border-bottom: 2px solid #2e7d32; padding-bottom: 5px; margin-top: 30px;'>💼 Darbo skelbimai Palangoje</h2>"
    if not darbai:
        html_body += (
            '<p>Šiandien naujų skelbimų Palangoje (be valymo darbų) nerasta.</p>'
        )
    else:
        html_body += "<ul style='padding-left: 20px;'>"
        for d in darbai:
            html_body += f"""
            <li style="margin-bottom: 12px;">
                <a href="{d['link']}" style="font-weight: bold; color: #2e7d32; text-decoration: none;">{d['title']}</a><br>
                <span style="color: #555; font-size: 13px;">{d['snippet']}</span>
            </li>
            """
        html_body += '</ul>'

    html_body += '</div>'

    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_user, email_password)
            server.sendmail(email_user, email_to, msg.as_string())
        print('Laiškas sėkmingai išsiųstas!')
    except Exception as e:
        print(f'Klaida siunčiant laišką: {e}')


if __name__ == '__main__':
    rasta_naujienu = ieskoti_naujienu()
    rasti_darbai = ieskoti_darbu()
    siusti_laiska(rasta_naujienu, rasti_darbai)
