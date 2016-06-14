import argparse
import json
import os
import pytest
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def run_tests():
    from pgsqlutils.base import get_db_conf
    description = 'Creates play admin user'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--config', help='config file path', default='./config/dev.json')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.loads(f.read())

    dbconf = get_db_conf()
    dbconf.DATABASE_URI = config['DATABASE_URI']

    pytest.main(['-s'])


def main():
        run_tests()

if __name__ == '__main__':
    main()
