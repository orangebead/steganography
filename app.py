import io
import streamlit as st
from PIL import Image

from encode import encode
from decode import decode

st.title("Steganography")

tab_encode, tab_decode = st.tabs(["Encode", "Decode"])

with tab_encode:
    uploaded = st.file_uploader("Upload an image", type=["png"], key="encode_upload")
    secret = st.text_area("Message to hide")

    if uploaded and secret and st.button("Encode"):
        image = Image.open(uploaded).convert("RGB")
        image.save("temp_input.png")
        encode("temp_input.png", secret, "temp_output.png")
        result = Image.open("temp_output.png")

        st.image(result, caption="Encoded image")

        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button("Download image", data=buf.getvalue(), file_name="secret.png", mime="image/png")

with tab_decode:
    decode_upload = st.file_uploader("Upload an image", type=["png"], key="decode_upload")

    if decode_upload and st.button("Decode"):
        image = Image.open(decode_upload).convert("RGB")
        image.save("temp_decode.png")
        message = decode("temp_decode.png")

        st.text_area("Message", value=message, height=150)