import random

from ciphers import Cipher

CODE = "ADFGVX"

class Adfgvx(Cipher):
    
    """This class implements the ADFGVX Cipher."""
    
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "ADFGVX"
        self.code_dict = {}
        self.keyword = ""
        self.perm_key = ""
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "ADFGVX Cipher"
    
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Get the keyword and permutation key from the user.
        # Get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter the keyword or phrase that was used to encrypt " +
            "this message:  ")
        # Get a permutation key.
        self.perm_key = self._get_keyword(
            "This cipher also requires a permutation keyword:  ")
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks) and turn it into
        #  all upper-case.
        self._block_input()
        # Then validate the ciphertext.
        invalid_msg = ""
        invalid_msg = self._validate()
        if invalid_msg:
            # If the ciphertext is not valid, inform the user and abort.
            print(invalid_msg)
            self.plaintext = ""
            return
        # end if (function exits)
        # Sort the letters of the permutation key into alphabetical
        #  order.
        perm_key_list = list(self.perm_key)
        for x in range(len(perm_key_list)):
            perm_key_list[x] += str(x).zfill(2)
        # end for
        perm_key_list.sort()
        # Slice the ciphertext into columns (lists).
        col_length = len(self.ciphertext) // len(self.perm_key)
        working_list = ["" for letter in self.perm_key]
        index = 0
        for pos in range(0, len(self.ciphertext), col_length):
            working_list[index] = self.ciphertext[pos : pos + col_length]
            index += 1
        # Rearrange the columns (lists) back into their correct order.
        input()
        correct_order_list = ["" for letter in self.perm_key]
        for x, pos in enumerate(perm_key_list):
            correct_order_list[int(pos[1:])] = str(working_list[x])
        # end for
        # Take each row to form a single string.
        working_string = ""
        for col in range(col_length):
            for row in range(len(correct_order_list)):
                working_string += correct_order_list[row][col]
            # end for
        # end for
        # Strip off any trailing nulls.
        while working_string[-1] == "V":
            working_string = working_string[: -1]
        # end while
        # Build the code dictionary.
        self._build_code_dict()
        # Go through the encrypted text two characters at a time.
        for pos in range(0, len(working_string), 2):
            # Turn each bigram back into a letter.
            bigram = working_string[pos : pos + 2]
            print(bigram)
            self.plaintext += (self.code_dict[bigram])
        # end for
        # Allow the user to enter a one-time pad code, if one was used
        #  to encrpyt the message.
        self._one_time_pad()
        self._intelligent_decrypt()
        
    
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter a keyword or phrase (no spaces) for " +
            "your text.\nAvoid words with repeating letters:  ")
        # Get a permutation key.
        self.perm_key = self._get_keyword(
            "This cipher also requires a permutation " +
            "keyword:  ")
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # Build the code dictionary.
        self._build_code_dict()
        # Convert the plaintext into bigrams.
        working_string = ""
        for letter in self.plaintext:
            working_string += (self.code_dict[letter])
        # end for
        # Pad with nulls if needed to make columns equal length.
        if len(working_string) % len(self.perm_key) > 0:
            # Calculate the number of nulls needed.
            nulls = (len(self.perm_key) - 
                     (len(working_string) % len(self.perm_key)))
            # For simplicity's sake this function pads the matrix with
            #  V characters.
            for _ in range(nulls):
                working_string += "V"
            # end for
        # end if
        # Sort the working string into columns (lists).
        working_list = ["" for letter in self.perm_key]
        index = 0
        for letter in working_string:
            working_list[index] += letter
            index += 1
            if index == len(self.perm_key):
                index = 0
            # end if
        # end for
        # Sort the letters of the permutation key into alphabetical
        #  order.
        perm_key_list = list(self.perm_key)
        for x in range(len(perm_key_list)):
            perm_key_list[x] += str(x).zfill(2)
        # end for
        perm_key_list.sort()
        # Merge the rearranged columns (lists) into the ciphertext.
        for item in perm_key_list:
            self.ciphertext += working_list[int(item[1:])]
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
        # Build an initial alphabet from the keyword.  Do not include
        # numbers at the end.
        code_alphabet = self._alphabet_from_keyword(self.keyword)
        # In this cipher, numerals are inserted after the first ten
        #  letters.
        num_dict = {
            "A": "1", "B": "2", "C": "3", "D": "4", "E": "5", "F": "6",
            "G": "7", "H": "8", "I": "9", "J": "0"}
        # Break the code alphabet apart and insert the numerals.
        alpha_list = list(code_alphabet)
        for x, letter in enumerate(alpha_list):
            if letter in num_dict:
                alpha_list.insert(x + 1, num_dict[letter])
        # end for
        # Create the bi-gram equivalents for each letter/number.
        for row in CODE:
            for col in CODE:
                if self.mode == "Encrypt":
                    # For encryption, letters as keys.
                    self.code_dict[alpha_list.pop(0)] = row + col
                else:
                    # For decryption, bigrams as keys.
                    self.code_dict[row + col] = alpha_list.pop(0)
            # end for
        # end for
    # end function
    
    
    def _validate(self):
        """Checks encrypted data to ensure that it contains only valid
        characters, and is a valid length.
        
        Arguments:  none.
        
        Returns:  True if the data is valid; False otherwise.
        """
        msg = ""
        # The length of the ciphertext must be a multiple of the length
        #  of the permutation key (the encryption method makes it so).
        #  If it is not, either the ciphertext or the permutation key is
        #  incorrect.
        if len(self.ciphertext) % len(self.perm_key) > 0:
            return "The encrypted text is incompatible with the specified key."
        # Loop through each character in the ciphertext to make sure
        #  that only the characters in the ADFGVX cipher are present.
        for char in self.ciphertext:
            if not (char.upper() in CODE):
                return "The encrypted text contains invalid characters."
            # end if (function exits)
        # end for
        # If none of the characters failed, return True.
        return msg
    # end function
    

        