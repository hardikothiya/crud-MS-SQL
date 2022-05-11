
from fastapi import FastAPI
from .db_connection import cursor, cxnn

app = FastAPI()
#
cursor = cursor
cxnn = cxnn


@app.get("/")
async def root():
    query = "insert into demo.dbo.tbl_user_info (username, fullname) values('hardikkk','hardlink')"
    # query = "select * from demo.dbo.tbl_user_info"
    cursor.execute(query)
    cxnn.commit()
    # for row in data:
    #     print("Id: ", row[0])
    #     print("Name: ", row[1])
    #     print("fullname: ", row[2])

    return {"message": "Hello World"}

