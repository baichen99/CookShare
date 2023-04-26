from fastapi import Depends, APIRouter
from auth.jwt_handler import sign_jwt, decode_jwt, TokenResponse
from auth.jwt_bearer import JWTBearer
from models.student import StudentLogin, StudentRegister, StudentUpdate, StudentQuery
from models.student import StudentResponse, StudentListResponse
from services.student import get_student_by_email, get_student_by_id, get_students, create_student, update_student
from services.student import Student
from middlewares.error_handler import JSONException
from passlib.context import CryptContext


jwt_bearer = JWTBearer()

hash_helper = CryptContext(schemes=["bcrypt"])

router = APIRouter()

@router.post("/login", tags=["Student"], description="Student login", response_model=TokenResponse)
async def login(form: StudentLogin):
    student = await get_student_by_email(form.email)
    if (not student) or (not hash_helper.verify(form.password, student.password)):
        raise JSONException(status_code=401, error_msg="Invalid credentials")
    token_rsp = sign_jwt(str(student.id), role='student')
    return token_rsp

@router.post("/register", tags=["Student"], description="Student register", response_model=StudentResponse)
async def register(form: StudentRegister):
    student = await get_student_by_email(form.email)
    if student:
        raise JSONException(status_code=400, error_msg="Email already exists")
    hashed_password = hash_helper.hash(form.password)
    student = Student(username=form.username, email=form.email, password=hashed_password)
    student = await create_student(student)
    return student

@router.get("/", tags=["Student"], description="Get all students")
async def list_students(query: StudentQuery, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    if decoded_token['role'] != 'admin':
        raise JSONException(status_code=401, error_msg="Unauthorized")
    students = await get_students(query)

    students = [student.to_dict() for student in students]
    return StudentListResponse(
        skip=query.skip+1,
        limit=query.limit,
        total=len(students),
        students=students
    )
    
@router.get('/{id}', tags=['Student'], description='Get student', response_model=StudentResponse)
async def get_student(id: str):
    student = await get_student_by_id(id)
    return student.to_dict()

@router.put("/{id}", tags=["Student"], description="Update student", response_model=StudentResponse)
async def update(id: str, form: StudentUpdate, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    if decoded_token['role'] != 'admin' and id != user_id:
        raise JSONException(status_code=401, error_msg="Unauthorized")
    student = await get_student_by_email(form.email)
    if student and str(student.id) != id:
        raise JSONException(status_code=400, error_msg="Email already exists")
    student = await update_student(id, form)
    return student.to_dict()
