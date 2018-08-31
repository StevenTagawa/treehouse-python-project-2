from ciphers import Cipher

# This cipher's alphabet contains an extra character to increase its
#  length to 37 characters.  Due to the nature of the Hill Cipher, an
#  alphabet whose length is a prime number guarantees that all keywords
#  are valid.  A 36-character alphabet would eliminate a majority of
#  keywords.  The extra character, a hyphen, is not used in plaintext,
#  but plaintext characters can be encrypted to it, and it can be
#  part of ciphertext strings.
ALPHANUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"


class Hill(Cipher):

    """This class implements the Hill Cipher"""
    
    def __init__(self, mode, text):
        """At initialization, the mode of the object is set and the
        appropriate attribute is set to the original text.
        """
        self.mode = mode
        self.name = "Hill"
        self.keyword = ""
        self.matrix = [None for _ in range(9)]
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
        return "Hill Cipher"
    # end method
    
    def decrypt(self):
        """This is the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter the keyword that was used to encrypt this " +
            "message:  ")
        # Build the key matrix.
        self._matrix_from_keyword()
        # Turn the matrix into its inverse.
        self._invert_matrix(len(ALPHANUM))
        # Before doing anything with the ciphertext, strip it of any
        #  spaces (if entered in five-character blocks) and turn it into
        #  all upper-case.
        self._block_input()
        # Now decrypt the ciphertext.  The Hill Cipher encrypts and
        #  decrypts three characters at a time.
        trigram = [None, None, None]
        for pos in range(0, len(self.ciphertext), 3):
            trigram[0] = ALPHANUM.index(self.ciphertext[pos])
            trigram[1] = ALPHANUM.index(self.ciphertext[pos + 1])
            trigram[2] = ALPHANUM.index(self.ciphertext[pos + 2])
            # Perform matrix multiplication to transform the plaintext.
            trigram[0], trigram[1], trigram[2] = self._matrix_mult(
                self.matrix, trigram, len(ALPHANUM))
            # Convert back to text and put in ciphertext.
            for num in range(3):
                self.plaintext += ALPHANUM[trigram[num]]
            # end for
        # end for
        # If there are one or two padding characters, remove them.
        for _ in range(2):
            if self.plaintext[-1] == "Q":
                self.plaintext = self.plaintext[:-1]
            # end if
        # end for
        # Allow the user to enter a one-time pad code, if one was used
        #  to encrpyt the message.
        self._one_time_pad()
        self._intelligent_decrypt()
        return
    # end function
    
    def encrypt(self):
        """This is the encrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        # Get the keyword for the cipher.
        self.keyword = self._get_keyword(
            "Please enter a keyword for this message:  ")
        # Present the option to perform intelligent encryption.
        self._intelligent_encrypt()
        # Format the plaintext for processing.
        self._format_plaintext()
        # Present the option to use a one-time pad.
        self._one_time_pad()
        # Build the cipher matrix using the keyword.
        self._matrix_from_keyword()
        # If necessary, pad the plaintext string until it is a multple of
        #  three.
        while len(self.plaintext) % 3 > 0:
            self.plaintext += "Q"
        # end while
        # The Hill Cipher encrypts and decrypts three characters at a
        #  time.
        trigram = [None, None, None]
        for pos in range(0, len(self.plaintext), 3):
            trigram[0] = ALPHANUM.index(self.plaintext[pos])
            trigram[1] = ALPHANUM.index(self.plaintext[pos + 1])
            trigram[2] = ALPHANUM.index(self.plaintext[pos + 2])
            # Perform matrix multiplication to transform the plaintext.
            trigram[0], trigram[1], trigram[2] = self._matrix_mult(
                self.matrix, trigram, len(ALPHANUM))
            # Convert back to text and put in ciphertext.
            for num in range(3):
                self.ciphertext += ALPHANUM[trigram[num]]
            # end for
        # end for
        # Finally, separate into five-character blocks if the user
        #  chooses.
        self._block_output()
        return
    # end function
    
    def _block_input(self):
        """Internal function that strips out any spaces or
        non-alphanumeric charactes.  Overrides the base class's method
        to allow hyphens in ciphertext.
        
        Called by the decrypt method.
        
        Arguments:  none.
        
        Returns:  nothing.
        """
        new_text = ""
        for char in self.ciphertext:
            # Discard any space and any non-alphanumeric characters
            #  (except hyphens).
            if (char.upper() in ALPHANUM):
                new_text += char.upper()
            # end if
        # end for
        self.ciphertext = new_text
        return
        # end function
    
    def _invert_matrix(self, mod):
        """Internal function which takes a 3x3 matrix and finds its
        inverse.
        
        Arguments:
        - mod -- the length of the alphabet.
        
        Returns:  the inverted matrix.
        """
        # Turn matrix elements into algebraic notation.
        a = self.matrix[0]
        b = self.matrix[1]
        c = self.matrix[2]
        d = self.matrix[3]
        e = self.matrix[4]
        f = self.matrix[5]
        g = self.matrix[6]
        h = self.matrix[7]
        i = self.matrix[8]
        # First calculate the determinant of the matrix.
        determinant = ((a*e*i)+(b*f*g)+(c*d*h)) - ((a*f*h)+(b*d*i)+(c*e*g))
        # Reduce determinant to % mod.
        determinant = determinant % mod
        # Now find the multiplicative inverse of det % mod, expressed as
        #  x for:  (x * det) % mod = 1
        # For small ranges, brute force is simpler than an equation.
        for num in range(mod):
            if ((num * determinant) % mod) == 1:
                determinant_inverse = num
                break
            # end if
        # end for
        # Now construct the adjugate matrix % mod of the key matrix.
        adjugate_matrix = [None for _ in range(9)]
        adjugate_matrix[0] = ((e*i)-(f*h)) % mod
        adjugate_matrix[1] = (((b*i)-(c*h)) * -1) % mod
        adjugate_matrix[2] = ((b*f)-(c*e)) % mod
        adjugate_matrix[3] = (((d*i)-(f*g)) * -1) % mod
        adjugate_matrix[4] = ((a*i)-(c*g)) % mod
        adjugate_matrix[5] = (((a*f)-(c*d)) * -1) % mod
        adjugate_matrix[6] = ((d*h)-(e*g)) % mod
        adjugate_matrix[7] = (((a*h)-(b*g)) * -1) % mod
        adjugate_matrix[8] = ((a*e)-(b*d)) % mod
        # Finally, multiply the inverse determinant by each element of
        #  the adjugate matrix % mod to arrive at the inverse of the
        #  key matrix.
        for num in range(9):
            self.matrix[num] = (determinant_inverse *
                                adjugate_matrix[num]) % mod
        # end for
    # end function
    
    def _matrix_from_keyword(self):
        """Internal function that builds a key matrix from a keyword.
        Called by both encrypt and decrypt functions.  (Decrypt must
        reconstruct the matrix in order to build its inverse.)
        
        Arguments:  none
        
        Returns:  nothing.
        """
        # Turn the first nine letters of the keyword into the key
        #  matrix.  If the keyword is less than nine letters, then pad
        #  with the beginning of the alphabet.
        pad = 0
        for pos in range(9):
            if pos < len(self.keyword):
                self.matrix[pos] = ALPHANUM.index(self.keyword[pos])
            else:
                self.matrix[pos] = pad
                pad += 1
            # end if
        # end for
        return
    # end function
    
    def _matrix_mult(self, m, t, mod):
        """Internal function which performs matrix multiplication on a
        3x3 matrix and a trigram.
        
        Arguments:
        - m -- the key matrix
        - t -- a trigram, a 1x3 column vector to be multiplied
        - mod -- the length of the alphabet
        
        Returns:  a tuple containing the three final values.
        """
        c1 = ((m[0] * t[0]) + (m[1] * t[1]) + (m[2] * t[2])) % 37
        c2 = ((m[3] * t[0]) + (m[4] * t[1]) + (m[5] * t[2])) % 37
        c3 = ((m[6] * t[0]) + (m[7] * t[1]) + (m[8] * t[2])) % 37
        return c1, c2, c3
    # end function
