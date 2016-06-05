from pgsqlutils import get_db_conf

class TestClass:

    def test_db_conf(self):
        """
        Test
        """
        conf = get_db_conf()
        assert hasattr(conf, 'hello') == False 

    def test_one(self):
        conf = get_db_conf()
        print(conf)
        x = "this"
        #assert 'h' in x
        assert conf.a == 'holaaaaaaaaaaaaaaaaaaaaaaaa'

    def test_two(self):
        x = "hello"
        #assert hasattr(x, 'hello')
