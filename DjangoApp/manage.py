#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line
from project.tunneling_service import tunnel
from project.db_service import database

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team20app.settings')
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    run_main = False
    if os.getenv('RUN_MAIN'):
        run_main = True
        tunnel = tunnel()
        database = database()
    main()
    if run_main:
        database.close_connection()
        tunnel.close_tunnel()
        