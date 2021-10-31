import unittest
from pathlib import Path
import os, sys, json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.clean import clean


class CleanTest(unittest.TestCase):
    def setUp(self):
        pass
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.

    def test_1(self):
        print("Checking that posts without title or title_text are removed...")
        f = open(os.path.join(parentdir, 'test', 'fixtures', 'test_1.json'), 'r')
        fixture = f.readline()

        cleaned_fixture = clean(fixture)
        self.assertIsNone(cleaned_fixture)
        print("OK!")
        f.close()

    def test_2(self):
        print("\nChecking that posts with createdAt dates that don't pass ISO datetime standard are removed...")

        f = open(os.path.join(parentdir, 'test', 'fixtures', 'test_2.json'), 'r')
        fixture = f.readline()
        
        cleaned_fixture = clean(fixture)
        self.assertIsNone(cleaned_fixture)
        print("OK!")
        f.close()

    def test_3(self):
        print("\nChecking that invalid JSON dictionaries are ignored...")
        f = open(os.path.join(parentdir, 'test', 'fixtures', 'test_3.json'), 'r')
        fixture = f.readline()
        # write test here

        cleaned_fixture = clean(fixture)
        self.assertIsNone(cleaned_fixture)
        print("OK!")
        f.close()
    
    def test_4(self):
        print("\nChecking that posts with invalid author fields are removed...")
        f = open(os.path.join(parentdir, 'test', 'fixtures', 'test_4.json'), 'r')
        fixture = f.readline()
        # write test here

        cleaned_fixture = clean(fixture)
        self.assertIsNone(cleaned_fixture)
        print("OK!")
        f.close()

    def test_5(self):
        print("\nChecking that total_count is a string containing cast-able number and is cast to an int properly...")
        f = open(os.path.join(parentdir, 'test', 'fixtures', 'test_5.json'), 'r')
        fixture = f.readline()
        # write test here
        cleaned_fixture = clean(fixture)
        fixture_dict = json.loads(fixture)
        converted = False
        try:
            int(float(fixture_dict['total_count']))
            converted = True
        except:
            converted = False

        if converted:
            self.assertIsInstance(cleaned_fixture['total_count'], int)
            print('string converted to int properly\nOK!')
        else:
            self.assertIsNone(cleaned_fixture)
            print('string is not cast-able to int\nOK!')     
        f.close()

    def test_6(self):
        print("\nChecking that tags with 3 words are split properly...")
        f = open(os.path.join(parentdir, 'test', 'fixtures', 'test_6.json'), 'r')
        fixture = f.readline()
        # write test here
        cleaned_fixture = clean(fixture)
        fixture_dict = json.loads(fixture)
        for tag in fixture_dict['tags']:
            split = tag.split()
            if len(split) == 3:
                for word in split:
                    self.assertIn(word, cleaned_fixture['tags'])
        print("OK!")
        f.close()      
if __name__ == '__main__':
    unittest.main()