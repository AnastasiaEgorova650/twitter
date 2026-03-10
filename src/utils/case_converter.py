import re

pattern1 = re.compile(r"(.)([A-Z][a-z]+)")
pattern2 = re.compile("([a-z0-9])([A-Z])")


def camel_case_to_snake_case(input_str: str) -> str:
    subbed = pattern1.sub(r"\1_\2", input_str)
    return pattern2.sub(r"\1_\2", subbed).lower()
