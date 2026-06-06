from rich.console import Console
from rich.panel import Panel
import psutil

console = Console()

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory
disk = psutil.disk_usage('/')

console.print(
    Panel.fit(
        f"[bold cyan]RAR Labs[/bold cyan]\n\nCPU: {cpu}%\nRAM {ram}%\nDISK {disk}%",
        title="RAR Dynamics"
    )
)