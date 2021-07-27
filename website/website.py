from fastapi import FastAPI

website: FastAPI = FastAPI()

@website.route("/")
async def test_f(req):
	pass
