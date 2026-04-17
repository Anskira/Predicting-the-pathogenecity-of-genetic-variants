import streamlit as st
import torch
import torch.nn as nn
import pandas as pd
import os

# -------- CONFIG --------
EMBEDDING_DIR = "/blue/egn6933/apatil2/embeddings/"
MODEL_PATH = "/blue/egn6933/apatil2/model_checkpoints/complex_model_val/model_epoch_25.pt"
THRESHOLD = 0.45

# -------- MODEL DEFINITION --------
# Must match the architecture used during training
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(768, 512),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, 1)
        )

    def forward(self, x):
        x = torch.nn.functional.normalize(x, dim=1)
        return self.model(x)

# -------- LOAD DATA --------
@st.cache_data
def load_dataframe():
    return pd.read_csv("combined_df.csv")

@st.cache_resource
def load_model():
    # Instantiate the model architecture first
    model = MLP()
    # Load the saved state dict (OrderedDict of weights) into it
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model

df = load_dataframe()
model = load_model()

# -------- UI --------
st.title("Genomic Variant Pathogenicity Predictor")
st.markdown("Select a variant from the ClinVar dataset to predict its pathogenicity.")

idx = st.number_input("Select Variant Index", min_value=0, max_value=len(df) - 1, step=1)
row = df.iloc[idx]

st.write("### Variant Info")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Chromosome", row["CHROM"])
col2.metric("Position", row["POS"])
col3.metric("REF", row["REF"])
col4.metric("ALT", row["ALT"])

# Show ground truth label if available
if "label" in df.columns:
    true_label = "Pathogenic" if row["label"] == 1 else "Benign"
    st.info(f"Ground Truth Label: **{true_label}**")

# -------- PREDICTION --------
if st.button("Predict Pathogenicity"):
    file_idx = (idx // 256) * 256
    pos_in_file = idx % 256
    file_path = os.path.join(EMBEDDING_DIR, f"embeddings_batch_{file_idx}.pt")

    with st.spinner("Loading embedding and running model..."):
        tensor = torch.load(file_path, map_location="cpu")

        # tensor shape: (batch_size, seq_len, hidden_dim)
        # Taking center position (index 64) as the variant embedding
        embedding = tensor['X'][pos_in_file, 64, :]
        embedding = embedding.unsqueeze(0).float()

        with torch.no_grad():
            output = model(embedding).squeeze()
            prob = torch.sigmoid(output).numpy()

    st.write("### Prediction Result")
    if prob >= THRESHOLD:
        st.error(f"🔴 **Pathogenic**")
    else:
        st.success(f"🟢 **Benign**")

    # st.progress(prob)
    st.write(f"**Model Confidence Score:** `{prob:.3f}`")
    st.caption(f"Decision threshold: {THRESHOLD}")