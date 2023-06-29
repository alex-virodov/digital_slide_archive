import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sha1sum_file", required=True, type=str, help="the generated sha1sum after copy")
    parser.add_argument("--uofl_json_files", required=True, type=str, help="List of json files to check", nargs='+')
    args = parser.parse_args()
    print(f'{args=}')

    uofl_data_dict = {}
    for uofl_json_file in args.uofl_json_files:
        with open(uofl_json_file, 'rt') as f:
            file_list = json.load(f)
            uofl_data_dict.update({file_entry["deident_file_path"]: file_entry["hash_sha1_after"]
                                   for file_entry in file_list})
    test_key = list(uofl_data_dict.keys())[0]
    print(f'{len(uofl_data_dict)=} {test_key=} {uofl_data_dict[test_key]=}')

    after_copy_dict = {}
    with open(args.sha1sum_file, 'rt') as f:
        file_list = f.readlines()
        file_list = [line.strip().split() for line in file_list]
        after_copy_dict = {line[1]: line[0] for line in file_list}

    print(f'{len(after_copy_dict)=} {test_key=} {after_copy_dict[test_key]=}')

    matching = 0
    mismatching = 0
    extra_in_uofl = set(uofl_data_dict.keys()).difference(set(after_copy_dict.keys()))
    extra_in_ours = set(after_copy_dict.keys()).difference(set(uofl_data_dict.keys()))
    print(f'{extra_in_uofl=}')
    print(f'{extra_in_ours=}')

    for key in set(uofl_data_dict.keys()).intersection(set(after_copy_dict.keys())):
        if uofl_data_dict[key] == after_copy_dict[key]:
            matching += 1
        else:
            print(f'mismatch! {key=} {uofl_data_dict[key]=} {after_copy_dict[key]=}')
            mismatching += 1


    print(f'{matching=} {mismatching=} {len(extra_in_uofl)=} {len(extra_in_ours)=}')





if __name__ == '__main__':
    main()