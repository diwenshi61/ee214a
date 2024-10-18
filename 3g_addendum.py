# It doesn't let me submit non-jpgs so I uploaded my solution here:
# https://github.com/diwenshi61/ee214a
# To show I didn't just upload the file after the deadline here is the hash of the file:
# MD5: 2a25db5a5dc4b974e77d4acb52467840
# SHA256: 809ea677b0e638374d4f5fdf4861477855d05d0f68844d9142954d3ee1b3ba8c
# If you run this hashing script (also uploaded to the same github) you will see the file hash matches this image, so I didn't modify it after the date of submission.

import sys
import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
sha256 = hashlib.sha256()

with open(sys.argv[1], 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)
        sha256.update(data)

print("MD5: {0}".format(md5.hexdigest()))
print("SHA256: {0}".format(sha256.hexdigest()))