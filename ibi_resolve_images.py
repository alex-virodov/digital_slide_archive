import argparse
import girder_client
from ibi_import import create_or_get_collection, create_or_get_folder

# To make a list of not-yet-imported slides:
# $ grep -v -x -f ibi_ml_import.txt full_dataset_slides_colon.txt | sort -R | head -n 100

def parse_slides_file(a_file):
    # Simple one-line-per-file format.
    if a_file is None:
        return []
    with open(a_file, 'rt') as f:
        return [l.strip() for l in f.readlines()]


def main():
    parser = argparse.ArgumentParser(description="dsa import")
    parser.add_argument("--api_key", required=True, type=str, help="API key")
    parser.add_argument("--api_url", default='https://dsa.ai.uky.edu/api/v1', type=str, help="API url")
    parser.add_argument("--collection_name", required=True, type=str, help="Name of collection to create/use")
    parser.add_argument("--folder_name", required=True, type=str, help="Name of folder to create/use")
    parser.add_argument("--slides", required=False, type=str, help="List of slides to import", nargs='+')
    parser.add_argument("--slides_file", required=False, type=str, help="File with list of slides to import")

    args = parser.parse_args()
    slides = (args.slides if args.slides is not None else []) + parse_slides_file(args.slides_file)


    print("start")
    gc = girder_client.GirderClient(apiUrl=args.api_url)
    gc.authenticate(apiKey=args.api_key)
    collection_id = create_or_get_collection(gc, args.collection_name)
    folder_id = create_or_get_folder(gc, collection_id, args.folder_name)
    for slide in slides:
        if slide.strip().startswith('#'):
            # Display comments, useful to break batches apart.
            print(f'{slide}')
            continue
        result = gc.listItem(folder_id, name=slide)
        item = next(result)
        link = f'https://dsa.ai.uky.edu/#item/{item["_id"]}'
        # print(f'{slide=} {link=}')
        print(f'{link} | {slide}')



if __name__ == '__main__':
    main()