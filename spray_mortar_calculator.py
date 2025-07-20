import streamlit as st

# --- ES Calculation Helper ---
def calculate_es(sieve_percentages):
    # ES = sum of % retained on 0.25mm + 0.125mm + 0.063mm (commonly used norm)
    if len(sieve_percentages) < 7:
        return None
    try:
        es = sieve_percentages[3] + sieve_percentages[4] + sieve_percentages[5]
        return round(es, 1)
    except Exception:
        return None

# --- Sand Blending Calculator ---
def sand_blend_ratio(es_unclean, es_clean, es_target):
    if es_clean == es_unclean:
        return 0, 1, "Clean and unclean sand have the same ES. Any ratio is OK."
    elif es_target <= es_unclean:
        return 0, 1, "Your unclean sand already meets or exceeds the target ES! No clean sand needed."
    else:
        ratio_clean = (es_target - es_unclean) / (es_clean - es_unclean)
        ratio_clean = max(0, min(ratio_clean, 1))
        ratio_unclean = 1 - ratio_clean
        return ratio_clean, ratio_unclean, None

# --- Main Mortar Mix Calculation ---
def calculate_mortar_mix(total_weight, cement_percent, lime_percent, hpmc_percent):
    cement_kg = round(total_weight * cement_percent / 100, 2)
    lime_kg = round(total_weight * lime_percent / 100, 2)
    hpmc_kg = round(total_weight * hpmc_percent / 100, 2)
    sand_percent = 100 - cement_percent - lime_percent - hpmc_percent
    sand_kg = round(total_weight * sand_percent / 100, 2)

    st.subheader("🔧 Spray Mortar Recipe:")
    st.write(f"**Total Batch Weight:** {total_weight} kg")
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Component**")
        st.write("Cement")
        if lime_percent > 0:
            st.write("Lime (optional)")
        st.write("HPMC (Cellulose Ether)")
        st.write("Crushed Sand")
    with col2:
        st.write("**Weight**")
        st.write(f"{cement_kg} kg ({cement_percent}%)")
        if lime_percent > 0:
            st.write(f"{lime_kg} kg ({lime_percent}%)")
        st.write(f"{hpmc_kg} kg ({hpmc_percent}%)")
        st.write(f"{sand_kg} kg ({sand_percent}%)")

    total_calc = cement_kg + lime_kg + hpmc_kg + sand_kg
    st.write("---")
    st.write(f"**Total Calculated:** {total_calc} kg")

    # --- Minimum Norms Checks ---
    min_cement = 15  # example: 15% cement minimum
    if cement_percent < min_cement:
        st.warning(f"⚠️ Cement percent is below the minimum norm ({min_cement}%).")
    if sand_percent < 50:
        st.warning("⚠️ Sand content is quite low for spray mortars (recommended >50%).")

# --- UI: Main Section ---
st.set_page_config(page_title="Spray Mortar & ES Calculator", layout="centered")
st.title("🧱 Spray Mortar & Sand ES Calculator")
st.caption("Modern, cost-effective recipes with quality control tools – by Omar 🇲🇦")

st.markdown("## 1️⃣ Mortar Mix Configuration")

total_batch = st.number_input("Total Batch Weight (kg)", value=1000, min_value=1, step=1)
col1, col2 = st.columns(2)
with col1:
    cement_percent = st.slider("Cement %", 10.0, 40.0, 25.0, 0.5)
    lime_percent = st.slider("Lime % (optional)", 0.0, 10.0, 3.0, 0.5)
with col2:
    hpmc_percent = st.slider("HPMC (Cellulose Ether) %", 0.1, 2.0, 0.6, 0.1)
    remaining = 100 - cement_percent - lime_percent - hpmc_percent
    st.metric("Crushed Sand %", f"{remaining:.1f}%")

if remaining < 0:
    st.error("⚠️ Total percentages exceed 100%. Please adjust the values.")
elif remaining < 40:
    st.warning("⚠️ Sand percentage is quite low. Consider reducing other components.")

if st.button("Calculate Mortar Recipe"):
    if remaining >= 0:
        calculate_mortar_mix(total_batch, cement_percent, lime_percent, hpmc_percent)
    else:
        st.error("Cannot calculate: Total percentages exceed 100%")

st.write("---")
st.markdown("## 2️⃣ ES Sand Calculator (Quality Control)")

with st.expander("Open Sand Sieve Analysis Calculator"):
    st.write("Enter your sand's sieve analysis (% retained on each):")
    sieves = ["2 mm", "1 mm", "0.5 mm", "0.25 mm", "0.125 mm", "0.063 mm", "Pan"]
    default_vals = [2, 5, 18, 34, 26, 12, 3]
    sieve_percentages = []
    for idx, sieve in enumerate(sieves):
        val = st.number_input(f"{sieve}", min_value=0.0, max_value=100.0, value=float(default_vals[idx]), step=0.1, key=f"sieve_{idx}")
        sieve_percentages.append(val)
    if st.button("Calculate ES Value"):
        es_value = calculate_es(sieve_percentages)
        if es_value is not None:
            st.success(f"**Calculated ES value:** {es_value}")
            if es_value < 45:
                st.warning("⚠️ ES value is below recommended minimum for spray mortars (45). Consider adjusting sand blend.")
            elif es_value > 55:
                st.warning("⚠️ ES value is above the maximum for optimal workability (55). Consider adjusting sand blend.")
            else:
                st.info("✅ ES value is within the typical recommended range (45 - 55).")
        else:
            st.error("Could not calculate ES. Please check your inputs.")

st.write("---")
st.markdown("## 3️⃣ Sand Blending Calculator (Achieve Target ES)")

st.write("""
Enter the ES of your unclean (crushed) sand, the ES of your clean (washed) sand,
and your target ES for mortar. Get the recommended blend ratio.
""")
col1, col2, col3 = st.columns(3)
with col1:
    es_unclean = st.number_input("Unclean Sand ES", min_value=0.0, max_value=100.0, value=40.0, step=0.1)
with col2:
    es_clean = st.number_input("Clean Sand ES", min_value=0.0, max_value=100.0, value=77.0, step=0.1)
with col3:
    es_target = st.number_input("Target ES", min_value=40.0, max_value=55.0, value=45.0, step=0.1)

if st.button("Calculate Sand Blend"):
    ratio_clean, ratio_unclean, message = sand_blend_ratio(es_unclean, es_clean, es_target)
    if message:
        st.info(message)
    else:
        st.markdown(f"**Mix {ratio_clean*100:.1f}% clean sand and {ratio_unclean*100:.1f}% unclean sand.**")
        if ratio_clean > 0.3:
            st.warning("⚠️ Clean sand required is above 30%. Consider finding a better unclean sand or using more clean sand.")

st.write("---")
st.info("**Recommended ES for mortar sand:** Minimum: 45, Maximum: 55. Most codes recommend staying within this range for proper workability and strength.")
st.caption("For best results, ensure all components and sand grading meet your project's local norms and requirements.")
