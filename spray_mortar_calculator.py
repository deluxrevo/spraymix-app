import streamlit as st

def calculate_mortar_mix(es_scnl, total_weight=1000, target_es=50, es_scl=77):
    if es_scnl >= target_es:
        scl_ratio = 0
        scnl_ratio = 1
    else:
        scl_ratio = (target_es - es_scnl) / (es_scl - es_scnl)
        scnl_ratio = 1 - scl_ratio
        if scl_ratio > 0.3:
            st.warning("⚠️ Le sable lavé nécessaire dépasse 30%. Pensez à une source plus propre.")

    sand_weight = total_weight * 0.7
    scnl_kg = round(sand_weight * scnl_ratio, 2)
    scl_kg = round(sand_weight * scl_ratio, 2)

    mix = {
        "SCNL (Sable Concassé Non Lavé)": f"{scnl_kg} kg",
        "SCL (Sable Lavé)": f"{scl_kg} kg",
        "CEM II 42.5": f"{total_weight * 0.26:.2f} kg",
        "Chaux Hydratée": f"{total_weight * 0.04:.2f} kg",
        "HPMC (Cellulose Ether)": f"{total_weight * 0.006:.2f} kg",
        "RDP (Poudre Polymère)": f"{total_weight * 0.008:.2f} kg",
        "Superplastifiant (PCE)": f"{total_weight * 0.0025:.2f} kg",
        "Fibres PP (Optionnelles)": f"{total_weight * 0.001:.2f} kg",
        "Retardateur (Usage Été)": f"{total_weight * 0.0005:.2f} kg"
    }

    st.subheader("🔧 Recette Optimale pour 1 Tonne de Mortier Projeté:")
    for k, v in mix.items():
        st.write(f"- {k}: {v}")

# Streamlit UI
st.set_page_config(page_title="Spray Mortar Calculator", layout="centered")
st.title("🧱 Calculateur Mortier Projeté")
st.caption("Optimise ta recette selon l'indice ES du sable – by Omar 🇲🇦")

es_value = st.slider("🧪 Valeur ES du Sable Actuel", 30, 77, 40)
target_es = st.slider("🎯 ES Ciblé", 45, 55, 50)
total_batch = st.number_input("⚖️ Poids Total du Mélange (kg)", value=1000)

if st.button("Calculer la Recette"):
    calculate_mortar_mix(es_scnl=es_value, total_weight=total_batch, target_es=target_es)