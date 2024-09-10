# %%
import pandas as pd

# %%
# Falta incluir qual o número de placa
df = pd.read_excel("Plate Specs SO 20466258.xlsx")

for nome, grupo in df.groupby("Plate Barcode"):
    grupo.to_csv(f"{nome}.tsv", sep='\t', index=False)