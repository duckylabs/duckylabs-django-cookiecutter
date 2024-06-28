import os
import secrets


TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def _remove_files(files_to_remove):
    for path_type, file_path in files_to_remove:
        if path_type == "f":
            os.remove(file_path)
        elif path_type == "d":
            os.rmdir(file_path)


def create_env_file():
    sample_env_file = os.path.join(".sample.env")
    env_file = os.path.join(".env")
    open(env_file, "w").write(open(sample_env_file).read())


def remvome_debugpy_files():
    files_to_remove = (
        ("d", os.path.join("{{cookiecutter.project_slug }}", ".vscode")),
    )
    _remove_files(files_to_remove)


def remove_celery_files():
    files_to_remove = (
        ("f", os.path.join("{{cookiecutter.project_slug }}", "celery.py")),
        ("f", os.path.join("{{cookiecutter.project_slug }}", "celery_config.py")),
    )
    _remove_files(files_to_remove)


def update_backend_env_var(env_value, new_value):
    envfle_path = os.path.join(".env")
    with open(envfle_path, "r+") as f:
        file_content = f.read().replace(env_value, new_value)
        f.seek(0)
        f.write(file_content)
        f.truncate()


def generate_django_secret_key(key_len: int = 64):
    env_name = "MY_SECRET_KEY"
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    secret_key = "".join([secrets.choice(chars) for _ in range(key_len)])
    update_backend_env_var(env_name, secret_key)


def main():
    create_env_file()
    generate_django_secret_key()

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()

    if "{{ cookiecutter.use_debugpy }}".lower() == "n":
        remvome_debugpy_files()


if __name__ == "__main__":
    main()
