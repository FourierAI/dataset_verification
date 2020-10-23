# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()
    input_filepath = args.input
    output_filepath = args.output

    output_content = []
    error_lines = []
    labels = set()
    with open(input_filepath) as file:
        for index, line in enumerate(file):
            contents = line.split('\t')
            labels.add(contents[0])
            if not len(contents) == 2:
                output_content.append(contents)
                error_lines.append(str(index))

    if len(output_content) > 0:
        with open(output_filepath, 'a+') as file:
            file.write('-' * 10 + 'error lines' + '-' * 10 + '\n')

    with open(output_filepath, 'a+') as file:
        for content in output_content:
            file.write(''.join(content))

    if len(output_content) > 0:
        with open(output_filepath, 'a+') as file:
            file.write('-' * 10 + 'error lines index' + '-' * 10 + '\n')

    if len(error_lines) > 0:
        with open(output_filepath, 'a+') as file:
            file.write(str(error_lines) + '\n')
    else:
        with open(output_filepath, 'a+') as file:
            file.write('-' * 10 + 'dataset is verified successfully!' + '-' * 10 + '\n')

    with open(output_filepath, 'a+') as file:
        file.write('-' * 10 + 'Dataset labels' + '-' * 10 + '\n')

    with open(output_filepath, 'a+') as file:
        file.write(str(list(labels)))
