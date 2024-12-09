import numpy as np
import base64
import os


class MatrixCrypto:
    def __init__(self, key_matrix=None):
        if key_matrix is None:
            # Default 4x4 key matrix
            self.key_matrix = np.array([[2, 3, 1, 5],
                                        [7, 1, 3, 4],
                                        [4, 5, 9, 6],
                                        [1, 8, 7, 2]])
        else:
            self.key_matrix = key_matrix

        # Ensure the matrix is invertible
        if np.linalg.det(self.key_matrix) == 0:
            raise ValueError("Provided key matrix is not invertible.")
        self.inverse_key = np.linalg.inv(self.key_matrix)

    def encrypt_text(self, text):
        """Encrypt a string using the key matrix."""
        text_bytes = text.encode('utf-8')
        matrix_size = self.key_matrix.shape[0]

        # Pad text to match matrix size
        padding = (matrix_size - len(text_bytes) % matrix_size) % matrix_size
        padded_text = text_bytes + b'\0' * padding

        # Convert text to numerical array
        text_array = np.frombuffer(padded_text, dtype=np.uint8).reshape(-1, matrix_size)

        # Perform matrix multiplication
        encrypted_array = np.dot(text_array, self.key_matrix).astype(int)
        encrypted_flat = encrypted_array.flatten()

        # Encode as base64 for safe transport
        return base64.b64encode(encrypted_flat.tobytes()).decode('utf-8')

    def decrypt_text(self, encrypted_b64):
        """Decrypt a base64 string using the key matrix."""
        encrypted_bytes = base64.b64decode(encrypted_b64)
        matrix_size = self.key_matrix.shape[0]

        # Convert back to numerical array
        encrypted_array = np.frombuffer(encrypted_bytes, dtype=np.int32).reshape(-1, matrix_size)

        # Perform matrix multiplication with the inverse key
        decrypted_array = np.dot(encrypted_array, self.inverse_key).round().astype(np.uint8)
        decrypted_bytes = decrypted_array.flatten().tobytes()

        # Remove padding and return the result
        return decrypted_bytes.rstrip(b'\0').decode('utf-8')

    def encrypt_file(self, file_path):
        """Encrypt the contents of a file."""
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        encrypted_data = self.encrypt_text(file_bytes.decode('latin1'))
        return encrypted_data

    def decrypt_file(self, encrypted_data):
        """Decrypt the contents of an encrypted file."""
        decrypted_text = self.decrypt_text(encrypted_data)
        return decrypted_text.encode('latin1')

    def export_encryption_key(self):
        """Export the encryption key matrix as a string."""
        return base64.b64encode(self.key_matrix.tobytes()).decode('utf-8')

    def import_encryption_key(self, key_str):
        """Import the encryption key matrix from a string."""
        key_bytes = base64.b64decode(key_str)
        self.key_matrix = np.frombuffer(key_bytes, dtype=np.float64).reshape(4, 4)
        self.inverse_key = np.linalg.inv(self.key_matrix)
