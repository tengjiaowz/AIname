from pydantic import BaseModel, Field
from typing import Annotated,Literal

class ResponseOut(BaseModel):    #视图函数，只要返回操作结果的模型
    result: Annotated[Literal["success","failuire"], Field("success", description="操作结果")]