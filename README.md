
<img width="500" height="751" alt="brepo" src="https://github.com/user-attachments/assets/41d6e590-0f91-4b6d-9f3e-52dba488748a" />

## Powder

Powder is a Python-based password wordlist generator designed for security researchers and penetration testers who need to "cook up" highly targeted dictionaries. Taking a cue from the Breaking Bad aesthetic, this tool specializes in transforming simple seed words into a massive array of potential credentials through advanced permutation and pattern matching.

### Usage

python powder.py 

```
positional arguments:
  inputs               Direct words or number patterns [Allowed format: password root admin 123,1234,12345,1990,1995-2025]

options:
  -h, --help           show this help message and exit
  -f, --file FILE      File containing source words
  -o, --output OUTPUT  Output filename
  --min MIN            Min length of GENERATED strings
  --max MAX            Max length of GENERATED strings
```
### Examples
##### Generate a wordlist of passwords from words 'admin' and 'root' and numbers in the range of 1990-2000, and save the generated content in the output file with the name wordlist.txt:
```
python powder.py admin root 1990-2000 -o wordlist.txt
```
##### Generate a wordlist of passwords with a minimum characters of 10 from company name and numbers such as 123,12345, and range between 2020-2025:
```
python powder.py CompanyName 123,12345,2020-2025 -o research.txt --min 10
```
##### Generate a wordlist of passwords with a minimum characters of 8 and maximum of 14 from a file containing words (each per new line) and numbers such as 123, and range between 2024-2026:
```
python powder.py -f target_names.txt 123,2024-2026 -o output.txt --min 8 --max 14
```

#### Required Modules
- itertools
- os
- string
- argparse
- sys

#### v1.1 Updates
Added:
- Examples in help page
- The number-symbol-word-symbol computed lines
- a tool banner
- README file
