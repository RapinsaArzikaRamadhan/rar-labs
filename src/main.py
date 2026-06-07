from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
import time
import psutil

console = Console()
layout = Layout()

layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="logs", size=8)
)

layout["body"].split_row(
    Layout(name="left"),
    Layout(name="right")
)

title = Text("RAR Labs", style="bold cyan")

with Live(layout, refresh_per_second=2, screen=True) as live:
    
    while True:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        width = console.size.width
        height = console.size.height

        layout["header"].update(
            Panel(
                f"{title}"
                )
        )
        layout["left"].update(
            Panel(
                f"CPU:{cpu}%\nDISK:{disk.percent}%"
                )
        )
        layout["right"].update(
            Panel(
                f"RAM: {ram.percent}%\nNET: {net.bytes_recv / 1024**3:.2f}GB"
                )
        )

        layout["logs"].update(
            Panel(
                f"upcoming"
                )
        )

        time.sleep(1)
