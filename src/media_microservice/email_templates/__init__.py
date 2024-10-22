"""SMTP Module"""
from .order_email import send_order_email
from .order_email_process import EmailConfirmationProcess

__all__ = ["send_order_email", "EmailConfirmationProcess"]
