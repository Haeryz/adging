import os
from basor_AI import client

# Use PORT environment variable if it exists (Azure sets this)
# Otherwise use 8000 as a default
port = int(os.getenv('PORT', 8000))

# Start the Discord bot
client.run(token=os.getenv('BASOR_TOKEN'))