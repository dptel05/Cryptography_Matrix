import numpy as np
import base64


class MatrixCrypto:
    def __init__(self, key_matrix=None):
        if key_matrix is None:
            # Default key matrix (4x4) for encryption
            self.key_matrix = np.array([[2, 3, 5, 7],
                                        [11, 13, 17, 19],
                                        [23, 29, 31, 37],
                                        [41, 43, 47, 53]])
        else:
            self.key_matrix = key_matrix
        self.inverse_key = np.linalg.inv(self.key_matrix)

    def _pad_data(self, data, block_size):
        """Pad the data to make it a multiple of block_size."""
        pad_length = (block_size - len(data) % block_size) % block_size
        return data + bytes([pad_length] * pad_length)

    def _unpad_data(self, data):
        """Remove padding from the data."""
        pad_length = data[-1]
        return data[:-pad_length]

    def encrypt_text(self, text):
        """Encrypt a string using the key matrix."""
        text_bytes = text.encode('utf-8')
        padded_data = self._pad_data(text_bytes, 4)  # Pad to match the 4x4 matrix
        data_array = np.frombuffer(padded_data, dtype=np.uint8).reshape(-1, 4)

        encrypted = np.dot(data_array, self.key_matrix).astype(np.int64)
        encrypted_flat = encrypted.flatten()
        encrypted_b64 = base64.b64encode(encrypted_flat.tobytes()).decode('utf-8')
        return encrypted_b64

    def decrypt_text(self, encrypted_b64):
        """Decrypt a base64 string using the key matrix."""
        encrypted_bytes = base64.b64decode(encrypted_b64)
        encrypted_array = np.frombuffer(encrypted_bytes, dtype=np.int64).reshape(-1, 4)

        print(f"Decrypted array shape: {encrypted_array.shape}")  # Debugging: print shape of decrypted data
        decrypted_array = np.dot(encrypted_array, self.inverse_key).round().astype(np.uint8)
        decrypted_bytes = decrypted_array.flatten().tobytes()

        # Debugging: print the decrypted bytes
        print(f"Decrypted bytes before unpadding: {decrypted_bytes}")

        decrypted_text = self._unpad_data(decrypted_bytes).decode('utf-8')
        return decrypted_text

    def encrypt_file(self, file_data):
        """Encrypt the contents of a file."""
        padded_data = self._pad_data(file_data, 4)  # Pad to match the 4x4 matrix
        data_array = np.frombuffer(padded_data, dtype=np.uint8).reshape(-1, 4)

        encrypted = np.dot(data_array, self.key_matrix).astype(np.int64)
        encrypted_flat = encrypted.flatten()
        encrypted_b64 = base64.b64encode(encrypted_flat.tobytes()).decode('utf-8')
        return encrypted_b64

    def decrypt_file(self, encrypted_b64):
        """Decrypt the contents of an encrypted file."""
        encrypted_bytes = base64.b64decode(encrypted_b64)
        encrypted_array = np.frombuffer(encrypted_bytes, dtype=np.int64).reshape(-1, 4)

        decrypted_array = np.dot(encrypted_array, self.inverse_key).round().astype(np.uint8)
        decrypted_bytes = decrypted_array.flatten().tobytes()
        return self._unpad_data(decrypted_bytes)

    def export_encryption_key(self):
        """Export the encryption key matrix as a base64 string."""
        return base64.b64encode(self.key_matrix.tobytes()).decode('utf-8')

    def import_encryption_key(self, key_str):
        """Import the encryption key matrix from a base64 string."""
        key_bytes = base64.b64decode(key_str)
        self.key_matrix = np.frombuffer(key_bytes, dtype=np.float64).reshape(4, 4)
        self.inverse_key = np.linalg.inv(self.key_matrix)
