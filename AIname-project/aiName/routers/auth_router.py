# from http.cookiejar import user_domain_match

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
import string
import random
from fastapi_mail import FastMail, MessageSchema, MessageType
from aiosmtplib import SMTPResponseException
from typing import Annotated
from models import AsyncSession
from models.user import User
from depebndencies import get_session, get_mail
from repository.user_repo import EmailCodeRepository, UserRepository
from schemas import ResponseOut
from schemas.user import RegisterIn,UserCreateSchema, LoginIn,LoginOut
from core.auth import AuthHandler

router = APIRouter(prefix="/auth", tags=["user"])
auth_handler = AuthHandler()

@router.get("/code", response_model=ResponseOut)
async def get_email_code(
        email: Annotated[EmailStr, Query(...)],
        mail: FastMail = Depends(get_mail),
        session: AsyncSession = Depends(get_session)

):
    #生成验证码
    source = string.digits*4
    code = "".join(random.sample(source, 4))
    message = MessageSchema(
        subject="【AI取名助手】注册验证码",
        recipients=[email],
        body=f"您的验证码为{code}\n10分钟有效",
        subtype=MessageType.plain
    )
    email_code_repo = EmailCodeRepository(session=session)
    try:
        print(f"验证码：{code}")
        await mail.send_message(message)
    except SMTPResponseException as e:
        # 检查是否是 QQ 特有的二进制响应错误
        if e.code == -1 and b"\\x00\\x00\\x00" in str(e).encode():
            print("⚠️ 忽略 QQ 邮箱 SMTP 关闭阶段的非标准响应（邮件已成功发送）")
        else:
            raise HTTPException(500,"邮件发送失败")
    # 发送成功（或 QQ 邮箱误报）都视为已发出，验证码落库
    await email_code_repo.create(email, code)
    return ResponseOut()

@router.post("/register", response_model=ResponseOut)
async def register(
        data: RegisterIn,
        session: AsyncSession = Depends(get_session)
):
    # 判断邮箱是否存在/占用
    user_repo = UserRepository(session=session)
    email_exist = await user_repo.email_exists(email=str(data.email))
    if email_exist:
        raise HTTPException(400,detail="该邮箱已经存在")
    # 校验验证码是否正确
    email_code_repo = EmailCodeRepository(session=session)
    email_code_match = await email_code_repo.check_email_code(email=str(data.email), code=str(data.code))
    if not email_code_match:
        raise HTTPException(400,"邮箱或验证码错误!")
    try:
        await user_repo.create(UserCreateSchema(email=str(data.email), password=data.password, username=data.username))
    except SMTPResponseException as e:
        raise HTTPException(500,detail=str(e))
    return ResponseOut()


@router.post('/login', response_model=LoginOut)
async def login(
        data: LoginIn,
        session: AsyncSession = Depends(get_session)
):
    user_repo = UserRepository(session=session)
    user: User|None = await user_repo.get_by_email(str(data.email))
    if not user:
        raise HTTPException(400,"该用户不存在！")
    if not user.check_password(data.password):
        raise HTTPException(400,detail="邮箱或密码错误！")
    # 生成JWToken
    token = auth_handler.encode_login_token(user.id)
    return {
        "user": user,
        "token": token['access_token']
    }