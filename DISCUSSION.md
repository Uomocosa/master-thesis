# Discussion — Bozza Speach Slide per Slide

_Bozza dello speach per il capitolo di discussione della tesi, strutturata slide per slide così da poter costruire le slide vere e proprie in seguito.
Ogni sezione qui sotto è una slide (o parte di slide)._

---

### 1. Il Problema, gli Esempi & l'Obiettivo della Tesi

_**POWERPOINT SLIDE**_ — _Slide di titolo/apertura: prima un'immagine che rappresenti il problema (es. acque reflue contaminate), poi 1-2 immagini/schemi di "spugne molecolari" prese da paper con buoni risultati (con citazione visibile), poi titolo della tesi con immagine/diagramma di un polimero "spugna" che adsorbe una molecola inquinante dall'acqua._

_**SPEACH**_ — Partiamo dal problema: le acque reflue contengono molecole inquinanti — farmaci, coloranti, altri contaminanti — che i trattamenti standard faticano a rimuovere in modo mirato. In letteratura esistono già esempi di "spugne molecolari", polimeri progettati per adsorbire selettivamente queste molecole, con risultati sperimentali incoraggianti. %TODO: inserire qui 1-2 esempi concreti di paper con buoni risultati (nome/autore, molecola target, capacità di adsorbimento ottenuta) — dimmi quali paper vuoi citare e li inserisco%. Il problema è che ogni nuovo polimero richiede tipicamente sintesi e test in laboratorio, un processo lento e costoso. L'obiettivo della mia tesi è quindi predire e generare polimeri — le "spugne molecolari" — capaci di adsorbire molecole inquinanti target dalle acque reflue, ma per via computazionale: invece di scegliere a mano un polimero e testarlo in laboratorio, ho costruito una pipeline in grado di proporre e valutare automaticamente polimeri candidati.

### 2. Due Sistemi Complementari

_**POWERPOINT SLIDE**_ — _Diagramma semplice a due riquadri: "Modello Generativo → nuovi candidati polimerici" e "Modello Predittivo → capacità di adsorbimento stimata", con una freccia che mostra come confluiscono in un'unica pipeline._

_**SPEACH**_ — La tesi si basa su due sistemi complementari. Uno è generativo: propone nuovi candidati polimerici. L'altro è predittivo: dato un polimero e una molecola target, stima quanto di quella molecola il polimero riesce ad adsorbire. A collegarli c'è un filtro basato sulla conoscenza di dominio. Questi due sistemi formano una pipeline, in grado, dato in input una molecola che vogliamo "catturare" (ed iperparametri configurabili), di proporre in output una serie di polimeri che il modello predice essere dei buoni candidati.

### 3. Raccolta Dati — Costruzione del Dataset PDCC

_**POWERPOINT SLIDE**_ — _Piccolo estratto di tabella con le colonne del PDCC: polimero, molecola, pH, concentrazione, capacità._

_**SPEACH**_ — Il primo lavoro è stato costruire il dataset stesso. Ho estratto dati di adsorbimento polimero-farmaco da articoli pubblicati per creare quello che chiamo dataset PDCC — "Polymer, Drug (più in generale Molecola), Concentration e Capacity" — a questi è stato inoltre associato anche il pH. Non esisteva un dataset già pronto per questo scopo, quindi questo lavoro di raccolta e cura dei dati è stato una base necessaria per tutto ciò che è venuto dopo. %scegli tu la formulazione che preferisci, alternative a "raccolta e cura dei dati": "raccolta e pulizia dei dati" / "raccolta e organizzazione dei dati" / "raccolta e curatela dei dati" (ripete "curatela" già usata sopra, quindi meno indicata qui)%

### 4. Scarsità di Dati — Un Vincolo Strutturale, Non un Fallimento

_**POWERPOINT SLIDE**_ — _Una singola frase/citazione forte sulla slide: "Pochi studi pubblicati sulla capacità polimero-molecola" — magari un grafico a barre che mostra quanti pochi punti dati esistono per coppia polimero-molecola._

_**SPEACH**_ — Purtroppo, questo campo di ricerca semplicemente non ha molti dati pubblicati. Pochissimi studi riportano capacità di adsorbimento polimero-molecola in modo direttamente confrontabile. Questo non è un limite del progetto — è un vincolo strutturale del settore — ma è la sfida centrale attorno a cui è costruita tutta la metodologia successiva, e ci tornerò quando parlerò dei risultati del modello predittivo.

### 5. SMILES e P-SMILES — Le Notazioni di Base

_**POWERPOINT SLIDE**_ — _Due esempi affiancati: a sinistra una piccola molecola con la sua stringa SMILES accanto (es. aspirina); a destra un'unità ripetuta di polimero con la sua stringa P-SMILES accanto. Titolo chiaro: "come rappresentiamo chimicamente molecole e polimeri come testo"._

_**SPEACH**_ — Prima di andare avanti, vale la pena spiegare due notazioni che torneranno in quasi tutte le slide successive. SMILES è un modo standard per scrivere una molecola come una semplice stringa di testo, che codifica atomi e legami. P-SMILES fa lo stesso per i polimeri, rappresentando l'unità ripetuta della catena polimerica. Tutta la parte generativa e predittiva della mia pipeline lavora proprio su queste due rappresentazioni testuali.

### 6. Pipeline di Featurizzazione

_**POWERPOINT SLIDE**_ — _Diagramma concettuale: stringa SMILES → immagine della molecola corrispondente (generata con rdkit); stringa P-SMILES → rappresentazione del polimero, se disponibile. Poi entrambe → un vettore di feature numeriche. Nessun codice mostrato in slide. %Da confermare: polymetrix è in grado di generare un'immagine della struttura polimerica a partire da P-SMILES? Se sì la mostriamo, altrimenti mostriamo solo il lato SMILES→molecola%._

_**SPEACH**_ — Per far lavorare i modelli su polimeri e molecole, serve prima trasformarli in numeri. Questa fase, che chiamo featurizzazione, prende una stringa SMILES o P-SMILES e ne estrae proprietà fisico-chimiche rilevanti — trasformando di fatto una rappresentazione testuale in un vettore di feature numeriche che i modelli successivi possono usare.

### 7. Gestire Dati Sparsi — Interpolazione

_**POWERPOINT SLIDE**_ — _Video generato in Python: mostra la curva originale in background, i punti sperimentali originali, e poi l'aggiunta progressiva dei punti interpolati. %TODO produzione: creare questo video con Python — non è una modifica di testo, va prodotto separatamente%_

_**SPEACH**_ — Quando i punti sperimentali erano pochi ma il loro andamento era abbastanza regolare da poter essere interpolato con fiducia, ho usato l'interpolazione per aumentare i dati disponibili. Solo dopo aver interpolato ho aggiunto anche il punto (0,0): a concentrazione zero del polimero, l'adsorbimento è per definizione zero. %scegli tu la frase che preferisci per l'inizio, alternative: "Dove i dati erano scarsi ma seguivano un andamento chiaro e prevedibile" / "Nei casi in cui i dati erano pochi ma mostravano un andamento regolare" / "Quando i punti sperimentali erano pochi ma il loro andamento era abbastanza regolare da poter essere interpolato con fiducia" (quella attualmente usata sopra)%

### 8. Modellazione Generativa — Approccio

_**POWERPOINT SLIDE**_ — _Diagramma: riquadro dell'architettura mingpt, input "token SMILES" → output "stringa SMILES / P-SMILES generata"._

_**SPEACH**_ — Per la parte generativa, ho addestrato un wrapper attorno a mingpt per generare stringhe SMILES valide per le molecole, e stringhe P-SMILES per i polimeri. Il modello impara la "grammatica" della notazione chimica notevolmente bene, al punto da proporre strutture nuove, sintatticamente e chimicamente valide, invece di limitarsi a memorizzare gli esempi di training.

### 9. Modellazione Generativa — Risultati

_**POWERPOINT SLIDE**_ — _Due numeri grandi affiancati: "SMILES: 5525 / 12800 nuovi e validi" e "P-SMILES: 7373 / 12800 nuovi e validi"._

_**SPEACH**_ — Su 12.800 molecole generate, 5.525 stringhe SMILES erano al tempo stesso nuove e chimicamente valide, mentre per le P-SMILES il numero era 7.373 su 12.800. Considero questo un risultato molto solido — il modello propone in modo affidabile candidati polimerici nuovi e validi, che è esattamente ciò che serve nella prima fase della pipeline, e in poche ore riesce a generare decine di migliaia di nuovi candidati.

### 10. Modellazione Predittiva — Metodologia (LOOCV)

_**POWERPOINT SLIDE**_ — _Diagramma: ciclo di Leave-One-Out Cross-Validation su molte configurazioni di iperparametri, che confluisce in "classificate per Q2" → selezione della configurazione migliore._

_**SPEACH**_ — Per la parte predittiva, ho eseguito una leave-one-out cross-validation su un gran numero di configurazioni di iperparametri, classificandole per punteggio Q2 — un punteggio che confronta l'errore del modello con l'errore che si avrebbe usando semplicemente il valore medio come previsione: più si avvicina a 1, più il modello è informativo rispetto a una previsione banale. Ho selezionato la configurazione con le prestazioni migliori come modello finale — lo chiamo PSCP, o "PSmileCapacityPredictor".

### 11. PSCP — Cosa Predice Davvero

_**POWERPOINT SLIDE**_ — _Riquadro input/output: input "polimero + molecola + concentrazione + pH" → PSCP → output "capacità di adsorbimento predetta"._

_**SPEACH**_ — Il modello PSCP trovato prende in input un polimero, una molecola target, la concentrazione e il pH, ne estrae le feature, scala gli input e restituisce in output una capacità di adsorbimento predetta. È quindi un unico modello che prova a riflettere tutte le condizioni sperimentali che possano influenzare realmente l'adsorbimento nella pratica.

### 12. Featurizzare i Polimeri — Un Contributo Metodologico

_**POWERPOINT SLIDE**_ — _Diagramma: unità ripetuta del polimero → SMILES del monomero → tappata con idrogeno → trattata come molecola → logP / SA score estratti con rdkit._

_**SPEACH**_ — Un problema pratico che ho dovuto risolvere: rdkit non supporta nativamente i polimeri, solo le molecole. La mia soluzione è stata prendere gli SMILES dei monomeri, "tapparli" con idrogeno e trattarli come molecole ordinarie, così da poter estrarre proprietà come il logP e il synthetic accessibility score. %tieni o togli questa slide? è un dettaglio tecnico ma anche un vero contributo metodologico — deciditu se ha abbastanza peso da meritare uno slide dedicato o se va accorpata altrove%

### 13. Modellazione Predittiva — Risultati (Q2)

_**POWERPOINT SLIDE**_ — _Estratto della leaderboard da `RESULTS/mlp_experiments/q2_leaderboard.md`: prima riga `experiment_hd_16_8_4_4_4`, Q2 = 0,984, MAE = 1,50, RMSE = 6,49, più qualche riga successiva per contesto._

_**SPEACH**_ — La configurazione migliore ha raggiunto un Q2 di 0,984, con un errore assoluto medio di circa 1,5 e un RMSE di circa 6,5. Questo risultato è da considerarsi un "proof-of-concept" — dimostra che l'approccio può funzionare, ed è validato sui dati attualmente disponibili — ma il vero banco di prova della generalizzazione arriverà con altre misurazioni pubblicate. Ed è esattamente qui che il punto sulla scarsità di dati, sollevato qualche slide fa, torna a farsi sentire.

### 14. Filtraggio dei Polimeri — Criteri della Teoria FMO

_**POWERPOINT SLIDE**_ — _Quattro criteri di filtro come icone/etichette: logP alto (rimane insolubile), TPSA più alto (siti di legame polari), gap FMO intermolecolare più basso (forza di legame donatore-accettore), SA score più basso (sintetizzabile su scala)._

_**SPEACH**_ — Una volta ottenuti i polimeri candidati, li filtro usando la teoria degli orbitali molecolari di frontiera. Seleziono un logP alto in modo che il polimero rimanga solido e insolubile in acqua, un TPSA più alto per i siti di legame polari, un gap FMO intermolecolare più basso per un legame donatore-accettore più forte, e un SA score più basso così da essere realisticamente sintetizzabile su scala.

### 15. Un Filtro Modulare, e Volutamente Aggressivo

_**POWERPOINT SLIDE**_ — _Diagramma: "10.000+ P-SMILES generati in poche ore" → filtro FMO/logP/TPSA/SA → "pochi candidati sopravvivono", con etichetta "filtro modulare, sostituibile"._

_**SPEACH**_ — Come il resto della pipeline, anche questo filtro è modulare: si può sostituire o affinare senza toccare il resto del sistema. Il filtro attuale è piuttosto severo e scarta molti dei polimeri generati — ma essendo in grado di generare diecimila nuovi P-SMILES nell'arco di poche ore, posso permettermi un filtro così "aggressivo": anche scartando la maggior parte dei candidati, restano comunque abbastanza polimeri promettenti da valutare.

### 16. Esplorazione Non Supervisionata — Clustering Gerarchico

_**POWERPOINT SLIDE**_ — _Curva del silhouette score con picco a 63 cluster; miniatura del dendrogramma. Risultati riferiti a `RESULTS/ahc_clustering/`._

_**SPEACH**_ — Ho anche eseguito un clustering gerarchico agglomerativo sul dataset per esplorare la struttura nelle coppie polimero-molecola. Il silhouette score ha avuto un picco a 63 cluster, il che riflette quanto sia eterogeneo questo dataset — non è di per sé una segmentazione utile. Lo presento come uno strumento esplorativo e di interpretabilità, che aiuta a capire cosa guida i raggruppamenti nei dati, non come un risultato predittivo di rilievo.

### 17. La Pipeline Integrata Completa

_**POWERPOINT SLIDE**_ — _Diagramma di flusso: molecola target → SMILES → generazione candidati (mingpt) → filtro (FMO/logP/TPSA/SA) → predizione capacità (PSCP) → ciclo finché la capacità target è raggiunta o il budget è esaurito._

_**SPEACH**_ — Tutto questo confluisce in un'unica funzione che chiamo `find_polymer_for_target_molecule`. Le si dà una molecola target, lei la converte in SMILES, genera polimeri candidati, li filtra, ne predice la capacità e ripete il ciclo — proponendo altri candidati — finché non raggiunge la capacità target. La maggior parte dei componenti della pipeline è inoltre modulare: possiamo teoricamente accomodare futuri sviluppi, miglioramenti, diversi filtri e modelli di generazione e predizione.

### 18. Ampliare i Dati — Il Tool paper_scraper

_**POWERPOINT SLIDE**_ — _Diagramma di flusso: OpenAlex (ricerca paper open access) → Grobid (estrazione testo da altri paper) → LLM (estrazione informazioni strutturate) → PDCC. Sotto, loghi/nomi degli LLM testati: Gemma, DeepSeek, Kimi, Claude Opus._

_**SPEACH**_ — Per attaccare il problema della scarsità di dati alla radice, ho costruito un secondo strumento, che chiamo paper_scraper. Recupera paper ad accesso aperto tramite OpenAlex, ne estrae altri tramite Grobid, e infine usa un LLM per estrarre automaticamente le informazioni utili — polimero, molecola, concentrazione, capacità, pH — direttamente dal testo dei paper. L'ho testato con diversi modelli: Gemma, DeepSeek, Kimi e Claude Opus.

### 19. Prospettive sulla Scarsità di Dati

_**POWERPOINT SLIDE**_ — _Freccia temporale: "oggi: pochi paper disponibili" → "domani: più paper pubblicati + LLM migliori e più economici" → "dataset PDCC più grande"._

_**SPEACH**_ — Ad oggi mancano ancora paper sufficienti, e questo resta un vincolo reale. Ma guardando avanti, mi aspetto che nel tempo emergano nuovi paper da cui estrarre dati, e che i modelli LLM diventino sempre più capaci ed efficienti: questo strumento è pensato proprio per sfruttare quella crescita ed espandere il dataset PDCC in modo via via più automatico.

### 20. Limiti — Dati & Validazione

_**POWERPOINT SLIDE**_ — _Lista a due colonne: "Dati" (scarsità, assenza di risultati negativi) / "Validazione" (nessuna conferma in laboratorio, solo computazionale)._

_**SPEACH**_ — Voglio essere diretto sui limiti. Primo, i dati: ci sono troppe poche misurazioni di capacità pubblicate per addestrare o validare in modo robusto il modello predittivo, e in particolare mancano dati di risultato negativo — polimeri che non adsorbono — che affinerebbero sia il filtro sia il modello. Secondo, la validazione: nulla di generato da questa pipeline è stato testato in laboratorio. Ogni risultato che ho mostrato è puramente computazionale.

### 21. Limiti — Ambito & Scelte di Modellazione

_**POWERPOINT SLIDE**_ — _Lista: dati sintetici PI1M vs PolyInfo proprietario; conversione P-SMILES manuale; solo polimero singolo, nessun composito._

_**SPEACH**_ — Ci sono anche alcuni limiti di ambito. Il modello generativo è stato addestrato sul dataset sintetico PI1M, non sul dataset proprietario PolyInfo da cui PI1M deriva, poiché non avevo accesso a quest'ultimo. Convertire i nomi grezzi dei materiali in SMILES è semplice grazie a PubChem, ma la conversione in P-SMILES è ancora manuale e limitata. E l'intera pipeline considera solo materiali a polimero singolo — nessun composito a doppio polimero o multi-materiale, per ora.

### 22. Sviluppi Futuri

_**POWERPOINT SLIDE**_ — _Lista in stile roadmap con icone: più dati (in particolare risultati negativi, anche via paper_scraper) → notazioni alternative (BigSmiles) → architetture GNN → accesso a PolyInfo → input multi-materiale._

_**SPEACH**_ — Guardando avanti, il prossimo passo a maggior valore è semplicemente più dati — in particolare risultati negativi — che migliorerebbero in modo significativo sia il filtro sia il modello predittivo. Oltre a questo, vorrei esplorare notazioni polimeriche alternative come BigSmiles se i dati lo permettono, provare architetture più complesse come le graph neural network una volta disponibili abbastanza dati da giustificarle, cercare l'accesso al dataset proprietario PolyInfo, ed estendere la pipeline a input multi-materiale e a doppio polimero.
