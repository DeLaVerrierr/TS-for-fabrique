from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.http import Http404
from django_q.models import Schedule
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Newsletter, Message, StatisticsNewletter
from .serializers import ClientSerializer, NewsletterSerializer, StatisticsNewletterSerializer, MessageSerializer
from django.utils import timezone
import logging
import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django_q.tasks import schedule, async_task
from decouple import config
from django.conf import settings


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def list(self, request):
        logging.info(f"GET request to /api/v1/client/ received. List of all clients.")
        return super().list(request)

    def retrieve(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            logging.info(f"GET request to /api/v1/client/{pk} received. Retrieving client with pk={pk}")
            logging.info(f"Client data: {ClientSerializer(client).data}")
        except Client.DoesNotExist:
            logging.warning(f"GET request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        return super().retrieve(request, pk)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logging.info(f"POST request to /api/v1/client/ created a new client: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.error(f"POST request to /api/v1/client/ failed with validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            previous_data = ClientSerializer(client).data  # Записываем предыдущие данные о клиенте

            serializer = self.get_serializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data  # Записываем текущие данные о клиенте

                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logging.info(f"PUT request to /api/v1/client/{pk} updated the client with pk={pk}")
                    logging.info(f"Changes: {changes}")
                else:
                    logging.info(f"PUT request to /api/v1/client/{pk} made no changes to the client with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            logging.warning(f"PUT request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"detail": f"Client with pk={pk} not found"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

    def partial_update(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            previous_data = ClientSerializer(client).data  # Записываем предыдущие данные о клиенте

            serializer = self.get_serializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data  # Записываем текущие данные о клиенте

                # Сравниваем данные и логируем изменения
                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logging.info(f"PATCH request to /api/v1/client/{pk} partially updated the client with pk={pk}")
                    logging.info(f"Changes: {changes}")
                else:
                    logging.info(f"PATCH request to /api/v1/client/{pk} made no changes to the client with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            logging.warning(f"PATCH request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            client_data = ClientSerializer(client).data  # Записываем данные о клиенте перед удалением

            logging.info(f"DELETE request to /api/v1/client/{pk} deleted the client with pk={pk}")
            logging.info(f"Deleted client data: {client_data}")

            client.delete()

            return Response({"message": "client delete"})
        except Client.DoesNotExist:
            logging.warning(f"DELETE request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def list(self, request):
        logging.info(f"GET request to /api/v1/newsletter/ received. List of all newsletters.")
        return super().list(request)

    def retrieve(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            logging.info(f"GET request to /api/v1/newsletter/{pk} received. Retrieving newsletter with pk={pk}")
            logging.info(f"Newsletter data: {NewsletterSerializer(newsletter).data}")
        except Newsletter.DoesNotExist:
            logging.warning(f"GET request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"message": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().retrieve(request, pk)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logging.info(f"POST request to /api/v1/newsletter/ created a new newsletter: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logging.error(f"POST request to /api/v1/newsletter/ failed with validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            previous_data = NewsletterSerializer(newsletter).data

            serializer = self.get_serializer(newsletter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data

                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logging.info(f"PUT request to /api/v1/newsletter/{pk} updated the newsletter with pk={pk}")
                    logging.info(f"Changes: {changes}")
                else:
                    logging.info(
                        f"PUT request to /api/v1/newsletter/{pk} made no changes to the newsletter with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Newsletter.DoesNotExist:
            logging.warning(f"PUT request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"detail": f"Newsletter with pk={pk} not found"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

    def partial_update(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            previous_data = NewsletterSerializer(newsletter).data  # Записываем предыдущие данные о клиенте

            serializer = self.get_serializer(newsletter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data  # Записываем текущие данные о клиенте

                # Сравниваем данные и логируем изменения
                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logging.info(
                        f"PATCH request to /api/v1/newsletter/{pk} partially updated the newsletter with pk={pk}")
                    logging.info(f"Changes: {changes}")
                else:
                    logging.info(
                        f"PATCH request to /api/v1/newsletter/{pk} made no changes to the newsletter with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Newsletter.DoesNotExist:
            logging.warning(f"PATCH request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"message": "newsletter not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            newsletter_data = NewsletterSerializer(newsletter).data

            logging.info(f"DELETE request to /api/v1/newsletter/{pk} deleted the newsletter with pk={pk}")
            logging.info(f"Deleted newsletter data: {newsletter_data}")

            newsletter.delete()

            return Response({"message": "Рассылка успешно удалена"}, status=status.HTTP_204_NO_CONTENT)

        except Newsletter.DoesNotExist:
            logging.warning(
                f"DELETE request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"message": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)


    # Выбираем по id рассылку какую отправить
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        try:
            newsletter = self.get_object()
        except Newsletter.DoesNotExist:
            logging.error("Newsletter not found")
            return Response({"status": "Рассылка не найдена"}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.localtime(timezone.now())
        start_datetime = newsletter.start_datetime
        end_datetime = newsletter.end_datetime

        if start_datetime <= current_time <= end_datetime:
            logging.info("Sending messages")
            clients = Client.objects.filter(client_tag=newsletter.client_tag)

            for client in clients:
                try:
                    if client.client_tag == newsletter.client_tag:
                        message = Message.objects.create(
                            created_datetime=current_time,
                            status="Отправлено",
                            newsletter=newsletter,
                            client=client
                        )

                        # Обновляем статистику
                        try:
                            newsletter_statistic = StatisticsNewletter.objects.get(tag=newsletter.client_tag)
                            newsletter_statistic.total_messages_sent += 1
                            newsletter_statistic.save()
                        except StatisticsNewletter.DoesNotExist:
                            StatisticsNewletter.objects.create(
                                tag=newsletter.client_tag,
                                total_messages_sent=1
                            )
                    else:
                        # Логика, если тег клиента не совпадает с тегом рассылки
                        pass

                except Exception as e:
                    # Обработка ошибок при отправке сообщения
                    logging.error(f"Error sending message to client {client.id}: {str(e)}")

            # Здесь можно добавить логику для обработки завершения рассылки, если нужно
            logging.info(f'Рассылка {newsletter.id} выполнена')
            return Response({"status": "Рассылка выполнена"})
        else:
            logging.warning("Attempted to send messages outside of the allowed time window")
            return Response({"status": "Вне диапазона времени для рассылки"}, status=status.HTTP_400_BAD_REQUEST)


# получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
class StatisticsNewletterList(APIView):
    def get(self, request, tag=None):
        if tag:
            queryset = StatisticsNewletter.objects.filter(tag=tag)
            if queryset.exists():
                serializer = StatisticsNewletterSerializer(queryset, many=True)
                logging.info(f"Retrieved statistics for tag: {tag}")
                return Response(serializer.data)
            else:
                logging.warning(f"Statistics not found for tag: {tag}")
                return Response({"message": "Тег не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = StatisticsNewletter.objects.all()
            serializer = StatisticsNewletterSerializer(queryset, many=True)
            logging.info("Retrieved all statistics")
            return Response(serializer.data)



# def send_statistics_email():
#     statistics = StatisticsNewletter.objects.all()
#     message = "Статистика отправленных сообщений:\n\n"
#     for stat in statistics:
#         message += str(stat) + "\n"
#
#     subject = "Статистика отправленных сообщений"
#     print('Letter sent')
#     send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.RECIPIENT_ADDRESS])
#
#
#

# # получения детальной статистики отправленных сообщений по конкретной рассылке
# class NewsletterDetailStatistics(APIView):
#     def get(self, request, newsletter_id):
#         # Попытайтесь получить рассылку
#         try:
#             newsletter = Newsletter.objects.get(pk=newsletter_id)
#         except Newsletter.DoesNotExist:
#             # Если рассылка не найдена, верните ошибку в JSON формате
#             return Response({"error": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         # Получите все сообщения, связанные с этой рассылкой
#         messages = Message.objects.filter(newsletter=newsletter)
#
#         # Сериализуйте данные
#         serializer = MessageSerializer(messages, many=True)
#
#         return Response(serializer.data)

# #POST GET
# class ClientAPIList(generics.ListCreateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
# #PUT
# class ClientAPIUpdate(generics.UpdateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
# #CRUD
# class ClientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer

# Создание клиента по API POST
# class ClientCreateAPIView(APIView):
#     def get(self, request):
#         client = Client.objects.all().values()
#
#         return Response({'client_get': ClientSerializer(client, many=True).data})
#
#     def post(self, request):
#         serializer = ClientSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'client_post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': 'Method PUT not allowed'})
#
#         try:
#             instance =Client.objects.get(pk=pk)
#         except:
#             return Response({'error':'Object does not exists'})
#
#         serializer = ClientSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post':serializer.data})
