
def encrypt_railfence(plaintext: str, nr_rails: int, binary: bool) -> str:
    """Encrypt plaintext using a Railfence cipher with a rail number.

    @param plaintext text to be encrypted
    @type plaintext string
    @param nr_rails the number of rails used at the railfence
    @type nr_rails positive integer

    @return encrypted string
    """
    low_rail_index = nr_rails - 1
    step = 2*(low_rail_index)

    ciphertext = plaintext[::step]
    for rail_i in range(1, low_rail_index):
        odd_chars = plaintext[rail_i::step]
        even_chars = plaintext[step-rail_i::step]
        merged_chars = [None]*(len(odd_chars)+len(even_chars))
        merged_chars[0::2] = odd_chars
        merged_chars[1::2] = even_chars
        ciphertext += (bytes(merged_chars) if binary else ''.join(merged_chars))
    ciphertext += plaintext[low_rail_index::step]

    return ciphertext

def decrypt_railfence(ciphertext: str, nr_rails: int, binary: bool) -> str:
    """Decrypt ciphertext using a Railfence cipher with a rail number.

    @param ciphertext text to be decrypted
    @type ciphertext string
    @param nr_rails the number of rails used at the railfence
    @type nr_rails positive integer

    @return decrypted string
    """
    length = len(ciphertext)
    segment_length = nr_rails - 1
    step = 2 * segment_length
    segment_nr = length // segment_length
    back_n_forth_segment_nr = segment_nr // 2
    truncated_segment_length = length % (segment_length * 2)

    plaintext = [None]*length

    processed_length = back_n_forth_segment_nr
    if truncated_segment_length > 0:
        processed_length += 1
    plaintext[::step] = ciphertext[:processed_length]

    for rail_i in range(1, segment_length):
        if truncated_segment_length <= rail_i:
            rail_length = 2 * back_n_forth_segment_nr
        elif truncated_segment_length <= 2 * segment_length - rail_i:
            rail_length = 2 * back_n_forth_segment_nr + 1
        else:
            rail_length = 2 * back_n_forth_segment_nr + 2
        rail = ciphertext[processed_length:processed_length+rail_length]
        processed_length += rail_length

        odd_chars = rail[0::2]
        even_chars = rail[1::2]
        plaintext[rail_i::step] = odd_chars
        plaintext[step-rail_i::step] = even_chars

    plaintext[segment_length::step] = ciphertext[processed_length:]

    return bytes(plaintext) if binary else ''.join(plaintext)
