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
    Layout(name="header", size=3), Layout(name="body"), Layout(name="logs", size=25)
)

layout["body"].split_row(Layout(name="left"), Layout(name="right"))

title = Text("RAR Labs", style="bold cyan")


def bar(percent):
    filled = int(percent / 5)
    return "▰" * filled + "▱" * (20 - filled)


with Live(layout, refresh_per_second=2, screen=True) as live:
    while True:
        cpu = psutil.cpu_percent(interval=None)
        cores = psutil.cpu_percent(interval=None, percpu=True)
        C0 = cores[0]
        C1 = cores[1]
        C2 = cores[2]
        C3 = cores[3]

        temps = psutil.sensors_temperatures()

        cpu_package = temps["thinkpad"][0].current

        C0t = temps["coretemp"][0].current
        C1t = temps["coretemp"][1].current

        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()
        width = console.size.width
        height = console.size.height

        layout["header"].update(Panel(f"{title}"))
        layout["left"].update(
            Panel(
                f"CPU:{cpu}%\nC0:{bar(C0)} {C0:.1f}% CT{bar(C0t)} {C0t:.1f}%\nC1:{bar(C1)} {C1:.1f}% CT{bar(C1t)} {C1t:.1f}%\nC2:{bar(C2)} {C2:.1f}%\nC3:{bar(C3)} {C3:.1f}%\n\nDISK:{disk.percent}%"
            )
        )
        layout["right"].update(
            Panel(f"RAM: {ram.percent}%\n\nNET: {net.bytes_recv / 1024**3:.2f}GB")
        )

        layout["logs"].update(Panel(f"upcoming"))

        time.sleep(1)
