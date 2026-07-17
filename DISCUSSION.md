# Discussion — Speach Slide per Slide

_Una sezione per ogni slide visibile di `Slide_Samuele_Maggiori_v3.pptx`; sotto ogni titolo, il discorso da tenere._

---

### 1. Pipeline End-to-End per la generazione di Polimeri

Buongiorno a tutti, sono Samuele Maggiori e oggi vi presento il mio lavoro di tesi: una pipeline computazionale end-to-end per la generazione di polimeri adsorbenti — delle vere e proprie "spugne molecolari" — pensati per rimuovere molecole inquinanti dalle acque reflue.

### 2. Il Problema & l'Obiettivo della Tesi

Partiamo dal problema: le acque reflue contengono molecole inquinanti — farmaci, coloranti, altri contaminanti — che i trattamenti standard faticano a rimuovere in modo mirato. In letteratura esistono già esempi di "spugne molecolari", polimeri progettati per adsorbire selettivamente queste molecole, con risultati sperimentali incoraggianti. %TODO: inserire qui 1-2 esempi concreti di paper con buoni risultati (nome/autore, molecola target, capacità di adsorbimento ottenuta) — dimmi quali paper vuoi citare e li inserisco%. Il problema è che ogni nuovo polimero richiede tipicamente sintesi e test in laboratorio, un processo lento e costoso. L'obiettivo della mia tesi è quindi predire e generare polimeri — le "spugne molecolari" — capaci di adsorbire molecole inquinanti target dalle acque reflue, ma per via computazionale: invece di scegliere a mano un polimero e testarlo in laboratorio, ho costruito una pipeline in grado di proporre e valutare automaticamente polimeri candidati.

### 3. Due Sistemi Complementari

La tesi si basa su due sistemi complementari. Uno è generativo: propone nuovi candidati polimerici. L'altro è predittivo: dato un polimero e una molecola target, stima quanto di quella molecola il polimero riesce ad adsorbire. A collegarli c'è un filtro basato sulla conoscenza di dominio. Questi due sistemi formano una pipeline, in grado, dato in input una molecola che vogliamo "catturare" (ed iperparametri configurabili), di proporre in output una serie di polimeri che il modello predice essere dei buoni candidati.

### 4. Raccolta Dati — Costruzione del Dataset PDCC

Il primo lavoro è stato costruire il dataset stesso. Ho estratto dati di adsorbimento polimero-farmaco da articoli pubblicati per creare quello che chiamo dataset PDCC — "Polymer, Drug (più in generale Molecola), Concentration e Capacity" — a questi è stato inoltre associato anche il pH. Non esisteva un dataset già pronto per questo scopo, quindi questo lavoro di raccolta e cura dei dati è stato una base necessaria per tutto ciò che è venuto dopo. %scegli tu la formulazione che preferisci, alternative a "raccolta e cura dei dati": "raccolta e pulizia dei dati" / "raccolta e organizzazione dei dati" / "raccolta e curatela dei dati"%

### 5. Scarsità di Dati — Un Vincolo Strutturale

Purtroppo, questo campo di ricerca semplicemente non ha molti dati pubblicati. Pochissimi studi riportano capacità di adsorbimento polimero-molecola in modo direttamente confrontabile. Questo non è un limite del progetto — è un vincolo strutturale del settore — ma è la sfida centrale attorno a cui è costruita tutta la metodologia successiva, e ci tornerò quando parlerò dei risultati del modello predittivo.

### 6. SMILES e P-SMILES — Le Notazioni di Base

Prima di andare avanti, vale la pena spiegare due notazioni che torneranno in quasi tutte le slide successive. SMILES è un modo standard per scrivere una molecola come una semplice stringa di testo, che codifica atomi e legami. P-SMILES fa lo stesso per i polimeri, rappresentando l'unità ripetuta della catena polimerica. Tutta la parte generativa e predittiva della mia pipeline lavora proprio su queste due rappresentazioni testuali.

### 7. Pipeline per l'estrazione delle feature

Per far lavorare i modelli su polimeri e molecole, serve prima trasformarli in numeri. Questa fase, che chiamo featurizzazione, prende una stringa SMILES o P-SMILES e ne estrae proprietà fisico-chimiche rilevanti — trasformando di fatto una rappresentazione testuale in un vettore di feature numeriche che i modelli successivi possono usare.

### 8. Gestire Dati Sparsi — Interpolazione

Quando i punti sperimentali erano pochi ma il loro andamento era abbastanza regolare da poter essere interpolato con fiducia, ho usato l'interpolazione per aumentare i dati disponibili. Solo dopo aver interpolato ho aggiunto anche il punto (0,0): a concentrazione zero del polimero, l'adsorbimento è per definizione zero. %scegli tu la frase che preferisci per l'inizio, alternative: "Dove i dati erano scarsi ma seguivano un andamento chiaro e prevedibile" / "Nei casi in cui i dati erano pochi ma mostravano un andamento regolare" / "Quando i punti sperimentali erano pochi ma il loro andamento era abbastanza regolare da poter essere interpolato con fiducia" (quella attualmente usata sopra)%

### 9. Modellazione Generativa — Approccio

Per la parte generativa, ho addestrato un wrapper attorno a mingpt per generare stringhe SMILES valide per le molecole, e stringhe P-SMILES per i polimeri. Il modello impara la "grammatica" della notazione chimica notevolmente bene, al punto da proporre strutture nuove, sintatticamente e chimicamente valide, invece di limitarsi a memorizzare gli esempi di training.

### 10. Modellazione Generativa — Risultati

Su 12.800 molecole generate, 5.525 stringhe SMILES erano al tempo stesso nuove e chimicamente valide, mentre per le P-SMILES il numero era 7.373 su 12.800. Considero questo un risultato molto solido — il modello propone in modo affidabile candidati polimerici nuovi e validi, che è esattamente ciò che serve nella prima fase della pipeline, e in poche ore riesce a generare decine di migliaia di nuovi candidati.

### 11. Modellazione Predittiva — Metodologia (LOOCV)

Per la parte predittiva, ho eseguito una leave-one-out cross-validation su un gran numero di configurazioni di iperparametri, classificandole per punteggio Q2 — un punteggio che confronta l'errore del modello con l'errore che si avrebbe usando semplicemente il valore medio come previsione: più si avvicina a 1, più il modello è informativo rispetto a una previsione banale. Ho selezionato la configurazione con le prestazioni migliori come modello finale — lo chiamo PSCP, o "PSmileCapacityPredictor".

### 12. PSCP — Cosa Predice Davvero

Il modello PSCP trovato prende in input un polimero, una molecola target, la concentrazione e il pH, ne estrae le feature, scala gli input e restituisce in output una capacità di adsorbimento predetta. È quindi un unico modello che prova a riflettere tutte le condizioni sperimentali che possano influenzare realmente l'adsorbimento nella pratica.

### 14. Modellazione Predittiva — Risultati (Q2)

La configurazione migliore ha raggiunto un Q2 di 0,984, con un errore assoluto medio di circa 1,5 e un RMSE di circa 6,5. Questo risultato è da considerarsi un "proof-of-concept" — dimostra che l'approccio può funzionare, ed è validato sui dati attualmente disponibili — ma il vero banco di prova della generalizzazione arriverà con altre misurazioni pubblicate. Ed è esattamente qui che il punto sulla scarsità di dati, sollevato qualche slide fa, torna a farsi sentire.

### 15. Filtraggio dei Polimeri — Criteri della Teoria FMO

Una volta ottenuti i polimeri candidati, li filtro usando la teoria degli orbitali molecolari di frontiera. Seleziono un logP alto in modo che il polimero rimanga solido e insolubile in acqua, un TPSA più alto per i siti di legame polari, un gap FMO intermolecolare più basso per un legame donatore-accettore più forte, e un SA score più basso così da essere realisticamente sintetizzabile su scala.

### 16. Un Filtro Modulare, Volutamente Aggressivo

Come il resto della pipeline, anche questo filtro è modulare: si può sostituire o affinare senza toccare il resto del sistema. Il filtro attuale è piuttosto severo e scarta molti dei polimeri generati — ma essendo in grado di generare diecimila nuovi P-SMILES nell'arco di poche ore, posso permettermi un filtro così "aggressivo": anche scartando la maggior parte dei candidati, restano comunque abbastanza polimeri promettenti da valutare.

### 18. La Pipeline Integrata Completa

Tutto questo confluisce in un'unica funzione che chiamo `find_polymer_for_target_molecule`. Le si dà una molecola target, lei la converte in SMILES, genera polimeri candidati, li filtra, ne predice la capacità e ripete il ciclo — proponendo altri candidati — finché non raggiunge la capacità target. La maggior parte dei componenti della pipeline è inoltre modulare: possiamo teoricamente accomodare futuri sviluppi, miglioramenti, diversi filtri e modelli di generazione e predizione.

### 19. Ampliare i Dati — Il Tool paper_scraper

Per attaccare il problema della scarsità di dati alla radice, ho costruito un secondo strumento, che chiamo paper_scraper. Recupera paper ad accesso aperto tramite OpenAlex, ne estrae altri tramite Grobid, e infine usa un LLM per estrarre automaticamente le informazioni utili — polimero, molecola, concentrazione, capacità, pH — direttamente dal testo dei paper.

### 20. Estrazione con LLM — Analisi dei Paper

Il cuore dello strumento è proprio l'estrazione con LLM: il modello legge il testo del paper e ne ricava, in forma strutturata, le righe da aggiungere al dataset PDCC. Ho testato questo passaggio con diversi modelli — Gemma, DeepSeek, Kimi e Claude Opus — per confrontarne l'affidabilità nell'estrarre correttamente polimero, molecola, concentrazione, capacità e pH.

### 21. Prospettive sulla Scarsità di Dati

Ad oggi mancano ancora paper sufficienti, e questo resta un vincolo reale. Ma guardando avanti, mi aspetto che nel tempo emergano nuovi paper da cui estrarre dati, e che i modelli LLM diventino sempre più capaci ed efficienti: questo strumento è pensato proprio per sfruttare quella crescita ed espandere il dataset PDCC in modo via via più automatico.

### 22. Limiti — Dati & Validazione

Voglio essere diretto sui limiti. Primo, i dati: ci sono troppe poche misurazioni di capacità pubblicate per addestrare o validare in modo robusto il modello predittivo, e in particolare mancano dati di risultato negativo — polimeri che non adsorbono — che affinerebbero sia il filtro sia il modello. Secondo, la validazione: nulla di generato da questa pipeline è stato testato in laboratorio. Ogni risultato che ho mostrato è puramente computazionale.

### 23. Limiti — Ambito & Scelte di Modellazione

Ci sono anche alcuni limiti di ambito. Il modello generativo è stato addestrato sul dataset sintetico PI1M, non sul dataset proprietario PolyInfo da cui PI1M deriva, poiché non avevo accesso a quest'ultimo. Convertire i nomi grezzi dei materiali in SMILES è semplice grazie a PubChem, ma la conversione in P-SMILES è ancora manuale e limitata. E l'intera pipeline considera solo materiali a polimero singolo — nessun composito a doppio polimero o multi-materiale, per ora.

### 24. Sviluppi Futuri

Guardando avanti, il prossimo passo a maggior valore è semplicemente più dati — in particolare risultati negativi — che migliorerebbero in modo significativo sia il filtro sia il modello predittivo. Oltre a questo, vorrei esplorare notazioni polimeriche alternative come BigSmiles se i dati lo permettono, provare architetture più complesse come le graph neural network una volta disponibili abbastanza dati da giustificarle, cercare l'accesso al dataset proprietario PolyInfo, ed estendere la pipeline a input multi-materiale e a doppio polimero.
