# Discussion — Speach Slide per Slide

_Una sezione per ogni slide visibile di `Slide_Samuele_Maggiori_v4.pptx`; sotto ogni titolo, il discorso da tenere._

---

### 1. Pipeline End-to-End per la generazione di Polimeri

Buongiorno a tutti, sono Samuele Maggiori e oggi vi presenterò il mio lavoro di tesi: una pipeline per la generazione in silico di polimeri adsorbenti, pensati per rimuovere molecole inquinanti dalle acque reflue.

### 2. Il Problema & l'Obiettivo della Tesi

Partiamo dal problema: le acque reflue contengono molecole inquinanti — farmaci, coloranti, altri contaminanti — che i trattamenti standard faticano a rimuovere in modo mirato. 
In letteratura esistono già esempi di "spugne molecolari".
Ovvero polimeri progettati per adsorbire selettivamente queste molecole, con risultati sperimentali incoraggianti.
Qui vediamo un esmpio di spugna molecolare creata dal gruppo di Zagni e Carroccio in grado di adsorbire due colaranti specifici.
Il problema è che ogni nuovo polimero richiede tipicamente sintesi e test in laboratorio, un processo lento e costoso. 
L'obiettivo della mia tesi è quindi predire e generare polimeri — le "spugne molecolari" — capaci di adsorbire molecole inquinanti target dalle acque reflue, ma per via computazionale.

### 3. Due Sistemi Complementari

La tesi si basa su due sistemi complementari. 
Uno è generativo: propone nuovi candidati polimerici. 
L'altro è predittivo: dato un polimero e una molecola target, stima quanto di quella molecola il polimero riesce ad adsorbire. 
Questi due sistemi formano una pipeline, in grado, dato in input una molecola che vogliamo "catturare", di proporre in output una serie di polimeri che il modello predice essere dei buoni candidati.

### 4. Raccolta Dati — Costruzione del Dataset PDCC

Il primo lavoro è stato costruire il dataset stesso. 
Ho estratto dati di adsorbimento polimero-farmaco da articoli pubblicati per creare quello che chiamo dataset PDCC — "Polymer, Drug (più in generale Molecola), Concentration e Capacity" — a questi è stato inoltre associato anche il pH. 
Non esisteva un dataset già pronto per questo scopo, quindi questo lavoro di raccolta e cura dei dati è stato una base necessaria per tutto ciò che è venuto dopo.


### 6. SMILES e P-SMILES — Le Notazioni di Base

Prima di andare avanti, vale la pena spiegare due notazioni che torneranno in quasi tutte le slide successive. 
SMILES è un modo standard per scrivere una molecola come una semplice stringa di testo, che codifica atomi e legami. 
P-SMILES fa lo stesso per i polimeri, rappresentando l'unità ripetuta della catena polimerica. 
Tutta la parte generativa e predittiva della mia pipeline lavora proprio su queste due rappresentazioni testuali.

### 7. Pipeline per l'estrazione delle feature

Per far lavorare i modelli su polimeri e molecole, serve prima trasformarli in numeri. 
Questa fase, che chiamo featurizzazione, prende una stringa SMILES o P-SMILES e ne estrae proprietà fisico-chimiche rilevanti — trasformando di fatto una rappresentazione testuale in un vettore di feature numeriche che i modelli successivi possono usare.

### 8. Gestire Dati Sparsi — Interpolazione

Quando i punti sperimentali erano pochi ma il loro andamento era abbastanza regolare da poter essere interpolato con fiducia, ho usato l'interpolazione per aumentare i dati disponibili. 
Dopodichè ho aggiunto anche il punto (0,0). 
Ovver a concentrazione zero del polimero, l'adsorbimento è per definizione zero.

### 9. Modellazione Generativa — Approccio

Per la parte generativa, ho addestrato un wrapper attorno a mingpt per generare stringhe P-SMILES, ovvero i polimeri che vorremmo testare. 
Il modello impara la "grammatica" della notazione chimica notevolmente bene, al punto da proporre strutture nuove, sintatticamente e chimicamente valide, invece di limitarsi a memorizzare gli esempi di training.

### 10. Modellazione Generativa — Risultati

Come possiamo vedere oltre la metà dei SMILE e PSMILE generati sono nuovi, e soprattutto validi.
Questo ci permette in poche ore di generare decine di migliaia di nuovi candidati.

### 11. Modellazione Predittiva — Metodologia (LOOCV)

Per la parte predittiva, ho eseguito una leave-one-out cross-validation su un gran numero di configurazioni di iperparametri, classificandole per punteggio Q2 — un punteggio che confronta l'errore del modello con l'errore che si avrebbe usando semplicemente il valore medio come previsione: più si avvicina a 1, più il modello è informativo rispetto a una previsione banale.
Ho selezionato la configurazione con le prestazioni migliori come modello finale — lo chiamo PSCP, o "PSmileCapacityPredictor".

### 12. PSCP — Cosa Predice Davvero

Il modello PSCP trovato prende in input un polimero, una molecola target, la concentrazione e il pH, ne estrae le feature, scala gli input e restituisce in output una capacità di adsorbimento predetta. 

### 14. Modellazione Predittiva — Risultati (Q2)

La configurazione migliore ha raggiunto un Q2 di 0,984. 
Questo risultato è da considerarsi un "proof-of-concept".
Dimostra che l'approccio può funzionare. 
Ma la scarisità di dati ci vieta di addestrare un vero modello utile. 

### 15. Modellazione Predittiva — Parity Plot

Questo è il parity plot della configurazione migliore: ogni punto confronta la capacità reale misurata con quella predetta dal modello in leave-one-out. 
Più i punti giacciono sulla diagonale tratteggiata — la predizione perfetta — migliore è il modello.

### 16. Filtraggio dei Polimeri — Criteri della Teoria FMO

Una volta ottenuti i polimeri candidati, li filtro usando la teoria degli orbitali molecolari di frontiera. 
Seleziono un logP alto in modo che il polimero rimanga solido e insolubile in acqua.
Un TPSA più alto per i siti di legame polari.
Un gap FMO intermolecolare più basso per un legame donatore-accettore più forte.
Ed un SA score più basso così da essere realisticamente sintetizzabile su scala.

### 19. La Pipeline Integrata Completa

Qui possiamo vedere un esempio della pipeline completa, dato una molecola target ed il pH il modello genera polimeri, trova i migliori candidati e crea questa curva di concentrazione/capacità predetta.

### 20. Ampliare i Dati — Il Tool paper_scraper

Per attaccare il problema della scarsità di dati alla radice, ho costruito un secondo strumento, che ho chiamato paper_scraper.
Recupera paper ad accesso aperto tramite OpenAlex, ne estrae altri tramite Grobid, e infine usa un LLM per estrarre automaticamente le informazioni utili — polimero, molecola, concentrazione, capacità, pH — direttamente dal testo e immagini dei paper.

### 21. Estrazione con LLM — Analisi dei Paper

Ho testato quest'ultimo passaggio, (il cuore dello strumento), con diversi modelli — Gemma, DeepSeek, Kimi e Claude Opus — per confrontarne l'affidabilità nell'estrarre correttamente i dati dai paper.

### 22. Estrazione con LLM — Risultati

In questa tabella ho riporato il contributo di ciascun modello al dataset estratto.

### 23. Prospettive sulla Scarsità di Dati

Ad oggi mancano ancora paper sufficienti, questo porta ad una grave mancanza di dati reali.
Ma guardando avanti, mi aspetto che nel tempo emergano nuovi paper da cui estrarre dati, e che i modelli LLM diventino sempre più capaci ed efficienti.


### 25. Limiti — Ambito & Scelte di Modellazione

Ci sono anche alcuni limiti di ambito.
Il modello generativo è stato addestrato sul dataset sintetico PI1M, non sul dataset proprietario PolyInfo da cui PI1M deriva, poiché non avevo accesso a quest'ultimo. 
Convertire i nomi grezzi dei materiali in SMILES è semplice grazie a PubChem, ma la conversione in P-SMILES è ancora manuale e limitata.
E l'intera pipeline considera solo materiali a polimero singolo — nessun composito a doppio polimero o multi-materiale, per ora.

### 26. Sviluppi Futuri

Guardando avanti, il prossimo passo a maggior valore è semplicemente più dati — in particolare risultati negativi — che migliorerebbero in modo significativo sia il filtro sia il modello predittivo.
Oltre a questo, potremmo esplorare notazioni polimeriche alternative come BigSmiles se i dati lo permettono; E provare architetture più complesse come le graph neural networks.
Inoltre ricevere l'accesso al dataset proprietario PolyInfo, ed estendere la pipeline a input multi-materiale e a doppio polimero.
