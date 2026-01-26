import itertools
import os
import string
import argparse
import sys

def get_substitutions():
    return {
        'a': ['4', '@', '&', '^', '!', '1', ' '],
        'b': ['8', '*', '9', '&'],
        'c': ['ts','TS'],
        'd': ['$'],
        'e': ['3', '€'],
        'f': ['ph'],
        'g': ['6', '9', '&'],
        'h': ['#'],
        'i': ['1', '!', '|','l', '(', ')'],
        'j': [],
        'k': ['x'],
        'l': ['1', '|', '£', 'I', '[', '!', '(', ')'],
        'm': ['^^'],
        'n': ['№', '#'],
        'o': ['0', '()', '°', '*'],
        'p': ['%', '9', '+', '£'],
        'q': ['9'],
        'r': ['®'],
        's': ['5', '$', '§', '#'],
        't': ['7'],
        'u': ['|_|'],
        'v': [],
        'w': ['vv', 'ω'],
        'x': ['%', '><', '×'],
        'y': ['¥', 'j', 'γ'],
        'z': ['2', '0']
    }

def get_keyboard_symbols():
    return list(string.punctuation)

def parse_number_input(num_inputs):
    final_numbers = []
    for num_string in num_inputs:
        parts = num_string.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    step = 1 if start <= end else -1
                    for i in range(start, end + step, step):
                        final_numbers.append(str(i))
                except ValueError:
                    print(f"[!] Warning: Invalid range format ignored: {part}")
            elif part:
                final_numbers.append(part)
    return final_numbers

def generate_wordlist(words, numbers, output_file, min_len, max_len):
    subs = get_substitutions()
    symbols = get_keyboard_symbols()
    count = 0
    
    def write_if_valid(f_obj, line):
        nonlocal count
        clean_line = line.strip()
        length = len(clean_line)
        # Apply min/max filter to the FINAL generated string
        if (min_len is None or length >= min_len) and \
           (max_len is None or length <= max_len):
            f_obj.write(line)
            count += 1

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for word in words:
                word = word.strip()
                if not word: continue
                
                char_options = []
                for char in word:
                    l_c, u_c = char.lower(), char.upper()
                    options_set = {l_c, u_c}
                    if l_c in subs: options_set.update(subs[l_c])
                    char_options.append(list(options_set))

                print(f"[*] Permutating: {word}...")
                for combination in itertools.product(*char_options):
                    gen_word = "".join(combination)
                    
                    # If it's a pure letter permutation, run the complex patterns
                    if gen_word.isalpha() and numbers:
                        write_if_valid(f, gen_word + '\n')
                        for num in numbers:
                            # Patterns with 1 symbol
                            for sym in symbols:
                                write_if_valid(f, f"{gen_word}{sym}{num}\n")
                                write_if_valid(f, f"{gen_word}{num}{sym}\n")
                                write_if_valid(f, f"{sym}{gen_word}{num}\n")
                                write_if_valid(f, f"{num}{gen_word}{sym}\n")
                                write_if_valid(f, f"{gen_word}{num}{sym}{num}\n")

                            # Pattern with 2 symbols (the "two sources" requirement)
                            for sym1, sym2 in itertools.product(symbols, repeat=2):
                                write_if_valid(f, f"{gen_word}{sym1}{num}{sym2}\n")
                    else:
                        # For leet speak variants, just check length and write
                        write_if_valid(f, gen_word + '\n')

        print(f"\n[+] Success! {count} valid rows saved to: {os.path.abspath(output_file)}")
    except IOError as e:
        print(f"[-] Error writing to file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional Wordlist Generator CLI")
    parser.add_argument("inputs", nargs='*', help="Direct words or number patterns")
    parser.add_argument("-f", "--file", help="File containing source words")
    parser.add_argument("-o", "--output", required=True, help="Output filename")
    parser.add_argument("--min", type=int, help="Min length of GENERATED strings")
    parser.add_argument("--max", type=int, help="Max length of GENERATED strings")
    
    args = parser.parse_args()

    target_words = []
    number_pattern_strings = []

    # Load file
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, 'r') as f:
                target_words.extend([line.strip() for line in f if line.strip()])
        else:
            print(f"[-] Error: File {args.file} not found.")
            sys.exit(1)

    # CLI Inputs
    for item in args.inputs:
        if any(char.isdigit() for char in item):
            number_pattern_strings.append(item)
        else:
            target_words.append(item)

    if not target_words:
        print("[-] Error: No words provided.")
        sys.exit(1)

    parsed_numbers = parse_number_input(number_pattern_strings)
    generate_wordlist(target_words, parsed_numbers, args.output, args.min, args.max)
