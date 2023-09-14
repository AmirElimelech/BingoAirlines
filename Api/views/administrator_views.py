

import logging
from rest_framework import status
from django.db import transaction
from django.forms.utils import ErrorList
from Api.permissions import IsAdministrator
from rest_framework.response import Response
from ..serializers import CustomersSerializer
from rest_framework.decorators import api_view
from Bingo.facades.facade_base import FacadeBase
from Bingo.decorators import check_permissions , login_required
from Bingo.facades.administrator_facade import AdministratorFacade
from Bingo.forms import UsersForm, CustomerForm, AirlineCompanyForm, AdministratorForm









logger = logging.getLogger(__name__)






@api_view(['POST'])
@login_required
@check_permissions(IsAdministrator)
def user_registration_api(request):
    logger.debug(f"Received data: {request.data}")

    allowed_roles = {
        "Customer": 3,
        "AirlineCompany": 2,
        "Administrator": 1
    }

    user_role_param = request.data.get('user_role', None)

    if user_role_param not in allowed_roles:
        logger.error(f"Invalid user role received: {user_role_param}")
        return Response({"message": f"Invalid user role: {user_role_param}"}, status=status.HTTP_400_BAD_REQUEST)
    
    request.data['user_role'] = allowed_roles[user_role_param]

    user_form = UsersForm(request.data, request.FILES)
    entity_form = None

    if user_role_param == "Customer":
        entity_form = CustomerForm(request.data)
    elif user_role_param == "AirlineCompany":
        entity_form = AirlineCompanyForm(request.data, request.FILES)
    elif user_role_param == "Administrator":
        entity_form = AdministratorForm(request.data)

    try:
        if user_form.is_valid() and (entity_form is None or entity_form.is_valid()):
            user_data = {
                "id": user_form.cleaned_data.get("id"),
                "username": user_form.cleaned_data.get("username"),
                "email": user_form.cleaned_data.get("email"),
                "password": user_form.cleaned_data.get("password"),
                "user_role": user_form.cleaned_data.get("user_role"),
                "image": user_form.cleaned_data.get("image"),
            }
            
            with transaction.atomic():
                facade = FacadeBase(request)
                user_instance = facade.create_new_user(user_data)

                login_token_dict = request.session.get('login_token')
                admin_facade = AdministratorFacade(request, user_instance, login_token_dict)

                if user_role_param == "Customer":
                    customer_data = {
                        'user_id': user_instance.id,
                        'first_name': entity_form.cleaned_data.get("first_name"),
                        'last_name': entity_form.cleaned_data.get("last_name"),
                        'address': entity_form.cleaned_data.get("address"),
                        'phone_no': entity_form.cleaned_data.get("phone_no"),
                        'credit_card_no': entity_form.cleaned_data.get("credit_card_no")
                    }
                    customer_instance = admin_facade.add_customer(customer_data)

                elif user_role_param == "AirlineCompany":
                    airline_data = {
                        'user_id': user_instance.id,
                        'iata_code': entity_form.cleaned_data.get("iata_code"),
                        'name': entity_form.cleaned_data.get("name"),
                        'country_id': entity_form.cleaned_data.get("country_id").id,
                        'logo': entity_form.cleaned_data.get("logo"),
                    }
                    airline_instance = admin_facade.add_airline(airline_data)

                elif user_role_param == "Administrator":
                    admin_data = {
                        'user_id': user_instance.id,
                        'first_name': entity_form.cleaned_data.get("first_name"),
                        'last_name': entity_form.cleaned_data.get("last_name"),
                    }
                    admin_instance = admin_facade.add_administrator(admin_data)

            return Response({"message": f"Successfully created {user_role_param} instance."}, status=status.HTTP_201_CREATED)

        else:
            user_form_errors = ", ".join([f"{field}: {ErrorList(errors)}" for field, errors in user_form.errors.items()])
            logger.error(f"User form errors: {user_form_errors}")

            if entity_form:
                entity_form_errors = ", ".join([f"{field}: {ErrorList(errors)}" for field, errors in entity_form.errors.items()])
                logger.error(f"Entity form errors: {entity_form_errors}")

            errors = {"user_errors": user_form.errors}
            if entity_form:
                errors["entity_errors"] = entity_form.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@login_required
@check_permissions(IsAdministrator)
def get_all_customers_api(request):

    """
    Get all customers from the database.
    """
    try:
        # Extract the login token as a dictionary from the session
        login_token_dict = request.session.get('login_token')

        facade = AdministratorFacade(request, request.user, login_token_dict)
        customers = facade.get_all_customers()
        
        serializer = CustomersSerializer(customers, many=True)
        if not customers:
            logger.info("No customers found in the database.")
            return Response({"message": "No customers found in the database."}, status=status.HTTP_200_OK)
        
        logger.info("Successfully fetched all customers.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return Response({"error": "Error fetching customers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





