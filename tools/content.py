# -*- coding: utf-8 -*-
"""Conteúdo do site (PT/EN). Edite aqui e rode `python3 tools/build.py`."""

SRC = "Meus Trabalhos separados por cliente"

WHATSAPP = "5511965746636"
EMAIL = "alanllacerda@gmail.com"
INSTAGRAM = "https://www.instagram.com/lirukkkkk/"
BEHANCE = "https://www.behance.net/alanllacer8389"

SEGMENTS = {
    "saude": {"pt": "Saúde e estética", "en": "Health & aesthetics"},
    "arquitetura": {"pt": "Arquitetura", "en": "Architecture"},
    "musica": {"pt": "Música e eventos", "en": "Music & events"},
    "marca": {"pt": "Marca", "en": "Brand"},
}

NS_CREDIT = {"pt": "Projeto desenvolvido na Next Step Agência", "en": "Project developed at Next Step Agência"}


def seq(folder, names):
    return [f"{folder}/{n}" for n in names]


KITS = [
    ("azul-clinico", "Azul Clínico", "Clinical Blue", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Azul Clínico/Estáticos", [f"Azul Clínico - Estático {i}.png" for i in range(1, 6)])),
    ("azul-claro", "Azul Claro", "Light Blue", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Azul Claro/Carrossel", [f"Azul Claro - Carrossel 1 - {i}.png" for i in range(1, 7)]) + seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Azul Claro/Estáticos", [f"Azul Claro - Estático {i}.png" for i in range(1, 4)])),
    ("rosa", "Rosa", "Pink", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Rosa/Estáticos", [f"Rosa - Estático {i}.png" for i in range(1, 6)])),
    ("rosa-azul", "Rosa e Azul", "Pink & Blue", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Rosa e Azul/Estáticos", [f"Rosa e Azul - Estático {i}.png" for i in range(1, 6)])),
    ("vermelho", "Vermelho", "Red", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Vermelho/Carrossel", [f"Vermelho - Carrossel 1 - {i}.png" for i in range(1, 6)]) + seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Vermelho/Estáticos", [f"Vermelho - Estático {i}.png" for i in range(1, 4)])),
    ("amarelo-azul", "Amarelo e Azul", "Yellow & Blue", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Amarelo e Azul/Carrossel", [f"Amarelo e Azul - Carrossel 1 - {i}.png" for i in range(1, 5)]) + seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Amarelo e Azul/Estáticos", [f"Amarelo e Azul - Estático {i}.png" for i in range(1, 4)])),
    ("amarelo-royal", "Amarelo e Azul Royal", "Yellow & Royal Blue", seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Amarelo e Azul Royal/Carrossel", [f"Amarelo e Azul Royal - Carrossel 1 - {i}.png" for i in range(1, 6)]) + seq("Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Amarelo e Azul Royal/Estáticos", [f"Amarelo e Azul Royal - Estático {i}.png" for i in range(1, 4)])),
]

BL = "Arquiteto Breno Lima"
CASES = [
    {
        "slug": "next-step",
        "client": "Next Step",
        "segment": "marca",
        "featured": True,
        "credit": NS_CREDIT,
        "title": {"pt": "Uma agência que precisava parecer o que vende.", "en": "An agency that needed to look like what it sells."},
        "deliver": {"pt": ["Identidade visual", "Social media", "Motion"], "en": ["Visual identity", "Social media", "Motion"]},
        "intro": {
            "pt": "A Next Step é uma agência de marketing. Trabalhei a identidade da própria agência: o símbolo em degraus, o violeta sobre preto, a tipografia e as aplicações, do documento de marca ao feed. Junto veio um carrossel sobre o que é (e o que não é) rebranding, e vídeos em motion para apresentar o CRM da agência.",
            "en": "Next Step is a marketing agency. I worked on the agency's own identity: the stepped symbol, violet on black, the typography and its applications, from the brand document to the feed. Alongside it came a carousel on what rebranding is (and isn't), and motion videos presenting the agency's CRM.",
        },
        "cover": "Next Step/1.jpg",
        "groups": [
            {"kind": "wide", "label": {"pt": "Documento de marca", "en": "Brand document"}, "items": seq("Next Step", ["1.jpg", "4.jpg", "6504.jpg", "6505.jpg", "6.jpg", "8.jpg", "7.jpg", "2.jpg", "9.jpg", "3.jpg", "5.jpg"])},
            {"kind": "carousel", "label": {"pt": "Carrossel · Isso não é rebranding", "en": "Carousel · This is not rebranding"}, "items": seq("Next Step/Isso Não é Rebranding", ["Slide 01.jpg", "Slide 02.jpg", "Slide 03.jpg", "Slide 4.jpg"])},
            {"kind": "video", "label": {"pt": "Motion", "en": "Motion"}, "items": ["nextstep-crm", "nextstep-logo"]},
        ],
    },
    {
        "slug": "breno-lima",
        "client": "Arquiteto Breno Lima",
        "segment": "arquitetura",
        "featured": True,
        "credit": NS_CREDIT,
        "title": {"pt": "Explicar obra para quem nunca construiu.", "en": "Explaining construction to first-time builders."},
        "deliver": {"pt": ["Social media mensal", "Carrosséis educativos", "Vídeos de eventos"], "en": ["Monthly social media", "Educational carousels", "Event videos"]},
        "intro": {
            "pt": "Breno Lima é arquiteto e trabalha com construção modular e industrializada. O desafio era transformar decisões técnicas (fundação, steel frame, prazo de obra) em conteúdo que qualquer pessoa entende. Criei um sistema de carrosséis em verde-limão e oliva, com croquis à mão e fotos reais, uma agenda dos eventos de arquitetura e design de 2026 e a edição dos vídeos de evento.",
            "en": "Breno Lima is an architect working with modular and industrialized construction. The challenge was turning technical decisions (foundations, steel frame, build time) into content anyone can follow. I built a carousel system in lime and olive, with hand sketches and real photos, a 2026 agenda of architecture and design events, and edited the event videos.",
        },
        "cover": f"{BL}/CARROSSEL - CONSTRUÇÃO MODULAR 01/CARROSSEL - CONSTRUÇÃO MODULAR 01.jpg",
        "groups": [
            {"kind": "carousel", "label": {"pt": "Construção modular", "en": "Modular construction"}, "items": seq(f"{BL}/CARROSSEL - CONSTRUÇÃO MODULAR 01", ["CARROSSEL - CONSTRUÇÃO MODULAR 01.jpg", "CARROSSEL - CONSTRUÇÃO MODULAR 02.jpg", "CARROSSEL - CONSTRUÇÃO MODULAR 03.jpg", "CARROSSEL - CONSTRUÇÃO MODULAR 5.jpg"])},
            {"kind": "carousel", "label": {"pt": "Tradicional ou industrializado", "en": "Traditional or industrialized"}, "items": seq(f"{BL}/Maio - 2026/Carrossel Tradicional ou Industrializado", [f"Carrossel - 1 - {i} Tradicional ou Industrial.png" for i in range(1, 5)])},
            {"kind": "carousel", "label": {"pt": "Fundação", "en": "Foundations"}, "items": seq(f"{BL}/Maio - 2026/Carrossel Fundacao", [f"Carrossel 2 - {i} Fundacao.png" for i in range(1, 5)])},
            {"kind": "carousel", "label": {"pt": "Alvenaria ou steel frame", "en": "Masonry or steel frame"}, "items": seq(f"{BL}/Maio - 2026/Carrossel Alvenaria ou Steel Frame", ["Carrossel 3 - 1 Alvenaria ou Steel Frame.png", "Carrossel 3 - 2 Alvenaria ou Steel Frame.png", "Carrossel 3 - 3 Alvenaria ou Steel Frame.png", "Carrossel 3 - 4Alvenaria ou Steel Frame.png"])},
            {"kind": "carousel", "label": {"pt": "Por onde começa uma construção", "en": "Where a build begins"}, "items": seq(f"{BL}/Maio - 2026/Carrossel Por Onde Comeca", ["Carrossel 4 - 1 Por onde comeca.png", "Carrossel 4 - 3 Por onde comeca.jpg", "Carrossel 4 - 4 Por onde comeca.png"])},
            {"kind": "carousel", "label": {"pt": "Processo simplificado", "en": "Simplified process"}, "items": seq(f"{BL}/Carrossel - Processo Simplificado (1)", ["CARROSSEL - PROCESSO SIMPLIFICADO 01.jpg", "CARROSSEL - PROCESSO SIMPLIFICADO 2.jpg", "CARROSSEL - PROCESSO SIMPLIFICADO 3.jpg", "CARROSSEL - PROCESSO SIMPLIFICADO 4.jpg"])},
            {"kind": "carousel", "label": {"pt": "Agenda 2026 · eventos de arquitetura e design", "en": "2026 agenda · architecture and design events"}, "items": seq(f"{BL}/Carrossel - Calendario ", [f"{i}.jpg" for i in range(1, 13)])},
            {"kind": "video", "label": {"pt": "Vídeos de evento", "en": "Event videos"}, "items": ["breno-evento-1", "breno-evento-2", "breno-evento-3"]},
        ],
    },
    {
        "slug": "brenda-seda",
        "client": "Dra. Brenda Seda",
        "segment": "saude",
        "featured": True,
        "credit": NS_CREDIT,
        "title": {"pt": "Harmonização facial com linguagem de moda.", "en": "Facial aesthetics with a fashion voice."},
        "deliver": {"pt": ["Social media", "Direção de arte"], "en": ["Social media", "Art direction"]},
        "intro": {
            "pt": "Para a Dra. Brenda Seda, o feed precisava vender naturalidade, não exagero. Usei retratos em fundo escuro, tipografia direta e um único rosa de destaque. As frases curtas fazem o trabalho de conversa, e a médica aparece como autoridade, não como anúncio.",
            "en": "For Dr. Brenda Seda, the feed had to sell naturalness, not excess. I used portraits on dark grounds, direct typography and a single pink accent. Short lines carry the conversation, and the doctor appears as an authority, not an ad.",
        },
        "cover": "Dr Brenda/Frame 427321733.png",
        "groups": [
            {"kind": "grid", "label": {"pt": "Feed", "en": "Feed"}, "items": seq("Dr Brenda", ["Frame 427321733.png", "Estático 2.jpg", "Frame 427321734.png", "Estático 1.jpg", "Frame 427321732.png", "Frame 427321735.png"])},
        ],
    },
    {
        "slug": "kits-odonto",
        "client": "Kits para clínicas odontológicas",
        "client_en": "Dental clinic kits",
        "segment": "saude",
        "featured": True,
        "credit": NS_CREDIT,
        "title": {"pt": "A mesma pauta, sete identidades.", "en": "One content plan, seven identities."},
        "deliver": {"pt": ["Sistema de criativos", "Estáticos", "Carrosséis"], "en": ["Creative system", "Statics", "Carousels"]},
        "intro": {
            "pt": "Uma rede de clínicas odontológicas precisava de conteúdo constante sem que todas as unidades parecessem iguais. Organizei os criativos por cor, não por clínica: sete paletas, cada uma com estáticos e carrosséis prontos sobre prótese, implante, gengiva, diabetes e datas do ano. Cada clínica escolhe o kit que combina com a sua marca.",
            "en": "A network of dental clinics needed steady content without every location looking the same. I organized the creatives by color, not by clinic: seven palettes, each with ready statics and carousels on dentures, implants, gums, diabetes and dates of the year. Each clinic picks the kit that fits its brand.",
        },
        "cover": "Criativos Genéricos Para Clinicas Odontologicas/Genéricos - Azul Claro/Carrossel/Azul Claro - Carrossel 1 - 1.png",
        "groups": [
            {"kind": "kit", "slug": k[0], "label": {"pt": k[1], "en": k[2]}, "items": k[3]} for k in KITS
        ],
    },
    {
        "slug": "cop",
        "client": "COP Clínicas Odontológicas",
        "segment": "saude",
        "featured": False,
        "credit": NS_CREDIT,
        "title": {"pt": "Informação clara para o paciente salvar.", "en": "Clear information patients save."},
        "deliver": {"pt": ["Social media", "Estáticos", "Carrosséis"], "en": ["Social media", "Statics", "Carousels"]},
        "intro": {
            "pt": "Peças para as unidades da COP em Francisco Morato, Campo Limpo e Pindamonhangaba: azul royal, respostas objetivas para dúvidas comuns e checklists que o paciente guarda.",
            "en": "Pieces for COP's locations in Francisco Morato, Campo Limpo and Pindamonhangaba: royal blue, direct answers to common questions and checklists patients keep.",
        },
        "cover": "COP Clínicas Odontológicas/Estático 3 - COP Pinda.jpg",
        "groups": [
            {"kind": "grid", "label": {"pt": "Feed", "en": "Feed"}, "items": seq("COP Clínicas Odontológicas", ["Carrossel 1 - 1 Pinda.jpg", "Estático 1 - COP Morato.jpg", "Estático 3 - COP Pinda.jpg", "Estático 2 - COP Campo Limpo.jpg", "Estático 4 - COP Morato.jpg", "Estático 3 - COP Campo Limpo.jpg", "Estático 3 - COP Morato.jpg"])},
        ],
    },
    {
        "slug": "raggaclubberz",
        "client": "Raggaclubberz",
        "segment": "musica",
        "featured": False,
        "credit": None,
        "title": {"pt": "A estética da cena grime e bass.", "en": "The look of the grime and bass scene."},
        "deliver": {"pt": ["Identidade visual", "Flyers", "Artes de evento"], "en": ["Visual identity", "Flyers", "Event artwork"]},
        "intro": {
            "pt": "Raggaclubberz é um selo e coletivo de DJs e MCs da cena grime e bass de São Paulo. Cuido da parte visual: flyers, avisos e artes de festa como Hallowgrime e Cr1a Grime, com a textura e a energia do som.",
            "en": "Raggaclubberz is a São Paulo label and collective of DJs and MCs from the grime and bass scene. I handle the visuals: flyers, notices and party artwork such as Hallowgrime and Cr1a Grime, with the texture and energy of the sound.",
        },
        "cover": "Raggaclubbersz/Hallowgrime/HallowGrime 1.jpg",
        "groups": [
            {"kind": "grid", "label": {"pt": "Flyers e avisos", "en": "Flyers and notices"}, "items": seq("Raggaclubbersz", ["Hallowgrime/HallowGrime 1.jpg", "Cr1a Grime Festa Junina/Frame 6.jpg", "Hallowgrime/HallowGrime Festa Fantasia.jpg", "Hallowgrime/Aviso Feed.jpg"])},
        ],
    },
]

SERVICES = [
    ({"pt": "Social media mensal", "en": "Monthly social media"},
     {"pt": "Feed, stories e carrosséis planejados como um sistema, mês a mês, para a marca ser reconhecida em qualquer post.", "en": "Feed, stories and carousels planned as one system, month after month, so the brand is recognizable in every post."}),
    ({"pt": "Identidade visual", "en": "Visual identity"},
     {"pt": "Logo, paleta, tipografia e as regras que mantêm a marca igual em todo lugar.", "en": "Logo, palette, typography and the rules that keep the brand consistent everywhere."}),
    ({"pt": "Carrosséis e estáticos", "en": "Carousels and statics"},
     {"pt": "Peças avulsas para campanhas, lançamentos e datas do calendário.", "en": "One-off pieces for campaigns, launches and calendar dates."}),
    ({"pt": "Motion e reels", "en": "Motion and reels"},
     {"pt": "Vídeos curtos, motion de produto e edição para o formato vertical.", "en": "Short videos, product motion and editing for vertical formats."}),
    ({"pt": "Flyers e artes de evento", "en": "Flyers and event art"},
     {"pt": "Pôsteres, line-ups e capas para festas, selos e artistas.", "en": "Posters, line-ups and covers for parties, labels and artists."}),
    ({"pt": "Para agências", "en": "For agencies"},
     {"pt": "Design terceirizado (white label) no seu prazo e no padrão do seu cliente.", "en": "White-label design on your deadline, in your client's standard."}),
]

PROCESS = [
    ({"pt": "Briefing com esboço", "en": "Briefing with a sketch"},
     {"pt": "Chego na primeira reunião já com referências e um esboço. A conversa começa concreta.", "en": "I come to the first meeting with references and a sketch, so the talk starts concrete."}),
    ({"pt": "Projeto", "en": "Design"},
     {"pt": "Desenvolvo o sistema visual e as primeiras peças.", "en": "I develop the visual system and the first pieces."}),
    ({"pt": "Proposta visual", "en": "Visual proposal"},
     {"pt": "Apresento a proposta com as peças aplicadas, do jeito que vão aparecer no feed.", "en": "I present the proposal with the pieces applied, as they will appear in the feed."}),
    ({"pt": "Ajustes e entrega", "en": "Adjustments and delivery"},
     {"pt": "Alinhamos os ajustes e entrego os arquivos prontos, em poucos dias úteis.", "en": "We align adjustments and I deliver the final files within a few business days."}),
]

# Planos (da Proposta Comercial). Valores em R$.
SINGLES = [
    ({"pt": "Estático", "en": "Static post"}, None, 80),
    ({"pt": "Carrossel", "en": "Carousel"}, {"pt": "3 a 6 lâminas", "en": "3 to 6 slides"}, 120),
    ({"pt": "Reels", "en": "Reels"}, {"pt": "edição", "en": "editing"}, 150),
    ({"pt": "Pack 5 stories", "en": "Pack of 5 stories"}, None, 120),
    ({"pt": "Identidade visual", "en": "Visual identity"}, None, 600),
]

# entregas por plano: estáticos, carrosséis, reels, stories, identidade (1º mês)
PLANS = [
    {"key": "basico", "name": {"pt": "Básico", "en": "Basic"}, "price": 200, "single": 360, "off": 45,
     "for": {"pt": "Para começar com presença no feed.", "en": "To start building a presence on the feed."},
     "items": {"static": 3, "carousel": 1, "reels": 0, "stories": 0, "identity": False}},
    {"key": "regular", "name": {"pt": "Regular", "en": "Regular"}, "price": 350, "single": 680, "off": 50,
     "for": {"pt": "Presença consistente com baixo investimento.", "en": "Consistent presence on a small budget."},
     "items": {"static": 4, "carousel": 2, "reels": 0, "stories": 5, "identity": False}},
    {"key": "premium", "name": {"pt": "Premium", "en": "Premium"}, "price": 700, "single": 1430, "off": 50,
     "for": {"pt": "Crescimento acelerado e posicionamento de marca.", "en": "Faster growth and brand positioning."},
     "items": {"static": 4, "carousel": 2, "reels": 1, "stories": 5, "identity": True}},
]

# Textos de interface. data-i18n="chave"
T = {
    "nav.work": {"pt": "Trabalhos", "en": "Work"},
    "nav.services": {"pt": "Serviços", "en": "Services"},
    "nav.about": {"pt": "Sobre", "en": "About"},
    "nav.contact": {"pt": "Contato", "en": "Contact"},
    "nav.plans": {"pt": "Planos", "en": "Plans"},
    "plans.title": {"pt": "Planos e valores", "en": "Plans and pricing"},
    "plans.lede": {"pt": "Planos mensais para manter a marca presente e consistente, ou peças avulsas quando você precisar.", "en": "Monthly plans to keep your brand present and consistent, or one-off pieces whenever you need them."},
    "plans.month": {"pt": "/mês", "en": "/month"},
    "plans.single": {"pt": "Valor avulso", "en": "One-off value"},
    "plans.off": {"pt": "de economia", "en": "savings"},
    "plans.cta": {"pt": "Quero este plano", "en": "I want this plan"},
    "plans.compare": {"pt": "Comparativo", "en": "Comparison"},
    "plans.singles": {"pt": "Serviços avulsos", "en": "One-off services"},
    "plans.singles.note": {"pt": "Contratação individual, por demanda.", "en": "Hired individually, on demand."},
    "plans.foot": {"pt": "Identidade visual inclusa no 1º mês do plano Premium. Desconto calculado sobre os valores avulsos.", "en": "Visual identity included in the first month of the Premium plan. Savings calculated on one-off prices."},
    "plans.custom": {"pt": "Precisa de outro escopo, ou é uma agência buscando parceria? Monto um orçamento sob medida.", "en": "Need a different scope, or are you an agency looking for a partner? I'll put together a custom quote."},
    "plans.custom.cta": {"pt": "Pedir orçamento", "en": "Ask for a quote"},
    "plans.see": {"pt": "Ver planos e valores", "en": "See plans and pricing"},
    "pl.static": {"pt": "estáticos", "en": "static posts"},
    "pl.static1": {"pt": "estático", "en": "static post"},
    "pl.carousel": {"pt": "carrosséis", "en": "carousels"},
    "pl.carousel1": {"pt": "carrossel", "en": "carousel"},
    "pl.reels1": {"pt": "reels", "en": "reels"},
    "pl.stories": {"pt": "stories", "en": "stories"},
    "pl.identity": {"pt": "Identidade visual completa", "en": "Full visual identity"},
    "pl.identity.when": {"pt": "no 1º mês", "en": "in month one"},
    "pl.plan": {"pt": "Plano", "en": "Plan"},
    "pl.h.static": {"pt": "Estáticos", "en": "Statics"},
    "pl.h.carousel": {"pt": "Carrosséis", "en": "Carousels"},
    "pl.h.reels": {"pt": "Reels", "en": "Reels"},
    "pl.h.stories": {"pt": "Stories", "en": "Stories"},
    "pl.h.identity": {"pt": "Identidade", "en": "Identity"},
    "pl.h.single": {"pt": "Avulso", "en": "One-off"},
    "pl.h.off": {"pt": "Desconto", "en": "Savings"},
    "pl.h.month": {"pt": "Valor/mês", "en": "Per month"},
    "pl.firstmonth": {"pt": "1º mês", "en": "Month 1"},
    "available": {"pt": "Disponível para novos projetos", "en": "Available for new projects"},
    "role": {"pt": "Social media e branding", "en": "Social media & branding"},
    "tagline": {"pt": "Design para redes sociais e branding com identidade, impacto e consistência visual.", "en": "Social media design and branding with identity, impact and visual consistency."},
    "tagline.short": {"pt": "Do clínico ao urbano, cada marca com a sua cara.", "en": "From clinical to street, every brand with its own face."},
    "cta.whats": {"pt": "Chamar no WhatsApp", "en": "Message on WhatsApp"},
    "cta.brief": {"pt": "Enviar um briefing", "en": "Send a brief"},
    "cta.see": {"pt": "Ver case", "en": "View case"},
    "work.title": {"pt": "Trabalhos selecionados", "en": "Selected work"},
    "archive.title": {"pt": "Arquivo", "en": "Archive"},
    "archive.all": {"pt": "Tudo", "en": "All"},
    "palettes.title": {"pt": "Sete paletas, uma pauta", "en": "Seven palettes, one plan"},
    "palettes.text": {"pt": "Kits de criativos para clínicas odontológicas, organizados por cor. Toque numa paleta para ver as peças.", "en": "Creative kits for dental clinics, organized by color. Tap a palette to see the pieces."},
    "services.title": {"pt": "O que eu faço", "en": "What I do"},
    "services.note": {"pt": "Planos mensais a partir de R$ 200, ou peças avulsas.", "en": "Monthly plans from R$ 200, or one-off pieces."},
    "process.title": {"pt": "Como trabalho", "en": "How I work"},
    "about.title": {"pt": "Sobre", "en": "About"},
    "about.p1": {"pt": "Sou Alan Veloso, designer e ilustrador em São Paulo. Há 7 anos desenho para marcas que precisam aparecer bem nas redes, de clínicas e escritórios de arquitetura a selos de música e festas.", "en": "I'm Alan Veloso, a designer and illustrator in São Paulo. For 7 years I've designed for brands that need to look right on social media, from clinics and architecture studios to music labels and parties."},
    "about.p2": {"pt": "Comecei autodidata e me formei em artes digitais e audiovisual na SAGA. Já atendi 10 clientes, direto ou por agência, e gosto de clientes que chegam sabendo o que querem e deixam espaço para criar.", "en": "I started self-taught and trained in digital art and audiovisual at SAGA. I've worked with 10 clients, directly or through agencies, and I like clients who know what they want and leave room to create."},
    "contact.title": {"pt": "Vamos conversar?", "en": "Let's talk?"},
    "contact.text": {"pt": "Me conta o que você precisa. Respondo de segunda a sexta, das 9h às 22h.", "en": "Tell me what you need. I reply Monday to Friday, 9am to 10pm (BRT)."},
    "form.name": {"pt": "Seu nome", "en": "Your name"},
    "form.company": {"pt": "Empresa ou agência", "en": "Company or agency"},
    "form.service": {"pt": "O que você precisa", "en": "What you need"},
    "form.segment": {"pt": "Segmento", "en": "Industry"},
    "form.deadline": {"pt": "Prazo", "en": "Deadline"},
    "form.refs": {"pt": "Links de referência (opcional)", "en": "Reference links (optional)"},
    "form.msg": {"pt": "Conte um pouco do projeto", "en": "Tell me about the project"},
    "form.send.whats": {"pt": "Enviar pelo WhatsApp", "en": "Send via WhatsApp"},
    "form.send.mail": {"pt": "Enviar por e-mail", "en": "Send via e-mail"},
    "form.required": {"pt": "Preencha seu nome e o que você precisa.", "en": "Fill in your name and what you need."},
    "form.hint": {"pt": "O botão abre o WhatsApp ou seu e-mail com a mensagem pronta. Nada é enviado sem você confirmar.", "en": "The button opens WhatsApp or your e-mail with the message ready. Nothing is sent until you confirm."},
    "opt.choose": {"pt": "Escolha", "en": "Choose"},
    "opt.monthly": {"pt": "Social media mensal", "en": "Monthly social media"},
    "opt.identity": {"pt": "Identidade visual", "en": "Visual identity"},
    "opt.pieces": {"pt": "Peças avulsas", "en": "One-off pieces"},
    "opt.motion": {"pt": "Motion / reels", "en": "Motion / reels"},
    "opt.agency": {"pt": "Parceria com agência", "en": "Agency partnership"},
    "opt.other": {"pt": "Outro", "en": "Other"},
    "case.segment": {"pt": "Segmento", "en": "Industry"},
    "case.deliver": {"pt": "Entregas", "en": "Deliverables"},
    "case.client": {"pt": "Cliente", "en": "Client"},
    "case.next": {"pt": "Próximo case", "en": "Next case"},
    "case.back": {"pt": "Todos os trabalhos", "en": "All work"},
    "case.cta": {"pt": "Quer algo assim para a sua marca?", "en": "Want something like this for your brand?"},
    "theme": {"pt": "Alternar tema claro/escuro", "en": "Toggle light/dark theme"},
    "lang": {"pt": "Mudar idioma", "en": "Change language"},
    "slides": {"pt": "lâminas", "en": "slides"},
    "swipe": {"pt": "arraste", "en": "drag"},
    "prev": {"pt": "Anterior", "en": "Previous"},
    "next": {"pt": "Próxima", "en": "Next"},
    "close": {"pt": "Fechar", "en": "Close"},
    "skip": {"pt": "Pular para o conteúdo", "en": "Skip to content"},
    "footer": {"pt": "Feito com cuidado em São Paulo.", "en": "Made with care in São Paulo."},
    "sound": {"pt": "Ativar som", "en": "Turn sound on"},
}
