from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Newsletter, Message, StatisticsNewletter
from .serializers import ClientSerializer, NewsletterSerializer, StatisticsNewletterSerializer, MessageSerializer
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('app.log')


logger.addHandler(file_handler)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def list(self, request):
        logger.info(f"GET request to /api/v1/client/ received. List of all clients.")
        return super().list(request)

    def retrieve(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            logger.info(f"GET request to /api/v1/client/{pk} received. Retrieving client with pk={pk}")
            logger.info(f"Client data: {ClientSerializer(client).data}")
        except Client.DoesNotExist:
            logger.warning(f"GET request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        return super().retrieve(request, pk)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"POST request to /api/v1/client/ created a new client: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"POST request to /api/v1/client/ failed with validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            previous_data = ClientSerializer(client).data  # Предыдущие данные о клиенте

            serializer = self.get_serializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data  # Текущие данные о клиенте

                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logger.info(f"PUT request to /api/v1/client/{pk} updated the client with pk={pk}")
                    logger.info(f"Changes: {changes}")
                else:
                    logger.info(f"PUT request to /api/v1/client/{pk} made no changes to the client with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            logger.warning(f"PUT request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"detail": f"Client with pk={pk} not found"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

    def partial_update(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            previous_data = ClientSerializer(client).data  #Предыдущие данные о клиенте

            serializer = self.get_serializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data  # Текущие данные о клиенте

                # Сравниваем данные
                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logger.info(f"PATCH request to /api/v1/client/{pk} partially updated the client with pk={pk}")
                    logger.info(f"Changes: {changes}")
                else:
                    logger.info(f"PATCH request to /api/v1/client/{pk} made no changes to the client with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            logger.warning(f"PATCH request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            client = Client.objects.get(pk=pk)
            client_data = ClientSerializer(client).data  # Данные о клиенте перед удалением

            logger.info(f"DELETE request to /api/v1/client/{pk} deleted the client with pk={pk}")
            logger.info(f"Deleted client data: {client_data}")

            client.delete()

            return Response({"message": "client delete"})
        except Client.DoesNotExist:
            logger.warning(f"DELETE request to /api/v1/client/{pk} received, but client with pk={pk} not found")
            return Response({"message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def list(self, request):
        logger.info(f"GET request to /api/v1/newsletter/ received. List of all newsletters.")
        return super().list(request)

    def retrieve(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            logger.info(f"GET request to /api/v1/newsletter/{pk} received. Retrieving newsletter with pk={pk}")
            logger.info(f"Newsletter data: {NewsletterSerializer(newsletter).data}")
        except Newsletter.DoesNotExist:
            logger.warning(f"GET request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"message": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().retrieve(request, pk)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"POST request to /api/v1/newsletter/ created a new newsletter: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"POST request to /api/v1/newsletter/ failed with validation errors: {serializer.errors}")
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
                    logger.info(f"PUT request to /api/v1/newsletter/{pk} updated the newsletter with pk={pk}")
                    logger.info(f"Changes: {changes}")
                else:
                    logger.info(
                        f"PUT request to /api/v1/newsletter/{pk} made no changes to the newsletter with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Newsletter.DoesNotExist:
            logger.warning(f"PUT request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"detail": f"Newsletter with pk={pk} not found"}, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

    def partial_update(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            previous_data = NewsletterSerializer(newsletter).data  # Предыдущие данные о клиенте

            serializer = self.get_serializer(newsletter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                current_data = serializer.data  # Текущие данные о клиенте

                # Сравниваем данные
                changes = {}
                for field in current_data:
                    if current_data[field] != previous_data.get(field):
                        changes[field] = {
                            'from': previous_data.get(field),
                            'to': current_data[field]
                        }

                if changes:
                    logger.info(
                        f"PATCH request to /api/v1/newsletter/{pk} partially updated the newsletter with pk={pk}")
                    logger.info(f"Changes: {changes}")
                else:
                    logger.info(
                        f"PATCH request to /api/v1/newsletter/{pk} made no changes to the newsletter with pk={pk}")

                return Response(current_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Newsletter.DoesNotExist:
            logger.warning(f"PATCH request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"message": "newsletter not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            newsletter = Newsletter.objects.get(pk=pk)
            newsletter_data = NewsletterSerializer(newsletter).data

            logger.info(f"DELETE request to /api/v1/newsletter/{pk} deleted the newsletter with pk={pk}")
            logger.info(f"Deleted newsletter data: {newsletter_data}")

            newsletter.delete()

            return Response({"message": "Рассылка успешно удалена"}, status=status.HTTP_204_NO_CONTENT)

        except Newsletter.DoesNotExist:
            logger.warning(
                f"DELETE request to /api/v1/newsletter/{pk} received, but newsletter with pk={pk} not found")
            return Response({"message": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)


    # Выбираем по id рассылку какую отправить
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        try:
            newsletter = self.get_object()
        except Newsletter.DoesNotExist:
            logger.error("Newsletter not found")
            return Response({"status": "Рассылка не найдена"}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.localtime(timezone.now())
        start_datetime = newsletter.start_datetime
        end_datetime = newsletter.end_datetime

        if start_datetime <= current_time <= end_datetime:
            logger.info("Sending messages")
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
                        pass

                except Exception as e:
                    # Обработка ошибок при отправке сообщения
                    logger.error(f"Error sending message to client {client.id}: {str(e)}")

            logger.info(f'Рассылка {newsletter.id} выполнена')
            return Response({"status": "Рассылка выполнена"})
        else:
            logger.warning("Attempted to send messages outside of the allowed time window")
            return Response({"status": "Вне диапазона времени для рассылки"}, status=status.HTTP_400_BAD_REQUEST)


# получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
class StatisticsNewletterList(APIView):
    def get(self, request, tag=None):
        if tag:
            queryset = StatisticsNewletter.objects.filter(tag=tag)
            if queryset.exists():
                serializer = StatisticsNewletterSerializer(queryset, many=True)
                logger.info(f"Retrieved statistics for tag: {tag}")
                return Response(serializer.data)
            else:
                logger.warning(f"Statistics not found for tag: {tag}")
                return Response({"message": "Тег не найден"}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = StatisticsNewletter.objects.all()
            serializer = StatisticsNewletterSerializer(queryset, many=True)
            logger.info("Retrieved all statistics")
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
# class NewsletterDetailStatistics(APIView):
#     def get(self, request, newsletter_id):
#         try:
#             newsletter = Newsletter.objects.get(pk=newsletter_id)
#         except Newsletter.DoesNotExist:
#             return Response({"error": "Newsletter not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         messages = Message.objects.filter(newsletter=newsletter)
#
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
