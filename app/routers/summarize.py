from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import TextRequest, TextResponse

router = APIRouter(
    prefix="/summarize",
    tags=["summarize"]
)

@router.post("/", response_model=TextResponse)
async def summarize_text(request: Request, payload: TextRequest):
    try:
        output = request.app.state.summarize_pipeline(
            payload.text,
            max_length=259,
            min_length=40,
            length_penalty=2.0,
            do_sample=False
        )
        
        summary = (
            output[0].get("summary_text")
            or output[0].get("generated_text", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization error: {e}")
    
    return TextResponse(result=summary)