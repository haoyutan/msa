import binascii, os


def random_hex_string(length=40):
    return binascii.hexlify(os.urandom(int(length / 2))).decode()
