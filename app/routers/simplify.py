from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import TextRequest, TextResponse

router = APIRouter(
    prefix="/simplify",
    tags=["simplify"]
)

@router.post("/", response_model=TextResponse)
async def simplify_text(request: Request, payload: TextRequest):
    task_input = f"simplify: {payload.text}"
    
    try:
        output = request.app.state.simplify_pipeline(
            task_input,
            max_length=259,
            truncation=True
        )
        if isinstance(output, list) and isinstance(output[0], dict):
            simplified = output[0]["generated_text"]
        else: 
            simplified = output[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simplification error: {e}")
    
    return TextResponse(result=simplified)