import girder_client
import argparse
import glob


def create_or_get_collection(gc, collection_name):
    # Create a collection (if needed)
    collections = gc.listCollection()  # Assuming relatively small number.
    collections = [collection for collection in collections if collection['name'] == collection_name]
    if not collections:
        collections = [gc.createCollection(collection_name)]
    collection_id = collections[0]['_id']
    print(f'{collection_name=} {collection_id=}')
    return collection_id


def create_or_get_folder(gc, collection_id, folder_name):
    # Create a folder (if needed)
    folders = gc.listFolder(parentId=collection_id, parentFolderType='collection')  # Assuming relatively small number.
    folders = [folder for folder in folders if folder['name'] == folder_name]
    if not folders:
        folders = [gc.createFolder(name=folder_name, parentId=collection_id, parentType='collection')]
    folder_id = folders[0]['_id']
    print(f'{folder_name=} {folder_id=}')
    return folder_id


def import_slide(gc, assetstore_id, root_directory, folder_id, slide, return_slide_id=False):
    # API: https://automl.ai.uky.edu/api/v1/assetstore/635beec8e30b1d0b7c14ddbd/import
    # importPath=/mounted_assetstore/needle-biopsy-deident/deident_00e24427-6b2f-4919-9664-1c630825db42.isyntax
    # &leafFoldersAsItems=false
    # &destinationId=635be36deb3717ab9f09c1d4
    # &destinationType=folder
    # &progress=true
    gc.post(path=f'assetstore/{assetstore_id}/import', parameters={
        'importPath': f'{root_directory}/{slide}',
        'leafFoldersAsItems': 'false',
        'destinationId': folder_id,
        'destinationType': 'folder',
    })

    if not return_slide_id:
        return None

    # Find the uploaded slide id
    items = gc.listItem(folder_id)
    # print(f'{list(items)=}')
    items = [item for item in items if item['name'] == slide]
    item_id = items[0]['_id']
    print(f'{items[0]["name"]=} {item_id=}')
    return item_id


def add_dsa_args(parser):
    parser.add_argument("--api_key", required=True, type=str, help="API key")
    parser.add_argument("--api_url", default='https://dsa.ai.uky.edu/api/v1', type=str, help="API url")
    parser.add_argument("--collection_name", required=True, type=str, help="Name of collection to create/use")
    parser.add_argument("--assetstore_id", default='635beec8e30b1d0b7c14ddbd', type=str,
                        help="Assetstore ID that contains the slides. See Admin Console -> Assetstores")
    parser.add_argument("--root_directory", required=True, type=str,
                        help="Root directory for slides inside the assetstore (absolute path)")


def main():
    parser = argparse.ArgumentParser(description="dsa import")
    add_dsa_args(parser)
    parser.add_argument("--folder_name", required=True, type=str, help="Name of folder to create/use")
    parser.add_argument("--slides", required=False, type=str, help="List of slides to import", nargs='+')


    args = parser.parse_args()

    print("start")
    gc = girder_client.GirderClient(apiUrl=args.api_url)
    gc.authenticate(apiKey=args.api_key)
    collection_id = create_or_get_collection(gc, args.collection_name)
    folder_id = create_or_get_folder(gc, collection_id, args.folder_name)

    # Upload slides
    for slide in args.slides:
        print(f'importing {slide=}')
        import_slide(gc, args.assetstore_id, args.root_directory, folder_id, slide)


if __name__ == "__main__":
    main()