# Application Commands

## create_superuser

Create superuser of this backend application. User `make` or execute with python module run command

```text
# Use make

make create-superuser

# Python module run command

python -m apps.commands.create_superuser
```

Execution Example

```
> make create-superuser

✨Creating Superuser
Enter username: Junho Yoon
Enter email: andrewyoon10@naver.com
Enter password:
Enter password again:
Superuser 'Junho Yoon' created successfully
User ID: 2
Email: andrewyoon10@naver.com
Done
```

### Flags

- `--hide-password`: Hide password input field
- `--show-password`: Show password input field (Not Recommended)
