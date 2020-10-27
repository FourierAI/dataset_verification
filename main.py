import argparse
import json


def verify_single_classification(input_filepath):
    error_lines = []
    error_lines_index = []
    labels = set()
    with open(input_filepath) as file:
        for index, line in enumerate(file):
            contents = line.split('\t')
            labels.add(contents[0])
            if not len(contents) == 2:
                error_lines.append(line)
                error_lines_index.append(str(index + 1))
    return error_lines, error_lines_index, list(labels)


def verify_multi_classification(input_filepath):
    error_lines = []
    error_lines_index = []
    labels = set()
    with open(input_filepath) as file:
        for index, line in enumerate(file):
            contents = line.split('\t')
            label_list = contents[0].split(',')
            labels.add(label_list)
            if '' in label_list or not len(contents) == 2:
                error_lines.append(line)
                error_lines_index.append(str(index + 1))
    return error_lines, error_lines_index, list(labels)


def verify_named_entity_recognition(input_filepath):
    error_lines = []
    error_lines_index = []
    labels = set()
    with open(input_filepath) as file:
        for index, line in enumerate(file):
            try:
                jsobj = json.loads(line)
            except Exception:
                error_lines.append(line)
                error_lines_index.append(str(index + 1))
            if jsobj and not ('raw_text' in jsobj and 'entities' in jsobj):
                error_lines.append(line)
                error_lines_index.append(str(index + 1))

            if jsobj and 'entities' in jsobj and len(jsobj['entities']) > 0:
                for entity in jsobj['entities']:
                    labels.add(entity['class_name'])

    return error_lines, error_lines_index, list(labels)


def dump_result(output_filepath, error_lines, error_lines_index, labels):
    json_obj = {}
    if len(error_lines) > 0:
        json_obj['result'] = 'failure'
        json_obj['error lines'] = error_lines
        json_obj['error lines index'] = error_lines_index
    else:
        json_obj['result'] = 'successful'
    json_obj['labels'] = labels
    with open(output_filepath, 'w') as file:
        json.dump(json_obj, file, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--type', choices=['SC', 'MC', 'NER'], default='SC', type=str,
                        help='SC: single classification, MC: multi classification, NER: named entity recognition')
    args = parser.parse_args()
    input_filepath = args.input
    output_filepath = args.output
    dataset_type = args.type
    if dataset_type == 'SC':
        error_lines, error_lines_index, labels = verify_single_classification(input_filepath)
    elif dataset_type == 'MC':
        error_lines, error_lines_index, labels = verify_multi_classification(input_filepath)
    else:
        error_lines, error_lines_index, labels = verify_named_entity_recognition(input_filepath)
    dump_result(output_filepath, error_lines, error_lines_index, labels)


if __name__ == '__main__':
    main()
