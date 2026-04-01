

# Thesis Summary

This is a really simple an brief summary of each chapter in my thesis.

To build the pdf locally run the following commands:
1. `pdflatex -output-directory=build main.tex`
2. `bibtex build/main`
3. `pdflatex -output-directory=build main.tex`
4. `pdflatex -output-directory=build main.tex`

All in one:
`pdflatex -output-directory=build main.tex; bibtex build/main; pdflatex -output-directory=build main.tex; pdflatex -output-directory=build main.tex`

# Introduction

Here's what I've done for my master thesis.

I have created a mingpt wrapper to generate new valid smiles and polymer smiles given a dataset of them. Note that the p-smiles dataset was syntetic. 

I have scraped many papers, that talk about polymer-molecule interaction, specifically they use a polymer to absorb one or more molecule in water, mosty wastewater. I searched for data with the following metrics, to train my ML model.
- PH: ph of the water that the sponge and compound was placed in.
- CONCENTRATION: ${\text{mg} \over \text{L}}$
- CAPACITY: ${\text{mg} \over \text{g}}$
Where the CONCENTRATION is the starting amount of the pharmaceutical in the water before the polymer is added.
And the CAPACITY measures how many milligrams of the pollutant were absorbed by every single gram of the polymer material used.
My hope was that with sufficient data, we might be able to train a model capable of predicting the CAPACITY, given a new polymer-molecule couple. However the data is really scarse, so at the moment this is not possible.

I augmented the data, using interpolation where possible
I used rdkit, polymetrix and tblite to obtain many features from the data.

I made MANY experiments with the MLP and the "few" data I menaged to procure.
I used k-fold cross validation with varying hyperparameters to see how the model would do.

----

# Problem Description

Description of the problem tachled, and a focused biology background

----

# Machine Learning Architectures

Description of the machine learning models used.


----

# Data Acquisisition and Feature Engineering

I searched for many different papers, and scraped them for data. And saved all the data in the 'polymer_drug_concentration_capacity.csv' (each paper's link is in the SOURCE, I will copy all of their citings properly later)

I've created the PDCC dataclass, representing the dataset, and useful methods.

I've created the MLP dataclass, representing the model, and useful methods.

I've create the featurizer with an Options dataclass to list all possible features that we can extract from just the SMILES and P-SMILES using well-knwown python libraries

Finally I've create the Experiment dataclass with an extensive configuration. So I could test different interpolation methods

----

# Generative Modeling for Molecular Discovery

I have created a mingpt wrapper to generate new valid smiles and polymer smiles given a dataset of them. Note that the p-smiles dataset was syntetic.

I've tested with both the genration of SMILES (ZINC_base dataset) and PSMILES (PI1M syntetic dataset)
As a test: for SMILES I've generated 12800 molecules and only 5525 of them are novel and valid (Footnote see: `lele-py-bioinformatics\SMILES_checkpoints\2026_02_07_110058_333737\generate_mnt128_t100000000\2026_02_10_103702_472515`)
For P-SMIELS I've generated 12800 molecules and only 7373 of them are novel and valid. (Footnote see: `lele-py-bioinformatics\PSMILES_checkpoints\2026_02_07_121136_450914\generate_mnt128_t100000000\2026_02_10_094417_233255`)

So we have a model that can generate novel, and valid p-smiles, this is one part of the whole process, that will allow us to generate and find novel polymer that can bind to a specific molecule of our choosing.

----

# Predictive Modeling of Adsorption Capacity

To test the ability of a simple model to predict the CAPACITY, given the polymer features, molecule features, as well as the WATER_PH and CONCENTRATION, I tried to use a small MLP (Multi-Layer Perceptron).

First of all to get the most from this model, and the few gathered data, I experimented with many different hyperparamenters and evaluated their LOOCV (leave one out cross validation). I then calculated for each experiment its Q2 score, and took the same hyperparameters of the best-ranking one. From those I finalized the PeeSmileCapacity model.

I then trained the PSCP model on all the available data. This models takes in input a polymer (p-smiles), a molecule (smiles), the CONCENTRATION and WATER_PH, it first extracts the fetures from polymer and molecule, then it scales the input, and if finally outputs the predicted CAPACITY.

Note! While featurizing the molecule is straigh forwars as all python library used account for them, featurize polymers is a little more treaky, as for example the most used bio-informatic library rdkit, does not account for them, so to get the features like logp and SA score from them I had to "convert" each polymer into a molecule, meaning I studied only the monomer_smiles for each molecule and capped it with hydrogen atoms.

----

# Polymer Filtering

From different papars we found that usually polymers that we search for (polymers that can absorb specific molecules in water) have some disting features. Namely:

High logp: high enough to remain a solid, insoluble phase

Higher TPSA: more polar sites to grab residues

Lower intermolecular FMO gap: better for strong binding!

Lower SA score: the polymer must be easily synthesizable at scale!

FMO (Frontier Molecular Orbital) Theory
Having the HOMO and LUMO energies for both the polymer and the target drug unlocks a very powerful concept in computational chemistry called Frontier Molecular Orbital (FMO) Theory.
Instead of looking at the internal stability of the polymer (its own HOMO-LUMO gap), you can use these four values to predict how strongly the polymer and the drug will bind to each other via electron sharing (like π−π stacking or charge-transfer complexes).
The Science: Intermolecular FMO Gaps
When two molecules interact, one typically acts as an electron "donor" and the other as an electron "acceptor." The interaction is strongest when the energy level of the donor's highest occupied orbital (HOMO) is very close to the acceptor's lowest unoccupied orbital (LUMO).
You have two possible interactions here:
    Polymer donates to Drug: ΔE1​=∣ELUMO, drug​−EHOMO, poly​∣
    Drug donates to Polymer: ΔE2​=∣ELUMO, poly​−EHOMO, drug​∣
The smaller of these two gaps represents the dominant interaction pathway. If this "cross-gap" is small, the polymer and the drug will have a strong electronic affinity for one another—exactly what you want for a wastewater sponge!

Check for aromatic ring althoug I did not actually need this filter, because I already built a trap for aromatic rings.
The FMO (Frontier Molecular Orbital) gap filter is currently doing the heavy lifting. How do molecules achieve small HOMO-LUMO gaps that allow for strong donor-acceptor interactions? By having highly conjugated π-electron systems—which almost exclusively means aromatic rings.
The FMO filter already implicitly screens for aromaticity. It's the reason the surviving polymer from your last test had two massive benzene rings (a styrene group and an azobenzene group). The quantum math naturally selected them.

----

# Untrained Model: Agglomerative Hierarchical Clustering

I used an Agglomerative Hierarchical Clustering (AHC) pipeline, to provide insight into how the data points (drugs/polymers) were grouped and which features drive those groupings.

I first tried to find the optimal cluster count for my specific dataset, using the ononomim function, the result is that to get the highest Silhouette Score we would need 63 different clusters. This is to be expected since there is a high heterogenity in polymer-drug pairs. This high segmentation is not really useful.

I also tested with an arbitrary number of clusters. The results of this pipeline can be found in the `RESULTS/ahc_clustering`.

----

# Final Result

As the final result I put it all toghter creating the `find_polymer_for_target_molecule` function.

1. It requires as an input a target molecule (like "aspirin", "ibuprofen", ...). And convert it into SMILES notation.
2. It uses the PeeSmileGenerator (based on the mingpt model) to create a vast array of polymers.
3. It uses the PeeSmileFilter to disacard the one that we consider incapable of adsorption.
4. It uses the PeeSmileCapacityPredictor (MLP model) to predict the capacity of the polymer with the molecule.
5. If the predicted capacity is higher that a certain target capacity (default: `1.0`) it outputs the polymer found, and create two graphs: one that show how the prediction changes by changing the initial concentration, and onother that shows how the prediction changes with different whater Ph. If the target capacity is not reached, the loop will start over and the PeeSmileGenerator will create a new batch of polymers to test.

The `find_polymer_for_target_molecule` function takes in input many possible options, that can be changed.
The filter can be made more (or less) strict.
The target capacity can be increased.
The water ph can be changed.
The function uses sensible defaults to be used more easily.


----

# Conclusion and Future Work

The first thing that need to be addressed in any future work, using this "framework"/"pipeline" is the scarsity of experiment results, to see the adsorption of the polymer for specific molecules, for many different polymers, molecules, and in different waters. Not only good results, but also failures, so many data of polymers that do not absorb specific molecules.

This pipeline assumes that the polymers are all represented in a p-smiles string notation. If data emerges, it could be interesting see the results using diffrent notations, suchs as BigSmiles.

If given more data we could also study if there are some useless or redundant features. As well as try to use different, more-complex model architecutures. For example GNN.

The PeeSmileGenerative model was trained on syntethic data (Pl1M dataset), there exists a propietary dataset "PolyInfo" that require access, but containes many real-polymer data. Pl1M was generated from that dataset.

The dataset is not automatically converted to SMILES and P-SMILES string but it only reports the material used and the target molecule. The conversion from a molecule to a SMILES string is straightforward, each of them is registered in the PubChem database. However for polymers the conversion to P-SMILES is not so straightforward, and my ability to do so is very limited. I made it possible and easy to change the representation of each material. (See `bio.__global__`)

Lastly in this study we only used polymers, but many studies tried the use of many different materials, and dual-polymers. If possible a multi-format input could be of interest.
