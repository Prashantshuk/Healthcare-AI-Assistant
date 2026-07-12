from fastapi import FastAPI;

app=FastAPI(
  title="Healthcare AI Assistant",
  version="1.0.0"
);

@app.get("/")
def root():
  return {
        "message": "Healthcare AI Assistant Backend is Running 🚀"
    }