from unidecode import unidecode
import styles

def decodetxt(text):
    # TODO do the reverse of encode, meh
    decoded_text = unidecode(text)
    return decoded_text

def encodetxt(text, style=None):
    # TODO this can be a bit better, i mean really
    d_styles = {
              'bold':        styles.BOLD,
              'italic':      styles.ITALIC,
              'bold_italic': styles.BOLD_ITALIC
             }
    if style.lower() in d_styles.keys():
        style = d_styles[style.lower()]
    else:
        style = d_styles['bold']

    characters = list(text)

    for position, char in enumerate(characters):
        if char in style.keys():
            characters[position] = style[char]
    return ''.join(characters)

