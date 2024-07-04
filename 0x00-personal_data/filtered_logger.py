#!/usr/bin/env python3
"""filtered_logger.py"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated.
    Args:
        fields (list): List of strings
        representing all fields to obfuscate.
        redaction (str): String representing by what
        the field will be obfuscated.
        message (str): String representing the log line.
        separator (str): String representing by which character is
        separating all fields in the log line.
    Returns:
        str: Obfuscated log message.
    """
    return re.sub(f"({'|'.join(fields)})=.*?{separator}",
                  lambda m: f"{m.group(1)}={redaction}{separator}",
                  message)
