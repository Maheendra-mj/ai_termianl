import asyncio
import subprocess
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from . import database

class AITerminalClient:
    def __init__(self, server_url: str = "http://127.0.0.1:8000"):
        self.server_url = server_url
        self.console = Console()
        self.session_id: str | None = None
        database.initialize_db()

    async def initialize_session(self, client: httpx.AsyncClient):
        self.console.print("[cyan]Initializing session with MCP Server...[/cyan]")
        try:
            response = await client.post(f"{self.server_url}/session/start")
            response.raise_for_status()
            data = response.json()
            self.session_id = data.get("session_id")
            if self.session_id:
                self.console.print(f"[green]✓ Session established. ID: {self.session_id}[/green]")
            else:
                self.console.print("[bold red]Error: Server did not provide a session ID.[/bold red]")
        except httpx.RequestError:
            self.console.print(f"[bold red]Error: Could not connect to MCP Server at {self.server_url}. Is it running?[/bold red]")
            return False
        return self.session_id is not None

    async def handle_ai_command(self, prompt: str, client: httpx.AsyncClient):
        if not self.session_id:
            self.console.print("[bold red]Cannot process command: No active session.[/bold red]")
            return

        payload = {"session_id": self.session_id, "prompt": prompt}
        
        with self.console.status("[magenta]Sending context to MCP Server...[/magenta]"):
            try:
                response = await client.post(f"{self.server_url}/process_command", json=payload)
                response.raise_for_status()
                data = response.json()
            except httpx.RequestError as e:
                self.console.print(f"[bold red]Error communicating with MCP Server: {e}[/bold red]")
                return

        plan = data.get('plan')
        if not (plan and plan.get("commands")):
            self.console.print(Panel(data.get('raw_response', 'No response'), title="[red]MCP Server Error[/red]"))
            return

        self.console.print(Panel(Markdown(plan.get('explanation', '')), title="Execution Plan"))
        
        # --- LOGIC UPDATED HERE ---
        # This loop now safely handles both strings and dictionaries from the AI
        for command_item in plan["commands"]:
            cmd_text = ""
            if isinstance(command_item, str):
                cmd_text = command_item
            elif isinstance(command_item, dict) and 'command' in command_item:
                cmd_text = command_item['command']
            else:
                self.console.print(f"[yellow]Skipping malformed command item: {command_item}[/yellow]")
                continue

            self.console.print(Panel(Syntax(cmd_text, "bash", theme="monokai"), title="Suggested Command"))
            confirm = input("Run this command? (y/N/e)dit > ").strip().lower()
            
            final_cmd = cmd_text
            if confirm == 'e':
                final_cmd = input(f"Edit command > {cmd_text}\n> ")

            if confirm in ('y', 'e'):
                self.execute_shell_command(final_cmd, is_ai=True)
            else:
                self.console.print("[yellow]Execution skipped.[/yellow]")

    def execute_shell_command(self, command: str, is_ai: bool = False):
        if not command: return
        try:
            subprocess.run(command, shell=True, check=True)
            database.add_command_to_history(command, is_ai)
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error executing command: {e}[/red]")

    async def run_repl(self):
        session = PromptSession(history=InMemoryHistory())
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            if not await self.initialize_session(client):
                return

            self.console.print(Panel("[bold green]AI Terminal Initialized.[/bold green] Type `?` followed by your task for AI, or any standard shell command.", title="Welcome"))
            
            while True:
                try:
                    command = await session.prompt_async("➤ ")
                    if command.lower() in ("exit", "quit"): break

                    if command.startswith('?'):
                        await self.handle_ai_command(command[1:].strip(), client)
                    else:
                        self.execute_shell_command(command)
                except (KeyboardInterrupt, EOFError):
                    break
        self.console.print("[cyan]Goodbye![/cyan]")

def main():
    client = AITerminalClient()
    asyncio.run(client.run_repl())

