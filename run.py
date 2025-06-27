from website import app
from website.routes import uploaded_files, uploaded_files_lock
from website.utils.cleanup import cleanup_expired_uploads
import threading

# Start cleanup thread
threading.Thread(
    target=cleanup_expired_uploads,
    args=(uploaded_files, uploaded_files_lock),
    daemon=True
).start()

if __name__ == "__main__":
    app.run()