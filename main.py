import streamlit as st
import pandas as pd

# Import backend logic
from Bahar_classification import detect_best_bahr
from radeef_qafiya import detect_radeef_multi, detect_qafiya_multi
from meter_model import predict_meter_lines
from rhyme_suggestions import suggest_rhymes

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="Urdu Poetry Analysis", page_icon="✒️")

st.title("✒️ Urdu Poetry Analysis")
st.markdown("### Meter, Bahr, and Rhyme Detection")

# ------------------ Sidebar / Info ------------------ #
with st.sidebar:
    st.info("**Instructions:**")
    st.markdown("""
    1. Enter 1–4 lines of Urdu poetry.
    2. Click **Analyze**.
    3. View Meter, Bahr, and Rhyme suggestions.
    """)
    st.caption("Powered by BERT & Custom Algorithms")

# ------------------ Input Section ------------------ #
text_input = st.text_area(
    "Enter Verses:",
    height=150,
    placeholder="دل ناداں تجھے ہوا کیا ہے\nآخر اس درد کی دوا کیا ہے"
)

# ------------------ Analysis Logic ------------------ #
if st.button("🔍 Analyze", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some poetry first.")
    else:
        # Split text into lines
        lines = [l.strip() for l in text_input.split('\n') if l.strip()]

        # Enforce the 4-line limit from your original logic
        if len(lines) > 4:
            st.error("⚠️ Please restrict input to 4 lines maximum.")
        else:
            with st.spinner("Analyzing poetry patterns..."):
                try:
                    # 1. Meter Prediction
                    line_meters = predict_meter_lines(lines)
                    merged_meter = "".join(line_meters)
                    
                    # 2. Bahr Detection
                    bahr_result = detect_best_bahr(merged_meter)

                    # 3. Radeef & Qafiya
                    radeef = detect_radeef_multi(lines)
                    qafiya = detect_qafiya_multi(lines, radeef)

                    # 4. Rhyme Suggestions
                    rhyme_data = suggest_rhymes(lines, top_k=10)

                    # ------------------ Display Results ------------------ #
                    
                    st.divider()
                    
                    # Top Metric Row
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Identified Bahr", bahr_result.get("Bahar", "Unknown"))
                    c2.metric("Radeef", radeef)
                    c3.metric("Qafiya", ", ".join(qafiya))

                    # Meter Scansion
                    st.subheader("Meter Scansion")
                    for i, (line, meter) in enumerate(zip(lines, line_meters)):
                        st.text(f"Line {i+1}: {line}\nMeter:  {meter}")

                    # Suggestions Table
                    st.subheader("Rhyme Suggestions")
                    if rhyme_data.get("suggestions"):
                        df = pd.DataFrame(rhyme_data["suggestions"])
                        # Renaming for cleaner UI
                        df.rename(columns={"sher": "Suggested Rhyme", "score": "Relevance"}, inplace=True)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.caption("No strong rhyme suggestions found.")

                except Exception as e:
                    st.error(f"Error: {e}")

                    st.info("Ensure 'optimized_meter_model.pt' and 'qafiya_merged.json' are in the root directory.")
