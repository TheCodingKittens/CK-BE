from app.services.parser import Parser, TypingCollector


def create_vistor() -> TypingCollector:
    return TypingCollector()


def create_parser() -> Parser:
    return Parser()
