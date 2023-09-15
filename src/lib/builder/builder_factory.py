from typing import Type, Any

from src.lib.builder.builder import Builder


class BuilderFactory:

    def __init__(self) -> None:
        self.__builders: dict[str, Type[Builder]] = {}

    def register_builder(self, key: str, builder: Type[Builder]) -> None:
        self.__builders[key] = builder

    def create(self, key: str, **kwargs) -> Builder:
        builder_class: Type[Builder] = self.__builders.get(key)

        if not builder_class:
            raise ValueError(f"No builder registered for key: {key}")

        return builder_class(**kwargs)
