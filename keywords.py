import streamlit as st
from google_play_scraper import app
from keybert import KeyBERT

# Initialize the keyword model
kw_model = KeyBERT()

st.set_page_config(page_title="Play Store Keyword Generator", layout="centered")

st.title("📱 Play Store ASO Keyword Generator")
st.write("Enter a Play Store App ID to generate ASO-friendly keywords from its description.")

# Input field
app_id = st.text_input("Enter Google Play App ID", value="")

if st.button("Generate Keywords"):
    if not app_id:
        st.warning("Please enter a valid App ID.")
    else:
        try:
            with st.spinner("Fetching app data..."):
                # Get app details from Google Play
                data = app(app_id)

                title = data.get('title', 'N/A')
                description = data.get('description', '')
                category = data.get('genre', 'Unknown')

                # Extract keywords from the description
                keywords = kw_model.extract_keywords(
                    description,
                    keyphrase_ngram_range=(1, 2),
                    stop_words='english',
                    top_n=10
                )
                keywords_list = [kw[0] for kw in keywords]

            # Display Results
            st.success(f"Keywords generated for: {title}")
            st.markdown(f"**Category:** {category}")
            st.markdown(f"**Description:**\n\n{description[:500]}...")  # Show a short version
            st.markdown("### 🔑 Suggested Keywords:")
            for i, kw in enumerate(keywords_list, 1):
                st.markdown(f"{i}. `{kw}`")

        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
