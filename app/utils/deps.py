from app.services.parser import CustomVisitor, Parser


def create_vistor() -> CustomVisitor:
    return CustomVisitor()


def create_parser() -> Parser:
    return Parser()
