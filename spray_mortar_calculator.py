import streamlit as st

st.set_page_config(page_title="Mortier Pro – Coût & Fiche Technique", layout="centered")

st.title("🧱 Mortier Sec Projétable – Calculateur Complet")
st.caption("Par Omar 🇲🇦 — coût, dosage, fiche technique intégrée")

# 📥 Batch size input
st.markdown("### ⚖️ Taille du lot")
batch_kg = st.number_input("Taille du lot (kg)", min_value=25, value=1000, step=25)

# 🧱 Material prices
st.markdown("### 🔧 Prix des matériaux (MAD/tonne)")
cement_price = st.number_input("💠 Ciment (CEM II 42.5)", value=1300)
lime_price = st.number_input("🟩 Chaux aérienne", value=1800)
sand_price = st.number_input("🪨 Sable ES 47", value=120)
kaolin_price = st.number_input("🧼 Kaolin", value=150)
hydrofuge_price = st.number_input("💊 Hydrofuge Sika® Poudre (MAD/kg)", value=12)

# 📦 Overhead costs
st.markdown("### 📦 Coûts fixes (par tonne)")
packaging_cost = st.number_input("📦 Emballage", value=150)
labor_cost = st.number_input("👷 Main d'œuvre", value=100)
transport_cost = st.number_input("🚚 Transport", value=150)

# ⚙️ Ratios based on batch
cement_pct = 0.25
lime_pct = 0.03
kaolin_pct = 0.02
sand_pct = 0.70
hydrofuge_pct = 0.005  # 0.5% of cement

cement_kg = batch_kg * cement_pct
lime_kg = batch_kg * lime_pct
kaolin_kg = batch_kg * kaolin_pct
sand_kg = batch_kg * sand_pct
hydrofuge_kg = cement_kg * 0.01

# 💰 Cost calculations
material_cost = (
    (cement_kg / 1000) * cement_price +
    (lime_kg / 1000) * lime_price +
    (kaolin_kg / 1000) * kaolin_price +
    (sand_kg / 1000) * sand_price +
    (hydrofuge_kg / 1000) * hydrofuge_price
)

fixed_costs = packaging_cost + labor_cost + transport_cost
total_cost = material_cost + fixed_costs

# 📊 Output
st.markdown("### 📊 Coût Total")
st.write(f"💰 Coût total pour {batch_kg} kg : **{round(total_cost, 2)} MAD**")
st.write(f"📦 ≈ **{round(total_cost / batch_kg * 25, 2)} MAD** par sac de 25 kg")

# 📄 Fiche Technique
with st.expander("📄 Voir la Fiche Technique"):
    st.markdown(f"""
**Nom du produit** : Mortier sec prêt à projeter — haute adhérence et imperméabilité  
**Type** : Pré-mélange en poudre pour projection mécanique  
**Conditionnement** : Sacs de 25 kg  
**Stockage** : 12 mois à l’abri de l’humidité  
**Aspect** : Poudre beige-gris  
**Utilisation** : Façades, sous-enduits, murs intérieurs/extérieurs

---

### 🧪 Composition (pour {batch_kg} kg)

| Composant                  | Quantité (kg)  | Rôle                            |
|---------------------------|----------------|----------------------------------|
| Sable ES 47               | {sand_kg:.1f}     | Granulat                        |
| Ciment 42.5               | {cement_kg:.1f}   | Résistance                      |
| Chaux aérienne CL 90      | {lime_kg:.1f}     | Souplesse / perméabilité        |
| Kaolin                    | {kaolin_kg:.1f}   | Thixotropie / finesse           |
| Hydrofuge Sika® Poudre    | {hydrofuge_kg:.1f} | Imperméabilité / plasticité     |

---

### ⚙️ Caractéristiques Techniques

- Granulométrie ≤ 1.2 mm  
- Densité ~1.4 g/cm³  
- pH ~11–12  
- Eau d’ajout : ~5–6 L / sac  
- Rendement : ~18–20 kg/m² pour 10 mm  
- Adhérence élevée sur supports minéraux  
- Temps de travail ≥ 2h

---

### 🛠️ Mode d’emploi

1. Support propre, humidifié  
2. Mélange avec eau selon consistance  
3. Application par pompe ou machine à projeter  
4. Finition selon besoin : taloché, gratté, lissé
""")

# 🎨 Optional label preview
with st.expander("🎨 Étiquette Sack Preview"):
    st.text(f"""
MORTIER À PROJETER – 25 kg
Usage : Façade / Sous-enduit / Intérieur
Formulation : ES 47 / CEM II / CL 90 / Kaolin / Hydrofuge
Eau recommandée : 5–6 L
""")
