from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(
    title="广应科智能校务与学业决策系统 - API",
    description="提供学业预警、综测算分与毕业资格诊断服务",
    version="1.0.0"
)

class StudentRiskRequest(BaseModel):
    student_id: str = Field(..., description="学生学号", example="202301001")
    name: str = Field(..., description="学生姓名", example="张三")
    failed_credits: float = Field(..., ge=0, description="累计不及格学分(必须>=0)", example=8.5)
    gpa: float = Field(..., ge=0.0, le=5.0, description="平均学分绩点(0.0-5.0)", example=1.8)
    

class RiskEvaluationResponse(BaseModel):
    student_id: str
    name: str
    failed_credits: float
    warning_level: str
    icon: str
    action_advice: str
    should_interview: bool = Field(..., description="是否需要辅导员面谈")
    degree_risk: bool = Field(..., description="是否存在 GPA 不达标导致的学位风险")

def evaluate_academic_risk(credits: float, gpa: float):
    if credits < 5:
        level, icon, advice, should_interview = "正常", "🟢", "学业状况良好，请继续保持。", False
    elif 5 <= credits < 10:
        level, icon, advice, should_interview = "黄色预警", "🟡", "触发口头警告，需建立学业辅导档案。", False
    elif 10 <= credits < 16:
        level, icon, advice, should_interview = "橙色预警", "🟠", "下发《学业预警通知书》，寄送/告知家长。", True
    else:
        level, icon, advice, should_interview = "红色预警", "🔴", "达到降级/退学审查红线，提交教务处处理。", True
    degree_risk = gpa < 2.0
    return level, icon, advice, should_interview, degree_risk

@app.post(
    "/api/v1/academic-risk/evaluate",
    response_model=RiskEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="学生学业风险综合评估接口"
)
async def evaluate_student_risk(request: StudentRiskRequest):
    level, icon, advice, should_interview, degree_risk = evaluate_academic_risk(
        request.failed_credits, request.gpa
    )
    return RiskEvaluationResponse(
        student_id=request.student_id,
        name=request.name,
        failed_credits=request.failed_credits,
        warning_level=level,
        icon=icon,
        action_advice=advice,
        should_interview=should_interview,
        degree_risk=degree_risk
    )
    
@app.get("/api/v1/health", summary="健康检查接口")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    