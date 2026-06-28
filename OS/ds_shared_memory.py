from multiprocessing import shared_memory, Process
import numpy as np

# 공유 메모리에서 데이터를 생성하는 함수
def worker(name):
    # 이미 생성된 공유 메모리에 연결
    existing_shm = shared_memory.SharedMemory(name=name)
    # 공유 메모리를 numpy 배열로 변환
    shared_array = np.ndarray((10,), dtype=np.int32, buffer=existing_shm.buf)
    
    # 데이터 수정
    shared_array[0] += 1
    print(f"Worker updated array: {shared_array}")
    
    # 연결 해제
    existing_shm.close()

if __name__ == "__main__":
    # 공유 메모리 생성
    shm = shared_memory.SharedMemory(create=True, size=10 * 4)  # 10개 int32 크기
    array = np.ndarray((10,), dtype=np.int32, buffer=shm.buf)
    array[:] = np.arange(10)  # 초기 데이터 설정
    print(f"Initial array: {array}")
    
    # 프로세스 시작
    p = Process(target=worker, args=(shm.name,))
    p.start()
    p.join()
    
    # 메인 프로세스에서 수정 확인
    print(f"Array after worker: {array}")
    
    # 공유 메모리 닫기 및 해제
    shm.close()
    shm.unlink()
