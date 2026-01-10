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

    # Initialize ChromaDB
    try:
        collection = utils.get_chroma_collection()
    except Exception as e:
        st.sidebar.error(f"Failed to initialize ChromaDB: {e}")
        collection = None

    # Sidebar for API Key and Stats
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
        if not api_key:
            st.warning("Please enter your Google API Key to proceed.")
            st.info("You can get a key from [Google AI Studio](https://aistudio.google.com/).")

        st.divider()
        st.header("Database Stats")
        if collection:
            count = collection.count()
            st.metric("Stored Documents", count)
            if st.button("Refresh Stats"):
                st.rerun()

    if not api_key:
        return

    # Tabs for main functionality
    tab1, tab2 = st.tabs(["📤 Upload & Embed", "🗄️ Stored Documents"])

    with tab1:
        # File Uploader
        uploaded_file = st.file_uploader("Choose a file...", type=['txt', 'md', 'pdf', 'jpg', 'jpeg', 'png'])

        if uploaded_file is not None:
            st.divider()
            st.subheader("File Processing")

            content_to_embed = ""
            file_type = uploaded_file.type
            source_filename = uploaded_file.name

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
                        # Reset file pointer to beginning after reading for display
                        uploaded_file.seek(0)
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

                        col1, col2 = st.columns(2)
                        with col1:
                            # Option to download
                            st.download_button(
                                label="Download Embedding JSON",
                                data=str(embedding),
                                file_name=f"{uploaded_file.name}_embedding.json",
                                mime="application/json"
                            )
                        with col2:
                            # Save to ChromaDB
                            if st.button("Save to ChromaDB"):
                                if collection:
                                    try:
                                        metadata = {"source": source_filename, "type": file_type}
                                        doc_id = utils.save_to_chroma(collection, content_to_embed, embedding, metadata)
                                        st.success(f"Saved to ChromaDB with ID: {doc_id}")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error saving to DB: {e}")
                                else:
                                    st.error("ChromaDB is not initialized.")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with tab2:
        st.header("Stored Documents")
        if collection:
            try:
                # Get last 10 documents
                count = collection.count()
                if count > 0:
                    results = collection.get(limit=10)
                    ids = results['ids']
                    metadatas = results['metadatas']
                    documents = results['documents']

                    for i in range(len(ids)):
                        with st.expander(f"Document {ids[i]} ({metadatas[i].get('source', 'Unknown')})"):
                            st.write(f"**Source:** {metadatas[i]}")
                            st.text(documents[i][:500] + "..." if len(documents[i]) > 500 else documents[i])
                else:
                    st.info("No documents stored yet.")
            except Exception as e:
                st.error(f"Error fetching documents: {e}")

if __name__ == "__main__":
    main()
