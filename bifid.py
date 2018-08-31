from ciphers import Cipher


class Bifid(Cipher):

    """This class implements the Bifid Cipher"""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Bifid"
        self.keyword = ""
        self.code_dict = {}
        self.code_dict_rev = {}
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    # end method
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Bifid Cipher"
    # end method
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # First get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter the keyword that was used to encrypt this " +
            "message:  ")
        # Build the code dictionaries.
        self._build_code_dicts()
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks) and turn it into
        #  all upper-case.
        self._block_input()
        # Create a string of all the character sequences.
        working_string = ""
        for char in self.ciphertext:
            working_string += self.code_dict[char]
        # end for
        # Split the string into two lists.
        working_list = [[], []]
        working_list[0] = working_string[:len(working_string) // 2]
        working_list[1] = working_string[len(working_string) // 2:]
        for char in range(len(working_list[0])):
            # turn each two-character sequence (one from each list) back
            #  into a letter.
            self.plaintext += self.code_dict_rev[working_list[0][char] +
                                                 working_list[1][char]]
        # end for
        # Finally call one_time_pad and intelligent_decrypt.
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    # end method
    
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # First get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter a keyword or phrase (no spaces) for " +
            "your text.\nWords with a large number of unique letters " +
            "are more secure:  ")
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # Build the code dictionaries.
        self._build_code_dicts()
        # Convert the plaintext into two-digit sequences, separated.
        working_list = ["", ""]
        for char in self.plaintext:
            working_list[0] += self.code_dict[char][0]
            working_list[1] += self.code_dict[char][1]
        # end for
        # Combine the two strings into one.
        working_string = working_list[0] + working_list[1]
        # Reset working_list and reuse it.
        working_list = []
        # Turn the string into a list of two-digit sequences.
        for pos in range(0, len(working_string), 2):
            working_list.append(working_string[pos:pos + 2])
        # end for
        # Reset working_string and reuse it.
        working_string = ""
        # Go through the list and turn the sequences back into letters.
        for item in working_list:
            working_string += self.code_dict_rev[item]
        # end for
        # Put the result in ciphertext.
        self.ciphertext = working_string
        # Format if user chooses.
        self._block_output()
        return
    # end method
    
    def _build_code_dicts(self):
        """Builds the dictionary for encoding/decoding letters.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Build an initial alphabet from the keyword.  Include numbers.
        code_alphabet = self._alphabet_from_keyword(
            self.keyword, include_numbers=True)
        # Build dictionaries equating letters/numerals and values (used
        #  both ways during both encryption and decryption).
        row = 0
        col = 0
        for char in code_alphabet:
            self.code_dict[char] = str(row) + str(col)
            self.code_dict_rev[str(row) + str(col)] = char
            col += 1
            if col == 6:
                col = 0
                row += 1
            # end if
        # end for
        return
    # end method