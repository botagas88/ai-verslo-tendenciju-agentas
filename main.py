"""AI Verslo Tendencijų Agentas – renka naujienas, analizuoja su AI ir siunčia ataskaitą."""

from __future__ import annotations

import os
import re
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from urllib.request import Request, urlopen

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUTPUT_FILE = Path(__file__).resolve().parent / "business_ideas.txt"
USER_AGENT = "AIVersloTendencijuAgentas/1.0 (+https://github.com/botagas88/ai-verslo-tendenciju-agentas)"
NEWS_LIMIT = 12

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.artificialintelligence-news.com/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
]

DDG_QUERIES = [
    "AI business news",
    "artificial intelligence startup funding",
    "AI small business tools",
]


def collect_news(limit: int = NEWS_LIMIT) -> list[dict[str, str]]:
    """Surenka AI / verslo naujienas iš RSS ir DuckDuckGo."""
    items: list[dict[str, str]] = []
    items.extend(_fetch_rss_news())
    items.extend(_fetch_ddg_news())
    return _dedupe_news(items)[:limit]


def _fetch_rss_news() -> list[dict[str, str]]:
    import feedparser

    items: list[dict[str, str]] = []
    for url in RSS_FEEDS:
        try:
            raw = _http_get(url)
            feed = feedparser.parse(raw)
        except Exception as exc:  # noqa: BLE001 – tinklo klaidos neturi nutraukti visos rinkimo
            print(f"RSS nepavyko ({url}): {exc}")
            continue
        for entry in feed.entries[:6]:
            title = _clean_text(getattr(entry, "title", ""))
            link = str(getattr(entry, "link", "")).strip()
            summary = _clean_text(getattr(entry, "summary", "") or getattr(entry, "description", ""))
            if not title:
                continue
            items.append(
                {
                    "title": title,
                    "url": link,
                    "summary": summary[:400],
                    "source": "rss",
                }
            )
    return items


def _fetch_ddg_news() -> list[dict[str, str]]:
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS  # type: ignore[no-redef]

    items: list[dict[str, str]] = []
    try:
        with DDGS() as ddgs:
            for query in DDG_QUERIES:
                try:
                    results = ddgs.news(query, max_results=5)
                except Exception as exc:  # noqa: BLE001
                    print(f"DuckDuckGo paieška nepavyko ({query}): {exc}")
                    continue
                for row in results or []:
                    title = _clean_text(str(row.get("title") or ""))
                    url = str(row.get("url") or row.get("href") or "").strip()
                    body = _clean_text(str(row.get("body") or row.get("excerpt") or ""))
                    if not title:
                        continue
                    items.append(
                        {
                            "title": title,
                            "url": url,
                            "summary": body[:400],
                            "source": "duckduckgo",
                        }
                    )
    except Exception as exc:  # noqa: BLE001
        print(f"DuckDuckGo paieška nepavyko: {exc}")
    return items


def _http_get(url: str, timeout: int = 20) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def _clean_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _dedupe_news(items: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for item in items:
        key = (item.get("url") or item.get("title") or "").lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def analyze_news(news: list[dict[str, str]], generated_at: datetime) -> str:
    """AI iš naujienų paruošia trumpą verslo įžvalgų ataskaitą."""
    headlines = "\n".join(
        f"- {item['title']}\n  {item['summary']}\n  Šaltinis: {item['url']}"
        for item in news
    )
    system = (
        "Tu esi verslo analitikas. Rašyk lietuviškai, trumpai ir konkretiai. "
        "Neduok investavimo ar teisinio patarimo. Remkis tik pateiktomis naujienomis."
    )
    user = f"""Šiandienos data: {generated_at.strftime("%Y-%m-%d")}.

Naujienos:
{headlines}

Paruošk tekstinę ataskaitą su šiomis dalimis:
1) PASTEBĖTOS TENDENCIJOS – 3–5 punktai, kas keičiasi AI ir versle.
2) 3 VERSLO IDĖJOS – kiekvienai: pavadinimas, santrauka, kodėl dabar, pirmas žingsnis.
3) TRUMPA IŠVADA – 2–3 sakiniai, kam tai aktualu smulkiam / vidutiniam verslui.

Nenaudok Markdown žvaigždučių. Rašyk gryną tekstą."""

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    if openai_key:
        return _analyze_openai(system, user, openai_key)
    if anthropic_key:
        return _analyze_anthropic(system, user, anthropic_key)
    raise RuntimeError(
        "Nerastas AI raktas. Nustatykite OPENAI_API_KEY arba ANTHROPIC_API_KEY faile .env"
    )


def _analyze_openai(system: str, user: str, api_key: str) -> str:
    from openai import OpenAI

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("OpenAI grąžino tuščią atsakymą.")
    return content.strip()


def _analyze_anthropic(system: str, user: str, api_key: str) -> str:
    import anthropic

    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5").strip() or "claude-sonnet-4-5"
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=1600,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text_parts = [block.text for block in response.content if getattr(block, "type", "") == "text"]
    content = "\n".join(text_parts).strip()
    if not content:
        raise RuntimeError("Claude grąžino tuščią atsakymą.")
    return content


def build_report(news: list[dict[str, str]], insights: str, generated_at: datetime) -> str:
    lines = [
        "AI VERSLO TENDENCIJŲ AGENTAS",
        "Verslo įžvalgų ataskaita",
        f"Sugeneruota: {generated_at.strftime('%Y-%m-%d %H:%M')}",
        "",
        "Naujienos surinktos iš RSS ir DuckDuckGo. Analizė atlikta su AI.",
        "Idėjos skirtos inspiracijai, ne investavimo ar verslo patarimui.",
        "",
        "=" * 60,
        "ŠALTINIAI",
        "=" * 60,
        "",
    ]
    for index, item in enumerate(news, start=1):
        lines.append(f"{index}. {item['title']}")
        if item.get("url"):
            lines.append(f"   {item['url']}")
        lines.append("")
    lines.extend(
        [
            "=" * 60,
            "AI ĮŽVALGOS",
            "=" * 60,
            "",
            insights.strip(),
            "",
            "Pabaiga.",
            "",
        ]
    )
    return "\n".join(lines)


def send_report_email(report: str) -> bool:
    """Išsiunčia ataskaitą el. paštu, jei sukonfigūruotas SMTP."""
    to_addr = os.getenv("EMAIL_TO", "").strip()
    host = os.getenv("SMTP_HOST", "").strip()
    user = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    from_addr = os.getenv("EMAIL_FROM", "").strip() or user
    if not to_addr or not host or not from_addr:
        print("El. paštas praleistas: trūksta EMAIL_TO, SMTP_HOST arba EMAIL_FROM.")
        return False

    port = int(os.getenv("SMTP_PORT", "587") or "587")
    subject = os.getenv("EMAIL_SUBJECT", "AI verslo tendencijų ataskaita").strip()
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_addr
    message["To"] = to_addr
    message.set_content(report)

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(message)
    print(f"Ataskaita išsiųsta: {to_addr}")
    return True


def main() -> None:
    load_dotenv()
    generated_at = datetime.now()
    print("Renkamos AI verslo naujienos...")
    news = collect_news()
    if not news:
        raise RuntimeError("Nepavyko surinkti naujienų iš RSS ar DuckDuckGo.")

    print(f"Surinkta naujienų: {len(news)}. Analizuojama su AI...")
    insights = analyze_news(news, generated_at)
    report = build_report(news, insights, generated_at)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Ataskaita įrašyta: {OUTPUT_FILE}")
    print(report)

    try:
        send_report_email(report)
    except Exception as exc:  # noqa: BLE001
        print(f"El. pašto siuntimas nepavyko: {exc}")


if __name__ == "__main__":
    main()
