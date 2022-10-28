set -x
sudo mkdir -p /mounted_assetstore
sudo mount -t cifs -o username=avirodov,domain=UKRDMC,iocharset=utf8,file_mode=0700,dir_mode=0700,uid=$(id -u),gid=$(id -g) //iso2smb.rdmc.org/IBI/001IBI-TCGA/DSA/assetstore /mounted_assetstore

