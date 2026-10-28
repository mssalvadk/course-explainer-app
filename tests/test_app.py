import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Course Explainer', response.data)

    def test_index_has_no_stray_text(self):
        response = self.app.get('/')
        self.assertNotIn(b'...existing code...', response.data)
        self.assertNotIn(b'/* reset basics */', response.data)

    def test_index_is_single_document(self):
        response = self.app.get('/')
        self.assertEqual(response.data.count(b'<html'), 1)

    def test_index_lists_all_courses(self):
        from models import courses
        response = self.app.get('/')
        for i, course in enumerate(courses, start=1):
            self.assertIn(course.title.encode(), response.data)
            self.assertIn(f'href="/course/{i}"'.encode(), response.data)

    def test_course(self):
        response = self.app.get('/course/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Course Details', response.data)

    def test_course_shows_course_data(self):
        response = self.app.get('/course/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Web Development with Flask', response.data)
        self.assertIn(b'Jane Smith', response.data)
        self.assertIn(b'6 weeks', response.data)
        self.assertIn(b'<title>Web Development with Flask</title>', response.data)

    def test_course_page_is_single_document(self):
        response = self.app.get('/course/1')
        self.assertEqual(response.data.count(b'<html'), 1)

    def test_course_unknown_id_returns_404(self):
        for course_id in ('0', '4', 'abc'):
            response = self.app.get(f'/course/{course_id}')
            self.assertEqual(response.status_code, 404, course_id)

    def test_stylesheet_has_no_duplicate_selectors(self):
        import re
        response = self.app.get('/static/css/styles.css')
        self.assertEqual(response.status_code, 200)
        css = re.sub(r'/\*.*?\*/', '', response.get_data(as_text=True), flags=re.S)
        response.close()
        selectors = [s.strip() for s in re.findall(r'([^{}]+)\{', css)]
        duplicates = {s for s in selectors if selectors.count(s) > 1}
        self.assertEqual(duplicates, set())

if __name__ == '__main__':
    unittest.main()