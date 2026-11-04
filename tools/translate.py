#!/usr/bin/env python3
"""Rewrite the mirrored Otello pages in Brazilian Portuguese and localize links."""
import os
import re

from bs4 import BeautifulSoup, NavigableString

SITE = os.path.expanduser("~/otello/site")

GLOBAL = {
    "+123 45 56 789": "+55 11 4000 0000",
    "+12 (34) 567 89 23": "+55 11 4000 0000",
    "Email us": "Fale com a gente",
    "Search": "Buscar",
    "Hotel": "O Portal",
    "The Hotel": "O Portal",
    "Rooms": "Hospedagens",
    "Stay": "Anuncie",
    "Your Stay": "Anuncie",
    "Hotel Template": "Portal de Hospedagem",
    "Hotel template": "Portal de Hospedagem",
    "Cart": "Carrinho",
    "$ 0.00 USD": "R$ 0,00",
    "Pay with browser.": "Pague pelo navegador.",
    "Continue to Checkout": "Continuar para o pagamento",
    "Your Cart Awaits Items!": "Seu carrinho está vazio.",
    "Product is not available in this quantity.": "Produto indisponível nessa quantidade.",
    "Spa": "Experiências",
    "Blog": "Jornal",
    "Contact": "Contato",
    "Booking": "Reservar",
    "Home": "Início",
    "Packages": "Ofertas",
    "Wellness": "Bem-estar",
    "Gallery": "Galeria",
    "Questions": "Dúvidas",
    "Amenities": "Comodidades",
    "Address": "Endereço",
    "Majestic Manor,": "Av. Atlântica, 1500,",
    "5 Royal Garden Drive,": "Copacabana, Rio de Janeiro,",
    "Highland Hills": "RJ — Brasil",
    "Office hours": "Atendimento",
    "Our front desk is open 24/7 for your convenience.": "Nosso time responde todos os dias, das 8h às 22h.",
    "Follow us": "Siga o Otello",
    "Discover Your Ideal Room": "Descubra a sua hospedagem ideal",
    "Classic Room": "Pousada Maré Alta",
    "Superior Room": "Pousada Serra Azul",
    "Junior Suite": "Hotel Casa Bahia",
    "Executive Suite": "Hotel Vista Ibirapuera",
    "Garden Villa": "Villa Coral",
    "Hillside Villa": "Villa Alto Paraíso",
    "From $150 per night": "A partir de R$ 380 a diária",
    "From $200 per night": "A partir de R$ 480 a diária",
    "From $300 per night": "A partir de R$ 620 a diária",
    "From $400 per night": "A partir de R$ 780 a diária",
    "From $600 per night": "A partir de R$ 1.200 a diária",
    "From $800 per night": "A partir de R$ 1.800 a diária",
    "Close": "Fechar",
    "Price": "Diária",
    "Size": "Tipo",
    "Guests": "Hóspedes",
    "25 sqm / 269 sqft": "Quarto duplo",
    "35 sqm / 377 sqft": "Suíte",
    "45 sqm / 484 sqft": "Suíte",
    "60 sqm / 645 sqft": "Apartamento",
    "90 sqm / 969 sqft": "Villa",
    "120 sqm / 1292 sqft": "Villa",
    "Up to 2 adults": "Até 2 adultos",
    "Up to 3 adults": "Até 3 adultos",
    "Up to 2 adults and 1 child": "Até 2 adultos e 1 criança",
    "Up to 4 adults": "Até 4 adultos",
    "Up to 6 adults": "Até 6 adultos",
    "Elegant design, cozy ambiance, and modern amenities for a perfect stay.":
        "Pousada pé na areia em Paraty, com café da manhã caseiro e vista para a baía.",
    "Spacious elegance, upgraded amenities, and serene views for a superior stay.":
        "Chalé de madeira em Monte Verde, com lareira, hidromassagem e mata ao redor.",
    "Spacious suite with luxury amenities and integrated living area for comfort.":
        "Casarão restaurado no centro histórico de Tiradentes, com piscina e jardim.",
    "Ideal for business or leisure, offering separate living areas and VIP amenities.":
        "Hotel boutique nos Jardins, com varanda, academia e café da manhã até as 11h.",
    "Nestled in lush gardens, offering privacy, luxury, and a tranquil atmosphere.":
        "Casa inteira em Búzios com piscina privativa, cozinha equipada e praia a 300 m.",
    "Elevated luxury with stunning views, private pools, and exclusive amenities.":
        "Villa na serra de Itaipava com piscina aquecida, sauna e vista para o vale.",
    "Our stay at the Otello was nothing short of magical. From the warm welcome at check-in to the breathtaking views from our suite, every detail was perfectly curated to ensure our comfort and satisfaction. The staff went above and beyond, making us feel like royalty.":
        "Encontrei a pousada em Paraty em dois cliques e falei direto com a dona. Chegamos e o quarto estava exatamente como nas fotos, com café quentinho toda manhã.",
    "The Otello has set a new standard for luxury for me. The attention to detail in the design and service is unparalleled. I was particularly impressed by the concierge's knowledge and recommendations for local experiences, making my business trip unexpectedly enjoyable.":
        "Já rodei o Brasil inteiro e é o único guia em que confio para achar pousada boa fora do óbvio. A curadoria acerta sempre e a reserva é direto com a casa.",
    "As a travel blogger, I've stayed in numerous hotels around the world, and the Otello stands out for its exquisite blend of luxury and culture. The staff made me feel welcomed and valued, and the room's comfort was unmatched. The culinary delights offered were a journey through local flavors and international cuisine.":
        "Uso o Otello para montar toda a pauta de viagem. Economizo horas de pesquisa e ainda descubro endereços que não aparecem em nenhum outro lugar.",
    "Sophia and Luca": "Marina e Rafael",
    "Rome, Italy": "São Paulo, SP",
    "Elijah Smith": "Diego Nascimento",
    "New York, USA": "Belo Horizonte, MG",
    "Amira Patel": "Camila Torres",
    "Mumbai, India": "Recife, PE",
    "Store Packages": "Ofertas da semana",
    "Exclusive Offers": "Ofertas exclusivas",
    "All packages": "Ver todas as ofertas",
    "$ 890.00 USD": "R$ 1.290,00",
    "Spa Retreat Ultimate Package": "Fim de semana na serra",
    "Relaxation awaits: spa treatments, wellness access, and gourmet.":
        "Duas noites com café, spa e jantar para dois.",
    "$ 1,490.00 USD": "R$ 1.890,00",
    "Romantic Getaway Package": "Escapada romântica no litoral",
    "Indulge in romance: suite stay, dinner, champagne, and late checkout.":
        "Três noites, espumante na chegada e late checkout.",
    "$ 1,190.00 USD": "R$ 1.590,00",
    "Gourmet Experience Package": "Rota gastronômica",
    "A culinary adventure: tasting menu, cooking class, and wine dinner.":
        "Hospedagem com menu degustação e aula de cozinha local.",
    "Suite Selections:": "Seleções da casa:",
    "Details": "Ver detalhes",
    "Our Featured Reads": "Do nosso jornal",
    "Insights": "Jornal",
    "Awards Season: Celebrating Our Recent Hospitality Accolades":
        "Os 12 destinos brasileiros que bombaram em 2026",
    "Join us in celebrating our recent awards, a testament to our commitment to excellence in hospitality.":
        "Do Jalapão à Serra do Cipó: para onde o Brasil está viajando nesta temporada.",
    "Read now": "Ler agora",
    "Hotel News": "Hospedagem",
    "Elevating Luxury: Our Hotel's Latest Renovations Unveiled":
        "Pousada ou hotel? Como escolher a hospedagem certa",
    "Experience unparalleled luxury with our latest renovations, blending timeless elegance.":
        "Um guia direto para acertar na escolha sem cair em armadilha de foto.",
    "Join Our Community": "Receba a nossa",
    "for Insider Updates": "carta semanal",
    "Exclusive News & Offers": "Novidades do guia",
    "Straight to Your Inbox": "direto no seu e-mail",
    "By clicking this button, you agree to our": "Ao clicar, você concorda com os nossos",
    "Terms of Service": "Termos de uso",
    "Fantastic!": "Pronto!",
    "You are now our subscriber.": "Você está na lista.",
    "Oops! Something went wrong while submitting the form.": "Ops! Algo deu errado. Tente de novo.",
    "Book a Reservation": "Reservar agora",
    "Instructions": "Instruções",
    "Licenses": "Licenças",
    "Changelog": "Novidades",
    "Discover the rich history and unmatched excellence of our esteemed hotel.":
        "Cada endereço é visitado e aprovado pela nossa equipe antes de entrar no guia.",
    "Experience the pinnacle of service and comfort with our dedicated team.":
        "Sem intermediários: você fala direto com a pousada e paga o preço de lá.",
    "Indulge in unparalleled luxury and serene beauty in every corner.":
        "Do litoral à serra, do Pantanal à Chapada — hospedagens que respeitam o lugar onde estão.",
    "Our suites offer unmatched luxury, space, and personalized services.":
        "Hotéis de bairro e boutiques, com estrutura completa para trabalho ou lazer.",
    "Enjoy ultimate privacy and luxury in our exclusive beachfront, garden, and hillside villas.":
        "Imóveis inteiros para famílias e grupos, com cozinha, piscina e espaço de sobra.",
}

PAGE = {
    "index.html": {
        "Unwind in our oasis": "Encontre o seu refúgio",
        "of luxury & serenity": "em cada canto do Brasil",
        "Experience ultimate relaxation in our luxurious haven of peace.":
            "Pousadas, hotéis e villas escolhidos a dedo — do litoral à serra, para reservar direto com quem hospeda.",
        "The hotel's essence": "A essência do Otello",
        "Accommodation": "Hospedagem",
        "Experience Unmatched Comfort & Luxury": "Hospedagens para todos os jeitos de viajar",
        "Escape to a world of sophistication and serene Otello's beauty.":
            "Mais de 2 mil endereços aprovados pela nossa curadoria em 27 estados.",
        "Discover Your Perfect Room With Us": "Pousadas com alma brasileira",
        "Experience Suite Luxury at Its Best": "Hotéis para chegar e descansar",
        "Private Villas for Your Exclusive Retreat": "Villas para ir com todo mundo",
        "Revilatize": "Desperte",
        "Your": "os seus",
        "Senses": "sentidos",
        "Discover Your Ideal Stay": "Escolhas da semana",
        "Choose from a variety of rooms and suites, tailored to every need.":
            "Uma seleção renovada toda semana pela nossa equipe.",
        "Excellence in every": "O Brasil inteiro",
        "moment of your stay": "em uma só curadoria",
        "Book a stay": "Explorar hospedagens",
        "Our Heritage": "Nossa curadoria",
        "Discover the rich history and unmatched excellence of our esteemed hotel.":
            "Cada endereço é visitado e aprovado pela nossa equipe antes de entrar no guia.",
        "Unrivaled Experience": "Reserva direta",
        "Experience the pinnacle of service and comfort with our dedicated team.":
            "Sem intermediários: você fala direto com a pousada e paga o preço de lá.",
        "About": "Sobre",
        "A Sanctuary of Luxury": "Feito para o Brasil",
        "Indulge in unparalleled luxury and serene beauty in every corner.":
            "Do litoral à serra, do Pantanal à Chapada — hospedagens que respeitam o lugar onde estão.",
        "Guests Love Their Stay": "Quem viajou",
        "in the Otello Hotel": "recomenda o Otello",
        "in the Otello": "recomenda o Otello",
        "Suite Selections:": "Seleções da semana:",
        "Sophie Chen": "Helena Prado",
        "Anita Johnson": "Bruno Salles",
    },
    "the-hotel.html": {
        "The hotel": "O portal",
        "A Journey Through": "Um guia feito por",
        "Unparalleled Hotel Excellence": "quem viaja o Brasil inteiro",
        "Our commitment to excellence shines in every moment of your stay.":
            "Um diretório independente de hospedagens — cada endereço passou pela nossa curadoria.",
        "Discover": "Conheça",
        "About": "Sobre",
        "Revel in bespoke services and exquisite comfort during your stay.":
            "Dois mil endereços em 27 estados, todos visitados ou verificados por nós.",
        "Luxurious Otello's rooms that offer the perfect blend of comfort and style.":
            "Uma seleção que privilegia quem hospeda bem, não quem paga mais anúncio.",
        "The Epitome of Luxury": "A nossa promessa",
        "Legacy": "Curadoria",
        "Our Heritage and Excellence": "Como escolhemos cada endereço",
        "Service": "Reserva direta",
        "Unrivaled Experience": "Você fala com a casa",
        "Elegance": "Brasil profundo",
        "A Sanctuary of Luxury": "Hospedagem com identidade",
        "Excellence in every": "O Brasil inteiro",
        "moment of your stay": "em uma só curadoria",
        "Book a stay": "Explorar hospedagens",
        "A Glimpse into Elegance": "Um pouco do que você encontra",
        "Recognized Excellence:": "Na imprensa:",
        "Our Awards & Honors": "onde o Otello apareceu",
        "Guests Love Their Stay": "Quem viajou",
        "in the Otello Hotel": "recomenda o Otello",
        "Hotel's Staff": "Quem faz o Otello",
        "Management": "Curadoria",
        "Elena Petrova": "Helena Prado",
        "Housekeeping Supervisor": "Curadoria de litoral",
        "James Kim": "Tiago Ferraz",
        "Head Chef": "Curadoria de serra",
        "Liam O'Reilly": "André Lobo",
        "Concierge": "Curadoria de interior",
        "Maria Gonzalez": "Marina Costa",
        "Front Desk Receptionist": "Atendimento",
        "Sophie Chen": "Rafael Almeida",
        "General Manager": "Editor-chefe",
        "Anita Johnson": "Camila Torres",
        "Director of Sales and Marketing": "Parcerias",
    },
    "rooms.html": {
        "Dream Stays Await": "Hospedagens para lembrar",
        "Welcome to a place where comfort and": "Do chalé na serra à casa inteira na praia —",
        "elegance are seamlessly intertwined.": "escolha onde dormir sem susto.",
        "Discover": "Explorar",
        "Elegant and Cozy Rooms for Every Guest": "Todas as hospedagens do guia",
        "Luxurious Suites with Exclusive Comfort": "Hotéis com serviço de verdade",
        "Private Luxury Villas for Ultimate Seclusion": "Casas inteiras para ir em grupo",
        "Excellence in every": "O Brasil inteiro",
        "moment of your stay": "em uma só curadoria",
        "Book a stay": "Explorar hospedagens",
        "THe Hotel": "O Portal",
        "Discover Your Home Away From Home": "Sobre o Otello",
        "Harmony": "Curadoria",
        "Where Every Stay": "Onde cada diária",
        "is Unforgettable": "vale a viagem",
        "From the moment you step through our doors, you're enveloped in a world where luxury meets comfort in perfect harmony.":
            "A gente lê cada avaliação, confere cada foto e conversa com o anfitrião antes de publicar qualquer endereço.",
        "Activities": "Destinos",
        "Your Gateway": "O Brasil",
        "to Adventures": "sem roteiro pronto",
        "Nestled in the heart of unparalleled beauty, our hotel serves as the ultimate gateway to exceptional adventures.":
            "Do litoral ao Pantanal: escolha pelo jeito de viajar, não pelo mapa.",
        "About the Hotel": "Sobre o portal",
    },
    "stay-with-us.html": {
        "Accommodations": "Para anfitriões",
        "Discover Your": "Coloque a sua",
        "Perfect Retreat": "hospedagem no mapa",
        "Step into a world where each room is a sanctuary of peace and luxury.":
            "O Otello é visitado por quem procura pousada, chalé e casa inteira — e a sua pode estar aqui.",
        "Discover your stay": "Como funciona",
        "Experience Ultimate Comfort and Style": "Cadastro simples, sem comissão",
        "Revel in the sophistication of our suites, the tranquil beauty of our villas, and the cozy charm of our rooms.":
            "Você envia fotos e informações, a gente revisa em até 5 dias e publica. Nada de taxa por reserva.",
        "Elegant Rooms Designed for Unforgettable Comfort and Style": "Pousadas e chalés",
        "Choose from elegant rooms offering comfort, style, and convenience.":
            "Hospedagens pequenas, com atendimento de família e café da manhã feito na casa.",
        "Spacious, Luxurious Suites for the Ultimate in Comfort and Elegance": "Hotéis independentes",
        "Private Luxury Villas for Ultimate Seclusion": "Villas, casas e fazendas",
        "Indulge in Exclusive Villas with Private Pools and Breathtaking Views":
            "Imóveis inteiros para famílias e grupos, com cozinha, piscina e espaço de sobra.",
        "Excellence in every": "O Brasil inteiro",
        "moment of your stay": "em uma só curadoria",
        "Book a stay": "Quero anunciar",
        "Store Packages": "Planos",
        "Exclusive Offers": "Planos de anúncio",
        "All packages": "Falar com a equipe",
        "$ 890.00 USD": "R$ 0,00",
        "Spa Retreat Ultimate Package": "Plano Essencial",
        "Relaxation awaits: spa treatments, wellness access, and gourmet.":
            "Cadastro, fotos e texto revisados. Sem comissão por reserva.",
        "$ 1,490.00 USD": "R$ 149,00/mês",
        "Romantic Getaway Package": "Plano Destaque",
        "Indulge in romance: suite stay, dinner, champagne, and late checkout.":
            "Posição privilegiada na busca e selo de curadoria.",
        "$ 1,190.00 USD": "R$ 249,00/mês",
        "Gourmet Experience Package": "Plano Vitrine",
        "A culinary adventure: tasting menu, cooking class, and wine dinner.":
            "Página própria, agenda integrada e relatório mensal.",
        "Guests Love Their Stay": "Anfitriões que",
        "in the Otello": "estão no Otello",
        "Frequently Asked Questions": "Perguntas frequentes",
        "Have questions about your upcoming stay?": "Dúvidas sobre anunciar?",
        "We've compiled a comprehensive list of frequently asked questions to help you prepare for your visit.":
            "Reunimos as perguntas que mais chegam para a nossa equipe.",
        "What time is check-in and check-out?": "Como faço para cadastrar minha hospedagem?",
        "Check-in is available from 3:00 PM, and we kindly ask guests to check out by 11:00 AM. Early check-in and late check-out can be arranged subject to availability and may incur additional charges.":
            "É só preencher o formulário abaixo. A gente confere os dados, pede ajustes se precisar e publica em até 5 dias úteis.",
        "Do you offer parking facilities?": "Quanto custa anunciar?",
        "Yes, we offer complimentary on-site parking for all our guests. Valet parking is also available for an additional fee. Our concierge team can provide further details and assist with any special parking needs.":
            "O cadastro é gratuito e não cobramos comissão por reserva. Os planos pagos são opcionais.",
        "Can I bring my pet with me?": "Em quanto tempo meu anúncio entra no ar?",
        "We are delighted to welcome pets at our hotel. We offer pet-friendly rooms and amenities for an additional fee. Please inform us at the time of booking so we can prepare for your furry friend's arrival.":
            "A revisão leva até 5 dias úteis. Você recebe um e-mail a cada etapa, do recebimento à publicação.",
    },
}

CLASS_RULES = [
    (("heading", "is-stay-large-title"), {"Rooms": "Pousadas", "Suites": "Hotéis", "Villas": "Villas"}),
    (("heading", "is-room-hero-title"), {"Rooms": "Hospedagens"}),
    (("medium-uppercase-title",), {"Rooms": "Hospedagens", "Suites": "Hotéis", "Villas": "Villas"}),
    (("small-uppercase-title",), {"Rooms": "Hospedagens", "Suites": "Hotéis", "Villas": "Villas"}),
    (("stay-description-text",), {"Rooms": "Pousadas", "Suites": "Hotéis", "Villas": "Villas"}),
]

LINK_MAP = {
    "/": "index.html",
    "/the-hotel": "the-hotel.html",
    "/rooms": "rooms.html",
    "/stay-with-us": "stay-with-us.html",
    "/wellness-spa": "index.html",
    "/blog": "index.html",
    "/contact": "stay-with-us.html",
    "/book-a-stay": "rooms.html",
    "/store": "index.html",
    "/gallery": "index.html",
    "/faq": "stay-with-us.html",
    "/amenities": "index.html",
    "/checkout": "#",
    "/utility-pages/instructions": "#",
    "/utility-pages/licenses": "#",
    "/utility-pages/changelog": "#",
}

TITLES = {
    "index.html": ("Otello — Hospedagem no Brasil",
                   "O maior diretório de hospedagem do Brasil: pousadas, hotéis e villas "
                   "escolhidos a dedo, com reserva direto com quem hospeda."),
    "the-hotel.html": ("O Portal | Otello — Hospedagem no Brasil",
                       "Conheça o Otello: um diretório independente de hospedagens, feito por "
                       "quem viaja o Brasil inteiro e confere cada endereço de perto."),
    "rooms.html": ("Hospedagens | Otello — Hospedagem no Brasil",
                   "Pousadas, hotéis e casas inteiras em todo o Brasil. Filtre por destino, "
                   "veja diárias e fale direto com o anfitrião."),
    "stay-with-us.html": ("Anuncie | Otello — Hospedagem no Brasil",
                          "Coloque a sua pousada, hotel ou villa no maior diretório de "
                          "hospedagem do Brasil. Cadastro gratuito e sem comissão por reserva."),
}


def norm(text):
    return " ".join(text.split())


def apply_map(soup, mapping):
    for s in list(soup.find_all(string=True)):
        if not isinstance(s, NavigableString) or s.parent.name in ("script", "style"):
            continue
        raw = str(s)
        key = norm(raw)
        if key in mapping:
            lead = raw[: len(raw) - len(raw.lstrip())]
            trail = raw[len(raw.rstrip()):]
            s.replace_with(NavigableString(lead + mapping[key] + trail))


def apply_class_rules(soup):
    for classes, mapping in CLASS_RULES:
        for el in soup.find_all(class_=classes):
            for s in list(el.find_all(string=True)):
                key = norm(str(s))
                if key in mapping:
                    s.replace_with(NavigableString(mapping[key]))


def localize_links(soup):
    for a in soup.find_all("a", href=True):
        href = a["href"]
        path = href.split("#")[0].split("?")[0]
        if path in LINK_MAP:
            frag = ("#" + href.split("#", 1)[1]) if "#" in href else ""
            a["href"] = LINK_MAP[path] + frag
        elif path.startswith("/room/"):
            a["href"] = "rooms.html"
        elif path.startswith("/blog-post/"):
            a["href"] = "index.html"


def set_meta(soup, title, desc):
    if soup.title:
        soup.title.string = title
    for prop in ("og:title", "twitter:title"):
        tag = soup.find("meta", attrs={"property": prop}) or soup.find("meta", attrs={"name": prop})
        if tag:
            tag["content"] = title
    for prop in ("description", "og:description", "twitter:description"):
        tag = soup.find("meta", attrs={"name": prop}) or soup.find("meta", attrs={"property": prop})
        if tag:
            tag["content"] = desc
    for prop in ("og:url",):
        tag = soup.find("meta", attrs={"property": prop})
        if tag:
            tag["content"] = "https://otello.lle.sh/"


def main():
    for filename, overrides in PAGE.items():
        path = os.path.join(SITE, filename)
        soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
        apply_class_rules(soup)
        apply_map(soup, overrides)
        apply_map(soup, GLOBAL)
        localize_links(soup)
        title, desc = TITLES[filename]
        set_meta(soup, title, desc)
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print("ok", filename)


if __name__ == "__main__":
    main()
