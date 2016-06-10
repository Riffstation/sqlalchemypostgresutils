import os
import pytest
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../'))


def run_tests():
    pytest.main(['-s'])


def main():
        run_tests()

if __name__ == '__main__':
    main()
