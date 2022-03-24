from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from browser_calls_flask import app, db
from browser_calls_flask.models import SupportTicket

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=5002))


@manager.command
def test():
    """Run the unit tests."""
    import sys
    import unittest

    tests = unittest.TestLoader().discover('.', pattern="*_tests.py")
    test_result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not test_result.wasSuccessful():
        sys.exit(1)


@manager.command
def dbseed():
    ticket1 = SupportTicket(
        name="Ihsaan", phone_number="+13612326374", description="Got an issue while..."
    )
    db.session.add(ticket1)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
