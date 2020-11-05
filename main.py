import argparse
import json
import os


# package data as object
class VerificationResult:

    def __init__(self, num_samples, num_each_label, num_error, correct_ratio, error_lines, error_lines_index, labels,
                 labels_files, labels_files_name):
        self.num_samples = num_samples
        self.num_each_labels = num_each_label
        self.num_error = num_error
        self.correct_ratio = correct_ratio
        self.labels = list(labels)
        self.status = 'successful'
        self.labels_files = labels_files
        self.labels_files_name = labels_files_name
        if self.num_error > 0:
            self.error_lines = error_lines
            self.error_lines_index = error_lines_index
            self.status = 'failure'


# single label dataset verification module
def verify_single_classification(input_filepath):
    error_lines = []
    error_lines_index = []
    labels = set()
    num_error = 0
    num_each_label = {}
    labels_files = {}
    labels_files_name = {}
    with open(input_filepath) as file:
        for index, line in enumerate(file):
            contents = line.split('\t')
            if len(contents) == 2:
                label = contents[0]
                labels.add(label)

                # count labels files
                if label not in labels_files:
                    labels_files[label] = []
                else:
                    labels_files[label].append(line)

                # count each labels
                if label not in num_each_label:
                    num_each_label[label] = 1
                else:
                    num_each_label[label] += 1

            # count error lines
            if not len(contents) == 2:
                num_error += 1
                error_lines.append(line)
                error_lines_index.append(str(index + 1))

    # create labels file name
    label_str = 'label'
    for index, label in enumerate(labels):
        file_name = label_str + str(index + 1) + '.txt'
        labels_files_name[label] = file_name

    # compute statistical indicators
    num_samples = index + 1
    correct_ratio = (num_samples - num_error) / num_samples

    verification_result = VerificationResult(num_samples, num_each_label, num_error, correct_ratio, error_lines,
                                             error_lines_index, labels,
                                             labels_files, labels_files_name)
    return verification_result


# multi labels dataset verification module
def verify_multi_classification(input_filepath):
    error_lines = []
    error_lines_index = []
    labels = set()
    num_error = 0
    num_each_label = {}
    labels_files_name = {}
    labels_files = {}
    with open(input_filepath) as file:
        for index, line in enumerate(file):
            contents = line.split('\t')
            if len(contents) == 2:
                label_list = contents[0].split(',')
                labels.update(label_list)

                # count labels files
                if label not in labels_files:
                    labels_files[label] = []
                else:
                    labels_files[label].append(line)

                # count each labels
                for label in label_list:
                    if label not in num_each_label:
                        num_each_label[label] = 1
                    else:
                        num_each_label[label] += 1

            # count error lines
            if '' in label_list or not len(contents) == 2:
                num_error += 1
                error_lines.append(line)
                error_lines_index.append(str(index + 1))

    # create labels file name
    label_str = 'label'
    for index, label in enumerate(labels):
        file_name = label_str + str(index + 1) + '.txt'
        labels_files_name[label] = file_name

    # compute statistical indicators
    num_samples = index + 1
    correct_ratio = (num_samples - num_error) / num_samples

    verification_result = VerificationResult(num_samples, num_each_label, num_error, correct_ratio, error_lines,
                                             error_lines_index, labels,
                                             labels_files, labels_files_name)
    return verification_result


# named entity recognition dataset verification module
def verify_named_entity_recognition(input_filepath):
    error_lines = []
    error_lines_index = []
    labels = set()
    num_error = 0
    num_each_label = {}
    labels_files_name = {}
    labels_files = {}
    with open(input_filepath) as file:
        for index, line in enumerate(file):

            # count error lines
            try:
                json_obj = json.loads(line)
            except Exception:
                error_lines.append(line)
                error_lines_index.append(str(index + 1))
                num_error += 1
            if json_obj and not ('raw_text' in json_obj and 'entities' in json_obj):
                error_lines.append(line)
                error_lines_index.append(str(index + 1))
                num_error += 1

            if json_obj and 'entities' in json_obj and len(json_obj['entities']) > 0:
                for entity in json_obj['entities']:
                    label = entity['class_name']
                    labels.add(label)

                    # count labels files
                    if label not in labels_files:
                        labels_files[label] = []
                    else:
                        labels_files[label].append(line)

                    # count each labels
                    if label not in num_each_label:
                        num_each_label[label] = 1
                    else:
                        num_each_label[label] += 1

    # create labels file name
    label_str = 'label'
    for index, label in enumerate(labels):
        file_name = label_str + str(index + 1) + '.txt'
        labels_files_name[label] = file_name

    # compute statistical indicators
    num_samples = index + 1
    correct_ratio = (num_samples - num_error) / num_samples

    verification_result = VerificationResult(num_samples, num_each_label, num_error, correct_ratio, error_lines,
                                             error_lines_index, labels,
                                             labels_files, labels_files_name)
    return verification_result


def dump_result(output_directory_path, verification_result):
    statistical_indicators_filename = 'statistics.json'
    error_lines_filename = 'error_lines.txt'
    error_lines_index_filename = 'error_lines_index.txt'

    if verification_result.num_error > 0:
        error_lines = verification_result.error_lines
        error_lines_index = verification_result.error_lines_index

        # write error lines
        with open(os.path.join(output_directory_path, error_lines_filename), 'w') as file:
            file.write(''.join(error_lines))

        # write error lines index
        with open(os.path.join(output_directory_path, error_lines_index_filename), 'w') as file:
            file.write(','.join(error_lines_index))

        # write label files
        labels_files = verification_result.labels_files_name
        files = verification_result.labels_files
        for label in labels_files:
            file_name = labels_files[label]
            file_content = files[label]
            with open(file_name, 'w') as file:
                file.write(''.join(file_content))

        del verification_result.error_lines
        del verification_result.error_lines_index
        del verification_result.labels_files

    # write statistical indicators
    with open(os.path.join(output_directory_path, statistical_indicators_filename), 'w') as file:
        json.dump(verification_result, file, ensure_ascii=False, default=lambda obj: obj.__dict__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--type', choices=['SC', 'MC', 'NER'], default='SC', type=str,
                        help='SC: single classification, MC: multi classification, NER: named entity recognition')
    args = parser.parse_args()
    input_filepath = args.input
    output_directory_path = args.output
    dataset_type = args.type
    if dataset_type == 'SC':
        verification_result = verify_single_classification(input_filepath)
    elif dataset_type == 'MC':
        verification_result = verify_multi_classification(input_filepath)
    else:
        verification_result = verify_named_entity_recognition(input_filepath)
    dump_result(output_directory_path, verification_result)


if __name__ == '__main__':
    main()
