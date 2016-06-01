import argparse

import os
import pytest
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def run_tests():
    from pgsqlutils import get_db_conf
    conf = get_db_conf()
    print(conf)
    pytest.main()

def main():
    run_tests()

if __name__ == '__main__':
    main()
