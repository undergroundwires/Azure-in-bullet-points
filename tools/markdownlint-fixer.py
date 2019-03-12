'''
Not tested for generic usage. It fixes following lint issues in md files:
    MD007 - Unordered list indentation
    MD009 - No trailing whitespaces
    MD004 - Unordered list style
    MD002 - Headings should be surruonded by blank lines
'''
import math, os.path, sys, argparse

parser = argparse.ArgumentParser(description="markdownlint fixer")
parser.add_argument('-i',
                    help='File to fix',
                    dest='filename',
                    type=argparse.FileType('r', encoding='UTF-8'), 
                    required=True)
args = parser.parse_args()
path = str(args.filename.name)
new_lines = []

def count_leading_whitespaces(text):
    return len(text) - len(text.lstrip(' '))

with open(path, 'r', encoding = 'UTF-8') as file:
    lines = file.readlines()
    for line_index, line in enumerate(lines):
        # Ensure 2 whitespaces are used instead of tabs (MD007 - Unordered list indentation)
        if line.startswith('    '):
            total_white_spaces = count_leading_whitespaces(line)
            line = line.lstrip(' ')
            total_white_spaces = total_white_spaces / 2
            if int(total_white_spaces) != total_white_spaces:
                normalized = math.ceil(total_white_spaces)
                print(f'Bad total white spaces: {str(total_white_spaces)} normalized to {str(normalized)}. Line: "{line}"')
                total_white_spaces = normalized
            total_white_spaces = int(total_white_spaces)
            for i in range(total_white_spaces):
                line = ' ' + line
        # Fix MD009 - No trailing whitespaces
        text_part = line.split('\n')[0].rstrip(' ')
        if line.endswith('\n'):
            line = f'{text_part}\n'
        else:
            line = f'{text_part}'
        # MD004 - Unordered list style
        if line.lstrip().startswith('-'):
            total_white_spaces = 0
            while line.startswith(' '):
                total_white_spaces += 1
                line = line[1:len(line)]
            line = "*" + line[1:len(line)]
            while total_white_spaces != 0:
                line = ' ' + line
                total_white_spaces -= 1
        # MD002 - Headings should be surruonded by blank lines
        if line_index < len(lines) - 1:
            next_line = lines[line_index + 1].lstrip(' ')
            if next_line.startswith('#') and line != '\n':
                line = f'{line}\n'
            else:
                if line.lstrip().startswith("#") and next_line != '\n':
                    line = f'{line}\n'
        new_lines.append(line)

filename, file_extension = os.path.splitext(path)
output_path = f'{filename}_fixed{file_extension}'
with open(output_path, 'w', encoding='UTF-8') as fixed_file:
    fixed_file.writelines(new_lines)