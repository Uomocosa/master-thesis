from pathlib import Path

from create_slides.DeckBuilding import build_full_deck
from create_slides.Slide import Slide
from create_slides.UnisiBackground import UNISI_CONTENT_SLIDE

REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_PATH = REPO_ROOT / "SLIDES" / "thesis_discussion_deck.pptx"
PAPERS_DIR = REPO_ROOT / "create_slides" / "assets" / "papers"
RESULTS_DIR = REPO_ROOT / "RESULTS"

SLIDES = [
    Slide(
        number=1,
        title="Il Problema, gli Esempi & l'Obiettivo della Tesi",
        visual_bullets=[
            "Acque reflue: farmaci, coloranti e contaminanti difficili da rimuovere",
            "In letteratura: \"spugne molecolari\" con buoni risultati sperimentali",
            "Obiettivo: predire e generare polimeri adsorbenti per via computazionale",
        ],
        images=[PAPERS_DIR / "cryogel_dual_sponge_photo.png"],
        speech=(
            "Partiamo dal problema: le acque reflue contengono molecole inquinanti — farmaci, "
            "coloranti, altri contaminanti — che i trattamenti standard faticano a rimuovere in "
            "modo mirato. In letteratura esistono già esempi di \"spugne molecolari\", polimeri "
            "progettati per adsorbire selettivamente queste molecole, con risultati sperimentali "
            "incoraggianti. Il problema è che ogni nuovo polimero richiede tipicamente sintesi e "
            "test in laboratorio, un processo lento e costoso. L'obiettivo della mia tesi è quindi "
            "predire e generare polimeri — le \"spugne molecolari\" — capaci di adsorbire molecole "
            "inquinanti target dalle acque reflue, ma per via computazionale: invece di scegliere a "
            "mano un polimero e testarlo in laboratorio, ho costruito una pipeline in grado di "
            "proporre e valutare automaticamente polimeri candidati."
        ),
        todos=[
            "Foto acque reflue contaminate ancora da trovare.",
            "Citazione visibile per la spugna dual (Single and dual polymeric sponges, "
            "Eur. Polym. J. 2022).",
        ],
    ),
    Slide(
        number=2,
        title="Due Sistemi Complementari",
        visual_bullets=[
            "Modello Generativo → nuovi candidati polimerici",
            "Modello Predittivo → capacità di adsorbimento stimata",
            "Filtro di dominio a collegarli → un'unica pipeline",
        ],
        speech=(
            "La tesi si basa su due sistemi complementari. Uno è generativo: propone nuovi "
            "candidati polimerici. L'altro è predittivo: dato un polimero e una molecola target, "
            "stima quanto di quella molecola il polimero riesce ad adsorbire. A collegarli c'è un "
            "filtro basato sulla conoscenza di dominio. Questi due sistemi formano una pipeline, "
            "in grado, dato in input una molecola che vogliamo \"catturare\" (ed iperparametri "
            "configurabili), di proporre in output una serie di polimeri che il modello predice "
            "essere dei buoni candidati."
        ),
        todos=["Produrre il diagramma a due riquadri con freccia di confluenza."],
    ),
    Slide(
        number=3,
        title="Raccolta Dati — Costruzione del Dataset PDCC",
        visual_bullets=[
            "PDCC: Polymer, Drug/Molecola, Concentration, Capacity (+ pH)",
            "Dati estratti manualmente da articoli pubblicati",
            "Nessun dataset esistente: base necessaria per tutto il resto",
        ],
        speech=(
            "Il primo lavoro è stato costruire il dataset stesso. Ho estratto dati di adsorbimento "
            "polimero-farmaco da articoli pubblicati per creare quello che chiamo dataset PDCC — "
            "\"Polymer, Drug (più in generale Molecola), Concentration e Capacity\" — a questi è "
            "stato inoltre associato anche il pH. Non esisteva un dataset già pronto per questo "
            "scopo, quindi questo lavoro di raccolta e cura dei dati è stato una base necessaria "
            "per tutto ciò che è venuto dopo."
        ),
        todos=["Inserire un piccolo estratto di tabella PDCC come immagine."],
    ),
    Slide(
        number=4,
        title="Scarsità di Dati — Un Vincolo Strutturale, Non un Fallimento",
        visual_bullets=[
            "\"Pochi studi pubblicati sulla capacità polimero-molecola\"",
            "Vincolo strutturale del settore, non un limite del progetto",
            "La sfida centrale attorno a cui è costruita la metodologia",
        ],
        speech=(
            "Purtroppo, questo campo di ricerca semplicemente non ha molti dati pubblicati. "
            "Pochissimi studi riportano capacità di adsorbimento polimero-molecola in modo "
            "direttamente confrontabile. Questo non è un limite del progetto — è un vincolo "
            "strutturale del settore — ma è la sfida centrale attorno a cui è costruita tutta la "
            "metodologia successiva, e ci tornerò quando parlerò dei risultati del modello "
            "predittivo."
        ),
        todos=["Eventuale grafico a barre: punti dati per coppia polimero-molecola."],
    ),
    Slide(
        number=5,
        title="SMILES e P-SMILES — Le Notazioni di Base",
        visual_bullets=[
            "SMILES: una molecola come stringa di testo (atomi e legami)",
            "P-SMILES: lo stesso per l'unità ripetuta di un polimero",
            "Tutta la pipeline lavora su queste rappresentazioni testuali",
        ],
        speech=(
            "Prima di andare avanti, vale la pena spiegare due notazioni che torneranno in quasi "
            "tutte le slide successive. SMILES è un modo standard per scrivere una molecola come "
            "una semplice stringa di testo, che codifica atomi e legami. P-SMILES fa lo stesso per "
            "i polimeri, rappresentando l'unità ripetuta della catena polimerica. Tutta la parte "
            "generativa e predittiva della mia pipeline lavora proprio su queste due "
            "rappresentazioni testuali."
        ),
        todos=[
            "Generare con rdkit: aspirina + SMILES a sinistra, unità ripetuta + P-SMILES a destra."
        ],
    ),
    Slide(
        number=6,
        title="Pipeline di Featurizzazione",
        visual_bullets=[
            "SMILES / P-SMILES → proprietà fisico-chimiche rilevanti",
            "Da rappresentazione testuale a vettore di feature numeriche",
        ],
        speech=(
            "Per far lavorare i modelli su polimeri e molecole, serve prima trasformarli in "
            "numeri. Questa fase, che chiamo featurizzazione, prende una stringa SMILES o P-SMILES "
            "e ne estrae proprietà fisico-chimiche rilevanti — trasformando di fatto una "
            "rappresentazione testuale in un vettore di feature numeriche che i modelli successivi "
            "possono usare."
        ),
        todos=[
            "Diagramma: SMILES → immagine molecola (rdkit) → vettore di feature.",
            "Verificare se polymetrix genera immagini della struttura polimerica da P-SMILES.",
        ],
    ),
    Slide(
        number=7,
        title="Gestire Dati Sparsi — Interpolazione",
        visual_bullets=[
            "Pochi punti sperimentali, andamento regolare → interpolazione",
            "Aggiunta del punto (0,0): a concentrazione zero, adsorbimento zero",
        ],
        images=[
            PAPERS_DIR / "oxazoline_capacity_indomethacin_oestradiol_ibuprofen.png",
            PAPERS_DIR / "cryogel_cmegl_kinetics_piroxicam.png",
        ],
        speech=(
            "Quando i punti sperimentali erano pochi ma il loro andamento era abbastanza regolare "
            "da poter essere interpolato con fiducia, ho usato l'interpolazione per aumentare i "
            "dati disponibili. Solo dopo aver interpolato ho aggiunto anche il punto (0,0): a "
            "concentrazione zero del polimero, l'adsorbimento è per definizione zero."
        ),
        todos=[
            "Produrre il video Python: curva originale + punti sperimentali + punti interpolati "
            "aggiunti progressivamente.",
        ],
    ),
    Slide(
        number=8,
        title="Modellazione Generativa — Approccio",
        visual_bullets=[
            "Wrapper attorno a mingpt addestrato su token SMILES / P-SMILES",
            "Impara la \"grammatica\" chimica → strutture nuove e valide",
        ],
        speech=(
            "Per la parte generativa, ho addestrato un wrapper attorno a mingpt per generare "
            "stringhe SMILES valide per le molecole, e stringhe P-SMILES per i polimeri. Il "
            "modello impara la \"grammatica\" della notazione chimica notevolmente bene, al punto "
            "da proporre strutture nuove, sintatticamente e chimicamente valide, invece di "
            "limitarsi a memorizzare gli esempi di training."
        ),
        todos=["Diagramma: architettura mingpt, input token SMILES → output stringa generata."],
    ),
    Slide(
        number=9,
        title="Modellazione Generativa — Risultati",
        visual_bullets=[
            "SMILES: 5525 / 12800 nuovi e validi",
            "P-SMILES: 7373 / 12800 nuovi e validi",
            "Decine di migliaia di candidati generabili in poche ore",
        ],
        speech=(
            "Su 12.800 molecole generate, 5.525 stringhe SMILES erano al tempo stesso nuove e "
            "chimicamente valide, mentre per le P-SMILES il numero era 7.373 su 12.800. Considero "
            "questo un risultato molto solido — il modello propone in modo affidabile candidati "
            "polimerici nuovi e validi, che è esattamente ciò che serve nella prima fase della "
            "pipeline, e in poche ore riesce a generare decine di migliaia di nuovi candidati."
        ),
        todos=["Valutare layout \"due numeri grandi affiancati\" invece dei bullet."],
    ),
    Slide(
        number=10,
        title="Modellazione Predittiva — Metodologia (LOOCV)",
        visual_bullets=[
            "Leave-One-Out CV su molte configurazioni di iperparametri",
            "Classificate per Q2 → selezione della configurazione migliore",
            "Modello finale: PSCP — \"PSmileCapacityPredictor\"",
        ],
        speech=(
            "Per la parte predittiva, ho eseguito una leave-one-out cross-validation su un gran "
            "numero di configurazioni di iperparametri, classificandole per punteggio Q2 — un "
            "punteggio che confronta l'errore del modello con l'errore che si avrebbe usando "
            "semplicemente il valore medio come previsione: più si avvicina a 1, più il modello è "
            "informativo rispetto a una previsione banale. Ho selezionato la configurazione con le "
            "prestazioni migliori come modello finale — lo chiamo PSCP, o "
            "\"PSmileCapacityPredictor\"."
        ),
        todos=["Diagramma del ciclo LOOCV → classifica per Q2 → selezione."],
    ),
    Slide(
        number=11,
        title="PSCP — Cosa Predice Davvero",
        visual_bullets=[
            "Input: polimero + molecola + concentrazione + pH",
            "Output: capacità di adsorbimento predetta",
            "Un unico modello per tutte le condizioni sperimentali rilevanti",
        ],
        speech=(
            "Il modello PSCP trovato prende in input un polimero, una molecola target, la "
            "concentrazione e il pH, ne estrae le feature, scala gli input e restituisce in output "
            "una capacità di adsorbimento predetta. È quindi un unico modello che prova a "
            "riflettere tutte le condizioni sperimentali che possano influenzare realmente "
            "l'adsorbimento nella pratica."
        ),
        todos=["Riquadro input/output grafico."],
    ),
    Slide(
        number=12,
        title="Featurizzare i Polimeri — Un Contributo Metodologico",
        visual_bullets=[
            "rdkit non supporta i polimeri, solo le molecole",
            "Soluzione: SMILES del monomero \"tappato\" con idrogeno",
            "Trattato come molecola → logP, SA score estraibili",
        ],
        speech=(
            "Un problema pratico che ho dovuto risolvere: rdkit non supporta nativamente i "
            "polimeri, solo le molecole. La mia soluzione è stata prendere gli SMILES dei "
            "monomeri, \"tapparli\" con idrogeno e trattarli come molecole ordinarie, così da "
            "poter estrarre proprietà come il logP e il synthetic accessibility score."
        ),
        todos=[
            "Decidere se questa slide resta dedicata o va accorpata altrove.",
            "Diagramma: unità ripetuta → SMILES monomero → tappata con H → feature rdkit.",
        ],
    ),
    Slide(
        number=13,
        title="Modellazione Predittiva — Risultati (Q2)",
        visual_bullets=[
            "Migliore configurazione: experiment_hd_16_8_4_4_4",
            "Q2 = 0,984 — MAE = 1,50 — RMSE = 6,49",
            "Proof-of-concept validato sui dati oggi disponibili",
        ],
        speech=(
            "La configurazione migliore ha raggiunto un Q2 di 0,984, con un errore assoluto medio "
            "di circa 1,5 e un RMSE di circa 6,5. Questo risultato è da considerarsi un "
            "\"proof-of-concept\" — dimostra che l'approccio può funzionare, ed è validato sui "
            "dati attualmente disponibili — ma il vero banco di prova della generalizzazione "
            "arriverà con altre misurazioni pubblicate. Ed è esattamente qui che il punto sulla "
            "scarsità di dati, sollevato qualche slide fa, torna a farsi sentire."
        ),
        todos=[
            "Estratto leaderboard da RESULTS/mlp_experiments/q2_leaderboard.md come "
            "immagine/tabella.",
        ],
    ),
    Slide(
        number=14,
        title="Filtraggio dei Polimeri — Criteri della Teoria FMO",
        visual_bullets=[
            "logP alto → il polimero resta solido e insolubile in acqua",
            "TPSA più alto → siti di legame polari",
            "Gap FMO intermolecolare più basso → legame donatore-accettore più forte",
            "SA score più basso → sintetizzabile su scala",
        ],
        speech=(
            "Una volta ottenuti i polimeri candidati, li filtro usando la teoria degli orbitali "
            "molecolari di frontiera. Seleziono un logP alto in modo che il polimero rimanga "
            "solido e insolubile in acqua, un TPSA più alto per i siti di legame polari, un gap "
            "FMO intermolecolare più basso per un legame donatore-accettore più forte, e un SA "
            "score più basso così da essere realisticamente sintetizzabile su scala."
        ),
        todos=["Icone/etichette per i quattro criteri."],
    ),
    Slide(
        number=15,
        title="Un Filtro Modulare, e Volutamente Aggressivo",
        visual_bullets=[
            "10.000+ P-SMILES generati in poche ore",
            "Filtro FMO / logP / TPSA / SA → pochi candidati sopravvivono",
            "Filtro modulare e sostituibile senza toccare il resto",
        ],
        speech=(
            "Come il resto della pipeline, anche questo filtro è modulare: si può sostituire o "
            "affinare senza toccare il resto del sistema. Il filtro attuale è piuttosto severo e "
            "scarta molti dei polimeri generati — ma essendo in grado di generare diecimila nuovi "
            "P-SMILES nell'arco di poche ore, posso permettermi un filtro così \"aggressivo\": "
            "anche scartando la maggior parte dei candidati, restano comunque abbastanza polimeri "
            "promettenti da valutare."
        ),
        todos=["Diagramma a imbuto: generati → filtro → sopravvissuti."],
    ),
    Slide(
        number=16,
        title="Esplorazione Non Supervisionata — Clustering Gerarchico",
        visual_bullets=[
            "Clustering gerarchico agglomerativo sulle coppie polimero-molecola",
            "Silhouette score con picco a 63 cluster → dataset molto eterogeneo",
            "Strumento esplorativo e di interpretabilità, non risultato predittivo",
        ],
        images=[RESULTS_DIR / "ahc_clustering_with_optimal_cluster_count" / "ahc_dendrogram.png"],
        speech=(
            "Ho anche eseguito un clustering gerarchico agglomerativo sul dataset per esplorare "
            "la struttura nelle coppie polimero-molecola. Il silhouette score ha avuto un picco a "
            "63 cluster, il che riflette quanto sia eterogeneo questo dataset — non è di per sé "
            "una segmentazione utile. Lo presento come uno strumento esplorativo e di "
            "interpretabilità, che aiuta a capire cosa guida i raggruppamenti nei dati, non come "
            "un risultato predittivo di rilievo."
        ),
        todos=["Aggiungere curva del silhouette score con picco a 63 cluster (da produrre)."],
    ),
    Slide(
        number=17,
        title="La Pipeline Integrata Completa",
        visual_bullets=[
            "find_polymer_for_target_molecule: molecola target → polimeri candidati",
            "Genera (mingpt) → filtra (FMO/logP/TPSA/SA) → predici (PSCP) → ripeti",
            "Componenti modulari: filtri e modelli sostituibili",
        ],
        images=[
            RESULTS_DIR / "find_polymer_for_target_molecule" / "aspirin" / "plot_conc_aspirin.png"
        ],
        speech=(
            "Tutto questo confluisce in un'unica funzione che chiamo "
            "find_polymer_for_target_molecule. Le si dà una molecola target, lei la converte in "
            "SMILES, genera polimeri candidati, li filtra, ne predice la capacità e ripete il "
            "ciclo — proponendo altri candidati — finché non raggiunge la capacità target. La "
            "maggior parte dei componenti della pipeline è inoltre modulare: possiamo "
            "teoricamente accomodare futuri sviluppi, miglioramenti, diversi filtri e modelli di "
            "generazione e predizione."
        ),
        todos=["Diagramma di flusso completo della pipeline con ciclo."],
    ),
    Slide(
        number=18,
        title="Ampliare i Dati — Il Tool paper_scraper",
        visual_bullets=[
            "OpenAlex (paper open access) → Grobid (estrazione testo) → LLM → PDCC",
            "LLM testati: Gemma, DeepSeek, Kimi, Claude Opus",
        ],
        speech=(
            "Per attaccare il problema della scarsità di dati alla radice, ho costruito un "
            "secondo strumento, che chiamo paper_scraper. Recupera paper ad accesso aperto "
            "tramite OpenAlex, ne estrae altri tramite Grobid, e infine usa un LLM per estrarre "
            "automaticamente le informazioni utili — polimero, molecola, concentrazione, "
            "capacità, pH — direttamente dal testo dei paper. L'ho testato con diversi modelli: "
            "Gemma, DeepSeek, Kimi e Claude Opus."
        ),
        todos=["Diagramma di flusso OpenAlex → Grobid → LLM → PDCC con nomi dei modelli."],
    ),
    Slide(
        number=19,
        title="Prospettive sulla Scarsità di Dati",
        visual_bullets=[
            "Oggi: pochi paper disponibili",
            "Domani: più paper pubblicati + LLM migliori e più economici",
            "→ dataset PDCC più grande, in modo via via più automatico",
        ],
        speech=(
            "Ad oggi mancano ancora paper sufficienti, e questo resta un vincolo reale. Ma "
            "guardando avanti, mi aspetto che nel tempo emergano nuovi paper da cui estrarre "
            "dati, e che i modelli LLM diventino sempre più capaci ed efficienti: questo "
            "strumento è pensato proprio per sfruttare quella crescita ed espandere il dataset "
            "PDCC in modo via via più automatico."
        ),
        todos=["Freccia temporale oggi → domani."],
    ),
    Slide(
        number=20,
        title="Limiti — Dati & Validazione",
        visual_bullets=[
            "Dati: scarsità di misurazioni pubblicate, nessun risultato negativo",
            "Validazione: nessuna conferma in laboratorio, solo computazionale",
        ],
        speech=(
            "Voglio essere diretto sui limiti. Primo, i dati: ci sono troppe poche misurazioni "
            "di capacità pubblicate per addestrare o validare in modo robusto il modello "
            "predittivo, e in particolare mancano dati di risultato negativo — polimeri che non "
            "adsorbono — che affinerebbero sia il filtro sia il modello. Secondo, la validazione: "
            "nulla di generato da questa pipeline è stato testato in laboratorio. Ogni risultato "
            "che ho mostrato è puramente computazionale."
        ),
    ),
    Slide(
        number=21,
        title="Limiti — Ambito & Scelte di Modellazione",
        visual_bullets=[
            "Addestrato su PI1M (sintetico), non sul proprietario PolyInfo",
            "Conversione in P-SMILES ancora manuale e limitata",
            "Solo polimero singolo: nessun composito multi-materiale",
        ],
        speech=(
            "Ci sono anche alcuni limiti di ambito. Il modello generativo è stato addestrato sul "
            "dataset sintetico PI1M, non sul dataset proprietario PolyInfo da cui PI1M deriva, "
            "poiché non avevo accesso a quest'ultimo. Convertire i nomi grezzi dei materiali in "
            "SMILES è semplice grazie a PubChem, ma la conversione in P-SMILES è ancora manuale e "
            "limitata. E l'intera pipeline considera solo materiali a polimero singolo — nessun "
            "composito a doppio polimero o multi-materiale, per ora."
        ),
    ),
    Slide(
        number=22,
        title="Sviluppi Futuri",
        visual_bullets=[
            "Più dati, in particolare risultati negativi (anche via paper_scraper)",
            "Notazioni alternative (BigSmiles) e architetture GNN",
            "Accesso a PolyInfo; input multi-materiale e a doppio polimero",
        ],
        speech=(
            "Guardando avanti, il prossimo passo a maggior valore è semplicemente più dati — in "
            "particolare risultati negativi — che migliorerebbero in modo significativo sia il "
            "filtro sia il modello predittivo. Oltre a questo, vorrei esplorare notazioni "
            "polimeriche alternative come BigSmiles se i dati lo permettono, provare architetture "
            "più complesse come le graph neural network una volta disponibili abbastanza dati da "
            "giustificarle, cercare l'accesso al dataset proprietario PolyInfo, ed estendere la "
            "pipeline a input multi-materiale e a doppio polimero."
        ),
        todos=["Lista in stile roadmap con icone."],
    ),
]


def main() -> None:
    build_full_deck([(slide, UNISI_CONTENT_SLIDE) for slide in SLIDES], OUTPUT_PATH)


if __name__ == "__main__":
    main()
