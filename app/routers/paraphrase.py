from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import TextRequest, TextResponse

router = APIRouter(
    prefix="/paraphrase",
    tags=["paraphrase"]
)

@router.post("/", response_model=TextResponse)
async def paraphrase_text(request: Request, payload: TextRequest):
    task_input = f"paraphrase: {payload.text}"
    
    try:
        output = request.app.state.paraphrase_pipeline(
            task_input,
            do_sample=True,
            top_k=120,
            top_p=0.95,
            temperature=0.9,
            num_return_sequences=1
        )
        
        paraphrased = (
            output[0]["generated_text"]
            if isinstance(output, list) and isinstance(output[0], dict)
            else output[0]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Paraphrase pipeline error: {e}" )
    
    return TextResponse(result=paraphrased)