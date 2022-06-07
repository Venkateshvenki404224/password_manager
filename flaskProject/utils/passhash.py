alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def caeser(plain_text,shift_no,cipher_choice):
    final_out = ""
    for char in plain_text:
        if char in alphabet:
            position = alphabet.index(char)
            if cipher_choice == 'encode':
                new_pos = position + shift_no
                new_letter = alphabet[new_pos]
                final_out += new_letter
            else:
                new_pos = position - shift_no
                new_letter = alphabet[new_pos]
                final_out += new_letter
        else:
            final_out += char
    print(f"The {cipher_choice}d text is: {final_out}")


Final = True
while Final:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    shift = shift % 26
    caeser(text, shift, direction)
    restart = input('Type yes if you want to go again Otherwise type no :\n')
    if restart == "no":
        Final = False
        print("Good Bye")
