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
