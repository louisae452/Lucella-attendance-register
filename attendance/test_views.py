import pytest
from django.contrib.auth.models import User, Group, AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from .models import DailyRegister, Student, Subject, Timetable
from .views import LandingView, landing_router


class TestHomeview(TestCase):
    """Tests Homeview loads succesfully"""
    def test_homepage_status_code_and_template(self):
        """Checks page loads successfully and uses correct template"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendance/home.html')


@pytest.mark.django_db
class TestLandingrouter:
    """Tests Landing_router redirects users to the appropriate landing page"""
    # Allow all tests to use the setup_data
    @pytest.fixture(autouse=True)
    def setup_data(self):
        """Set up the parent and teacher groups"""
        self.factory = RequestFactory()
        self.teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.parent_group, _ = Group.objects.get_or_create(name='parent')
        self.user = User.objects.create(
            username='FlorenceFox', password='testpassword')

    def test_teacher_redirect(self):
        """Test teachers access the landing page."""
        self.user.groups.add(self.teacher_group)
        request = self.factory.get('/landing/')
        request.user = self.user
        response = landing_router(request)
        assert response is not None
        assert response.status_code == 200

    def test_parent_redirect(self):
        """Tests parents access the landing page"""
        self.user.groups.add(self.parent_group)
        request = self.factory.get('/landing/')
        request.user = self.user
        response = landing_router(request)
        assert response is not None
        assert response.status_code == 200

    def test_wrong_user(self):
        """
        Tests a user that is not a parent or a teacher gets redirected home
        """
        request = self.factory.get('/landing')
        request.user = self.user
        response = landing_router(request)
        assert response.status_code == 302
        assert response. url == '/'


class TestLandingview(TestCase):
    """Tests LandingView. Requires user log in"""
    def setUp(self):
        """Sets up url and creates a user"""
        self.factory = RequestFactory()
        self.url = reverse('landing')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.user.groups.add(teacher_group)

    def test_nonuser_is_redirected(self):
        """Tests a non user is directed to login page"""
        request = self.factory.get("/landing/")
        request.user = AnonymousUser()
        response = LandingView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_user_gets_access(self):
        """ Tests a teacher user gets access to landing page"""
        login_successful = self.client.login(
            username='MiriamGonzalez', password='mypassword')
        self.assertTrue(login_successful, "Test failed")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/landing.html")


class TestChildrenlist(TestCase):
    """Tests that parents are directed to landing page"""
    def setUp(self):
        """
        Creates an instance of a parent user with a registered child
        and a degegistered child.
        Creates a different instance of a parent user with a differet
        child.
        Sets up url
        """
        self.test_user = User.objects.create_user(
            username="FrederikFox", password="mypassword")
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.test_user.groups.add(parent_group)
        self.test_child1 = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3, group=0,
            music_option=4,
            parent_name=self.test_user,
            deregistered=False)
        self.test_child2 = Student.objects.create(
            student_code='0609PIDE',
            date_of_birth="2006-09-12",
            sex=3, group=0,
            music_option=4,
            parent_name=self.test_user,
            deregistered=True)
        self.test_user1 = User.objects.create_user(
            username="MidgePeterson", password="mypassword1")
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.test_user1.groups.add(parent_group)
        self.test_child3 = Student.objects.create(
            student_code='060PESR',
            date_of_birth="2006-09-12",
            sex=3,
            group=0,
            music_option=4,
            parent_name=self.test_user1,
            deregistered=False)
        self.url = reverse('landing')

    def test_unauthentificateduser_is_redirected(self):
        """Unauthenticated users cannot access the landing page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_only_registered_children_on_list(self):
        """
        Tests only the registered children belonging to parent user appear
        on list
        """
        self.client.login(username='FrederikFox', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/landing.html")
        children_in_context = response.context['children']
        self.assertIn(self.test_child1, children_in_context)
        self.assertNotIn(self.test_child2, children_in_context)
        self.assertNotIn(self.test_child3, children_in_context)


class TestStudentlist(TestCase):
    """Tests  students_list(). Requires teacher user """
    def setUp(self):
        """
        Sets up url.
        Sets up teacher user
        Sets up a registered and deregistered students (Require parent user)
        Sets up daily register records for registered student (Require teacher
        user, Timetable and Session instance)
        """
        self.url = reverse('students')
        # Teacher user
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        # Registered and deregistered students
        self.test_user = User.objects.create_user(
            username="FrederikFox", password="mypassword")
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.test_user.groups.add(parent_group)
        self.test_student1 = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=0,
            music_option=4,
            parent_name=self.test_user,
            deregistered=False)
        self.test_student2 = Student.objects.create(
            student_code='0609PIDE',
            date_of_birth="2006-09-12",
            sex=3,
            group=0,
            music_option=4,
            parent_name=self.test_user,
            deregistered=True)
        # DailyRegisters records for self.test_child1
        self.test_subject = Subject.objects.create(
            subject_name='Maths A',
            teacher_name=self.teacher_user,
            set=1,
            room=1)
        self.test_session = Timetable.objects.create(
            session_id=2,
            day=1,
            session=0,
            group=1,
            subject_name=self.test_subject)
        self.test_register1 = DailyRegister.objects.create(
            session_id=self.test_session,
            date='2026-06-16',
            student_code=self.test_student1,
            mark=1)
        self.test_register2 = DailyRegister.objects.create(
            session_id=self.test_session,
            date='2026-06-23',
            student_code=self.test_student1,
            mark=0)

    def test_unauthentificated_user_is_redirected(self):
        """Unauthenticated users cannot access the students page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_registered_students_on_list(self):
        """
            Checks teacher users can access the page
            Checks only registered students appear on the list
            """
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attendance/students_list.html")
        students_in_context = response.context['students']
        self.assertIn(self.test_student1, students_in_context)
        self.assertNotIn(self.test_student2, students_in_context)


class TestAddparent(TestCase):
    """Tests add_parent(). Requires user to be admissions_officer"""
    def setUp(self):
        """Creates teacher and admissions_officer users. Sets up url"""
        self.url = reverse('newparent')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        admissions_group, _ = Group.objects.get_or_create(
            name='admissions_officer')
        self.admissions_user = User.objects.create_user(
            username='Headmaster', password='whatnow24')
        self.admissions_user.groups.add(admissions_group)

    def test_non_user_rejected(self):
        """Tests non users have not access to the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_wrong_group_rejected(self):
        """Tests a user that is not admissions_officer is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_officer_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='Headmaster', password='whatnow24')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_form_submission(self):
        """Tests validated form is submitted correctly"""
        post_data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        Group.objects.get_or_create(name='parent')
        self.client.login(username='Headmaster', password='whatnow24')
        response = self.client.post(reverse('newparent'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('parentdata'))


class TestAddparentdata(TestCase):
    """Tests add_parentdata(). Requires user to be admissions_officer"""
    def setUp(self):
        """
            Sets url
            Creates addmissions_officer user
            Creates teacher user
            Creates parent user
        """
        self.url = reverse('parentdata')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        admissions_group, _ = Group.objects.get_or_create(
            name='admissions_officer')
        self.admissions_user = User.objects.create_user(
            username='Headmaster', password='mypassword')
        self.admissions_user.groups.add(admissions_group)
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username='LauraSmith', password='mypassword')
        self.parent_user.groups.add(parent_group)

    def test_non_user_rejected(self):
        """Tests non users have not access to the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_wrong_group_rejected(self):
        """Tests a user that is not admissions_officer is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_officer_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_form_submission(self):
        """Tests data is submitted correctly"""
        post_data = {
            'parent_name': self.parent_user.id,
            'phone_number': '089765454',
        }
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.post(reverse('parentdata'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('landing'))


class TestAddstudent(TestCase):
    """Tests add_student(). Requires admissions_officer user"""
    def setUp(self):
        """
            Sets up url
            Creates admissions_officer user
            Creates teacher user
            Creates parent user
        """
        self.url = reverse('newstudent')
        admissions_group, _ = Group.objects.get_or_create(
            name='admissions_officer')
        self.admissions_user = User.objects.create_user(
            username='Headmaster', password='mypassword')
        self.admissions_user.groups.add(admissions_group)
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username='LauraSmith', password='mypassword')
        self.parent_user.groups.add(parent_group)

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_wrong_group_rejected(self):
        """Tests a user that is not admissions_officer is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_officer_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_submitted(self):
        """Tests the form is submitted correctly"""
        post_data = {
            'student_name': 'Peter',
            'student_surname': 'Smith',
            'student_code': '0605SMPE',
            'parent_name': self.parent_user.id,
            'date_of_birth': '2006-05-14',
            'sex': '3',
            'group': '1',
            'music_option': '4'
            }
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.post(reverse('newstudent'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('landing'))


class TestAddteacher(TestCase):
    """Tests add_teacher(). Requires admissions_officer user"""
    def setUp(self):
        """Creates admissions_officer and teacher users"""
        self.url = reverse('newteacher')
        admissions_group, _ = Group.objects.get_or_create(
            name='admissions_officer')
        self.admissions_user = User.objects.create_user(
            username='Headmaster', password='mypassword')
        self.admissions_user.groups.add(admissions_group)
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_wrong_group_rejected(self):
        """Tests a user that is not admissions_officer is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_officer_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_form_submission(self):
        """Tests validated form is submitted correctly"""
        post_data = {
            'username': "PeterSmith",
            'first_name': "Peter",
            'last_name': "Smith",
            'email': "peter@lucella.com",
            'password': "mypassword",
        }
        Group.objects.get_or_create(name='teacher')
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.post(reverse('newteacher'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('teacherdata'))


class TestTeacherdata(TestCase):
    """Tests add_teacherdata. Requires admissions_officer user"""
    def setUp(self):
        """Sets url. Creates admissions_officer and teacher users"""
        self.url = reverse('teacherdata')
        admissions_group, _ = Group.objects.get_or_create(
            name='admissions_officer')
        self.admissions_user = User.objects.create_user(
            username='Headmaster', password='mypassword')
        self.admissions_user.groups.add(admissions_group)
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_wrong_group_rejected(self):
        """Tests a user that is not admissions_officer is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_officer_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_is_submitted(self):
        """Tests form is submitted correctly"""
        post_data = {
            'teacher_name': self.teacher_user.id,
            'phone_number': '0987857473'
        }
        self.client.login(username='Headmaster', password='mypassword')
        response = self.client.post(reverse('teacherdata'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('landing'))


class TestGetregister(TestCase):
    """Tests get_register(). Requires teacher user"""
    def setUp(self):
        """Sets url. Creates teacher and regular user"""
        self.url = reverse('dailyregister')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        self.test_subject = Subject.objects.create(
            subject_name='Maths A',
            teacher_name=self.teacher_user,
            set=1,
            room=1)

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a user that is not teacher is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_teacher_user_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestSaveregister(TestCase):
    """Tests saveregister(). Requires teacher user"""
    def setUp(self):
        """Sets url. Creates teacher and regular user"""
        self.url = reverse('saveregister')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        self.test_subject = Subject.objects.create(
            subject_name='Maths A',
            teacher_name=self.teacher_user,
            set=1,
            room=1)

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a user that is not teacher is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestStudentdetail(TestCase):
    """Tests student_detail(). Requires attendance_officer user"""
    def setUp(self):
        """
            Creates teacher and regular user
            Creates parent and student
            Creates, subject, timetable and dailyregister instances
            Sets up url
            """
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        attendance_group, _ = Group.objects.get_or_create(
            name='attendance_officer')
        self.attendance_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        self.attendance_user.groups.add(attendance_group)
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword1")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=0,
            music_option=4,
            parent_name=self.parent_user,
            deregistered=False)
        self.test_subject = Subject.objects.create(
            subject_name='Maths A',
            teacher_name=self.teacher_user,
            set=1,
            room=1)
        self.test_timetable = Timetable.objects.create(
            session_id=3,
            day=2,
            session=1,
            group=1,
            subject_name=self.test_subject)
        self.test_record1 = DailyRegister.objects.create(
            date='2026-06-23',
            session_id=self.test_timetable,
            student_code=self.test_student,
            mark=1,
            status=0)
        self.test_record2 = DailyRegister.objects.create(
            date='2026-06-30',
            session_id=self.test_timetable,
            student_code=self.test_student,
            mark=1,
            status=0)
        self.url = reverse(
            'studentdetail', kwargs={'student_code': self.test_student})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_teacher_user_rejected(self):
        """Tests a user teacher is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_attendances_user_accepted(self):
        """Tests the attendance_officer user is accepted"""
        self.client.login(username='JuanSoto', password='mypassword')
        self.test_student.refresh_from_db()
        self.url = reverse(
            'studentdetail',
            kwargs={'student_code': self.test_student.student_code})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestSendemail(TestCase):
    """Tests sendemail(). Requires admissions_officer user"""
    def setUp(self):
        """Creates teacher and admissions_officer user
            Creates parent and student instances
            Sets up url
        """
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        attendance_group, _ = Group.objects.get_or_create(
            name='attendance_officer')
        self.attendance_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        self.attendance_user.groups.add(attendance_group)
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword1")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=0,
            music_option=4,
            parent_name=self.parent_user,
            deregistered=False)
        self.url = reverse(
            'sendemail', kwargs={'student_code': self.test_student})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_teacher_user_rejected(self):
        """Tests a teacher user is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_attendance_user_accepted(self):
        """Tests the attendance_officer user is accepted"""
        self.client.login(username='JuanSoto', password='mypassword')
        self.url = reverse(
            'sendemail',
            kwargs={'student_code': self.test_student.student_code})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestReason(TestCase):
    """Tests givereason(). Requires parent user"""
    def setUp(self):
        """
        Creates parent user
        Creates student instance
        Creates teacher, subject, timetable and dailyregister instances
        Sets up url
        """
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=0,
            music_option=4,
            parent_name=self.parent_user,
            deregistered=False)
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        self.test_subject = Subject.objects.create(
            subject_name='Maths A',
            teacher_name=self.teacher_user,
            set=1,
            room=1)
        self.test_timetable = Timetable.objects.create(
            session_id=3,
            day=2,
            session=1,
            group=1,
            subject_name=self.test_subject)
        self.test_record = DailyRegister.objects.create(
            date='2026-06-23',
            session_id=self.test_timetable,
            student_code=self.test_student,
            mark=1,
            status=2)
        self.url = reverse(
            'givereason',
            kwargs={
                'student_code': self.test_student.student_code,
                'date': self.test_record.date,
                'session_id': self.test_record.session_id.pk})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_teacher_user_rejected(self):
        """Tests a teacher user is rejected"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_parent_user_accepted(self):
        """Tests the user is accepted"""
        self.client.login(username='MidgePeterson', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestChildtimetable(TestCase):
    """Tests child_timetabel. Requires parent user"""
    def setUp(self):
        """Creates regular user, parent and student. Sets up url"""
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=1,
            music_option=5,
            parent_name=self.parent_user,
            deregistered=False)
        self.url = reverse(
            'childdetail',
            kwargs={'student_code': self.test_student.student_code})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestReportabsence(TestCase):
    """Tests report_abscence. Requires parent user."""
    def setUp(self):
        """Creates regular user. Sets up url"""
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=1,
            music_option=5,
            parent_name=self.parent_user,
            deregistered=False)
        self.url = reverse(
            'reportabsence',
            kwargs={
                'student_code': self.test_student.student_code,
                'session_id': 3})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestChildrecord(TestCase):
    """ Tests child_record(). Requires parent user """
    def setUp(self):
        """Creates regular user. Sets up url"""
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=1,
            music_option=5,
            parent_name=self.parent_user,
            deregistered=False)
        self.url = reverse(
            'childrecord',
            kwargs={'student_code': self.test_student.student_code})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestPendingabsences(TestCase):
    """Tests pending_absences. Requires attendance_officer user"""
    def setUp(self):
        """Creates regular and attendance_officer user. Sets url"""
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        attendance_group, _ = Group.objects.get_or_create(
            name='attendance_officer')
        self.attendance_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword")
        self.attendance_user.groups.add(attendance_group)
        self.url = reverse('pending')

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_user_accepted(self):
        """Tests the admissions_officer user is accepted"""
        self.client.login(username='MidgePeterson', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestAbsencedetail(TestCase):
    """Tests absence_detail(). Requires attendance_officer user"""
    def setUp(self):
        """
        Creates regular and attendance_officer user
        Creates parent and student
        Sets url
        """
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        attendance_group, _ = Group.objects.get_or_create(
            name='attendance_officer')
        self.attendance_user = User.objects.create_user(
            username="MidgePeterson", password="mypassword")
        self.attendance_user.groups.add(attendance_group)
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="CarlosRomero", password="mypassword")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=1,
            music_option=5,
            parent_name=self.parent_user,
            deregistered=False)
        self.url = reverse(
            'absencedetail',
            kwargs={
                'student_code': self.test_student.student_code,
                'date': '2026-06-30',
                'session_id': 3})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestGetclass(TestCase):
    """Test get_class(). Requires teacher user"""
    def setUp(self):
        "Creates a regular and teacher user. Sets url"
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        self.url = reverse('myclass')

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_teacher_user_accepted(self):
        """Tests the teacher user is accepted"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestClassdetail(TestCase):
    """Tests class_detail(). Requires teacher permission"""
    def setUp(self):
        """
        Creates regular and teacher users.
        Creates parent, student and subject instances
        Sets url
        """
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        teacher_group, _ = Group.objects.get_or_create(name='teacher')
        self.teacher_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.teacher_user.groups.add(teacher_group)
        parent_group, _ = Group.objects.get_or_create(name='parent')
        self.parent_user = User.objects.create_user(
            username="CarlosRomero", password="mypassword")
        self.parent_user.groups.add(parent_group)
        self.test_student = Student.objects.create(
            student_code='0609PITE',
            date_of_birth="2006-09-12",
            sex=3,
            group=1,
            music_option=5,
            parent_name=self.parent_user,
            deregistered=False)
        self.test_subject = Subject.objects.create(
            subject_name='Maths A',
            teacher_name=self.teacher_user,
            set=1,
            room=1)
        self.url = reverse(
            'classdetail',
            kwargs={
                'subject_name': self.test_subject.subject_name,
                'student_code': self.test_student.student_code})

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_teacher_user_accepted(self):
        """Tests the teacher user is accepted"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestTruantinglist(TestCase):
    """Tests truanting_list(). Requires attendance_officer user"""
    def setUp(self):
        """Creates regular and attendance_officer user. Sets url"""
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        attendance_group, _ = Group.objects.get_or_create(
            name='attendance_officer')
        self.attendance_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.attendance_user.groups.add(attendance_group)
        self.url = reverse('truanting')

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_attendance_user_accepted(self):
        """Tests the attendance_officer user is accepted"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestRemovestudent(TestCase):
    """Tests remove_student(). Requires admissions_officer permission"""
    def setUp(self):
        """Creates regular and admissions_officer users. Sets url"""
        self.regular_user = User.objects.create_user(
            username='JuanSoto', password='mypassword')
        admissions_group, _ = Group.objects.get_or_create(
            name='admissions_officer')
        self.admissions_user = User.objects.create_user(
            username='MiriamGonzalez', password='mypassword')
        self.admissions_user.groups.add(admissions_group)
        self.url = reverse('remove')

    def test_unauthorised_user_is_rejected(self):
        """Tests an unauthorised user is not given access to page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_regular_user_rejected(self):
        """Tests a regular user is rejected"""
        self.client.login(username='JuanSoto', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_admissions_user_accepted(self):
        """Tests the admisssions_officer user is accepted"""
        self.client.login(username='MiriamGonzalez', password='mypassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
