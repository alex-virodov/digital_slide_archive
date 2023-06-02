# --api_key ZZZ --collection_name "Molavi Conference" --root_directory /mounted_assetstore/deident_import/

import pandas as pd
import numpy as np
import math
import json
import re
import girder_client
import argparse
from ibi_import import create_or_get_collection, import_slide, add_dsa_args

corrections = {
}


def main():
    parser = argparse.ArgumentParser(description="dsa import")
    add_dsa_args(parser)
    args = parser.parse_args()

    print("start")
    gc = girder_client.GirderClient(apiUrl=args.api_url)
    gc.authenticate(apiKey=args.api_key)
    collection_id = create_or_get_collection(gc, args.collection_name)

    missing_cases = []
    case_column = 'UK Accession #'
    diagnosis_column = 'Diagnosis'
    history_column = 'History'
    xls = pd.ExcelFile('case_data_identified/EDUCORePS Molavi List.xlsx')
    with open('case_data_identified/ident_case_list.json') as f:
        case_data_all = json.load(f)
    with open('case_data_identified/slide_data.json') as f:
        slide_data_by_slide = json.load(f)
        slide_data_by_case = {}
        for slide, case in slide_data_by_slide.items():
            # Strip specimen
            match = re.fullmatch(r'([A-Za-z\d]+\-\d+).*', str(case))
            case_stripped = match.group(1)
            # print(f'{slide=} {case_stripped=} {case=}')
            slide_data_by_case[case_stripped] = slide_data_by_case.get(case_stripped, []) + [slide]

    print(f'{xls.sheet_names=}')
    sheets_to_import = xls.sheet_names
    sheets_to_import.remove('Master list')
    for sheet in sheets_to_import:
        # Create a folder (if needed)
        folder_name = sheet
        folders = gc.listFolder(parentId=collection_id,
                                parentFolderType='collection')  # Assuming relatively small number.
        folders = [folder for folder in folders if folder['name'] == folder_name]
        if not folders:
            folders = [gc.createFolder(name=folder_name, parentId=collection_id, parentType='collection')]
        folder_id = folders[0]['_id']
        print(f'{folder_name=} {folder_id=}')

        data = pd.read_excel(xls, sheet)
        print(f'{sheet=}')
        for row_number, row in data.iterrows():
            case = row[case_column]
            if isinstance(case, str):
                if case in corrections:
                    case = corrections[case]
                if re.fullmatch('#.+', str(case)):
                    print(f'Not parsing {case=}')
                    missing_cases.append(case)
                    continue
                # Assuming case is XXX-XXXXX-YYY, where the X's are case and Y's is slide number (which is ignored).
                match = re.fullmatch(r'([A-Za-z\d]+\-[A-Za-z\d]+)([\-\s][A-Za-z\d]+)?', str(case))
                if not match:
                    raise ValueError(f'failed to match {case=}')
                # print(f'{match=} {match[0]=} {match[1]=}')
                case = match[1]
                if case in case_data_all:
                    case_data = case_data_all[case]
                elif case in slide_data_by_case:
                    case = {
                        'SLIDES': slide_data_by_case[case],
                        'AGE_AT_EXAM': '',
                    }
                else:
                    missing_cases.append(case)
                    continue
                print(f'{case=} {row[diagnosis_column]=} {case_data["SLIDES"]=} {case_data["AGE_AT_EXAM"]=}')

                # TODO: remember if slide existed before upload. Upload seems to not do anything if slide is already
                #  there, but we would like to not change metadata if already uploaded (to preserve manual changes).
                # Upload slides
                # API: https://automl.ai.uky.edu/api/v1/assetstore/635beec8e30b1d0b7c14ddbd/import
                # importPath=/mounted_assetstore/needle-biopsy-deident/deident_00e24427-6b2f-4919-9664-1c630825db42.isyntax
                # &leafFoldersAsItems=false
                # &destinationId=635be36deb3717ab9f09c1d4
                # &destinationType=folder
                # &progress=true
                for slide_idx, slide in enumerate(case_data["SLIDES"]):
                    print(f'importing {slide=}')
                    item_id = import_slide(gc, args.assetstore_id, args.root_directory, folder_id, slide,
                                           return_slide_id=True)

                    # Row number + 2 to match the excel row number (+1 for zero-based, +1 for header)
                    sequential_name = f'{folder_name} {row_number+2}'
                    if len(case_data["SLIDES"]) > 1:
                        sequential_name = f'{sequential_name} (slide {slide_idx+1})'
                    gc.put(f'item/{item_id}', {'name': sequential_name})
                    print(f'{sequential_name=}')

                    # Use the details tag (https://www.w3schools.com/tags/tag_details.asp) to hide the diagnosis
                    # behind a clickable text.
                    diagnosis_spoiler_html = \
                        f'<details><summary><a><u>Click here to show answer</u></a></summary>' \
                        f'{row[diagnosis_column]}</details>'

                    # Write metadata.
                    metadata = {
                        "1) history": str(row[history_column]),
                        "2) age": case_data["AGE_AT_EXAM"],
                        # "3) ICD codes": ", ".join(case_data["ICD10_CD"]),
                        # "4) SNOMED codes": ", ".join(case_data["SNOMED_CD"]),
                        "Diagnosis": diagnosis_spoiler_html,
                    }
                    print(f'{metadata=}')
                    gc.addMetadataToItem(item_id, metadata)





    print(f'\n\n{len(missing_cases)=} {missing_cases=}')


if __name__ == "__main__":
    main()
