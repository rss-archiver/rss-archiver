import uvicorn
from rss_archiver.api import app
from rss_archiver import monitor

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
