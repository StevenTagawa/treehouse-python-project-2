from ciphers import Cipher

ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class Caesar(Cipher):
    
    """This class implements the Caesar Cipher"""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Caesar"
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
        
        
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Caesar Cipher"
    
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks).
        self._block_input()
        # To decrypt, just shift all characters back three places.
        for char in self.ciphertext:
            self.plaintext += ALPHANUM[(ALPHANUM.index(char) - 3) % 
                                        len(ALPHANUM)]
        # end for
        # Call one time pad and intelligent decrypt.
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    # end function
    
    
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # To encrypt, just shift letters/numbers three places forward.
        for char in self.plaintext:
            self.ciphertext += ALPHANUM[(ALPHANUM.index(char) + 3) %
                                        len(ALPHANUM)]
        # end for
        # Format text into blocks, if the user wants.
        self._block_output()
        return
    # end function
    