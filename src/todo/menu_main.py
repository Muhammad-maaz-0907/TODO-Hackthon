#!/usr/bin/env python3
"""
Main entry point for the menu-driven Todo application.
"""

from .menu_interface import TodoMenuInterface


def main():
    """Start the menu-driven Todo application."""
    app = TodoMenuInterface()
    app.run()


if __name__ == "__main__":
    main()