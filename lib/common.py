import hashlib


def fetch_file_md5(file_path):
    obj = hashlib.md5()
    f = open(file_path, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        obj.update(b)
    f.close()
    return obj.hexdigest()

