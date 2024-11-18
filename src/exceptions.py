class MissingEnvVar(Exception):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def __str__(self) -> str:
        return f"Missing environment variable '{self.var_name}'"
