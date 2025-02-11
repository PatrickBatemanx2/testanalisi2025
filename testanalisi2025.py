import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Titolo del modulo
st.title("Test di Valutazione Applicazione Principi Strategic Roadmap - Imprenditore Executive")
st.write("Rispondi alle domande e ottieni una valutazione del livello di implementazione dei principi e delle strategie applicate nel percorso di consulenza")

# Definizione delle sezioni e delle domande
test_structure = {
    "Strategia e Gestione": [
        "Ho una visione chiara e scritta di dove voglio portare la mia azienda nei prossimi 5 anni.",
        "Il mio team di direzione sa esattamente quali sono gli obiettivi e lavora in sintonia per raggiungerli.",
        "Prendo decisioni basandomi su dati concreti e non solo su sensazioni o urgenze del momento.",
        "Sono in grado di delegare compiti strategici senza dover sempre controllare tutto io.",
        "La mia azienda è in crescita e non dipende esclusivamente dalla mia presenza per funzionare."
    ],
    "Organizzazione e Ruoli": [
        "Ogni collaboratore ha un ruolo chiaro e ben definito con responsabilità precise.",
        "Abbiamo un organigramma strutturato e funzionante che evita sovrapposizioni di compiti.",
        "Non devo costantemente risolvere problemi che i miei collaboratori dovrebbero gestire da soli.",
        "Quando assumo nuove persone, il loro inserimento è rapido ed efficace grazie a un processo chiaro.",
        "Ho un sistema che mi permette di controllare che ogni settore stia lavorando nel modo giusto."
    ],
    "Vendite e Fidelizzazione": [
        "Abbiamo un sistema chiaro per mantenere il contatto con i clienti esistenti e stimolare acquisti ripetuti.",
        "Il nostro database clienti è aggiornato e segmentato per poter comunicare in modo mirato.",
        "I nostri venditori sanno esattamente come gestire e chiudere una vendita senza sconti inutili.",
        "Invio regolarmente offerte, promozioni o comunicazioni ai clienti per tenerli coinvolti.",
        "Monitoriamo costantemente quante vendite derivano da clienti abituali e quante da nuovi clienti."
    ],
    "Controllo Finanziario": [
        "Conosco esattamente i margini di guadagno dei miei prodotti o servizi.",
        "Ricevo report finanziari chiari e aggiornati che mi permettono di capire come sta andando l’azienda.",
        "I crediti e i pagamenti dei clienti vengono gestiti con puntualità senza accumulare problemi di liquidità.",
        "I miei costi sono sempre sotto controllo e so esattamente dove posso ottimizzare.",
        "Il sistema amministrativo dell’azienda mi fornisce dati precisi e affidabili per prendere decisioni."
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
        punteggio = st.slider(domanda, 1, 5, 3)
        risposte[sezione].append(punteggio)

# Calcolo del punteggio per ogni sezione
punteggi_totali = {sezione: sum(punteggi) for sezione, punteggi in risposte.items()}

# Somma totale e analisi dei risultati
punteggio_totale = sum(punteggi_totali.values())
punteggio_percentuale = (punteggio_totale / (len(test_structure) * 25)) * 100

if st.button("Calcola il Risultato"):
    st.subheader("Risultati del Test")
    for sezione, punteggio in punteggi_totali.items():
        st.write(f"**{sezione}:** {punteggio} punti ({(punteggio/25)*100:.1f}%)")
    
    # Analisi del punteggio totale
    st.subheader("Valutazione Generale")
    st.write(f"**Punteggio Totale:** {punteggio_totale} punti ({punteggio_percentuale:.1f}%)")
    
    if punteggio_totale > 160:
        st.success("Ottima gestione! La tua azienda è ben strutturata.")
    elif 120 <= punteggio_totale <= 160:
        st.info("Buona gestione, ma ci sono aree di miglioramento.")
    elif 80 <= punteggio_totale < 120:
        st.warning("Ci sono criticità importanti da risolvere.")
    else:
        st.error("Situazione critica, servono azioni immediate!")
    
    # Creazione del grafico a barre con linee di soglia
    labels = list(punteggi_totali.keys())
    values = list(punteggi_totali.values())
    
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, color='skyblue')
    ax.axhline(10, color='red', linestyle='dashed', label='Soglia critica (10)')
    ax.axhline(15, color='orange', linestyle='dashed', label='Soglia moderata (15)')
    ax.set_ylabel("Punteggio")
    ax.set_title("Confronto delle Sezioni del Test")
    plt.xticks(rotation=45, ha='right')
    ax.legend()
    
    st.pyplot(fig)
