from website import app
from website.routes import cleanup_expired_uploads
import threading
if __name__ == '__main__':
    threading.Thread(target=cleanup_expired_uploads, daemon=True).start()
    app.run(debug=True)