# DataFog

DataFog (or the product formerly known as Codexify) is a Python package that simplifies and automates data anonymization tasks. With DataFog, you can quickly scan your datasets for Personal Identifiable Information (PII), swap PII with synthetic data, save and look up original and synthetic data pairs, and more.

**Note** In some cases pip install will not work right off the bat; pip installing these dependencies has worked to-date:
```bash
pip install setuptools==65.5.0 "wheel<0.40.0"
```

**Product Demo** 
[Video](https://www.loom.com/share/ba2561a16d004f479a02c204272ccb28?sid=252cc726-8510-4242-a50e-1f7d1b5606e6)

## Libraries Used
* [faker](www.github.com/joke2k/faker) for Synthetic Data Generation
* Boilerplate PII detection code (swapping in with a custom solution soon)

## Coming Soon:
* product demo
* documentation
* `examples/` directory for more detailed examples and usage information

please see www.datafog.dev for more information or contact me at sidmohan001@gmail.com
## Installation

DataFog can be installed via pip. Use the following command to install:

```bash
pip install datafog
```

## Getting Started

Once you've installed DataFog, you can import it into your Python scripts as follows:

```python
from datafog import DataFog

datafog = DataFog()
```

Now, you're ready to use DataFog to handle your PII anonymization needs. Here are some basic examples:
#### `show_banlist(self)`
This method prints out the current ban list and its version. The ban list contains the field names considered as PII.

##### Example:
```python
datafog.show_banlist()
```
Output:

```
Ban List Version 1:
['address', 'age', 'bank_account', 'credit_card', 'credit_card_expiration', 'date', 'email_address', 'first_name', 'ip_address', 'last_name', 'location', 'city', 'latlong', 'country', 'state', 'zip', 'name', 'occupation', 'passport_number', 'password', 'phone_number', 'product_sku', 'routing_number', 'ssn', 'time', 'username', 'license_plate']
```

#### `add_to_banlist(self, *args)`
This method takes in any number of strings as arguments, and adds them to the ban list if they're not already present. It increments the ban list version and prints the updated ban list.

##### Example:
```python
datafog.add_to_banlist('height', 'weight')
```
Output:

```
Successfully added: ['height', 'weight']
Updated Ban List (Version 2):
['address', 'age', 'bank_account', 'credit_card', 'credit_card_expiration', 'date', 'email_address', 'first_name', 'ip_address', 'last_name', 'location', 'city', 'latlong', 'country', 'state', 'zip', 'name', 'occupation', 'passport_number', 'password', 'phone_number', 'product_sku', 'routing_number', 'ssn', 'time', 'username', 'license_plate', 'height', 'weight']
```

#### `remove_from_banlist(self, *args)`
This method takes in any number of strings as arguments, and removes them from the ban list if they're present. It increments the ban list version and prints the updated ban list.

##### Example:
```python
datafog.remove_from_banlist('height', 'weight')
```
Output:

```
Successfully removed: ['height', 'weight']
Updated Ban List (Version 3):
['address', 'age', 'bank_account', 'credit_card', 'credit_card_expiration', 'date', 'email_address', 'first_name', 'ip_address', 'last_name', 'location', 'city', 'latlong', 'country', 'state', 'zip', 'name', 'occupation', 'passport_number', 'password', 'phone_number', 'product_sku', 'routing_number', 'ssn', 'time', 'username', 'license_plate']
```

#### `scan(self, input_path: str) -> Tuple[bool, List[str]]`
This method takes an input file path as an argument and scans the file for personally identifiable information (PII). If any PII is found in the file, it returns a tuple where the first element is a boolean indicating the presence of PII, and the second element is a list of the PII fields.

##### Example:
```python
contains_pii, pii_fields = datafog.scan('data.csv')
```
Output:

```python
# Suppose 'data.csv' contains columns 'name', 'address', 'age', and 'email_address'.
True, ['name', 'address', 'age', 'email_address']
```

#### `swap(self, input_path: str, output_path: str) -> bool`
This method takes in an input file path and an output path as arguments. The method reads the file from the input path, creates synthetic values for PII fields, and writes the modified DataFrame to a new file in the output path. If the operation is successful, it returns `True`.

##### Example:
```python
datafog.swap('data.csv', 'synthetic_data/')
```
Output:

```python
# A new file 'synthetic_output.csv' is created in the 'synthetic_data/' directory. This file contains
# the same data as 'data.csv', but PII fields have been replaced with synthetic values.
True
```

#### `redact(value: str) -> str`
This is a static method that simply takes a string value as an input and returns the string '[REDACTED]'. This can be used to redact sensitive information in your data.

##### Example:
```python
DataFog.redact('Sensitive Data')
```
Output:

```python
'[REDACTED]'
```

#### `hash(value: str) -> str`
Another static method that takes a string value as an input, and returns a SHA256 hash of that string. This can be used to hash sensitive information in your data.

##### Example:
```python
DataFog.hash('Sensitive Data')
```
Output:

```python
# Returns a SHA256 hash of 'Sensitive Data'.
'6dcd4ce23d88e2ee95838fcae5f2356c17d6b9d8950fb7296e378ed50f9d299a'
```

#### `save(self, record_id, field_name, original_value, new_value)`
This instance method saves an original and synthetic value pair in the database. The parameters are as follows:

- `record_id`: the ID of the record in the original dataset.
- `field_name`: the name of the field where the value was found.
- `original_value`: the original value found in the dataset.
- `new_value`: the synthetic value that replaces the original one.

The method doesn't return anything.

##### Example:
```python
datafog.save(record_id='123', field_name='address', original_value='123 Main St', new_value='456 Oak Dr')
```

After this operation, the database would contain a new record where the original address '123 Main St' is mapped to the synthetic address '456 Oak Dr'.


#### `process_kafka_record(self, record: Dict) -> Dict`
This method takes in a Kafka record (in the form of a dictionary), and replaces the original values with synthetic values for each key that matches a field name in the record. It uses the `lookup` method (which we'll discuss next) to find corresponding synthetic values from the `ValueMapping` table in the database. The processed record, with replaced values, is then returned.

##### Example:
```python
record = {
    'message': {
        'record_id': '123',
        'address': '123 Main St',
        'age': '30',
    }
}
processed_record = datafog.process_kafka_record(record)
print(processed_record)
```

This example could output something like the following, assuming that the synthetic values for the `address` and `age` fields of record '123' were '456 Oak Dr' and '25', respectively.

```python
{
    'message': {
        'record_id': '123',
        'address': '456 Oak Dr',
        'age': '25',
    }
}
```

#### `lookup(self, record_id: str) -> Optional[List[ValueMapping]]`
This method takes in a record ID as an argument, and queries the `ValueMapping` table for records that match the given record ID. It returns a list of `ValueMapping` objects, or `None` if no matching records were found.

##### Example:
```python
record_id = '123'
value_mappings = datafog.lookup(record_id)
print(value_mappings)
```

The above example would output something like the following:

```python
[<ValueMapping record_id='123', field_name='address', original_value='123 Main St', new_value='456 Oak Dr'>,
<ValueMapping record_id='123', field_name='age', original_value='30', new_value='25'>]
```

#### `swap_back(self, record: Dict) -> Dict`
This method functions similarly to `process_kafka_record`, but instead of replacing original values with synthetic ones, it replaces synthetic values with their original counterparts. It takes in a Kafka record, looks up the original values from the `ValueMapping` table in the database, and returns the record with its original values restored.

##### Example:
```python
record = {
    'message': {
        'record_id': '123',
        'address': '456 Oak Dr',
        'age': '25',
    }
}
original_record = datafog.swap_back(record)
print(original_record)
```

This example could output something like the following:

```python
{
    'message': {
        'record_id': '123',
        'address': '123 Main St',
        'age': '30',
    }
}
```

