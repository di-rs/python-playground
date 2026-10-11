import json
import logging
from string.templatelib import Interpolation, Template


def render(template: Template) -> str:
    result = []

    for item in template:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, Interpolation):
            value = item.value

            if item.conversion == "r":
                value = repr(value)
            elif item.conversion == "s":
                value = str(value)

            result.append(format(value, item.format_spec))

    return "".join(result)


class TemplateFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, Template):
            return render(record.msg)

        return super().format(record)


class JsonTemplateFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if not isinstance(record.msg, Template):
            return json.dumps(
                {"level": record.levelname, "message": record.getMessage()}
            )

        fields = {
            item.expression: item.value for item in record.msg.interpolations
        }

        return json.dumps(
            {"level": record.levelname, "message": render(record.msg), **fields}
        )


logger = logging.getLogger()
logger.setLevel(logging.INFO)

plain_handler = logging.StreamHandler()
plain_handler.setFormatter(TemplateFormatter())

json_handler = logging.StreamHandler()
json_handler.setFormatter(JsonTemplateFormatter())

logger.addHandler(plain_handler)
logger.addHandler(json_handler)

user_id = 42
duration = 1.2345

logger.info(t"Processed request for user {user_id} in {duration:.2f}s")
