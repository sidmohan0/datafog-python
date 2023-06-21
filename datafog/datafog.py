from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from werkzeug.utils import secure_filename
import os
import logging
import binascii
import faker
from faker import Faker
from .models import ValueMapping
import binascii



# Logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)






class datafog:

    def __init__(self, db_path='sqlite:///./test.db'):
        self.engine = create_engine(db_path, echo = True)
        self.Session = sessionmaker(bind=self.engine)

    def scan(self, input_path):
        """
        The method returns a tuple, where the first element is the boolean contains_pii
         and the second element is the list pii_fields. You can then call this method 
         and handle the output as needed in your specific use case. 
         For example, you could convert the list of PII fields to JSON.
        """
        fake = Faker()

        predefined_header_values = ["account_number", "age", "date", "date_interval", "dob", "driver_license", "duration", "email_address", "event", "filename", "gender_sexuality", "healthcare_number", "ip_address", "language", "location", "location_address", "location_city", "location_coordinate", "location_country", "location_state", "location_zip", "marital_status", "money", "name", "name_family", "name_given", "numerical_pii", "organization", "occupation", "origin", "passport_number", "password", "phone_number", "physical_attribute", "political_affiliation", "religion", "ssn", "time", "url", "username", "vehicle_id", "zodiac_sign", "blood_type", "condition", "dose", "drug", "injury", "medical_process", "statistics", "bank_account", "credit_card", "credit_card_expiration", "cvv", "routing_number"]

        # Read the file from input_path
        df = pd.read_csv(input_path)

        # Initialize empty list for PII fields
        pii_fields = []

        for col in df.columns:
            if col in predefined_header_values:
                pii_fields.append(col)

        # Determine if any PII fields were found
        contains_pii = len(pii_fields) > 0

        return contains_pii, pii_fields

    def swap(self, input_path, output_path):





        # Faker Setup
        fake = Faker()

        faker_methods = {
            'account_number': fake.unique.random_number,
            'age': fake.random_int,
            'date': fake.date,
            'email_address': fake.email,
            'name': fake.name,
            'phone_number': fake.phone_number,
            # Add all other mappings
            # ...
        }

        predefined_header_values = ["account_number", "age", "date", "date_interval", "dob", "driver_license", "duration", "email_address", "event", "filename", "gender_sexuality", "healthcare_number", "ip_address", "language", "location", "location_address", "location_city", "location_coordinate", "location_country", "location_state", "location_zip", "marital_status", "money", "name", "name_family", "name_given", "numerical_pii", "organization", "occupation", "origin", "passport_number", "password", "phone_number", "physical_attribute", "political_affiliation", "religion", "ssn", "time", "url", "username", "vehicle_id", "zodiac_sign", "blood_type", "condition", "dose", "drug", "injury", "medical_process", "statistics", "bank_account", "credit_card", "credit_card_expiration", "cvv", "routing_number"]

        # Read the file from train_path
        df = pd.read_csv(input_path)

        for col in df.columns:
            if col in predefined_header_values and col in faker_methods:
                original_values = df[col].tolist()  # Keep a list of original values
                df[col] = df[col].apply(lambda x: faker_methods[col]())  # Synthetic values
                synthetic_values = df[col].tolist()  # Keep a list of synthetic values

                # Save each original and synthetic value pair in the database
                for original, synthetic in zip(original_values, synthetic_values):
                    self.save(record_id=None, field_name=col, original_value=original, new_value=synthetic)

        # Save the modified DataFrame to a new file
        df.to_csv(os.path.join(output_path, 'synthetic_output.csv'), index=False)

        return True

    def hash(self):
        # Implement your code to hash value here
        pass

    def redact(self):
        # Implement your code to apply redaction here
        pass

    def save(self, record_id, field_name, original_value, new_value):
        # create a new session
        session = self.Session()

        # create a new ValueMapping instance
        data = ValueMapping(
            record_id=record_id,
            field_name=field_name,
            original_value=original_value,
            new_value=new_value,
        )

        # add and commit
        session.add(data)
        session.commit()

    def kafka_consume(self):
        # Implement your code to consume Kafka stream and parse message here
        pass

    def lookup(self):
        # Implement your code to perform lookup to relational DB here
        pass

    def swap_back(self):
        # Implement your code to swap out original PII data with synthetic data before returning to application here
        pass
