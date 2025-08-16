import asyncio
import typer
from rich import print
from typing import Annotated
from datetime import datetime

from apps.containers import root_container
from apps.core.auth.hash import hash_password
from apps.core.database.models import User
from sqlalchemy import select

"""
Create superuser

Create superuser for application.
Inspired from Python Django createsuperuser command
"""


async def create_superuser_in_db(username: str, email: str, password: str):
    hashed_password = hash_password(password)

    db = root_container.db()

    try:
        async with db.session() as session:
            existing_username = await session.scalar(
                select(User).where(User.username == username)
            )
            if existing_username:
                raise ValueError(f"Username '{username}' already in use")

            existing_email = await session.scalar(
                select(User).where(User.email == email)
            )
            if existing_email:
                raise ValueError(f"Email '{email}' already in use")

            new_superuser = User(
                username=username,
                email=email,
                first_name="",
                last_name="",
                is_active=True,
                is_staff=True,
                is_superuser=True,
                date_joined=datetime.now(),
                hashed_password=hashed_password,
            )

            session.add(new_superuser)
            await session.commit()
            await session.refresh(new_superuser)

            return new_superuser
    finally:
        # Close all connected sessions
        # https://docs.sqlalchemy.org/en/20/core/connections.html#engine-disposal
        await db.engine.dispose()


def main(
    hide_password: Annotated[
        bool, typer.Option("--hide-password/--show-password")
    ] = True,
):
    print("[bold blue]✨Creating Superuser[/bold blue]")

    username = typer.prompt("Enter username")
    email = typer.prompt("Enter email")
    password = typer.prompt("Enter password", hide_input=hide_password)
    password_confirmation = typer.prompt(
        "Enter password again", hide_input=hide_password
    )

    if password != password_confirmation:
        print("[bold red]Password confirmation does not match[/bold red]")
        raise typer.Exit()

    if not username.strip():
        print("[bold red]Username cannot be empty[/bold red]")
        raise typer.Exit()

    if not email.strip():
        print("[bold red]Email cannot be empty[/bold red]")
        raise typer.Exit()

    if not password.strip():
        print("[bold red]Password must be at least 6 characters long[/bold red]")
        raise typer.Exit()

    try:
        superuser = asyncio.run(create_superuser_in_db(username, email, password))
        print(
            f"[bold green]Superuser '{superuser.username}' created successfully[/bold green]"
        )
        print(f"[bold green]User ID: {superuser.id}[/bold green]")
        print(f"[bold green]Email: {superuser.email}[/bold green]")
    except ValueError as e:
        print(f"[bold red]{str(e)}[/bold red]")
        raise typer.Exit()
    except Exception as e:
        print(f"[bold red]Failed to create superuser: {str(e)}[/bold red]")
        raise typer.Exit()


if __name__ == "__main__":
    typer.run(main)
