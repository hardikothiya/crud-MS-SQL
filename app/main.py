from fastapi import FastAPI

from pymemcache.client import base
from db_connection import cursor, cxnn
import json

app = FastAPI()
#
cursor = cursor
cxnn = cxnn


@app.post("/user")
async def create_user(name: str, fullname: str):
    query = f"insert into demo.dbo.tbl_user_info (username, fullname) values('{name}','{fullname}')"
    cursor.execute(query)
    cxnn.commit()
    return {"message": "{} has been added to the database".format(name)}


@app.get("/user/all")
async def all_users():
    users = []
    query = "select * from demo.dbo.tbl_user_info"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        users.append({"id": row[0], "name": row[1], "fullname": row[2]})
    return users


@app.put("/user/{username}")
def update_user(username: str, new_fullname: str):
    query = f"update demo.dbo.tbl_user_info set fullname = '{new_fullname}' where username = '{username}'"
    cursor.execute(query)
    cxnn.commit()
    return {"message": "{} has been updated".format(username)}


@app.delete("/user/")
def delete_user(username: str):
    client = base.Client(('localhost', 11211))
    client.delete(username)
    query = f"delete from demo.dbo.tbl_user_info where username = '{username}'"
    cursor.execute(query)
    cxnn.commit()
    return {"message": f"{username} has been deleted"}


@app.get("/users/{username}")
def get_user(username: str):
    client = base.Client(('localhost', 11211))
    data = client.get(username)
    if data:
        print("User found in cache")
        s = data.decode("utf-8").replace("'", '"')
        z = "[" + s + "]"
        data = json.loads(z)
        return data

    else:
        print("User not found in cache")
        query = f"select * from demo.dbo.tbl_user_info where username = '{username}'"
        cursor.execute(query)
        data = cursor.fetchone()
        if data is not None:
            client.set(username, {"id": data[0], "name": data[1], "fullname": data[2]}, expire=7770)
            print(type(data))
            print(data)
        else:
            return {"message": "User not found"}
    return {"id": data[0], "name": data[1], "fullname": data[2]}


