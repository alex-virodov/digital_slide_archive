import girder_client
import argparse
import json
from ibi_import import create_or_get_collection, create_or_get_folder, import_slide, add_dsa_args


def main():
    parser = argparse.ArgumentParser(description="dsa import")
    add_dsa_args(parser)
    parser.add_argument("--folder_name", required=True, type=str, help="Name of folder to create/use")
    parser.add_argument("--json_file", required=True, type=str, help="Json file of list of slides to import")

    args = parser.parse_args()

    with open(args.json_file, 'rt') as f:
        data = json.load(f)

    label_map = {0: 'Benign', 1: 'Malignant'}

    print("start")
    gc = girder_client.GirderClient(apiUrl=args.api_url)
    gc.authenticate(apiKey=args.api_key)
    collection_id = create_or_get_collection(gc, args.collection_name)
    folder_id = create_or_get_folder(gc, collection_id, args.folder_name)

    # Upload slides
    squential_id = 1
    for category in ['training', 'validation']:
        if category in data:
            for item in data[category]:
                image = item['image']
                label = label_map[item['label']]
                print(f'importing {image=}')
                item_id = import_slide(gc, args.assetstore_id, args.root_directory, folder_id, image,
                                       return_slide_id=True)

                metadata = {
                    "label": str(label),
                }
                print(f'{metadata=}')
                gc.addMetadataToItem(item_id, metadata)

                # sequential_name = f'{args.folder_name} {squential_id}'
                # gc.put(f'item/{item_id}', {'name': sequential_name})
                # squential_id += 1

if __name__ == "__main__":
    main()