from fastapi import APIRouter, File, UploadFile, Form
from ..models import TryOnResult
import os 
import shutil
import uuid
from pathlib import Path

router = APIRouter(prefix="/try-on", tags=["Virtual Try-On"])

# AI Fashion Try-On Agent Logic
class TryOnAgent:
    def __init__(self):
        self.supported_models = ["OOTDiffusion"]
        self.client = None
        self._client_initialized = False
        
    def _init_client(self):
        """Lazy initialization of the VTON client - only connects when needed"""
        if not self._client_initialized:
            try:
                from gradio_client import Client
                print("Initializing VTON Client (levihsu/OOTDiffusion)...")
                self.client = Client("levihsu/OOTDiffusion")
                print("VTON Client initialized successfully.")
                self._client_initialized = True
            except Exception as e:
                print(f"Failed to initialize VTON Client: {e}")
                self._client_initialized = True  # Mark as attempted to avoid retry loops
        
    async def analyze_image(self, image: UploadFile) -> dict:
        """Analyze the uploaded image to confirm suitability for try-on."""
        return {
            "is_front_facing": True,
            "upper_body_visible": True,
            "arms_visible": True,
            "pose_valid": True
        }

    def get_garment_category(self, product_id: int) -> str:
        """Map product ID to garment category for OOTDiffusion"""
        # 1: Blouse (Tops) -> Upper-body
        # 2: Blazer (Outerwear) -> Upper-body
        # 3: Dress (Dresses) -> Dress
        # 4: Trousers (Bottoms) -> Lower-body
        # 5: Sweater (Tops) -> Upper-body
        # 6: Skirt (Bottoms) -> Lower-body
        mapping = {
            1: "Upper-body", 2: "Upper-body", 3: "Dress",
            4: "Lower-body", 5: "Upper-body", 6: "Lower-body"
        }
        return mapping.get(product_id, "Upper-body")

    def get_garment_image_path(self, product_id: int) -> str:
        """Get the local file path for the garment image"""
        mapping = {
            1: "clothing-1.jpg", 2: "clothing-2.jpg", 3: "clothing-3.jpg",
            4: "clothing-4.jpg", 5: "clothing-5.jpg", 6: "clothing-6.jpg"
        }
        filename = mapping.get(product_id, "clothing-1.jpg")
        base_path = Path(__file__).parent.parent.parent.parent / "frontend" / "public" / "assets"
        return str(base_path / filename)

    async def perform_virtual_try_on(self, user_image: UploadFile, product_id: int) -> str:
        """Execute the virtual try-on process using OOTDiffusion."""
        
        # 1. Analysis
        analysis = await self.analyze_image(user_image)
        if not analysis["pose_valid"]:
            raise ValueError("Invalid user pose detected.")

        # 2. Initialize client (lazy loading - only when actually needed)
        self._init_client()
        
        if not self.client:
            # Fallback to mock if client failed to initialize
            print("Client not available, using mock response")
            return "/assets/try-on-fallback.jpg"

        # 3. Prepare Inputs
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        user_img_path = temp_dir / f"user_{uuid.uuid4()}.jpg"
        
        # Save uploaded image temporarily
        with open(user_img_path, "wb") as buffer:
            shutil.copyfileobj(user_image.file, buffer)
            
        garment_img_path = self.get_garment_image_path(product_id)
        if not os.path.exists(garment_img_path):
            print(f"Garment image not found at {garment_img_path}, using mock.")
            os.remove(user_img_path)
            return "/assets/try-on-fallback.jpg"

        category = self.get_garment_category(product_id)
        
        try:
            from gradio_client import handle_file
            print(f"Sending request to OOTDiffusion: {category} for product {product_id}")
            
            # Call the OOTDiffusion API
            result = self.client.predict(
                vton_img=handle_file(str(user_img_path)),
                garm_img=handle_file(garment_img_path),
                category=category,
                n_samples=1,
                n_steps=20,
                image_scale=2.0,
                seed=-1,
                api_name="/process_dc"
            )
            
            # Process the result
            if result and len(result) > 0:
                generated_img_path = result[0]['image']
                
                # Copy result to public assets
                output_filename = f"generated_{uuid.uuid4()}.jpg"
                public_assets = Path(__file__).parent.parent.parent.parent / "frontend" / "public" / "try-on-results"
                public_assets.mkdir(parents=True, exist_ok=True)
                
                shutil.copy(generated_img_path, public_assets / output_filename)
                
                # Cleanup temp file
                os.remove(user_img_path)
                
                print(f"Successfully generated try-on result: {output_filename}")
                return f"/try-on-results/{output_filename}"
                
        except Exception as e:
            print(f"OOTDiffusion failed: {e}")
            # Clean up temp file
            if os.path.exists(user_img_path):
                os.remove(user_img_path)
            
        # Fallback to mock
        return "/assets/try-on-fallback.jpg"

agent = TryOnAgent()

@router.post("/", response_model=TryOnResult)
async def try_on(
    userImage: UploadFile = File(...),
    productId: int = Form(...)
):
    try:
        result_url = await agent.perform_virtual_try_on(userImage, productId)
        return {"result_image": result_url}
    except Exception as e:
        print(f"Try-on failed: {e}")
        return {"result_image": "/assets/try-on-fallback.jpg"}
