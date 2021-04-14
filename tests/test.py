import unittest
from os.path import abspath, normpath
from pathlib import PurePath

from importlib import import_module


class TestBeerRecommender(unittest.TestCase):

    def test_index_template(self):
        flask_app = import_module('beer_recommender')
        flask_app.app.testing = True
        base = PurePath(abspath(__file__))
        template = normpath(PurePath(base, '../../templates/index.html'))
        with open(template, 'r') as f:
            whole_str = f.read()

        with flask_app.app.test_client() as c:
            result = c.get('/')
            self.assertEqual(result.data.decode('utf-8'), whole_str.strip())

    def test_result_render(self):
        flask_app = import_module('beer_recommender')
        flask_app.app.testing = True
        abv = 5.0
        ibu = 15.5
        with flask_app.app.test_client() as c:
            result = c.post('/result', data=dict(abv=abv, ibu=ibu), follow_redirects=True)
            as_text = result.get_data(as_text=True)
            self.assertTrue('度数: {}'.format(abv) in as_text,
                            'HTMLが正しくコーディングされていません')
            self.assertTrue('IBU: {}'.format(ibu) in as_text,
                            'HTMLが正しくコーディングされていません')


if __name__ == "__main__":
    unittest.main()
