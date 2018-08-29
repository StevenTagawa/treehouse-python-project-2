from ciphers import Cipher

ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class Keyword_(Cipher):
    
    """This class implements the Keyword Cipher."""
    
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Keyword"
        self.keyword = ""
        self.code_alphabet = ""
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Keyword Cipher"
    
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # First get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter the keyword that was used to encrypt this " +
            "message:  ")
        # Get the code alphabet.
        self.code_alphabet = self._alphabet_from_keyword(
            self.keyword, include_numbers=True)
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks) and turn it into
        #  all upper-case.
        self._block_input()
        # Loop through the ciphertext and decrypt each character.
        for char in self.ciphertext:
            self.plaintext += ALPHANUM[self.code_alphabet.index(char)]
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
        # Get a keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter a keyword for this message:  ")
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # Build the code alphabet.  Include numbers.
        self.code_alphabet = self._alphabet_from_keyword(
            self.keyword, include_numbers=True)
        # The plaintext is encrypted using the code alphabet.
        for char in self.plaintext:
            # Loop through and add to ciphertext.
            self.ciphertext += self.code_alphabet[ALPHANUM.index(char)]
        # end for
        # Finally, separate into five-character blocks if the user
        #  chooses.
        self._block_output()
        return
    # end function
    