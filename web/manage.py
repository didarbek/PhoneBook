from flask.cli import FlaskGroup

from project import app, db, Users


cli = FlaskGroup(app)


# creating command to create a database
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# creating command to seed a database
# in this case we create a new user with name="John" and phone=12345
@cli.command("seed_db")
def seed_db():
    db.session.add(Users(name="John", phone=12345))
    db.session.commit()


if __name__ == "__main__":
    cli()