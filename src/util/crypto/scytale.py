
def encrypt_scytale(plaintext: str, circumference: int) -> str:
    """Encrypt plaintext using a Scytale cipher with a circumference number.
    
    We make character sequences by selecting every 'circumference'th character
    starting from 1st, 2nd, ... characters and append these sequences

    @param plaintext text to be encrypted
    @type plaintext string
    @param circumference the number of rows used at the scytale
    @type circumference positive integer

    @return encrypted string
    """
    
    ciphertext = ''
    for i in range(circumference):
        ciphertext += ''.join(plaintext[i::circumference])
    return ciphertext

def decrypt_scytale(ciphertext: str, circumference: int) -> str:
    """Decrypt ciphertext using a Scytale cipher with a circumference number.
    
    1. Check if the length of the ciphertext is a perfect multiple of the circumference
    2. If yes, the decription is simmilar to encription
    2. Else we divide the cypher text into two parts based on the length of rows in the encripting method
        - whole rows
        - truncated rows
    3. We sort out the characters from the two parts alternatively

    @param ciphertext text to be decrypted
    @type ciphertext string
    @param circumference the number of rows used at the scytale
    @type circumference positive integer

    @return decrypted string
    """
    plaintext = ''
    length = len(ciphertext)
    whole_seq_nr = length // circumference

    if length % circumference == 0:
        for i in range(whole_seq_nr):
            plaintext += ''.join(ciphertext[i::whole_seq_nr])
    else:
        whole_row_nr = length - whole_seq_nr * circumference
        seq_nr = whole_seq_nr + 1
        whole_rows = ciphertext[:seq_nr*whole_row_nr]
        trunc_rows = ciphertext[seq_nr*whole_row_nr:]
        for i in range(whole_seq_nr):
            plaintext += ''.join(whole_rows[i::seq_nr])
            plaintext += ''.join(trunc_rows[i::whole_seq_nr])
        plaintext += ''.join(whole_rows[whole_seq_nr::seq_nr])

    return plaintext
