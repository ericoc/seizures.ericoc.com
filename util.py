
"""seizures.ericoc.com"""
import logging
import urllib


logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S %Z',
    format='%(asctime)s [%(levelname)s] (%(process)d): %(message)s'
)


def clean_name(name=None):
    """Clean JSON URL-encoded strings"""
    try:
        return urllib.parse.unquote(name).replace(
            u'\xa0', u' '
        ).replace(
            u"’", u"'"
        ).replace(
            "\n", ', '
        )

    except Exception as e:
        logging.exception(e)
        return name


def parse(data):
    """Parse JSON received from add()"""
    try:

        # Loop through appending each key=value to a line protocol string
        count = 0
        fields = ''
        for k, v in data.items():
            fields += f"{k}="

            # urldecode, and quote, any strings
            if isinstance(v, str):
                v = clean_name(v)
                fields += f"\"{v}\""
            else:
                fields += f"{v}"

            # Append a comma to all but the last field
            count += 1
            if count != len(data.items()):
                fields += ','

        # Return the line protocol style string of fields
        return fields

    except Exception as e:
        logging.exception(e)
        return data
