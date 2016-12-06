import argparse
import json
import os
import pytest
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def run_tests():
    from pgsqlutils.base import get_db_conf
    from pgsqlutils.base import init_db_conn, syncdb

    description = 'Creates play admin user'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--config', help='config file path', default='./config/dev.json')
    parser.add_argument(
        '--q', help='config file path', required=False,
        default=os.path.join(BASE_DIR, 'dbtests'))

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.loads(f.read())

    dbconf = get_db_conf()
    dbconf.DATABASE_URI = config['DATABASE_URI']
    init_db_conn()
    syncdb()
    exit(pytest.main(['-s', args.q]))


def main():
        run_tests()

if __name__ == '__main__':
    main()
