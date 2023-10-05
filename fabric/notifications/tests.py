from datetime import timezone

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Client, Newsletter, Message, StatisticsNewletter


class AccountTests(APITestCase):
    def test_create_client(self):
        """
        POST
        """
        data = {
            "phone_number": "+1122334455",
            "client_operator_code": "789",
            "client_tag": "new",
            "timezone": "Africa"
        }
        url_client = reverse('client-list')
        response = self.client.post(url_client, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().timezone, 'Africa')
        print('POST')

    def test_all_clients(self):
        """
        GET
        """
        client = Client.objects.create(
            phone_number="+1122334455",
            client_operator_code="789",
            client_tag="new",
            timezone="Africa"
        )
        url_client = reverse('client-list')
        response = self.client.get(url_client, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('GET')
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_client(self):
        """
        GET PK
        """
        client = Client.objects.create(
            phone_number="+1122334455",
            client_operator_code="789",
            client_tag="new",
            timezone="Africa"
        )

        url_retrieve = reverse('client-detail', kwargs={'pk': client.pk})

        response = self.client.get(url_retrieve)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['phone_number'], "+1122334455")
        self.assertEqual(response.data['client_operator_code'], "789")
        self.assertEqual(response.data['client_tag'], "new")
        self.assertEqual(response.data['timezone'], "Africa")
        print('GET PK')

    def test_update_client(self):
        """
        PUT PK
        """
        client = Client.objects.create(
            phone_number="+1122334455",
            client_operator_code="789",
            client_tag="new",
            timezone="Africa"
        )

        updated_data = {
            "phone_number": "+1122334466",
            "client_operator_code": "123",
            "client_tag": "updated",
            "timezone": "Europe"
        }

        url_put = reverse('client-detail', kwargs={'pk': client.pk})

        response = self.client.put(url_put, data=updated_data, format='json')

        self.assertEqual(response.status_code, 200)

        updated_client = Client.objects.get(pk=client.pk)
        self.assertEqual(updated_client.phone_number, updated_data['phone_number'])
        self.assertEqual(updated_client.client_operator_code, updated_data['client_operator_code'])
        self.assertEqual(updated_client.client_tag, updated_data['client_tag'])
        self.assertEqual(updated_client.timezone, updated_data['timezone'])

    def test_delete_client(self):
        """
        DELETE PK
        """
        client = Client.objects.create(
            phone_number="+1122334455",
            client_operator_code="789",
            client_tag="new",
            timezone="Africa"
        )

        url_delete = reverse('client-detail', kwargs={'pk': client.pk})

        response = self.client.delete(url_delete)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Client.objects.count(), 0)

    def test_over_client(self):
        """
        OVER PK
        """
        url_over = reverse('client-detail', kwargs={'pk': 999})
        response = self.client.get(url_over)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NewsletterTests(APITestCase):
    def test_create_newsletter(self):
        """
        POST
        """
        data = {
            "start_datetime": "2023-10-05T10:00:00Z",
            "message_text": "This is a test message",
            "end_datetime": "2023-10-06T10:00:00Z",
            "client_tag": "new"
        }
        url_newsletter = reverse('newsletter-list')
        response = self.client.post(url_newsletter, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Newsletter.objects.count(), 1)
        self.assertEqual(Newsletter.objects.get().client_tag, 'new')
        print('POST')

    def test_all_newsletters(self):
        """
        GET
        """
        newsletter = Newsletter.objects.create(
            start_datetime="2023-10-05T10:00:00Z",
            message_text="This is a test message",
            end_datetime="2023-10-06T10:00:00Z",
            client_tag="new"
        )
        url_newsletter = reverse('newsletter-list')
        response = self.client.get(url_newsletter, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('GET')
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_client(self):
        """
        GET PK
        """
        newsletter = Newsletter.objects.create(
            start_datetime='2023-10-03T16:00:10+03:00',
            message_text='Старая',
            end_datetime='2023-10-03T18:27:17+03:00',
            client_tag='new'
        )

        url_retrieve = reverse('newsletter-detail', kwargs={'pk': newsletter.pk})

        response = self.client.get(url_retrieve)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['start_datetime'], '2023-10-03T16:00:10+03:00')
        self.assertEqual(response.data['message_text'], 'Старая')
        self.assertEqual(response.data['end_datetime'], '2023-10-03T18:27:17+03:00')
        self.assertEqual(response.data['client_tag'], 'new')
        print('GET PK')

    def test_update_newsletter(self):
        """
        PUT PK
        """
        newsletter = Newsletter.objects.create(
            start_datetime="2023-10-05T10:00:00Z",
            message_text="This is a test message",
            end_datetime="2023-10-06T10:00:00Z",
            client_tag="new"
        )

        updated_data = {
            "start_datetime": "2023-10-07T10:00:00Z",
            "message_text": "Updated message",
            "end_datetime": "2023-10-08T10:00:00Z",
            "client_tag": "updated"
        }

        url_put = reverse('newsletter-detail', kwargs={'pk': newsletter.pk})

        response = self.client.put(url_put, data=updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_newsletter = Newsletter.objects.get(pk=newsletter.pk)
        self.assertEqual(updated_newsletter.start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ'), "2023-10-07T10:00:00Z")
        self.assertEqual(updated_newsletter.message_text, "Updated message")
        self.assertEqual(updated_newsletter.end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ'), "2023-10-08T10:00:00Z")
        self.assertEqual(updated_newsletter.client_tag, "updated")

    def test_delete_newsletter(self):
        """
        DELETE PK
        """
        newsletter = Newsletter.objects.create(
            start_datetime="2023-10-05T10:00:00Z",
            message_text="This is a test message",
            end_datetime="2023-10-06T10:00:00Z",
            client_tag="new"
        )

        url_delete = reverse('newsletter-detail', kwargs={'pk': newsletter.pk})

        response = self.client.delete(url_delete)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Newsletter.objects.count(), 0)

    def test_over_newsletter(self):
        """
        OVER PK
        """
        url_over = reverse('newsletter-detail', kwargs={'pk': 999})
        response = self.client.get(url_over)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class SendNewslettersTests(APITestCase):
    def test_send_valid_newsletter(self):
        newsletter = Newsletter.objects.create(
            start_datetime="2023-10-01T10:00:00Z",
            message_text="This is a test message",
            end_datetime="2023-10-30T10:00:00Z",
            client_tag="test"
        )

        client = Client.objects.create(
            phone_number="+1122334455",
            client_operator_code="789",
            client_tag="test",
            timezone="Africa"
        )

        url = reverse("newsletter-send", kwargs={"pk": newsletter.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.count(), 1) # Проверка на добавление в Message
        self.assertEqual(Message.objects.first().client, client) #Проверка на совпадение в Message
        self.assertEqual(Message.objects.first().status, "Отправлено")#Проверка статуса
        self.assertEqual(StatisticsNewletter.objects.count(), 1)#Проверка на создании статистики
        self.assertEqual(StatisticsNewletter.objects.first().total_messages_sent, 1)#Проверка на + к сообщениям


class StatisticsNewletterListTests(APITestCase):
    def test_get_all_statistics(self):
        StatisticsNewletter.objects.create(tag='test', total_messages_sent=3)
        StatisticsNewletter.objects.create(tag='new', total_messages_sent=4)

        url = reverse("statistics-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_statistics_by_tag(self):
        StatisticsNewletter.objects.create(tag='test', total_messages_sent=3)

        url = reverse("statistics-list") + "?tag=test"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_statistics_by_nonexistent_tag(self):
        url = reverse("statistics-tag", kwargs={"tag": "error"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_statistics_if_tag_not_provided(self):
        url = reverse("statistics-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_statistics_if_tag_provided(self):
        StatisticsNewletter.objects.create(tag="new_tag", total_messages_sent=10)

        url = reverse("statistics-list") + "?tag=new_tag"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(StatisticsNewletter.objects.first().total_messages_sent, 10)
