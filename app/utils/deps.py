from app.services.parser import Parser, TypingCollector, TypingTransformer


def create_vistor() -> TypingCollector:
    return TypingCollector()


def create_parser() -> Parser:
    return Parser()
