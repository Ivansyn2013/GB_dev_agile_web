from django.test import TestCase

from http import HTTPStatus
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from authapp.models import CustomUser, PostUser, LikeModel, DisLikeModel, CommentModel, ProfileUser, FriendsRequest
from authapp.views import get_relationship_status

# Create your tests here.
from authapp.views import PostCreated


class TestMainPage(TestCase):
    """Тест для url - главная страница работает"""
    def test_page_open(self):
        path = reverse("home")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class StaticURLTests(TestCase):
    """Тесты для url - статичных адресов"""

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_page_main(self) -> None:
        """Страница доступа по URL для ./web/urls"""

        pages: tuple = ('/', '', '/register/', '/login/')

        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_page_app(self) -> None:
        """Страница доступа по URL для ./authapp/urls"""

        pages: tuple = ('/pygbag/', '/game/', '/game/doom_game/', '/game/js_doom_game/', '/mario_js/', '/duck_hunt/',
                        '/users_all/')

        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names: dict = {
            '': 'index.html',
            '/pygbag/': 'game/pygbag.html',
            '/register/': 'register.html',
            '/login/': 'login.html',
            '/game/': 'game.html',
            # '/top_players/': 'top.html',
            '/game/doom_game/': 'game_stream.html',
            '/game/js_doom_game/': 'index_game.html',
            '/mario_js/': 'game/mario_js.html',
            '/duck_hunt/': 'game/duck_hunt.html',
            '/kerby/': 'game/kirby.html',
            '/tank/': 'game/tank.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)


class PostURLTests(TestCase):

    def setUp(self):

        self.guest_client = Client()  # неавторизованный пользователь

        self.user = CustomUser.objects.create_user(username='testik', password='testpassword', email='testik@mail.ru')
        self.authorized_client = Client()  # авторизованный пользователь
        self.authorized_client.force_login(self.user)

        self.profile_user = ProfileUser(user_name=self.user, id=1)
        self.profile_user.save()

        self.post = PostUser(author=self.user, title='Test Post', text='test text')
        self.post.save()
        self.like = LikeModel(user=self.user, post=self.post)
        self.dislike = DisLikeModel(user=self.user, post=self.post)
        self.comment = CommentModel(author=self.user, post=self.post, content='test comment', id=1)
        self.comment.save()

    def test_urls_guest_client(self):
        """Доступ неавторизованного пользователя к просмотру постов"""
        pages: tuple = ('/',
                        f'/detail_post/{str(self.post.slug)}',
                        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_authorized_client(self):
        """Доступ авторизованного пользователя"""
        pages: tuple = ('/',
                        f'/add_post/',
                        f'/game_add_profile/',
                        f'/edit_post/{self.post.slug}/',
                        f'/toggle_like/{self.post.id}/',
                        f'/toggle_dislike/{self.post.id}/',
                        f'/detail_profile_user/{self.user.id}/',
                        f'/duck_hunt_save_points/10/',
                        f'/super_mario_save_points/11/',
                        f'/game_progress_detail/{self.user.id}/',
                        f'/delete_comment/{self.comment.id}/',
                        f'/delete_post/{self.post.id}/',

                        # f'/request_friends/{self.user.id}/', #  POST форма
                        # f'/delete_request_friends/{self.user.id}/',
                        # f'/add_comment/{self.post.id}/', #  POST форма
                        # f'/kerby_save_points/',
                        # f'/game_progress_detail/',
                        )

        for page in pages:
            response = self.authorized_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)


class PostFormTests(TestCase):

    def setUp(self):
        self.guest_client = Client()  # неавторизованный пользователь

        self.user = CustomUser.objects.create_user(username='testik', password='testpassword', email='testik@mail.ru')
        self.authorized_client = Client()  # авторизованный пользователь
        self.authorized_client.force_login(self.user)

        self.post = self.post = PostUser(author=self.user, title='Test Post', text='test text')
        self.post.save()


    def test_create_post(self):
        '''Проверка создания поста'''
        posts_count = PostUser.objects.count()
        form_data = {'title': 'Название тестового поста', 'text': 'Текст поста записанный в форму'}

        response = self.authorized_client.post(reverse('add_post'),
                                               data=form_data,
                                               follow=True)

        error_name1 = 'Данные поста не совпадают'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(PostUser.objects.filter(
            text='Текст поста записанный в форму',
            author=self.user
        ).exists(), error_name1)
        error_name2 = 'Поcт не добавлен в базу данных'
        self.assertEqual(PostUser.objects.count(),
                         posts_count + 1,
                         error_name2)

    def test_edit_post(self):
        '''Проверка редактирования поста'''
        old_post = self.post  # сохраняем пост для проверки с измененным постом
        new_title = 'Change title post'
        form_data = {'title': new_title, 'text': 'Text test post'}
        response = self.authorized_client.post(
            reverse('edit_post', kwargs={'slug': old_post.slug}),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name1 = 'Данные поста не совпадают'
        self.assertTrue(PostUser.objects.filter(
            author=self.user,
        ).exists(), error_name1)
        error_name1 = 'Пользователь не может изменить содержание поста'
        self.assertNotEqual(old_post.text, form_data['text'], error_name1)
        error_name2 = 'Пользователь не может изменить название поста'
        self.assertNotEqual(old_post.title, form_data['title'], error_name2)

    def test_group_null(self):
        '''Проверка что 'title' поста обязателен'''
        old_post = self.post
        form_data = {'title': ''}
        response = self.authorized_client.post(
            reverse('edit_post', kwargs={'slug': old_post.slug}),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_name2 = 'Пользователь не может оставить поле нулевым'
        self.assertNotEqual(old_post.title, form_data['title'], error_name2)


class UsersTest(TestCase):

    def setUp(self):
        self.guest_client_1 = Client()  # пользователь 1
        self.guest_client_2 = Client()  # пользователь 2

        self.user_1 = CustomUser.objects.create_user(username='testik_1', password='testpassword1',
                                                     email='testik_1@mail.ru')

        self.user_2 = CustomUser.objects.create_user(username='testik_2', password='testpassword2',
                                                   email='testik_2@mail.ru')

        self.authorized_client = Client()  # авторизованный пользователь
        self.authorized_client.force_login(self.user_1)

    def test_relationship(self):
        '''Проверка запросов в друзья пользователей'''
        check_users = get_relationship_status(self.user_1, self.user_2)  #  проверка отношений пользователей
        error_name1 = 'Пользователи уже друзья'
        self.assertEqual(check_users, 'not_friends', error_name1)  # изначально новые пользователи "not_friends"

        response = self.authorized_client.post(
            reverse('request_friends', kwargs={'friends_id': self.user_2.id}),
            follow=True)  # отправка запроса пользователя 1 пользователю 2
        self.assertEqual(response.status_code, HTTPStatus.OK)  # ожидаем статус ОК

        check_users = get_relationship_status(self.user_1, self.user_2)
        error_name3 = 'Запрос на друзья не отправлен'
        self.assertEqual(check_users, 'request_sent', error_name3)  # ожидаем статус "request_sent"

        self.authorized_client.force_login(self.user_2)  # вход\логин пользователя 2
        response = self.authorized_client.post(
            reverse('done_cancel_friends', kwargs={'friend_id': self.user_1.id, 'status': 'done'}),
            follow=True)  # согласие пользователя 2 на запрос пользователя 1
        self.assertEqual(response.status_code, HTTPStatus.OK)  # ожидаем статус ОК

        check_users = get_relationship_status(self.user_1, self.user_2)
        error_name3 = 'Пользователи не друзья'
        self.assertEqual(check_users, 'friend', error_name3)  # ожидаем статус "friend"
