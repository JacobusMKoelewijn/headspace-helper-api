import uvicorn

if __name__ == '__main__':
    uvicorn.run("headspace-helper-api.main:app", port=5000, reload=True)