import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import get_word_counts, get_stop_words
from src.compute_pony_lang import get_tfidf

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        print("\nRUNNING TESTS FOR TASK 3")


    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print("Ensure word counts are calculated properly")
        true_word_counts = None
        with open(self.true_word_counts, 'r') as fp:
            true_word_counts = json.load(fp)

        stop_words = get_stop_words(os.path.join(parentdir, 'data', 'stopwords.txt'))
        calc_word_counts = get_word_counts(self.mock_dialog, stop_words)
        
        for pony in true_word_counts:
            self.assertEqual(len(calc_word_counts[pony]), len(true_word_counts[pony]))
            for word in true_word_counts[pony]:
                self.assertTrue(word in calc_word_counts[pony])
                self.assertEqual(true_word_counts[pony][word], calc_word_counts[pony][word])
        print('OK')

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        print("Ensure tf-idf scores are calculated properly")
        true_word_counts = None
        true_tf_idfs = None
        with open(self.true_tf_idfs, 'r') as fp:
            true_tf_idfs = json.load(fp)
        with open(self.true_word_counts, 'r') as fp:
            true_word_counts = json.load(fp)

        for pony in true_word_counts:
            for word in true_word_counts[pony]:
                calc_tfidf = round(get_tfidf(word, pony, true_word_counts), 4)
                true_tfidf = round(true_tf_idfs[pony][word], 4)
                self.assertEqual(calc_tfidf, true_tfidf)
        print('OK')
        
    
if __name__ == '__main__':
    unittest.main()