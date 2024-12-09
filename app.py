import streamlit as st
from main import MatrixCrypto
import os

# Initialize session state
if 'crypto_keys' not in st.session_state:
    st.session_state.crypto_keys = {}  # To store unique keys for text and files


def main():
    st.title("🔐 Matrix Cryptography App")
    st.sidebar.title("Navigation")

    menu = st.sidebar.radio("Choose Operation:", ["Text Encryption", "File Encryption"])

    if menu == "Text Encryption":
        text_encryption_page()
    elif menu == "File Encryption":
        file_encryption_page()


def text_encryption_page():
    st.header("📝 Text Encryption & Decryption")

    with st.expander("🔒 Encrypt Text"):
        input_text = st.text_area("Enter text to encrypt")
        if st.button("Encrypt Text"):
            if input_text.strip():
                # Generate a unique MatrixCrypto instance for this operation
                crypto = MatrixCrypto()
                encrypted_text = crypto.encrypt_text(input_text)

                # Store the encryption key in session
                text_key = crypto.export_encryption_key()
                st.session_state.crypto_keys['text'] = text_key

                st.success("Encrypted Text:")
                st.code(encrypted_text)

                st.info("Encryption Key (save this for decryption):")
                st.code(text_key)
            else:
                st.error("Please provide valid input.")

    with st.expander("🔓 Decrypt Text"):
        encrypted_text = st.text_area("Enter encrypted text")
        decryption_key = st.text_input("Enter the encryption key")
        if st.button("Decrypt Text"):
            if encrypted_text.strip() and decryption_key.strip():
                try:
                    crypto = MatrixCrypto()
                    crypto.import_encryption_key(decryption_key)
                    decrypted_text = crypto.decrypt_text(encrypted_text)
                    st.success("Decrypted Text:")
                    st.code(decrypted_text)
                except Exception as e:
                    st.error(f"Decryption failed: {e}")
            else:
                st.error("Please provide valid input and a valid key.")


def file_encryption_page():
    st.header("📁 File Encryption & Decryption")

    with st.expander("🔒 Encrypt File"):
        file = st.file_uploader("Upload a file to encrypt")
        if file:
            file_data = file.read()
            if st.button("Encrypt File"):
                try:
                    # Generate a unique MatrixCrypto instance for this operation
                    crypto = MatrixCrypto()
                    encrypted_data = crypto.encrypt_file(file_data)

                    # Store the encryption key in session
                    file_key = crypto.export_encryption_key()
                    st.session_state.crypto_keys['file'] = file_key

                    st.download_button("Download Encrypted File", encrypted_data,
                                       file_name=f"encrypted_{file.name}.txt")

                    st.info("Encryption Key (save this for decryption):")
                    st.code(file_key)
                except Exception as e:
                    st.error(f"File encryption failed: {e}")

    with st.expander("🔓 Decrypt File"):
        encrypted_file = st.file_uploader("Upload an encrypted file")
        decryption_key = st.text_input("Enter the encryption key")
        if encrypted_file and decryption_key.strip():
            encrypted_data = encrypted_file.read().decode('utf-8')
            if st.button("Decrypt File"):
                try:
                    crypto = MatrixCrypto()
                    crypto.import_encryption_key(decryption_key)
                    decrypted_data = crypto.decrypt_file(encrypted_data)

                    st.download_button("Download Decrypted File", decrypted_data,
                                       file_name=f"decrypted_{encrypted_file.name}")
                except Exception as e:
                    st.error(f"File decryption failed: {e}")


if __name__ == "__main__":
    main()
