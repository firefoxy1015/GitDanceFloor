#!/usr/bin/env python3
"""
AION 2 次元進攻提醒器
每小時 XX:30 開始 → 在 XX:28 提醒（提前 2 分鐘）

用法:
  python3 aion2_reminder.py                # 預設 09:00 ~ 24:00 提醒
  python3 aion2_reminder.py --all          # 24 小時全提醒
  python3 aion2_reminder.py --lead 5       # 提前 5 分鐘提醒
  python3 aion2_reminder.py --start 18 --end 23   # 只在 18~23 點提醒
"""

import argparse
import sys
import time
from datetime import datetime, timedelta


RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
BELL = "\a"


def next_alert_time(now: datetime, spawn_minute: int, lead_minutes: int) -> datetime:
    alert_minute = (spawn_minute - lead_minutes) % 60
    candidate = now.replace(minute=alert_minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(hours=1)
    return candidate


def in_active_window(spawn_dt: datetime, start_hour: int, end_hour: int) -> bool:
    h = spawn_dt.hour
    if start_hour <= end_hour:
        return start_hour <= h <= end_hour
    return h >= start_hour or h <= end_hour


def alert(spawn_dt: datetime, lead_minutes: int) -> None:
    bar = "=" * 56
    print(f"\n{BELL}{RED}{BOLD}{bar}{RESET}")
    print(f"{YELLOW}{BOLD}  ⚔  AION 2 次元進攻 即將開始！  ⚔{RESET}")
    print(f"{CYAN}  開始時間: {spawn_dt.strftime('%H:%M')}"
          f"   （還有 {lead_minutes} 分鐘）{RESET}")
    print(f"{GREEN}  → 按 M 開地圖找圖示，或等畫面上方橫幅{RESET}")
    print(f"{RED}{BOLD}{bar}{RESET}\n")
    sys.stdout.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description="AION 2 次元進攻提醒器")
    parser.add_argument("--lead", type=int, default=2,
                        help="提前幾分鐘提醒 (預設 2)")
    parser.add_argument("--spawn-minute", type=int, default=30,
                        help="刷新分鐘 (預設 30，即每小時半點)")
    parser.add_argument("--start", type=int, default=9,
                        help="開始提醒的小時 (預設 9)")
    parser.add_argument("--end", type=int, default=23,
                        help="結束提醒的小時 (預設 23)")
    parser.add_argument("--all", action="store_true",
                        help="24 小時都提醒")
    args = parser.parse_args()

    if args.all:
        args.start, args.end = 0, 23

    print(f"{CYAN}{BOLD}AION 2 次元進攻提醒器已啟動{RESET}")
    print(f"刷新時間: 每小時 :{args.spawn_minute:02d}")
    print(f"提前提醒: {args.lead} 分鐘")
    print(f"提醒時段: {args.start:02d}:00 ~ {args.end:02d}:59")
    print(f"按 Ctrl+C 結束\n")
    sys.stdout.flush()

    while True:
        now = datetime.now()
        alert_dt = next_alert_time(now, args.spawn_minute, args.lead)
        spawn_dt = alert_dt + timedelta(minutes=args.lead)

        if not in_active_window(spawn_dt, args.start, args.end):
            alert_dt += timedelta(hours=1)
            spawn_dt += timedelta(hours=1)

        sleep_seconds = (alert_dt - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            print(f"[{now.strftime('%H:%M:%S')}] 下次提醒: "
                  f"{alert_dt.strftime('%H:%M')} "
                  f"(刷新 {spawn_dt.strftime('%H:%M')})")
            sys.stdout.flush()
            time.sleep(sleep_seconds)

        alert(spawn_dt, args.lead)
        time.sleep(60)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n提醒器已停止")
        sys.exit(0)
