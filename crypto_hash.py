import hashlib
import json


def crypto_hash(*args):
    """
    Return sha-256 hash of the given data.
    """

    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    print(f'stringified_args: {stringified_args}')

    joined_data = ''.join(stringified_args)

    print(f'joined_data: {joined_data}')

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(
        f"crypto_hash('one', 'two', 'three'): {crypto_hash('one', 3, 'three')}")


if __name__ == '__main__':
    main()
