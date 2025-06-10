from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import TextRequest, TextResponse

router = APIRouter(
    prefix="/sentiment",
    tags=["sentiment"]   
)

@router.post("/", response_model=TextResponse)
async def sentiment_analysis(request: Request, payload: TextRequest):
    try:
        output = request.app.state.sentiment_pipeline(payload.text)
        
        result_item = output[0] if isinstance(output, list) else output
        label = result_item.get("label", "")
        score = result_item.get("score", 0.0)
        
        sentiment_str = f"{label} ({score:.4f})"
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis error: {e}")
    
    return TextResponse(result=sentiment_str)