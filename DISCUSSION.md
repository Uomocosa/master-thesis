# Discussion — Bozza Speach Slide per Slide

_Bozza dello speach per il capitolo di discussione della tesi, strutturata slide per slide così da poter costruire le slide vere e proprie in seguito.
Ogni sezione qui sotto è una slide (o parte di slide)._

---

### 1. Il Problema — Acque Reflue & Spugne Molecolari

_**POWERPOINT SLIDE**_ — _Slide di titolo: immagine/diagramma di un polimero "spugna" che adsorbe una molecola inquinante dall'acqua; titolo della tesi in una riga._

%Aggiungi all'inzio il PERCHE, voglio cominciare con un po' di PROBLEMA che abbiamo al momento, qualche esempio di spugne molecolari presi da paper che effettivamente hanno dei buoni risultati, e poi il mio obbiettivo della tesi%
_**SPEACH**_ — L'obiettivo della mia tesi è predire e generare polimeri, in particolare: "spugne molecolari" — capaci di adsorbire molecole inquinanti target dalle acque reflue. Invece di scegliere a mano un polimero e testarlo in laboratorio, ho voluto costruire una pipeline computazionale in grado di proporre e valutare automaticamente polimeri candidati.

### 2. Due Sistemi Complementari

_**POWERPOINT SLIDE**_ — _Diagramma semplice a due riquadri: "Modello Generativo → nuovi candidati polimerici" e "Modello Predittivo → capacità di adsorbimento stimata", con una freccia che mostra come confluiscono in un'unica pipeline._

_**SPEACH**_ — La tesi si basa su due sistemi complementari. Uno è generativo: propone nuovi candidati polimerici. L'altro è predittivo: dato un polimero e una molecola target, stima quanto di quella molecola il polimero riesce ad adsorbire. A collegarli c'è un filtro basato sulla conoscenza di dominio. Questi due sistemi formano una pipeline, in grado dato in input una molecola che vogliamo "catturare" (ed hyperparametrs configurabili), ed in output proporrà una serie di polimeri che il modello predice essere dei buoni canditati.

### 3. Raccolta Dati — Costruzione del Dataset PDCC

_**POWERPOINT SLIDE**_ — _Piccolo estratto di tabella con le colonne del PDCC: polimero, molecola, pH, concentrazione, capacità._

_**SPEACH**_ — Il primo lavoro è stato costruire il dataset stesso. Ho estratto dati di adsorbimento polimero-farmaco da articoli pubblicati per creare quello che chiamo dataset PDCC — "Polymer, Drug (più in generale Molecola), Concentration e Capacity", a questi è stato inoltre riportato anche il pH. Non esisteva un dataset già pronto per questo scopo, quindi questo lavoro di raccolta e curatura è stata una base necessaria per tutto ciò che è venuto dopo. %raccolta e curatura, si dice in itialiano? puoi darmi alternative tra cui scegliere%

### 4. Scarsità di Dati — Un Vincolo Strutturale, Non un Fallimento

_**POWERPOINT SLIDE**_ — _Una singola frase/citazione forte sulla slide: "Pochi studi pubblicati sulla capacità polimero-molecola" — magari un grafico a barre che mostra quanti pochi punti dati esistono per coppia polimero-molecola._

_**SPEACH**_ — Purtroppo, questo campo di ricerca semplicemente non ha molti dati pubblicati. Pochissimi studi riportano capacità di adsorbimento polimero-molecola in modo direttamente confrontabile. Questo non è un limite del progetto — è un vincolo strutturale del settore — ma è la sfida centrale attorno a cui è costruita tutta la metodologia successiva, e ci tornerò quando parlerò dei risultati del modello predittivo.

%Manca un capitolo dove spiego velocemente SMILE e PSMILE in quanto importanti nei capitoli successivi%

### 5. Pipeline di Featurizzazione & Strumenti

_**POWERPOINT SLIDE**_ — _Diagramma della pipeline: SMILES/P-SMILES grezzi → rdkit / polymetrix / tblite → vettore di feature. Facoltativo: mostrare i nomi delle dataclass PDCC/MLP/Featurizer/Experiment come riquadri etichettati._

_**SPEACH**_ — Per trasformare le strutture grezze di polimeri e molecole in qualcosa che un modello possa usare, ho costruito una pipeline di featurizzazione basata su rdkit, polymetrix e tblit, librerie python più o meno conosciute, in grado di lavorare con SMILE e PSMILE string e di estrapolarne capacità fisiche. %Non parlare mai di codice nel dettaglio, e non mostreremo mai il codice nelle slide% %In queste slide dove dico quali librerie ho usato è importante mettere immagine di SMILE -> molecola tramite rdkit e se riusciamo PSMILE -> polymer representation (non sono sicuro polymetrix lo possa fare)%

### 6. Gestire Dati Sparsi — Interpolazione

_**POWERPOINT SLIDE**_ — _Grafico a dispersione prima/dopo: punti dati sparsi, poi punti interpolati che riempiono i vuoti, con un'etichetta di avvertenza "usato solo dove giustificabile"._

_**SPEACH**_ — Dove i dati erano sparsi ma la relazione sottostante era ben comportata, ho usato l'interpolazione per aumentarli. E solo dopo l'interpolazione aggiunto anche il punto (0,0), ovviamente data una concentrazione 0 del polimero, otterremo una absorbimento pari a 0. %"Dove i dati erano sparsi ma la relazione sottostante era ben comportata" possiamo riformulare questa frase, non mi piace, dammi alcune opzioni"% %Qui è necessario con python aggiungere un video dove facciamo vedere l'aggiunta di punti con in background la curva dei dati originale, ed i punti originali e poi quelli interpolati%

### 7. Modellazione Generativa — Approccio

_**POWERPOINT SLIDE**_ — _Diagramma: riquadro dell'architettura mingpt, input "token SMILES" → output "stringa SMILES / P-SMILES generata"._

_**SPEACH**_ — Per la parte generativa, ho addestrato un wrapper attorno a mingpt per generare stringhe SMILES valide per le molecole, e stringhe P-SMILES per i polimeri. Il modello impara la "grammatica" della notazione chimica notevolmente bene da proporre strutture nuove, sintatticamente e chimicamente valide, invece di limitarsi a memorizzare gli esempi di training.

### 8. Modellazione Generativa — Risultati

_**POWERPOINT SLIDE**_ — _Due numeri grandi affiancati: "SMILES: 5525 / 12800 nuovi e validi" e "P-SMILES: 7373 / 12800 nuovi e validi"._

_**SPEACH**_ — Su 12.800 molecole generate, 5.525 stringhe SMILES erano al tempo stesso nuove e chimicamente valide, mentre per le P-SMILES il numero era 7.373 su 12.800. Considero questo un risultato molto solido — il modello propone in modo affidabile candidati polimerici nuovi e validi, che è esattamente ciò che serve nella prima fase della pipeline.

### 9. Modellazione Predittiva — Metodologia (LOOCV)

_**POWERPOINT SLIDE**_ — _Diagramma: ciclo di Leave-One-Out Cross-Validation su molte configurazioni di iperparametri, che confluisce in "classificate per Q2" → selezione della configurazione migliore._

_**SPEACH**_ — Per la parte predittiva, ho eseguito una leave-one-out cross-validation su un gran numero di configurazioni di iperparametri, le ho classificate per punteggio Q2, che rappresenta con un valore numerico quanto il modello sia "migliore" rispetto ad una semplice media. Ho selezionato la configurazione con le prestazioni migliori come modello finale — lo chiamo PSCP, o "PSmileCapacityPredictor". %"che rappresenta con un valore numerico quanto il modello sia "migliore" rispetto ad una semplice media", controlla che questo che ho detto abbia senso, in caso riformula%

### 10. PSCP — Cosa Predice Davvero

_**POWERPOINT SLIDE**_ — _Riquadro input/output: input "polimero + molecola + concentrazione + pH" → PSCP → output "capacità di adsorbimento predetta"._

_**SPEACH**_ — Il modello PSCP trovato prende in input un polimero, una molecola target, la concentrazione e il pH, ne estrae le feature, scala gli input e restituisce in output una capacità di adsorbimento predetta. È quindi un unico modello che prova a riflette tutte le condizioni sperimentali che possano influenzare realmente l'adsorbimento nella pratica.

### 11. Featurizzare i Polimeri — Un Contributo Metodologico Reale

_**POWERPOINT SLIDE**_ — _Diagramma: unità ripetuta del polimero → SMILES del monomero → tappata con idrogeno → trattata come molecola → logP / SA score estratti con rdkit._

_**SPEACH**_ — Un problema pratico che ho dovuto risolvere: rdkit non supporta nativamente i polimeri, solo le molecole. La mia soluzione è stata prendere gli SMILES dei monomeri, "tapparli" con idrogeno e trattarli come molecole ordinarie, così da poter estrarre proprietà come il logP e il synthetic accessibility score. %Non sono sicuro di voler aggiungere questa slide%

### 12. Modellazione Predittiva — Risultati (Q2)

_**POWERPOINT SLIDE**_ — _Estratto della leaderboard da `RESULTS/mlp_experiments/q2_leaderboard.md`: prima riga `experiment_hd_16_8_4_4_4`, Q2 = 0,984, MAE = 1,50, RMSE = 6,49, più qualche riga successiva per contesto._

_**SPEACH**_ — La configurazione migliore ha raggiunto un Q2 di 0,984, con un errore assoluto medio di circa 1,5 e un RMSE di circa 6,5. Questo risultato è da considerarsi un "proof-of-concept" — dimostra che l'approccio può funzionare, ed è validato sui dati attualmente disponibili — ma il vero banco di prova della generalizzazione arriverà con altre misurazioni pubblicate. Ed è esattamente qui che il punto sulla scarsità di dati, sollevato qualche slide fa, torna a farsi sentire.

### 13. Filtraggio dei Polimeri — Criteri della Teoria FMO

_**POWERPOINT SLIDE**_ — _Quattro criteri di filtro come icone/etichette: logP alto (rimane insolubile), TPSA più alto (siti di legame polari), gap FMO intermolecolare più basso (forza di legame donatore-accettore), SA score più basso (sintetizzabile su scala)._

_**SPEACH**_ — Una volta ottenuti i polimeri candidati, li filtro usando la teoria degli orbitali molecolari di frontiera. Seleziono un logP alto in modo che il polimero rimanga solido e insolubile in acqua, un TPSA più alto per i siti di legame polari, un gap FMO intermolecolare più basso per un legame donatore-accettore più forte, e un SA score più basso così da essere realisticamente sintetizzabile su scala.

### 14. Validazione del Filtro — Coerente con la Chimica Nota

_**POWERPOINT SLIDE**_ — _Immagine della struttura del polimero di test sopravvissuto al filtro, evidenziando i suoi due sistemi aromatici (stirene + azobenzene)._

_**SPEACH**_ — Ciò che mi ha convinto che questo filtro stia facendo qualcosa di reale, e non solo numericamente comodo, è che il criterio del gap FMO seleziona implicitamente per aromaticità e coniugazione. Il polimero sopravvissuto al filtraggio nel mio caso di test ha due sistemi aromatici — stirene e azobenzene — esattamente ciò che ci si aspetterebbe dalla chimica del legame nota. Il comportamento implicito del filtro coincide con la teoria di dominio senza che io abbia codificato quella regola a mano.
% rimuovi qeusto capitolo, al massimo possiamo dire che il filtro è modulare, come il resto della pipeline, questo filtro proposto scarta molti polimeri, ma essendo in grado di generare 10.000 nuovi PSMILE nell'arco di poche ore, è possibile usare un filtro così "agrressivo" %

### 15. Esplorazione Non Supervisionata — Clustering Gerarchico

_**POWERPOINT SLIDE**_ — _Curva del silhouette score con picco a 63 cluster; miniatura del dendrogramma. Risultati riferiti a `RESULTS/ahc_clustering/`._

_**SPEACH**_ — Ho anche eseguito un clustering gerarchico agglomerativo sul dataset per esplorare la struttura nelle coppie polimero-molecola. Il silhouette score ha avuto un picco a 63 cluster, il che riflette quanto sia eterogeneo questo dataset — non è di per sé una segmentazione utile. Lo presento come uno strumento esplorativo e di interpretabilità, che aiuta a capire cosa guida i raggruppamenti nei dati, non come un risultato predittivo di rilievo.

### 16. La Pipeline Integrata Completa

_**POWERPOINT SLIDE**_ — _Diagramma di flusso: molecola target → SMILES → generazione candidati (mingpt) → filtro (FMO/logP/TPSA/SA) → predizione capacità (PSCP) → ciclo finché la capacità target è raggiunta o il budget è esaurito._

_**SPEACH**_ — Tutto questo confluisce in un'unica funzione che chiamo `find_polymer_for_target_molecule`. Le si dà una molecola target, lei la converte in SMILES, genera polimeri candidati, li filtra, ne predice la capacità e ripete il ciclo — proponendo altri candidati — finché non raggiunge la capacità target. La maggior parte dei compoenti della pipeline è inoltre modulare, ciò vuol dire che possiamo teoricamente accomodare futuri sviluppi, miglioramenti, diversi filtri e modelli di generazione e predizione.

### 17. Limiti — Dati & Validazione

_**POWERPOINT SLIDE**_ — _Lista a due colonne: "Dati" (scarsità, assenza di risultati negativi) / "Validazione" (nessuna conferma in laboratorio, solo computazionale)._

_**SPEACH**_ — Voglio essere diretto sui limiti. Primo, i dati: ci sono troppe poche misurazioni di capacità pubblicate per addestrare o validare in modo robusto il modello predittivo, e in particolare mancano dati di risultato negativo — polimeri che non adsorbono — che affinerebbero sia il filtro sia il modello. Secondo, la validazione: nulla di generato da questa pipeline è stato testato in laboratorio. Ogni risultato che ho mostrato è puramente computazionale.

% Mancano una/due slide sulla nuova parte di aquisizione dati tramite un altro tool che ho costruito "paper_scarper", che permette ottenere open access papers tramite OpenAlex, estrarre altri papar tramite Grodid, ed infine estrarre dai paper informazioni utili tramite LLM, testato con gemma, deepseek, kimi e claude opus. Dì che comunque mancano i paper in generale, ma con in futuro ci aspettiamo nuovi paper da cui ottenere dati, nuovi modelli LLM migliori e più efficenti così da accrescere di più il dataset PDCC %

### 18. Limiti — Ambito & Scelte di Modellazione

_**POWERPOINT SLIDE**_ — _Lista: dati sintetici PI1M vs PolyInfo proprietario; conversione P-SMILES manuale; solo polimero singolo, nessun composito._

_**SPEACH**_ — Ci sono anche alcuni limiti di ambito. Il modello generativo è stato addestrato sul dataset sintetico PI1M, non sul dataset proprietario PolyInfo da cui PI1M deriva, poiché non avevo accesso a quest'ultimo. Convertire i nomi grezzi dei materiali in SMILES è semplice grazie a PubChem, ma la conversione in P-SMILES è ancora manuale e limitata. E l'intera pipeline considera solo materiali a polimero singolo — nessun composito a doppio polimero o multi-materiale, per ora.

### 19. Sviluppi Futuri

_**POWERPOINT SLIDE**_ — _Lista in stile roadmap con icone: più dati (in particolare risultati negativi) → notazioni alternative (BigSmiles) → architetture GNN → accesso a PolyInfo → input multi-materiale._

_**SPEACH**_ — Guardando avanti, il prossimo passo a maggior valore è semplicemente più dati — in particolare risultati negativi — che migliorerebbero in modo significativo sia il filtro sia il modello predittivo. Oltre a questo, vorrei esplorare notazioni polimeriche alternative come BigSmiles se i dati lo permettono, provare architetture più complesse come le graph neural network una volta disponibili abbastanza dati da giustificarle, cercare l'accesso al dataset proprietario PolyInfo, ed estendere la pipeline a input multi-materiale e a doppio polimero.
