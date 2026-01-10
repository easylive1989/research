import streamlit as st
import os
from dotenv import load_dotenv
import utils

# Page configuration
st.set_page_config(
    page_title="Google Embedding MVP",
    page_icon="🤖",
    layout="wide"
)

# Load environment variables
load_dotenv()

def main():
    st.title("🤖 Google Embedding MVP")
    st.markdown("""
    Upload text files, PDFs, or images to generate their vector embeddings using Google's Generative AI.

    - **Text/PDF**: Extracted text is embedded directly.
    - **Images**: The image is described using `Gemini 1.5 Flash`, and the description is embedded.
    """)

    # Sidebar for API Key
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
        if not api_key:
            st.warning("Please enter your Google API Key to proceed.")
            st.info("You can get a key from [Google AI Studio](https://aistudio.google.com/).")

    if not api_key:
        return

    # File Uploader
    uploaded_file = st.file_uploader("Choose a file...", type=['txt', 'md', 'pdf', 'jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        st.divider()
        st.subheader("File Processing")

        content_to_embed = ""
        file_type = uploaded_file.type

        with st.spinner("Processing file..."):
            try:
                # Handle different file types
                if file_type == "text/plain" or file_type == "text/markdown" or uploaded_file.name.endswith(('.txt', '.md')):
                    string_data = uploaded_file.getvalue().decode("utf-8")
                    content_to_embed = string_data
                    st.text_area("File Content", content_to_embed, height=200)

                elif file_type == "application/pdf":
                    content_to_embed = utils.extract_text_from_pdf(uploaded_file)
                    st.text_area("Extracted Text from PDF", content_to_embed, height=200)

                elif file_type in ["image/jpeg", "image/png", "image/jpg"]:
                    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                    st.info("Generating description for image...")
                    content_to_embed = utils.get_image_description(uploaded_file, api_key)
                    st.text_area("Generated Description", content_to_embed, height=150)

                else:
                    st.error(f"Unsupported file type: {file_type}")
                    return

                # Generate Embedding
                if content_to_embed:
                    st.subheader("Embedding Generation")
                    with st.spinner("Generating embedding..."):
                        embedding = utils.get_embedding(content_to_embed, api_key)

                    st.success("Embedding generated successfully!")
                    st.write(f"**Vector Dimension:** {len(embedding)}")

                    # Display a snippet of the vector
                    st.write("**Vector Preview (First 20 values):**")
                    st.code(str(embedding[:20]), language="python")

                    # Option to download
                    st.download_button(
                        label="Download Embedding JSON",
                        data=str(embedding),
                        file_name=f"{uploaded_file.name}_embedding.json",
                        mime="application/json"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
