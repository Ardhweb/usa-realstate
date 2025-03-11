# usa-realstate
#For Linux use python3

Applying Migrations and DB Schema
Starting with each  module

python manage.py makemigrations app_name
**"Hierarchy is important to successfully implement a schema."**
e.g.

python manage.py makemigrations core
python manage.py makemigrations buyer_module
python manage.py makemigrations seller_module
python manage.py makemigrations investors_module
python manage.py makemigrations property_module
python manage.py makemigrations firm_module
python manage.py makemigrations transactions_module
python manage.py makemigrations membership_module
python manage.py makemigrations agent_module
python manage.py makemigrations library
python manage.py makemigrations message_track
python manage.py makemigrations lender_module
python manage.py makemigrations accounts

### List of Apps for Migrations

1. **core**
    ```bash
    python manage.py makemigrations core
    ```

2. **buyer_module**
    ```bash
    python manage.py makemigrations buyer_module
    ```

3. **seller_module**
    ```bash
    python manage.py makemigrations seller_module
    ```

4. **investors_module**
    ```bash
    python manage.py makemigrations investors_module
    ```

5. **property_module**
    ```bash
    python manage.py makemigrations property_module
    ```

6. **firm_module**
    ```bash
    python manage.py makemigrations firm_module
    ```

7. **transactions_module**
    ```bash
    python manage.py makemigrations transactions_module
    ```

8. **membership_module**
    ```bash
    python manage.py makemigrations membership_module
    ```

9. **agent_module**
    ```bash
    python manage.py makemigrations agent_module
    ```

10. **library**
    ```bash
    python manage.py makemigrations library
    ```

11. **message_track**
    ```bash
    python manage.py makemigrations message_track
    ```

12. **lender_module**
    ```bash
    python manage.py makemigrations lender_module
    ```

13. **accounts**
    ```bash
    python manage.py makemigrations accounts
    ```

# Here’s the corrected sentence:

**"Hierarchy is important to successfully implement a schema."**

**Applying migrations**

just use this command after follow-up

```python manage.py migrate```





# Installing Dependeancy:

**For Linux Based (Porduaction)**
```pip install -r requirements.txt```

**For Windows or Development**
```pip install -r  requirements.txt```