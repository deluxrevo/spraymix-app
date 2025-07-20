import streamlit as st

def calculate_mortar_mix(total_weight, cement_percent, lime_percent, hpmc_percent):
    # Calculate weights for each component
    cement_kg = round(total_weight * cement_percent / 100, 2)
    lime_kg = round(total_weight * lime_percent / 100, 2)
    hpmc_kg = round(total_weight * hpmc_percent / 100, 2)
    
    # Calculate crushed sand as remainder
    sand_percent = 100 - cement_percent - lime_percent - hpmc_percent
    sand_kg = round(total_weight * sand_percent / 100, 2)
    
    # Display the mix breakdown
    st.subheader("🔧 Cost-Effective Spray Mortar Recipe:")
    st.write(f"**Total Batch Weight:** {total_weight} kg")
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Component**")
        st.write("Cement")
        if lime_percent > 0:
            st.write("Lime (optional)")
        st.write("HPMC (Cellulose Ether)")
        st.write("Mined Crushed Sand")
        
    with col2:
        st.write("**Weight**")
        st.write(f"{cement_kg} kg ({cement_percent}%)")
        if lime_percent > 0:
            st.write(f"{lime_kg} kg ({lime_percent}%)")
        st.write(f"{hpmc_kg} kg ({hpmc_percent}%)")
        st.write(f"{sand_kg} kg ({sand_percent}%)")
    
    # Show total verification
    total_calculated = cement_kg + lime_kg + hpmc_kg + sand_kg
    st.write("---")
    st.write(f"**Total Calculated:** {total_calculated} kg")

# Streamlit UI
st.set_page_config(page_title="Spray Mortar Calculator", layout="centered")
st.title("🧱 Spray Mortar Calculator")
st.caption("Cost-effective minimalist recipe for façade/wall renders")

st.markdown("### Mix Configuration")

# Input controls for batch weight and percentages
total_batch = st.number_input("Total Batch Weight (kg)", value=1000, min_value=1, step=1)

col1, col2 = st.columns(2)

with col1:
    cement_percent = st.slider("Cement %", 10.0, 40.0, 25.0, 0.5)
    lime_percent = st.slider("Lime % (optional)", 0.0, 10.0, 3.0, 0.5)
    
with col2:
    hpmc_percent = st.slider("HPMC (Cellulose Ether) %", 0.1, 2.0, 0.6, 0.1)
    
    # Calculate and display remaining percentage for sand
    remaining = 100 - cement_percent - lime_percent - hpmc_percent
    st.metric("Crushed Sand %", f"{remaining:.1f}%")

# Validation
if remaining < 0:
    st.error("⚠️ Total percentages exceed 100%. Please adjust the values.")
elif remaining < 40:
    st.warning("⚠️ Sand percentage is quite low. Consider reducing other components.")

st.write("---")

if st.button("Calculate Recipe"):
    if remaining >= 0:
        calculate_mortar_mix(total_batch, cement_percent, lime_percent, hpmc_percent)
    else:
        st.error("Cannot calculate: Total percentages exceed 100%")
