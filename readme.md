#   Introduction

Accurately predicting the pathogenicity of genetic variants is critical for understanding disease mechanisms and improving clinical decision-making. While variants in coding regions are relatively well-studied, interpreting variants in noncoding regions remains a major challenge due to their complex regulatory roles.
Recent advances in deep learning, particularly transformer-based models trained on multiple sequence alignments (MSA), enable the extraction of rich, evolutionarily informed genomic representations. In this project, we leverage GPN-MSA embeddings to capture both local sequence context and cross-species conservation for variant classification.
Our objective is to build a machine learning model that predicts variant pathogenicity using these embeddings, while evaluating performance differences between coding and noncoding regions.

# Getting Started
- Python 3.7+
- pip (Python package installer)

### Clone the Repository
```bash
git clone https://github.com/Anskira/Predicting-the-pathogenecity-of-genetic-variants.git
```

### Install the required packages
```bash
   pip install -r requirements.txt
```

# Data Information
## ClinVar Dataset

We used the ClinVar database as the primary source of labeled genetic variants.

ClinVar is a publicly available resource that aggregates information about genomic variants and their relationships to human health. Each variant is annotated with clinical significance labels such as benign, likely benign, pathogenic, or likely pathogenic.

For this project:

We extracted variants with clear pathogenicity labels
Selected key features: CHROM, POS, REF, ALT, Pathogenicity
Combined both coding and noncoding variants
Converted labels into a binary classification task (benign vs pathogenic)

One key challenge with this dataset is class imbalance, where benign variants significantly outnumber pathogenic ones.

## GPN-MSA Dataset (89.zarr)

We used the 89-species multiple sequence alignment (MSA) dataset (89.zarr) to generate embeddings using GPN-MSA.

This dataset contains aligned genomic sequences from 89 different species, allowing the model to capture evolutionary conservation and context across species.

Key characteristics:
Stored in Zarr format for efficient large-scale access
Provides multi-species alignment at nucleotide resolution
Enables extraction of sequence windows around genomic positions
Used as input to the GPN-MSA model for embedding generation
How it was used:
For each variant, a 128-nucleotide window centered around the variant position was extracted
The aligned sequences were passed into the GPN-MSA model
Generated embeddings of size (128 × 768)
The center position embedding was used to represent the variant

# Data Processing

- Extracted relevant features from the ClinVar dataset: CHROM, POS, REF, ALT, Pathogenicity
- Converted labels into binary format (benign vs pathogenic)
- Combined coding and noncoding variants into a single dataset and shuffled
- For each variant, a 128-length genomic window centered at the variant position was extracted from the 89-species MSA dataset
- Generated embeddings using GPN-MSA, producing vectors of size (128 × 768)
- Used the center embedding to represent each variant
- Processed data in batches and stored embeddings as .pt files for efficient reuse
- Split embedding files into train and test sets for model training

# Model training
- Trained a feedforward neural network on GPN-MSA embeddings to classify variants as benign or pathogenic
- Used the center embedding (768-dim) from each sequence as the model input
- Applied binary cross-entropy loss with class weights to address class imbalance
- Optimized using Adam optimizer with a learning rate scheduler
- Trained with a train–validation split and implemented early stopping based on loss convergence
- Evaluated performance using:
   1. Accuracy
   2. Precision & Recall
   3. Matthews Correlation Coefficient (MCC)
- Tuned the prediction threshold on validation data to improve precision–recall trade-off

# Results & Discussion

- 
