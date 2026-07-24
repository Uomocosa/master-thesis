# FAQ — Domande di preparazione alla discussione

Raccolta di domande concettuali sulla tesi, con risposte legate al lavoro svolto.

---

### Assorbimento vs Adsorbimento

***Qual è la differenza tra "assorbente" e "adsorbente"?***

Sono due fenomeni diversi, spesso confusi perché differiscono per una sola lettera. La differenza è **dove finisce la sostanza catturata**:

| | **Assorbimento** (ab-) | **Adsorbimento** (ad-) |
|---|---|---|
| **Cosa succede** | La sostanza penetra **dentro il volume** del materiale | La sostanza aderisce **sulla superficie** del materiale |
| **Natura** | Fenomeno di **volume** (bulk / 3D) | Fenomeno di **superficie** (2D) |
| **Analogia** | Una spugna che si imbeve d'acqua | Il vapore che si condensa sul vetro; polvere che si attacca a un panno |
| **Legame** | La molecola si dissolve/distribuisce nella massa | Van der Waals (fisisorbimento) o legami chimici (chemisorbimento) sui **siti attivi** superficiali |
| **Etimologia** | latino *absorbere* = "inghiottire, assorbire dentro" | latino *ad-* = "verso/su" + *sorbere* |

**In sintesi:** nell'**ass**orbimento la sostanza entra e si distribuisce **nel volume** (come l'acqua in una spugna); nell'**ads**orbimento le molecole si **fissano sulla superficie**, sui siti di legame, senza penetrare la massa del materiale.

**Perché conta per la tesi.** I polimeri — le "spugne molecolari" — lavorano per **adsorbimento**: le molecole inquinanti si legano ai **siti attivi sulla superficie** del polimero. Per questo:

- i candidati sono filtrati con la **teoria FMO** (gap donatore-accettore, TPSA per i siti polari): si ottimizza proprio il **legame superficiale**, tipico dell'adsorbimento;
- il modello predice la **capacità di adsorbimento** in funzione di concentrazione e pH — grandezze legate all'**equilibrio superficie/soluzione** (isoterme tipo Langmuir/Freundlich), non a un assorbimento di volume.

⚠️ **Attenzione al termine "spugna":** l'analogia suggerisce *ass*orbimento (l'acqua entra nel volume), ma i materiali catturano gli inquinanti per *ads*orbimento superficiale. È solo un'immagine divulgativa — il meccanismo reale è l'adsorbimento.

---

### Definizione di pH

***Che cos'è il pH?***

Il **pH** è una misura dell'**acidità o basicità** di una soluzione acquosa. Formalmente è il **logaritmo decimale negativo della concentrazione (attività) degli ioni idrogeno** H⁺ (più precisamente H₃O⁺):

$$pH = -\log_{10}[H^+]$$

dove $[H^+]$ è la concentrazione di ioni idrogeno in **mol/L**.

**Come si legge la scala** (da 0 a 14 a 25 °C):

| pH | Carattere | Esempi |
|---|---|---|
| **< 7** | **Acido** | succo di limone (~2), aceto (~3) |
| **= 7** | **Neutro** | acqua pura |
| **> 7** | **Basico (alcalino)** | bicarbonato (~9), candeggina (~13) |

Punti chiave:

- **È una scala logaritmica:** ogni unità di pH corrisponde a un fattore **×10** nella concentrazione di H⁺. Una soluzione a pH 4 è dieci volte più acida di una a pH 5, cento volte più di una a pH 6.
- **Più H⁺ → pH più basso** (per via del segno negativo): tanti ioni idrogeno = soluzione acida = pH basso.
- Nell'acqua vale sempre $[H^+]\cdot[OH^-] = 10^{-14}$ (a 25 °C): al neutro $[H^+]=[OH^-]=10^{-7}$ → pH 7.

**Perché il pH è rilevante nella tesi.** Il pH non è un dettaglio secondario, è una **feature di input del modello**:

- nel dataset **PDCC** il pH è associato a ogni misura di polimero–molecola–concentrazione–capacità;
- il modello predittivo **PSCP** prende in input polimero, molecola target, concentrazione **e pH**, e restituisce la capacità di adsorbimento.

Il motivo chimico è che il pH governa lo **stato di protonazione** sia del polimero sia della molecola inquinante: cambia le cariche superficiali, i siti di legame polari e quindi la forza dell'interazione donatore–accettore su cui si basa l'adsorbimento. Lo stesso polimero può adsorbire bene una molecola a un certo pH e male a un altro — per questo il pH entra esplicitamente tra le variabili del modello.

---

### Criteri di filtraggio: TPSA, LogP, SA score e gap FMO

***Cosa sono TPSA, LogP, SA score e gap FMO, e perché ci interessano?***

Sono i quattro criteri con cui i polimeri candidati vengono filtrati dopo la generazione (teoria FMO).

**LogP — Coefficiente di ripartizione (idrofobicità).** È il logaritmo del coefficiente di ripartizione tra ottanolo e acqua:

$$\text{logP} = \log_{10}\frac{[\text{sostanza}]_{\text{ottanolo}}}{[\text{sostanza}]_{\text{acqua}}}$$

Misura quanto una molecola "preferisce" un ambiente apolare rispetto all'acqua: **logP alto → idrofobica** (poco solubile), **logP basso → idrofila**. Il polimero deve funzionare come adsorbente **insolubile**: se fosse idrofilo si scioglierebbe e non sarebbe recuperabile. Serve un logP abbastanza alto da restare in fase solida, ma non così alto da perdere affinità per l'inquinante disciolto. **Soglia: logP ≥ 1,5.**

**TPSA — Topological Polar Surface Area.** È la somma delle aree superficiali degli atomi polari (principalmente **N, O** e gli H a essi legati), in **Å²**, calcolata dalla struttura 2D. Indica quanti gruppi polari possiede la molecola, cioè la sua capacità di fare legami idrogeno e interazioni elettrostatiche. L'adsorbimento avviene sui **siti polari** della superficie: un TPSA più alto significa più punti di legame disponibili. **Soglia: TPSA ≥ 60 Å².**

> *logP e TPSA tirano in direzioni opposte — l'uno vuole idrofobicità, l'altro polarità. Il filtro cerca l'equilibrio: un polimero solido ma con siti polari attivi.*

**SA score — Synthetic Accessibility.** Stima quanto è **difficile sintetizzare** una molecola, su scala **1 (facile) – 10 (difficile)**, dalle caratteristiche strutturali. Il modello generativo può proporre strutture valide ma impossibili o costosissime da sintetizzare; un adsorbente per acque reflue deve essere producibile **su scala**. Il filtro scarta i candidati troppo complessi. **Soglia: SA score ≤ 4,5.**

**Gap FMO — Frontier Molecular Orbital gap.** È il criterio più importante. Ogni molecola ha due orbitali di frontiera:

- **HOMO** (*Highest Occupied Molecular Orbital*) — orbitale occupato di energia più alta: da qui la molecola **cede** elettroni → **donatore**;
- **LUMO** (*Lowest Unoccupied Molecular Orbital*) — orbitale vuoto di energia più bassa: qui la molecola **accetta** elettroni → **accettore**.

L'interazione è tanto più forte quanto più vicini in energia sono l'HOMO di una molecola e il LUMO dell'altra. Si calcolano i due possibili canali:

$$\Delta E_1 = \lvert E_{\text{LUMO, molecola}} - E_{\text{HOMO, polimero}}\rvert \qquad \Delta E_2 = \lvert E_{\text{LUMO, polimero}} - E_{\text{HOMO, molecola}}\rvert$$

Il gap FMO rilevante è il **più piccolo dei due** (il canale dominante). Un gap piccolo = orbitali vicini = **forte accoppiamento elettronico** = legame donatore–accettore forte = adsorbimento efficace. **Soglia: gap FMO ≤ 4,0 eV.**

**Quadro d'insieme:**

| Criterio | Cosa garantisce | Direzione | Soglia |
|---|---|---|---|
| **logP** | resta **solido/insolubile** in acqua | alto | ≥ 1,5 |
| **TPSA** | ha **siti polari** per legarsi | alto | ≥ 60 Å² |
| **gap FMO** | **legame** donatore–accettore forte | basso | ≤ 4,0 eV |
| **SA score** | è **sintetizzabile** su scala | basso | ≤ 4,5 |

Questi filtri sono **fisicamente interpretabili** e **complementari al machine learning**: riducono drasticamente lo spazio dei candidati generati (decine di migliaia) usando principi chimici solidi, così il modello predittivo — più costoso e incerto per via della scarsità di dati — lavora solo sui polimeri già chimicamente sensati. È il punto in cui la pipeline combina **domain knowledge** (i filtri) e **pattern data-driven** (PSCP).

---

### Leave-One-Out Cross-Validation (LOOCV)

***Come abbiamo usato il LOOCV e come funziona il metodo stesso?***

**Come funziona.** Il **Leave-One-Out Cross-Validation** è il caso estremo della K-fold cross-validation, quello in cui il numero di fold è uguale al numero di dati ($K = n$). Con un dataset di $n$ osservazioni:

1. Metti da parte **una sola osservazione** (il "left-out") come test.
2. Addestri il modello su **tutte le altre $n-1$** osservazioni.
3. Predici quell'unica osservazione tenuta fuori e registri l'errore.
4. **Ripeti per ogni osservazione**: ognuna, a turno, fa da test una volta.
5. Ottieni $n$ predizioni "out-of-sample" (una per punto) da cui calcoli le metriche.

**Perché è utile per dataset piccoli** (il caso del PDCC, poche centinaia di osservazioni):

- **massimizza i dati di training** — in ogni iterazione il modello vede $n-1$ punti, quasi tutto il dataset;
- dà una **stima quasi non distorta** dell'errore di generalizzazione, perché ogni predizione è su un punto mai visto in addestramento;
- **svantaggio:** è costoso — il modello va addestrato $n$ volte (ma con poche centinaia di punti resta fattibile).

**Come è stato usato nella tesi.** Il LOOCV è stato la metodologia di valutazione primaria, con due scopi combinati:

- **Ricerca degli iperparametri** — è stato esplorato un ampio spazio (learning rate, numero di epoche, batch size, sottoinsiemi di feature, configurazioni di data augmentation). Per **ogni configurazione** è stato eseguito un intero ciclo LOOCV e calcolato il Q². Le configurazioni sono state ordinate per Q² (leaderboard `tab:q2_leaderboard`) e la migliore selezionata come modello finale, il **PSCP** (`hd_16_8_4_4_4`, **Q² = 0,984**).
- **Metrica risultante** — il Q² si legge dalle predizioni out-of-sample del LOOCV.

⚠️ **Il caveat cruciale (dichiarato esplicitamente nella tesi).** Il Q² di 0,984 in LOOCV **sopravvaluta** la reale capacità di generalizzazione: i dati contengono **curve di adsorbimento** (più punti per la stessa coppia polimero–molecola). Lasciando fuori un solo punto, gli altri della stessa curva restano nel training, quindi il modello sta facendo **interpolazione lungo una curva parzialmente osservata**, non **estrapolazione** a coppie nuove. Il Capitolo 6 rivaluta lo stesso modello con protocolli più severi (*grouped* e *fixed-test*) e mostra che quella generalizzazione **non regge**: il risultato è un **proof-of-concept**, limitato dalla scarsità di dati.

---

### Metriche: Q², MAE e RMSE

***Puoi spiegare nel dettaglio Q², MAE e RMSE?***

Sono le tre colonne della leaderboard (`tab:q2_leaderboard`). MAE e RMSE misurano **quanto** il modello sbaglia; Q² misura **quanto è informativo** rispetto a una previsione banale. Valori del modello migliore (`hd_16_8_4_4_4`): Q² = 0,984, MAE = 1,499, RMSE = 6,485.

**MAE — Mean Absolute Error.** Media degli errori in valore assoluto:

$$\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}\lvert y_i - \hat{y}_i\rvert$$

È nella **stessa unità del target** (capacità, mg/g): MAE = 1,499 significa "in media il modello sbaglia di ~1,5 unità". Facile da interpretare ed **robusto agli outlier** (un errore di 10 pesa 10 volte uno di 1, non di più).

**RMSE — Root Mean Squared Error.** Radice della media degli errori al quadrato:

$$\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

Anch'esso in mg/g, ma **penalizza pesantemente gli errori grandi**: un errore di 10 pesa **100 volte** uno di 1, quindi è molto sensibile agli outlier. Vale sempre **RMSE ≥ MAE**, e il divario tra i due è informativo: se RMSE ≈ MAE gli errori sono uniformi; se **RMSE ≫ MAE** ci sono pochi errori molto grandi. Nel modello migliore RMSE (6,485) è **>4 volte** il MAE (1,499): il modello è quasi sempre molto preciso ma sbaglia clamorosamente su pochi punti difficili.

**Q² — Coefficiente di determinazione predittivo.** Non misura l'errore assoluto ma **quanto il modello è migliore di predire sempre la media**. È l'analogo dell'R², calcolato sulle predizioni out-of-sample del LOOCV:

$$Q^2 = 1 - \frac{\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}{\sum_{i=1}^{n}(y_i - \bar{y})^2}$$

Il numeratore è l'errore del modello; il denominatore è l'errore del modello banale che predice sempre la media (la varianza totale). Il rapporto è la frazione di errore che resta; **1 meno** quel rapporto = frazione di varianza spiegata.

| Q² | Significato |
|---|---|
| **= 1** | Predizione **perfetta** (errore nullo) |
| **> 0** | Il modello è **migliore** della semplice media |
| **= 0** | Il modello **non fa meglio** di predire la media |
| **< 0** | Il modello è **peggio** della media (possibile out-of-sample) |

È **adimensionale e normalizzato**, quindi permette di confrontare configurazioni diverse (motivo per cui la leaderboard è ordinata per Q²). Valore = 0,984 → il modello spiega ~98,4% della varianza. Si chiama **Q²** e non R² perché usa le predizioni della cross-validation (punti mai visti), non il fit sul training: per questo può diventare **negativo**, cosa che l'R² sul training non fa mai.

**Perché usarle tutte e tre:**

| Metrica | Unità | Cosa cattura | Punto debole |
|---|---|---|---|
| **MAE** | mg/g | errore **tipico**, interpretabile | non distingue "sbaglia sempre poco" da "sbaglia molto ogni tanto" |
| **RMSE** | mg/g | errore che **penalizza i grossi sbagli** | dominato dagli outlier |
| **Q²** | — (0…1) | **quanto è informativo** vs. media; confrontabile tra modelli | non dice l'errore assoluto in mg/g |

Sono complementari: Q² dice "il modello è molto migliore del nulla" (0,984), MAE dà l'errore pratico (~1,5 mg/g), e il gap RMSE–MAE avverte che "ci sono pochi casi su cui sbaglio parecchio". Riportarle tutte e tre è buona pratica: una sola racconterebbe una storia incompleta.
