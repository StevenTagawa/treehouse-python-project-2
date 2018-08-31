from ciphers import Cipher

ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
GRID_WIDTH = 7


class Transposition(Cipher):
    
    """This class implements a Transposition Cipher."""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Transposition"
        self.keyword = ""
        if mode == "Encrypt":
            self.plaintext = text
            self.ciphertext = ""
        else:
            self.ciphertext = text
            self.plaintext = ""
        # end if
    
    def __str__(self):
        """Sets plain name for the cipher."""
        return "Transposition Cipher"
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Format the ciphertext for decryption.
        self._block_input()
        # Calculate the number of rows needed.
        grid_height = (len(self.ciphertext) // GRID_WIDTH)
        xtra = len(self.ciphertext) % GRID_WIDTH
        if xtra:
            grid_height += 1
        working_list = []
        xtra = len(self.ciphertext) - ((GRID_WIDTH - 1) * grid_height)
        # Slice the ciphertext into rows (lists).
        # If the length of the message divides evenly into the number of
        #  columns, all segments will be equal length.  Otherwise, the
        #  bottom row(s) will be one character shorter.
        while GRID_WIDTH < len(self.ciphertext):
            if xtra:
                working_list.append(self.ciphertext[:GRID_WIDTH])
                self.ciphertext = self.ciphertext[GRID_WIDTH:]
                xtra -= 1
            else:
                working_list.append(self.ciphertext[:GRID_WIDTH-1])
                self.ciphertext = self.ciphertext[GRID_WIDTH-1:]
            # end if
        # end while
        # Add the last partial line to the list.
        working_list.append(self.ciphertext)
        # Reverse every odd-indexed list.
        for row in range(len(working_list)):
            if row % 2:
                working_list[row] = working_list[row][::-1]
            # end if
        # end for
        # Now add the characters into plaintext going down successive
        #  columns.
        for row in range(GRID_WIDTH):
            for col in range(grid_height):
                try:
                    self.plaintext += working_list[col][row]
                except IndexError:
                    # ignore errors of not enough characters in column.
                    pass
                # end try
            # end for
        # end for
        # Finally, allow for a one-time pad.
        print(self.plaintext)
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    # end method
    
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
        print(self.plaintext)
        # Determine the size of the grid to use.
        grid_height = (len(self.plaintext) // GRID_WIDTH)
        if len(self.plaintext) % GRID_WIDTH > 0:
            grid_height += 1
        working_list = ["" for _ in range(grid_height)]
        # Write the plaintext down (into successive rows).
        row = 0
        for char in self.plaintext:
            working_list[row] += char
            row = (row + 1) % grid_height
            # end if
        # end for
        # Combine lists into string boustrophedonically, starting with
        #  left to right (i.e., reverse every other row).
        for row, string in enumerate(working_list):
            if row % 2 == 0:
                self.ciphertext += string
            else:
                self.ciphertext += string[::-1]
            # end if
        # end for
        # Finally, separate into five-character blocks if the user
        #  chooses.
        self._block_output()
        return
    # end method
