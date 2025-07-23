"""Services package for the ISP management system."""

from .sheets.service import SheetsServiceV2 as sheets_service

__all__ = ['sheets_service']