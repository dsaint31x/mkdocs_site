import signal
import os
import time

# 시그널 핸들러 함수 정의
def handle_signal(signum, frame):
    print(f"Received signal: {signum} in process {os.getpid()}")

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, handle_signal)  # Ctrl+C (SIGINT) 처리
signal.signal(signal.SIGTERM, handle_signal) # 종료 요청 시 처리

print(f"Process ID: {os.getpid()}")
print("Waiting for signals... Press Ctrl+C to send SIGINT")

try:
    while True:
        time.sleep(1)  # 무한 대기
except KeyboardInterrupt:
    print("Exiting program.")
