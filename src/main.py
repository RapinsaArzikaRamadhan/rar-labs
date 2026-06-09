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

def net_bar(speed, max_speed=1024*1024):
    percent = min(speed  / max_speed * 100, 100)
    return bar(percent)
# riwayat_ram = []

# def gfk(data):
#     karakter = "⣀⣄⣤⣦⣶⣷⣿"
#     hasil = ""

#     for nilai in data:
#         indeks = int(
#             nilai / 100 * (len(karakter)  -1)
#         )
    
#         hasil += karakter[indeks]

#     return hasil

old = psutil.net_io_counters()

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
        # riwayat_ram.append(ram.percent)
        # if len(riwayat_ram) > 20:
        #     riwayat_ram.pop(0)

        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()
        new = psutil.net_io_counters()
        old = new

        recv = new.bytes_recv - old.bytes_recv
        sent = new.bytes_sent - old.bytes_sent

        width = console.size.width
        height = console.size.height

        layout["header"].update(Panel(f"{title}"))
        layout["left"].update(
            Panel(
                Group(
                    Text(f"CPU:{cpu}%"),
                    Text(f"C0:{bar(C0)} {C0:.1f}% CT{bar(C0t)} {C0t:.1f}%"),
                    Text(f"C1:{bar(C1)} {C1:.1f}% CT{bar(C1t)} {C1t:.1f}%"),
                    Text(f"C2:{bar(C2)} {C2:.1f}%"),
                    Text(f"C3:{bar(C3)} {C3:.1f}%"),
                    Text(""),
                    Text(f"DS:{bar(disk.percent)} {disk.percent}%"),
                ),
                title="LEFT PANEL",
            )
        )
        layout["right"].update(
            Panel(
                Group(
                    # Text(f"RAM: {gfk(riwayat_ram)} {ram.percent:.1f}%"),
                    # Text(f"NET: {net.bytes_recv / 1024**3:.2f}GB"),
                    Text(f"RAM: {bar(ram.percent)} {ram.percent:.1f}%"),
                    Text(f"NET: {net_bar(sent)} {sent/1024:.1f}KB/s"),
                    Text(f"NET: {net_bar(recv)} {recv/1024:.1f}KB/s"),
                    Text(f"DEBUG recv={recv} sent={sent}")
                ),
                title="RIGHT PANEL",
            )
        )

        layout["logs"].update(Panel(f"upcoming"))

        time.sleep(1)
