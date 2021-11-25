import json
import os
import hashlib


BLOCKCHAIN_DIR = 'blockchain/'


def get_hash(prev_block):
    with open(BLOCKCHAIN_DIR + prev_block, 'rb') as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()


def write_block(borrower, lender, amount):

    blocks_count = len(os.listdir(BLOCKCHAIN_DIR))
    prev_block = str(blocks_count)

    data = {
        "borrower": borrower,
        "lender": lender,
        "amount": amount,
        "prev_block": {
            "hash": get_hash(prev_block),
            "filename": prev_block
        }
    }

    current_block = BLOCKCHAIN_DIR + str(blocks_count + 1)

    with open(current_block, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')


def main():
    write_block(borrower='Timme', lender='Jan', amount=1000)


if __name__ == '__main__':
    main()
