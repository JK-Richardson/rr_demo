from enum import Enum

class Target(Enum):
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"

TARGET_SYMBOLS = {
    Target.T1: "▲",
    Target.T2: "●",
    Target.T3: "■",
    Target.T4: "◆",
}

TARGET_COLORS = {
    Target.T1: (255, 0, 0),      # Red
    Target.T2: (0, 0, 255),      # Blue
    Target.T3: (0, 255, 0),      # Green
    Target.T4: (255, 255, 0),    # Yellow
}
