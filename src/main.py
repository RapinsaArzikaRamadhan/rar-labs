from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
import psutil

console = Console()

cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
disk = psutil.disk_usage('/')
net = psutil.net_io_counters()

title = Text("RAR Labs", style="bold cyan")

content = Group(
    title,
    Text(""),
    Text(f"CPU: {cpu}%"),
    Text(f"RAM: {ram.percent}%"),
    Text(f"DISK: {disk.percent}%"),
    Text(f"NET: {net.bytes_recv}%"),
) 

console.print(
    Panel.fit(
        content,
        title="RAR Dynamics"
    )
)
