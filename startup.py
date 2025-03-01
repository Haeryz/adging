import os
import threading
from basor_AI import client, app, start_keep_alive

# Use PORT environment variable if it exists (Azure sets this)
# Otherwise use 8000 as a default
port = int(os.getenv('PORT', 8000))

def run_flask():
    # Run Flask without blocking
    app.run(host='0.0.0.0', port=port)

def run_discord():
    # Run Discord bot
    client.run(token=os.getenv('BASOR_TOKEN'))

if __name__ == "__main__":
    # Start the keep-alive mechanism
    start_keep_alive()
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run Discord bot in the main thread
    run_discord()