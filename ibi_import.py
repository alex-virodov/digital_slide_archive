import girder_client
import argparse
import glob

def main():
    parser = argparse.ArgumentParser(description="dsa import")
    parser.add_argument("--api_key", required=True, type=str, help="API key")
    parser.add_argument("--api_url", default='https://automl.ai.uky.edu/api/v1', type=str, help="API url")
    parser.add_argument("--collection_name", required=True, type=str, help="Name of collection to create/use")
    parser.add_argument("--folder_name", required=True, type=str, help="Name of folder to create/use")
    parser.add_argument("--assetstore_id", default='635beec8e30b1d0b7c14ddbd', type=str,
                        help="Assetstore ID that contains the slides. See Admin Console -> Assetstores")
    parser.add_argument("--root_directory", required=True, type=str,
                        help="Root directory for slides inside the assetstore (absolute path)")
    parser.add_argument("--slides", required=True, type=str, help="List of slides to import", nargs='+')

    args = parser.parse_args()

    print("start")
    gc = girder_client.GirderClient(apiUrl=args.api_url)
    gc.authenticate(apiKey=args.api_key)

    # Create a collection (if needed)
    collections = gc.listCollection()  # Assuming relatively small number.
    collections = [collection for collection in collections if collection['name'] == args.collection_name]
    if not collections:
        collections = [gc.createCollection(args.collection_name)]
    collection_id = collections[0]['_id']
    print(f'{collection_id=}')

    # Create a folder (if needed)
    folders = gc.listFolder(parentId=collection_id, parentFolderType='collection')  # Assuming relatively small number.
    folders = [folder for folder in folders if folder['name'] == args.folder_name]
    if not folders:
        folders = [gc.createFolder(name=args.folder_name, parentId=collection_id, parentType='collection')]
    folder_id = folders[0]['_id']
    print(f'{folder_id=}')

    # Upload slides
    # API: https://automl.ai.uky.edu/api/v1/assetstore/635beec8e30b1d0b7c14ddbd/import
    # importPath=/mounted_assetstore/needle-biopsy-deident/deident_00e24427-6b2f-4919-9664-1c630825db42.isyntax
    # &leafFoldersAsItems=false
    # &destinationId=635be36deb3717ab9f09c1d4
    # &destinationType=folder
    # &progress=true
    for slide in args.slides:
        print(f'importing {slide=}')
        gc.post(path=f'assetstore/{args.assetstore_id}/import', parameters={
            'importPath': f'{args.root_directory}/{slide}',
            'leafFoldersAsItems': 'false',
            'destinationId': folder_id,
            'destinationType': 'folder',
        })


if __name__ == "__main__":
    main()