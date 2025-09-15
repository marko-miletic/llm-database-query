from dataclasses import dataclass


@dataclass
class Credentials:
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
