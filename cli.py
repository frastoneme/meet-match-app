import click
from database import (create_connection, create_tables, create_user, select_all_users, update_user, 
                      delete_user, create_interest, select_all_interests, add_user_interest, 
                      remove_user_interest, get_user_interests)

DATABASE = "dating_app.db"

@click.group()
def cli():
    pass

@cli.command()
@click.argument('name')
@click.argument('age', type=int)
@click.argument('gender')
@click.argument('bio')
def add_user(name, age, gender, bio):
    """Add a new user profile"""
    conn = create_connection(DATABASE)
    with conn:
        create_tables(conn)
        user = (name, age, gender, bio)
        user_id = create_user(conn, user)
        click.echo(f"User added with id {user_id}")

@cli.command()
def list_users():
    """List all user profiles"""
    conn = create_connection(DATABASE)
    with conn:
        users = select_all_users(conn)
        for user in users:
            click.echo(f"{user[0]}: {user[1]}, {user[2]}, {user[3]} - {user[4]}")

@cli.command()
@click.argument('user_id', type=int)
@click.argument('name')
@click.argument('age', type=int)
@click.argument('gender')
@click.argument('bio')
def update_user_profile(user_id, name, age, gender, bio):
    """Update an existing user profile"""
    conn = create_connection(DATABASE)
    with conn:
        user = (name, age, gender, bio, user_id)
        update_user(conn, user)
        click.echo(f"User {user_id} updated")

@cli.command()
@click.argument('user_id', type=int)
def delete_user_profile(user_id):
    """Delete a user profile by id"""
    conn = create_connection(DATABASE)
    with conn:
        delete_user(conn, user_id)
        click.echo(f"User {user_id} deleted")

@cli.command()
@click.argument('name')
def add_interest(name):
    """Add a new interest"""
    conn = create_connection(DATABASE)
    with conn:
        interest = (name,)
        interest_id = create_interest(conn, interest)
        click.echo(f"Interest added with id {interest_id}")

@cli.command()
def list_interests():
    """List all interests"""
    conn = create_connection(DATABASE)
    with conn:
        interests = select_all_interests(conn)
        for interest in interests:
            click.echo(f"{interest[0]}: {interest[1]}")

@cli.command()
@click.argument('user_id', type=int)
@click.argument('interest_id', type=int)
def add_user_interest_cmd(user_id, interest_id):
    """Add an interest to a user"""
    conn = create_connection(DATABASE)
    with conn:
        add_user_interest(conn, user_id, interest_id)
        click.echo(f"Added interest {interest_id} to user {user_id}")

@cli.command()
@click.argument('user_id', type=int)
@click.argument('interest_id', type=int)
def remove_user_interest_cmd(user_id, interest_id):
    """Remove an interest from a user"""
    conn = create_connection(DATABASE)
    with conn:
        remove_user_interest(conn, user_id, interest_id)
        click.echo(f"Removed interest {interest_id} from user {user_id}")

@cli.command()
@click.argument('user_id', type=int)
def list_user_interests(user_id):
    """List all interests of a user"""
    conn = create_connection(DATABASE)
    with conn:
        interests = get_user_interests(conn, user_id)
        for interest in interests:
            click.echo(f"{interest[0]}")

if __name__ == '__main__':
    cli()
