#!/usr/bin/env python3
"""Final polish: attributes, footer credits and contact links."""
import glob
import os

from bs4 import BeautifulSoup, NavigableString

SITE = os.path.expanduser("~/otello/site")

ATTRS = {
    "Close cart": "Fechar carrinho",
    "Search": "Buscar",
    "Stay Link Block": "Ver hospedagens",
    "Room Link Block": "Ver hospedagens",
    "Room Detail Link Block": "Ver hospedagem",
    "Otello: Hotel Webflow template illustrative image": "Hospedagem selecionada pelo Otello",
    "Classic Room": "Pousada Maré Alta",
    "Superior Room": "Pousada Serra Azul",
    "Rooms": "Hospedagens",
}

PLACEHOLDERS = {
    "Your Name": "Seu nome",
    "Your email": "Seu e-mail",
    "Subscribe for Newsletter": "Assinar a carta",
}


def main():
    for path in glob.glob(os.path.join(SITE, "*.html")):
        if path.endswith("probe.html"):
            continue
        soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")

        for tag in soup.find_all(True):
            for attr in ("placeholder", "value", "aria-label", "alt", "title"):
                v = tag.get(attr)
                if isinstance(v, str):
                    if v in ATTRS:
                        tag[attr] = ATTRS[v]
                    elif v in PLACEHOLDERS:
                        tag[attr] = PLACEHOLDERS[v]

        for a in soup.find_all("a", href=True):
            if a["href"] in ("/contact",):
                a["href"] = "mailto:oi@otello.com.br"

        for a in soup.find_all("a", class_="subfooter-link"):
            txt = a.get_text(strip=True)
            if txt in ("Instruções", "Licenças", "Novidades"):
                a["href"] = {"Instruções": "#", "Licenças": "#",
                             "Novidades": "mailto:oi@otello.com.br"}[txt]
            if a["href"].startswith(("https://webflow.com", "https://www.metrik.studio")):
                a.decompose()

        for section in soup.select(".subfooter-links"):
            if not section.find("a"):
                section.decompose()

        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print("ok", os.path.basename(path))


if __name__ == "__main__":
    main()
