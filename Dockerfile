# Note(avirodov): The first version was built from Dockerfile.v1 which was 'FROM girder/tox-and-node'
# latest at the time. However, that Dockerfile.v1 no longer builds, and I don't have a track of which version was used.
# So I am using the isyntax-supporting build as the base for further DSA fixes.

FROM ghcr.io/innovationcore/dsa_common_isyntax:v1

# Allow read-only slide access, but read-write annotation. The flag was already there, but there was no test for it
# in annotation update access checking.
# ./large_image/girder_annotation/girder_large_image_annotation/rest/annotation.py
COPY ibi_girder_large_image_annotation.patch .
RUN patch -d .. -p1 < ibi_girder_large_image_annotation.patch
