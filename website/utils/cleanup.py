import time

def cleanup_expired_uploads(uploaded_files, uploaded_files_lock, expire_seconds=600):
    print("* Starting cleanup thread for expired uploads")
    while True:
        time.sleep(60)
        now = time.time()
        keys_to_delete = []
        with uploaded_files_lock:
            for key, value in uploaded_files.items():
                if now - value['timestamp'] > expire_seconds:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del uploaded_files[key]