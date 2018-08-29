import random

from ciphers import Cipher

STABILIS = "ABCDEFGILMNOPQRSTVXZ1234"
MOBILIS = "gklnprtvz&xysomqihfdbace"
CHAR_MAP = {"H": "I", "J": "G", "K": "C", "U": "V", "W": "X", "Y": "Z",
            "0": "O", "4": "F", "5": "S", "6": "B", "7": "A", "8": "M",
            "9": "R"}
CHAR_MAP_REV = {"I": "H", "G": "J", "C": "K", "V": "U", "X": "W", "Z": "Y",
                "O": "0", "F": "4", "S": "5", "B": "6", "A": "7", "M": "8",
                "R": "9"}

class Alberti(Cipher):
    
    """This class implements the Alberti Cipher"""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Alberti"
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
        self.index = 0
    
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Alberti Cipher"
    
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # First get the index letter for the cipher.
        # Need to pass an upper-case version of the mobilis alphabet
        #  because _get_keyword expects keywords to be upper-case.
        index_letter = self._get_keyword(
            "Please enter the index letter that was used to encrypt this\n" +
            "cipher.  The index letter can be:  a, b, c, d, e, f, g, h, i,\n" +
            "k, l, m, n, o, p, q, r, s, t, v, x, y, z, or &:  ",
            keylist = MOBILIS.upper(), max_length = 1)
        # Now set the index, which is the offset for the cipher.
        self.index = MOBILIS.find(index_letter.lower())
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks).
        self._block_input(make_upper = False)
        # Cycle through the ciphertext, converting into plaintext.
        for char in self.ciphertext:
            # The & will pass this test for capital letters, so exclude
            #  it.
            if (char != "&") and (char.upper() == char):
                # If a capital letter, set a new key.
                key = STABILIS.index(char)
            else:
                self.plaintext += STABILIS[(MOBILIS.index(char) - key) % 24]
            # end if
        # end for
        # Now the plaintext needs to be reprocessed to decode excluded
        #  letters and numbers.
        self.__postprocess()
        # Allow the user to ender a one-time pad code, if one was used.
        self._one_time_pad()
        # Call _intelligent_decrypt
        self._intelligent_decrypt()
        return
    # end function
        
        
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # First get the index letter for the cipher.
        # Need to pass an upper-case version of the mobilis alphabet
        #  because _get_keyword expects keywords to be upper-case.
        index_letter = self._get_keyword(
            "Please enter the index letter for this cipher.  The index\n" +
            "letter can be:  a, b, c, d, e, f, g, h, i, k, l, m, n, o,\n" +
            "p, q, r, s, t, v, x, y, z, or &:  ", keylist = MOBILIS.upper(),
            max_length = 1)
        # Now set the index, which is the offset for the cipher.
        self.index = MOBILIS.find(index_letter.lower())
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # Because the Alberti Cipher does not include all letters and
        #  numbers, special processing has to be done to convert any
        #  excluded  characters.
        self.__preprocess()
        # Now that all letters and numbers are accounted for, encryption
        #  can begin.
        # First pick a random letter as the first key.
        key = random.randint(0, 23)
        self.ciphertext += STABILIS[key]
        # Set a counter to change the key letter.
        counter = random.randint(5, 15)
        # Cycle through the plaintext, converting to ciphertext.
        for char in self.plaintext:
            # Find the corresponding cipher character and append it to
            #  the cipher text.
            self.ciphertext += MOBILIS[(STABILIS.index(char) + key) % 24]
            counter -= 1
            if counter == 0:
                # Get a new key and reset the counter.
                key = random.randint(0, 23)
                self.ciphertext += STABILIS[key]
                counter = random.randint(5, 15)
            # end if
        # end for
        # Finally, separate into five-character blocks if the user
        #  chooses.
        self._block_output()
        return
    # end function
    
    
    def __postprocess(self):
        """This is the counterpart to __preprocess.  If scans the
        decrypted text for escape characters and numbers and converts
        them back into their original forms.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        new_string = ""
        # Go through the plaintext, scanning for the escape character 4.
        escape = False
        for char in self.plaintext:
            if char == "4":
                # If we hit the escape character, immediately get the
                #  next character.
                escape = True
            else:
                if escape:
                    # If escape is true the last character was a 4.
                    #  This character changes according to the map and
                    #  is added to the string.
                    new_string += CHAR_MAP_REV[char]
                    # Reset the escape flag.
                    escape = False
                else:
                    # Just pass through any non-numeric character.
                    new_string += char
                # end if
            # end if
        # end for
        # Put the result in plaintext.
        self.plaintext = new_string
        return
    # end function
    
    
    def __preprocess(self):
        """This internal function maps missing letters and numbers to
        existing letter/number sequences.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        new_string = ""
        # For missing letters and numbers, the numeral 4 is an escape
        #  character, with the letter or number mapped to an existing
        #  letter.
        for char in self.plaintext:
            if char in "HJKUWY0456789":
                new_string += "4" + CHAR_MAP[char]
            else:
                new_string += char
            # end if
        # end while
        # Put the result in plaintext.
        self.plaintext = new_string
        return
    # end function
    