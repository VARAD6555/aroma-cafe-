import click
from flask import current_app
from .extensions import db
from .models import CafeTable

def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        for number in ["01", "02", "03", "04", "05", "06", "07", "08"]:
            if not CafeTable.query.filter_by(table_number=number).first():
                db.session.add(CafeTable(table_number=number))
        db.session.commit()
        click.echo("Database initialized.")
