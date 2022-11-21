from fastapi import FastAPI


app = FastAPI()


@app.post('/tasks')
async def create_task():
    return {'ok': True}


@app.get('/tasks')
async def tasks_listing():
    return [{'ok': True}]


@app.get('/tasks/{task_id}')
async def tasks_listing():
    return {'ok': True}
