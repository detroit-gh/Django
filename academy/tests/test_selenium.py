from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.chrome.webdriver import WebDriver

from academy.models import Student


class SeleniumTest(StaticLiveServerTestCase):

    NUMBER_OF_STUDENTS = 30

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    def setUp(self) -> None:
        self.user = User.objects.create(first_name='Anton', last_name='Lysenko', email='detroit9gag@gmail.com')
        self._create_students(self.NUMBER_OF_STUDENTS)

    def _create_students(self, num):
        for num_of_stud in range(num):
            Student.objects.create(
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                email=self.user.email
            )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_unsuccessful_login(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_id('login')
        login_url.click()

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('test-selenium')

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('test-selenium777')

        submit_btn = self.selenium.find_element_by_id('submit_login')
        submit_btn.submit()

        error = self.selenium.find_element_by_id('error')
        expected_error = "Your username and password didn't match. Please try again."
        self.assertEqual(error.text, expected_error)

    def test_sign_up(self):
        self.selenium.get(self.live_server_url)

        login_url = self.selenium.find_element_by_id('login')
        login_url.click()

        sign_up_btn = self.selenium.find_element_by_id('sign_up')
        sign_up_btn.click()

        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('test-selenium@academy.com')

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('test-selenium')

        password_input = self.selenium.find_element_by_name('password1')
        password_input.send_keys('s1e2l3n4i5u6m7')

        password_input = self.selenium.find_element_by_name('password2')
        password_input.send_keys('s1e2l3n4i5u6m7')

        submit_btn = self.selenium.find_element_by_tag_name('button')
        submit_btn.submit()

        notification = self.selenium.find_element_by_id('notification')
        expected_notification = 'Please confirm your email address to complete the ' \
                                'registration.'
        self.assertEqual(notification.text, expected_notification)

    def test_check_pagination(self):
        self.selenium.get(self.live_server_url)

        students_url = self.selenium.find_element_by_id('students')
        students_url.click()

        pagination = self.selenium.find_element_by_class_name('pagination')
        self.assertTrue(bool(pagination))
