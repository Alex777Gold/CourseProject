from .models import Mission, Subscription
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTest(TestCase):
    def test_registration(self):
        initial_users_count = User.objects.count()

        response = self.client.post(reverse('signup'), {
                                    'username': 'testuser', 'password1': 'test1234', 'password2': 'test1234'})

        # Перевірка успішності запиту (не очікуємо перенаправлення)
        self.assertEqual(response.status_code, 200)
        # Перевірка, що кількість користувачів не збільшилася
        self.assertEqual(User.objects.count(), initial_users_count)
        # Перевірка відсутності нового користувача у базі даних
        self.assertFalse(User.objects.filter(username='testuser').exists())

# Test Registration if user input fail data


class RegistrationTestFail(TestCase):
    def test_registration(self):
        initial_users_count = User.objects.count()

        response = self.client.post(reverse('signup'), {
                                    'username': 'XXXXXXXX', 'password1': 'test1234', 'password2': 'test1234'})

        # Перевірка успішності запиту (не очікуємо перенаправлення)
        self.assertEqual(response.status_code, 200)
        # Перевірка, що кількість користувачів не збільшилася
        self.assertEqual(User.objects.count(), initial_users_count)
        # Перевірка відсутності нового користувача у базі даних
        self.assertFalse(User.objects.filter(username='XXXXXXXX').exists())


class AuthenticationTest(TestCase):
    def setUp(self):
        # Створюємо користувача для використання у тесті авторизації
        self.user = User.objects.create_user(
            username='testuser', password='test1234')

    def test_authentication(self):
        # Авторизуємо користувача
        self.client.login(username='testuser', password='test1234')

        # Перевіряємо, що користувач авторизований
        response = self.client.get(reverse('mission_list'))
        # Успішне отримання сторінки місій після авторизації
        self.assertEqual(response.status_code, 200)

# Test Authentication if user input fail data


class AuthenticationTestFail(TestCase):
    def setUp(self):
        # Створюємо користувача для використання у тесті авторизації
        self.user = User.objects.create_user(
            username='XXXXXXXX', password='test1234')

    def test_authentication(self):
        # Авторизуємо користувача
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXXX')

        # Перевіряємо, що користувач авторизований
        response = self.client.get(reverse('mission_list'))
        # Успішне отримання сторінки місій після авторизації
        self.assertEqual(response.status_code, 200)


class MissionListViewTest(TestCase):
    def setUp(self):
        Mission.objects.create(name='Mission 1', launch_date='2024-04-09',
                               mission_type='Type 1', country='Flight number: 1')
        Mission.objects.create(name='Mission 2', launch_date='2024-04-10',
                               mission_type='Type 2', country='flight number: 2')

    def test_mission_list_view(self):
        url = reverse('mission_list')
        response = self.client.get(url)
        # Перевірка, чи сторінка доступна
        self.assertEqual(response.status_code, 200)
        # Перевірка, чи відображаються дані місій на сторінці
        self.assertContains(response, 'Mission 1')
        self.assertContains(response, 'Mission 2')


class SubscriptionViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='test1234')
        self.mission = Mission.objects.create(
            name='Mission 1', launch_date='2024-04-09', mission_type='Type 1', country='Flight number: 1')

    def test_subscribe_view(self):
        self.client.login(username='testuser', password='test1234')
        url = reverse('subscribe', args=[self.mission.id])
        response = self.client.post(url)
        # Перевірка статусу відповіді
        self.assertEqual(response.status_code, 200)
        # Перевірка, чи користувач підписаний на місію
        self.assertTrue(Subscription.objects.filter(
            user=self.user, mission=self.mission).exists())

    def test_unsubscribe_view(self):
        self.client.login(username='testuser', password='test1234')
        Subscription.objects.create(user=self.user, mission=self.mission)
        url = reverse('unsubscribe', args=[self.mission.id])
        response = self.client.post(url)
        # Перевірка статусу відповіді
        self.assertEqual(response.status_code, 200)
        # Перевірка, чи користувач відписався від місії
        self.assertFalse(Subscription.objects.filter(
            user=self.user, mission=self.mission).exists())
