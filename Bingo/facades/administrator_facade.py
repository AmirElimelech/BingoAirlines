from .facade_base import FacadeBase
from ..models import Customers, Airline_Companies, Administrators , Users
from django.core.exceptions import ValidationError

class AdministratorFacade(FacadeBase):
    def __init__(self, request, user):
        super().__init__()
        self.request = request
        self.user = user

    def validate_admin_privileges(self):
        # Validate the user role from the session
        user_role = self.request.session.get('user_role', None)
        if user_role != "administrator":
            raise PermissionError("You do not have the necessary privileges to perform this operation.")


    def get_all_customers(self):
        self.validate_admin_privileges()
        return self.DAL.get_all(Customers)

    def add_airline(self, airline):
        self.validate_admin_privileges()
        if Airline_Companies.objects.filter(name=airline['name']).exists():
            raise ValidationError("Airline with this name already exists.")
        if Airline_Companies.objects.filter(iata_code=airline['iata_code']).exists():
            raise ValidationError("Airline with this IATA code already exists.")
        return self.DAL.add(Airline_Companies, **airline)

    def add_customer(self, customer):
        self.validate_admin_privileges()
        # Validate phone number
        if Customers.objects.filter(phone_no=customer['phone_no']).exists():
            raise ValidationError("Customer with this phone number already exists.")
        
        # Validate email
        if Users.objects.filter(email=customer['email']).exists():
            raise ValidationError("User with this email address already exists.")
        
        return self.DAL.add(Customers, **customer)

    def add_administrator(self, administrator):
        self.validate_admin_privileges()
        if not administrator["first_name"].isalpha() or not administrator["last_name"].isalpha():
            raise ValidationError("Names should only contain letters.")
        if Administrators.objects.filter(user_id=administrator['user_id']).exists():
            raise ValidationError("This user already has an administrator account.")
        return self.DAL.add(Administrators, **administrator)

    def remove_airline(self, airline):
        self.validate_admin_privileges()
        airline_instance = self.DAL.get_by_id(Airline_Companies, airline.get("iata_code"))
        if not airline_instance:
            raise ValidationError("Airline not found.")
        return self.DAL.remove(airline_instance)

    def remove_customer(self, customer):
        self.validate_admin_privileges()
        customer_instance = self.DAL.get_by_id(Customers, customer.get("id"))
        if not customer_instance:
            raise ValidationError("Customer not found.")
        return self.DAL.remove(customer_instance)

    def remove_administrator(self, administrator):
        self.validate_admin_privileges()
        admin_instance = self.DAL.get_by_id(Administrators, administrator.get("id"))
        if not admin_instance:
            raise ValidationError("Administrator not found.")
        return self.DAL.remove(admin_instance)


