from ciphers import Cipher

ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class Atbash(Cipher):

    """This class implements the Atbash Cipher"""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Atbash"
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Atbash Cipher"
    
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # First format the ciphertext for decryption.
        self._block_input()
        # Decrypt according to the standard formula.
        for char in self.ciphertext:
            plain_index = (len(ALPHANUM) - 1) - ALPHANUM.index(char)
            self.plaintext += ALPHANUM[plain_index]
        # end for
        # Finally, allow for a one-time pad.
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    # end function
        
        
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # The Atbash cipher doesn't use keywords, so...
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # To encrypt, just loop through the plaintext...
        for char in self.plaintext:
            # The cipher character is found through a formula.
            cipher_index = (len(ALPHANUM) - 1) - ALPHANUM.index(char)
            self.ciphertext += ALPHANUM[cipher_index]
        # end for
        # Allow the user to see the ciphertext in five-character blocks.
        self._block_output()
        return
    # end function.

