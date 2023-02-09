import hashlib

class HashHelper():
    def __init__(self, binary):
        self.binary = binary

        with open(binary, 'rb') as my_bin:
            f = my_bin.read()

        hash_list = [
            f'md5: {self.md5sum(f)}',
            f'sha1: {self.sha1sum(f)}',
            f'sha256: {self.sha256sum(f)}',
            f'sha512: {self.sha512sum(f)}'
            ]

        self.hash_list = hash_list
        self.provide_hashes(self.hash_list)

    def md5sum(self, binary):
        m = hashlib.md5()
        m.update(binary)
        return m.hexdigest()

    def sha1sum(self, binary):
        m = hashlib.sha1()
        m.update(binary)
        return m.hexdigest()

    def sha256sum(self, binary):
        m = hashlib.sha256()
        m.update(binary)
        return m.hexdigest()

    def sha512sum(self, binary):
        m = hashlib.sha512()
        m.update(binary)
        return m.hexdigest()

    def provide_hashes(self, hash_list):
        return hash_list


if __name__ == "__main__":
    HashHelper(binary)