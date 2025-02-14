import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF
import datetime
import os

# Configurazione SMTP
SMTP_HOST = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_USERNAME = "marco@mywayconsulting.it"
EMAIL_PASSWORD = "Vav30547"

# Titolo del modulo
st.title("Test di Valutazione Applicazione Principi Strategic Roadmap - Imprenditore Executive")
st.write("Compilare tutti i campi perché riceverai una copia via mail.")

# Inserimento dati utente
st.subheader("Inserisci i tuoi dati")
nome = st.text_input("Nome", key="input_nome")
cognome = st.text_input("Cognome", key="input_cognome")
azienda = st.text_input("Nome Azienda", key="input_azienda")
email = st.text_input("Email", key="input_email")
telefono = st.text_input("Numero di Telefono", key="input_telefono")
ruolo = st.text_input("Ruolo in Azienda", key="input_ruolo")
data_compilazione = datetime.date.today().strftime("%d/%m/%Y")

# Definizione delle sezioni e delle domande
test_structure = {
    "Strategia e Gestione": [
        "Ho una visione chiara e scritta di dove voglio portare la mia azienda nei prossimi 5 anni.",
        "La direzione aziendale sa esattamente quali sono gli obiettivi e lavora in sintonia per raggiungerli.",
        "Prendo decisioni basandomi su dati concreti e non solo su sensazioni o urgenze del momento.",
        "Sono in grado di delegare compiti strategici senza dover sempre controllare tutto io.",
        "La mia azienda è in crescita e non dipende esclusivamente dalla mia presenza per funzionare."
    ],
    "Organizzazione e Ruoli": [
        "Ogni collaboratore ha un ruolo chiaro e ben definito con responsabilità precise.",
        "Abbiamo un organigramma strutturato e funzionante che evita sovrapposizioni di compiti. 1 responsabile per funzione.",
        "Non devo costantemente risolvere problemi che i miei collaboratori dovrebbero gestire da soli.",
        "Quando assumo nuove persone, il loro inserimento è rapido ed efficace grazie a un processo chiaro.",
        "Ho un sistema di statistiche e KPI che mi permette di controllare che ogni settore stia lavorando nel modo giusto."
    ],
    "Gestione del Capitale Umano": [
        "Sono stati fatti i colloqui per gli obiettivi personali, professionali e finanziari (PPF) per tutti i dipendenti",
        "Sono stati applicati quindi piani di incentivi e crescita per legare gli obiettivi personali (PPF) a quelli aziendali",
        "Viene misurato il livello del clima aziendale almeno una volta ogni 6 mesi e imposto azioni di miglioramento basandomi sui risultati",
        "I miei responsabili sono capaci di gestire i loro team in modo efficace garantendo sia la produttività sia un ambiente di lavoro positivo"
    ],
    "Vendite e Fidelizzazione": [
        "Abbiamo un sistema chiaro per mantenere il contatto con i clienti esistenti e stimolare acquisti ripetuti.",
        "Il nostro database clienti è aggiornato e segmentato per poter comunicare in modo mirato.",
        "I nostri venditori sanno esattamente come gestire e chiudere una vendita senza sconti inutili.",
        "Invio regolarmente offerte, promozioni o comunicazioni ai clienti per tenerli coinvolti.",
        "Abbiamo in funzione attività di marketing regolari ed efficaci per farci conoscere e acquisire costantemente nuovi clienti."
    ],
    "Controllo Finanziario": [
        "Conosco esattamente i margini di guadagno dei miei prodotti o servizi.",
        "Ricevo report finanziari chiari e aggiornati al,eno 1 volta al mese che mi permettono di capire come sta andando l’azienda.",
        "I crediti e i pagamenti dei clienti vengono gestiti con puntualità senza accumulare problemi di liquidità.",
        "I miei costi sono sempre sotto controllo e so esattamente dove posso ottimizzare.",
        "Il sistema amministrativo dell’azienda e la contabilità mi fornisce dati precisi e affidabili per prendere decisioni."
    ],
    "Efficienza Produttiva": [
        "La mia azienda consegna prodotti o servizi nei tempi stabiliti senza ritardi continui.",
        "I miei processi produttivi sono efficienti e non generano sprechi inutili.",
        "I problemi produttivi vengono risolti con un metodo chiaro e senza rallentare l’attività.",
        "La qualità della produzione è sempre costante e non varia in base alla persona che svolge il lavoro.",
        "Esistono procedure scritte per gestire ogni fase della produzione in modo prevedibile e scalabile."
    ],
    "Qualità del Prodotto e del Servizio": [
        "La mia azienda ha un sistema di controllo qualità per evitare errori e problemi con i clienti.",
        "Raccolgo feedback dai clienti in modo strutturato per migliorare continuamente il prodotto/servizio.",
        "I miei collaboratori ricevono formazione periodica per garantire un alto livello di qualità.",
        "Quando c’è un problema di qualità, abbiamo una procedura chiara per risolverlo rapidamente.",
        "Investiamo nel miglioramento continuo per garantire un servizio o prodotto superiore alla concorrenza."
    ],
    "Espansione e Crescita": [
        "Abbiamo un sistema efficace per generare nuovi contatti e trasformarli in clienti paganti.",
        "Il nostro marketing è misurabile e ci permette di capire cosa funziona e cosa no.",
        "Il mio team commerciale sa esattamente come acquisire clienti nuovi senza dipendere dal passaparola.",
        "Monitoriamo le performance di ogni campagna pubblicitaria per ottimizzarle costantemente.",
        "Stiamo crescendo in modo costante e prevedibile, senza sbalzi improvvisi nel fatturato."
    ],
    "Gestione dello Stress": [
        "Riesco a staccare dal lavoro senza sentirmi in colpa o in ansia per quello che succede in azienda.",
        "Non passo la maggior parte del tempo a spegnere incendi invece di lavorare sulla crescita aziendale.",
        "Quando ci sono problemi, riesco a gestirli senza farmi sopraffare dalla tensione.",
        "Ho il pieno controllo della mia agenda e non vivo in uno stato di emergenza continua.",
        "La mia azienda può funzionare anche senza di me per qualche giorno senza che tutto si blocchi."
    ],
    "Principi di Management": [
        "So motivare i miei collaboratori in modo efficace senza dover sempre alzare la voce o rincorrerli.",
        "Ho stabilito regole chiare per come devono comportarsi i miei collaboratori.",
        "Ho riunioni organizzate e produttive con i responsabili dell’azienda.",
        "Il mio team sa cosa fare e non serve ripetere continuamente le stesse istruzioni.",
        "Ho lavorato sulla mia crescita personale come leader per guidare meglio la mia azienda."
    ],
    "Leadership e Self": [
        "Accetto feedback e suggerimenti per migliorare la mia azienda senza mettermi sulla difensiva.",
        "Sono disposto a sperimentare nuovi metodi per migliorare la gestione del business.",
        "Ho un sistema per monitorare le performance aziendali e non mi affido solo alle sensazioni.",
        "Quando ricevo consigli o formazione, li metto subito in pratica senza rimandare.",
        "Sono pronto a fare cambiamenti importanti se questo può portare risultati migliori."
    ]
}


# Dizionario per salvare i punteggi
risposte = {}

# Creazione del modulo interattivo
for sezione, domande in test_structure.items():
    st.subheader(sezione)
    risposte[sezione] = []
    for domanda in domande:
        domanda_senza_punto_interrogativo = domanda.lstrip("?")  # Rimuove il "?" iniziale
        punteggio = st.slider(domanda_senza_punto_interrogativo, 1, 5, 3)
        risposte[sezione].append(punteggio)

# Funzione per generare e salvare il grafico a barre
def genera_grafico_barre(punteggi_totali):
    fig, ax = plt.subplots(figsize=(8, 6))
    labels = list(punteggi_totali.keys())
    values = list(punteggi_totali.values())

    colors = ['red' if v <= 10 else 'orange' if v <= 20 else 'green' for v in values]
    ax.bar(labels, values, color=colors)
    
    ax.set_xticks(range(len(labels)))  # Imposta la posizione dei tick
    ax.set_xticklabels(labels, rotation=90, ha='right', fontsize=10)
    ax.axhline(10, color='red', linestyle='dashed', linewidth=2, label='Zona pericolo (<10)')
    ax.axhline(20, color='orange', linestyle='dashed', linewidth=2, label='Zona attenzione (10-20)')
    
    ax.set_ylabel("Punteggio")
    ax.set_title("Risultati per Area")
    ax.legend()

    grafico_path = "grafico_barre.png"
    fig.savefig(grafico_path, bbox_inches='tight')

    st.pyplot(fig)  # Mostra il grafico nella pagina web
    
    return grafico_path

# Funzione per correggere caratteri non supportati
def safe_text(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

# Funzione per generare il report PDF
def genera_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, safe_text("Report di Valutazione"), ln=True, align='C')
    pdf.ln(10)

    # Calcolo della valutazione complessiva
    punteggio_totale = sum(sum(punteggi) for punteggi in risposte.values())
    max_punteggio = sum(len(punteggi) * 5 for punteggi in risposte.values())
    percentuale_totale = round((punteggio_totale / max_punteggio) * 100, 1)

    # Valutazione complessiva al centro
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 10, safe_text(f"VALUTAZIONE COMPLESSIVA: {percentuale_totale}%"), ln=True, align='C')
    pdf.ln(10)

    # Dati del compilatore
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, safe_text(f"Dati del Compilatore: {nome} {cognome}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Azienda: {azienda}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Email: {email}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Telefono: {telefono}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Ruolo: {ruolo}"), ln=True)
    pdf.cell(0, 10, safe_text(f"Data compilazione: {data_compilazione}"), ln=True)
    pdf.ln(10)

    # Aree critiche con spazi per Piano di Azione
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, safe_text("Aree Critiche"), ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", '', 12)
    for idx, (sezione, domande) in enumerate(test_structure.items(), start=1):
        punteggi_sezione = risposte[sezione]
        punteggio_totale_sezione = sum(punteggi_sezione)
        max_punteggio_sezione = len(punteggi_sezione) * 5
        percentuale_sezione = round((punteggio_totale_sezione / max_punteggio_sezione) * 100, 1)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, safe_text(f"{idx}. {sezione} ({percentuale_sezione}%)"), ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", '', 12)
        for i, domanda in enumerate(domande):
            punteggio = risposte[sezione][i]
            if punteggio < 3:
                pdf.multi_cell(0, 10, safe_text(f" • {domanda}: {punteggio}/5"))
                pdf.ln(3)
                pdf.cell(0, 10, safe_text("Piano di Azione:"), ln=True)
                pdf.cell(0, 10, "________________________________________", ln=True)
                pdf.cell(0, 10, "________________________________________", ln=True)
                pdf.cell(0, 10, "________________________________________", ln=True)
                pdf.ln(10)

    pdf.ln(20)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, safe_text("Tutte le Risposte"), ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    for idx, (sezione, domande) in enumerate(test_structure.items(), start=1):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, safe_text(f"{idx}. {sezione}"), ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", '', 12)
        for i, domanda in enumerate(domande):
            punteggio = risposte[sezione][i]
            checkbox = "[✓]" if punteggio > 3 else "[ ]"
            pdf.multi_cell(0, 10, safe_text(f"• {checkbox} {domanda.lstrip('?')}: {punteggio}/5"))
            pdf.ln(3)

    # Genera il grafico e salva il percorso
    punteggi_totali = {sezione: sum(punteggi) for sezione, punteggi in risposte.items()}
    grafico_path = genera_grafico_barre(punteggi_totali)

    # Aggiunta del grafico a barre nel PDF
    pdf.add_page()
    pdf.image(grafico_path, x=10, y=pdf.get_y(), w=180)

    file_path = "valutazione_report.pdf"
    pdf.output(file_path, "F")
    return file_path

if st.button("Visualizza Report PDF"):
    file_path = genera_report()
    
    with open(file_path, "rb") as file:
        st.download_button(label="Scarica il Report PDF", data=file, file_name="valutazione_report.pdf", mime="application/pdf")

# Funzione per inviare email con allegato

def invia_email(destinatari, allegato, nome, cognome, azienda, email, telefono, ruolo, data_compilazione):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = ", ".join(destinatari)
    msg['Subject'] = "Notifica Test di Valutazione - Imprenditore Executive"
    
    # Corpo dell'email
    body = f"""
    Ciao,
    
    È stato completato un test di valutazione.
    
    Dati del compilatore:
    Nome: {nome} {cognome}
    Azienda: {azienda}
    Email: {email}
    Telefono: {telefono}
    Ruolo: {ruolo}
    Data di compilazione: {data_compilazione}
    
    In allegato il report PDF generato.
    
    Cordiali saluti,
    My Way Consulting
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # Allegato
    attachment = open(allegato, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(allegato)}")
    msg.attach(part)
    attachment.close()
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USERNAME, destinatari, text)
        server.quit()
        st.success("Email inviata con successo!")
    except Exception as e:
        st.error(f"Errore nell'invio dell'email: {str(e)}")

# Dopo la generazione del PDF
if st.button("Genera Report PDF", key="generate_report_pdf"):
    file_path = genera_report()
    
    # Destinatari dell'email
    destinatari = ["info@mywayconsulting.it"]
    if email:
        destinatari.append(email)
    
    # Invio email con allegato
    invia_email(destinatari, file_path, nome, cognome, azienda, email, telefono, ruolo, data_compilazione)
    
    # Fornire il download del PDF
    with open(file_path, "rb") as file:
        st.download_button(label="Scarica il Report PDF", data=file, file_name="valutazione_report.pdf", mime="application/pdf", key="download_report_pdf")
