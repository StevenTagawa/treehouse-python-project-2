from ciphers import Cipher

ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class Affine(Cipher):
    
    """This class implements the Affine Cipher"""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Affine"
        self.code_dict = {}
        self.key1 = 0
        self.key2 = 0
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    # end function
    
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Affine Cipher"
    # end function
    
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Get the keynumbers from the user.
        self.key1 = self._get_keynumber(
            "Please enter the first number that was used to encrypt " +
            "this message:  ")
        # Get a permutation key.
        self.key2 = self._get_keynumber(
            "Please enter the second number for this message:  ")
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks) and turn it into
        #  all upper-case.
        self._block_input()
        # Then validate the encrypted data.
        self._validate()
        # Build the code dictionary.
        self._build_code_dict()
        # Convert the ciphertext into plaintext.
        for char in self.ciphertext:
            self.plaintext += self.code_dict[char]
        # end for
        # Allow for one-time pad use.
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    
        
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Get the keynumbers for the cipher.
        self.key1 = self._get_keynumber(
            "Please enter the first key number for this cipher.  This key\n" +
            " must be one of the following: 5, 7, 11, 13, 17, 19, 23, 25,\n" +
            "29, 31, or 35. >>")
        self.key2 = self._get_keynumber(
            "Please enter the second key number for this cipher.  This key\n" +
            " can be any number.  >>")
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # Build the code dictionary.
        self._build_code_dict()
        # Convert the plaintext to ciphertext.
        for char in self.plaintext:
            self.ciphertext += self.code_dict[char]
        # end for        
        # Finally, separate into five-character blocks if the user
        #  chooses.
        self._block_output()
        return
    # end function

    def _build_code_dict(self):
        """Builds the dictionary for encoding/decoding letters.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Cycle through the alphanumeric string.
        for plain, char in enumerate(ALPHANUM):
            crypt = ((self.key1 * plain) + self.key2) % 36
            if self.mode == "Encrypt":
                # For encryption, keys are plaintext.
                self.code_dict[char] = ALPHANUM[crypt]
            else:
                # For decryption, keys are ciphertext.
                self.code_dict[ALPHANUM[crypt]] = char
            # end if
        # end for
        return
    #end function
    
    
    def _validate(self):
        """The validate method for this cipher just strips any non-
        alphanumeric characters from the ciphertext.  It does not
        reject any string as invalid.
                
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Cycle through the ciphertext, discarding any non-alphanumeric
        #  characters.
        new_string = ""
        for char in self.ciphertext:
            if char in ALPHANUM:
                new_string += char
            # end if
        # end for
        self.ciphertext = new_string
        return
    # end function
    