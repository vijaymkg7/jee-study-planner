import streamlit as st
from pdf2image import convert_from_bytes
import zipfile
import os
from io import BytesIO

st.set_page_config(page_title="PDF to Image Converter", layout="wide")

# Function to convert PDF to images
def pdf_to_images(pdf_file):
    images = convert_from_bytes(pdf_file.read(), dpi=300)
    return images

# Function to save images as a ZIP file
def create_zip(images):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, img in enumerate(images):
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            zip_file.writestr(f"page_{i+1}.png", img_buffer.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

# Streamlit UI
st.title("📄 Upload PDF & Convert to Images")

uploaded_file = st.file_uploader("📤 Upload your PDF file", type="pdf")

if uploaded_file:
    st.success("✅ PDF Uploaded Successfully!")

    # Convert PDF to images
    images = pdf_to_images(uploaded_file)

    # Show preview
    st.subheader("📑 Preview of Extracted Images")
    for i, img in enumerate(images[:3]):  # Show first 3 pages
        st.image(img, caption=f"Page {i+1}", use_column_width=True)

    # Create ZIP for download
    zip_buffer = create_zip(images)

    # Provide download link
    st.download_button(
        label="📥 Download All Images as ZIP",
        data=zip_buffer,
        file_name="pdf_images.zip",
        mime="application/zip"
    )
