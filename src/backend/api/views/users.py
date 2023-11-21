
# import requests
# from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
# from djoser import signals
from djoser.views import UserViewSet as DjoserUserViewSet
# from rest_framework.decorators import action
# from django.conf import settings
# from django.core.mail import send_mail

# from user.models import User
from api.serializers.users import (
    # ChangePasswordSerializer, ConfirmationCodeSerializer,
    # ResetPasswordSerializer, SendCodeSerializer, UserMeSerializer,
    UserSerializer,
    # TowTruckSerializer,
    # TariffSerializer,
    # PriceOrderSerializer,
    # UserSerializer,
    # UserCreateSerializer,
)
# from api.utils.verefications import (
#     activation_user_service, cache_and_send_confirmation_code,
#     change_password_service, registration_email,
#     resend_confirmation_code_service,
#     reset_password_confirmation_code_service,
#     reset_password_service,
# )

User = get_user_model()


class UserViewset(DjoserUserViewSet):
    """DjoserViewSet."""
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    token_generator = default_token_generator
    # permission_classes = (permissions.AllowAny,)

    # def get_permissions(self):
    #     """
    #     Предоставление прав на создание для неавторизованного пользователя.
    #     """
    #     if self.action == 'create':
    #         return (permissions.AllowAny(),)
    #     return super().get_permissions()

    # def perform_create(self, serializer, *args, **kwargs):
    #     """
    #     Создание и отправка пароля после успешной регистрации пользователя.
    #     """
    #     user = serializer.save(*args, **kwargs)
    #     cache_and_send_confirmation_code(user, registration_email)

    # def destroy(self, request, *args, **kwargs):
    #     """Удаление пользователя."""
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return response.Response(
    #         {'message': 'Пользователь успешно удален'},
    #         status=status.HTTP_200_OK
    #     )

    # @action(
    #     detail=False,
    #     methods=['post'],
    #     permission_classes=(permissions.AllowAny,),
    #     serializer_class=ConfirmationCodeSerializer
    # )
    # def activation(self, request, *args, **kwargs):
    #     """
    #     Активация юзера через код подтверждения.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     activation_user_service(serializer.validated_data)
    #     return response.Response(
    #         {'message': 'Электронная почта верифицирована'},
    #         status=status.HTTP_200_OK
    #     )

    # @action(
    #     detail=False,
    #     methods=['post'],
    #     permission_classes=(permissions.IsAuthenticated,),
    #     serializer_class=ChangePasswordSerializer
    # )
    # def change_password(self, request, *args, **kwargs):
    #     """
    #     Cмена пароля авторизованного пользователя.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     change_password_service(serializer.validated_data)
    #     return response.Response(
    #         {'message': 'Пароль изменен'}, status=status.HTTP_200_OK
    #     )

    # @action(
    #     detail=False,
    #     methods=['post'],
    #     permission_classes=(permissions.AllowAny,),
    #     serializer_class=ResetPasswordSerializer
    # )
    # def reset_password(self, request, *args, **kwargs):
    #     """
    #     Сброс пароля с последующим удаленим токена авторизации.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     reset_password_service(serializer.validated_data)
    #     return response.Response(
    #         {'message': 'Пароль изменен'},
    #         status=status.HTTP_200_OK
    #     )

    # @action(
    #     detail=False,
    #     permission_classes=(permissions.IsAuthenticated,),
    #     serializer_class=UserMeSerializer
    # )
    # def me(self, request, *args, **kwargs):
    #     """
    #     Получение пользователем информации информацию о себе.
    #     """
    #     serializer = self.get_serializer(request.user)
    #     return response.Response(serializer.data, status=status.HTTP_200_OK)

    # @me.mapping.patch
    # def patch_me(self, request, *args, **kwargs):
    #     """
    #     Изменение пользователем информации о себе.
    #     """
    #     serializer = self.get_serializer(
    #         request.user,
    #         data=request.data,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return response.Response(serializer.data, status=status.HTTP_200_OK)

    # @action(
    #     detail=False,
    #     methods=['post'],
    #     permission_classes=(permissions.AllowAny,),
    #     serializer_class=SendCodeSerializer
    # )
    # def reset_password_confirmation_code(self, request, *args, **kwargs):
    #     """
    #     Отправка кода подтверждения для сброса пароля.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     reset_password_confirmation_code_service(serializer.validated_data)
    #     return response.Response(
    #         {'message': 'Код подтверждения отправлен на почту'},
    #         status=status.HTTP_200_OK
    #     )

    # @action(
    #     detail=False,
    #     methods=['post'],
    #     permission_classes=(permissions.AllowAny,),
    #     serializer_class=SendCodeSerializer
    # )
    # def resend_confirmation_code(self, request, *args, **kwargs):
    #     """
    #     Повторная отправка кода подтверждения.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     resend_confirmation_code_service(serializer.validated_data)
    #     return response.Response(
    #         {'message': 'Код активации отправлен на почту'},
    #         status=status.HTTP_200_OK
    #     )

    # def send_sms_code(phone, code):
    #     params = {
    #         'api_id': settings.SMS_API_ID,
    #         'to': phone,
    #         'msg': settings.SMS_API_MSG.format(code)
    #     }

    #     response = requests.get(settings.SMS_API_URL, params=params)

    #     if response.status_code == status.HTTP_200_OK:
    #         print('SMS code sent successfully')
    #     else:
    #         print('Error sending SMS code')

    # def get_verefications(self, request, **kwargs):
    #     pass

    # def create(self, request, *args, **kwargs):
    #     serializer = CustomUserCreateSerializer
    #     serializer.is_valid(raise_exception=True)

    #     # Получение выбора способа подтверждения
    #     confirmation_method = request.data.get('confirmation_method')

    #     if confirmation_method == 'phone':
    #         # Логика для подтверждения по номеру телефона
    #         # Отправка SMS с кодом подтверждения
    #         # Проверка кода подтверждения
    #         pass

    #     elif confirmation_method == 'email':
    #         # Логика для подтверждения по электронной почте
    #         # Отправка письма с кодом подтверждения
    #         # Проверка кода подтверждения
    #         pass

    #     else:
    #         return response.Response(
    # {'error': 'Invalid confirmation method'})

    #     # Создание пользователя после успешной проверки кода подтверждения
    #     self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)
    #     return response.Response(
    #         serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )

    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     signals.user_registered.send(
    #         sender=self.__class__,
    #         user=user,
    #         request=self.request
    #     )

    # def perform_update(self, serializer):
    #     user = serializer.save()
    #     signals.email_confirmed.send(
    #         sender=self.__class__,
    #         user=user,
    #         request=self.request
    #     )
