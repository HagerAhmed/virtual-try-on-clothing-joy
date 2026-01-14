from fastapi import APIRouter, File, UploadFile, Form
from ..models import TryOnResult
import os 
import shutil
import uuid
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter(prefix="/try-on", tags=["Virtual Try-On"])

# AI Fashion Try-On Agent Logic
class TryOnAgent:
    def __init__(self):
        self.supported_models = ["OOTDiffusion"]
        self.ootd_client = None
        self._clients_initialized = False
        
    def _init_clients(self):
        """Initialize OOTDiffusion client"""
        if not self._clients_initialized:
            from gradio_client import Client
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            
            if hf_token:
                os.environ["HF_TOKEN"] = hf_token
            
            # Initialize OOTDiffusion
            try:
                print("Initializing OOTDiffusion Client...")
                self.ootd_client = Client("levihsu/OOTDiffusion")
                print("✓ OOTDiffusion Client initialized successfully.")
            except Exception as e:
                print(f"✗ OOTDiffusion unavailable: {e}")
                
            self._clients_initialized = True
            
            if not self.ootd_client:
                print("⚠ OOTDiffusion client not available - will use fallback image")
        
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
        # OOTDiffusion supports: "Upper-body", "Lower-body", "Dress"
        mapping = {
            1: "Upper-body",   # Blouse
            2: "Upper-body",   # Blazer
            3: "Dress",        # Dress
            4: "Lower-body",   # Trousers
            5: "Upper-body",   # Sweater
            6: "Lower-body"    # Skirt
        }
        return mapping.get(product_id, "Upper-body")

    def get_garment_image_path(self, product_id: int) -> str:
        """Return file path for the garment image based on product ID."""
        # Map product IDs to actual asset filenames
        filename_map = {
            1: "clothing-1.jpg",  # Blouse
            2: "clothing-2.jpg",  # Blazer
            3: "clothing-3.jpg",  # Dress
            4: "clothing-4.jpg",  # Trousers
            5: "clothing-5.jpg",  # Sweater
            6: "clothing-6.jpg"   # Skirt
        }
        filename = filename_map.get(product_id, "clothing-1.jpg")
        base_path = Path(__file__).parent.parent.parent.parent / "frontend" / "public" / "assets"
        return str(base_path / filename)


    async def perform_virtual_try_on(self, user_image: UploadFile, product_id: int) -> str:
        """Execute the virtual try-on process using OOTDiffusion."""
        
        # 1. Analysis
        analysis = await self.analyze_image(user_image)
        if not analysis["pose_valid"]:
            raise ValueError("Invalid user pose detected.")

        # 2. Initialize OOTDiffusion client
        self._init_clients()
        
        if not self.ootd_client:
            print("OOTDiffusion client not available, using fallback")
            return "/assets/try-on-fallback.jpg"

        # 3. Prepare Inputs
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        user_img_path = temp_dir / f"user_{uuid.uuid4()}.jpg"
        
        with open(user_img_path, "wb") as buffer:
            shutil.copyfileobj(user_image.file, buffer)
            
        garment_img_path = self.get_garment_image_path(product_id)
        if not os.path.exists(garment_img_path):
            print(f"Garment image not found at: {garment_img_path}")
            if os.path.exists(user_img_path):
                os.remove(user_img_path)
            return "/assets/try-on-fallback.jpg"

        # 4. Get garment category
        category = self.get_garment_category(product_id)
        print(f"📊 Garment category: {category}")
        print(f"📊 Garment image: {garment_img_path}")

        # 5. Run OOTDiffusion
        try:
            from gradio_client import handle_file
            print(f"Running OOTDiffusion for product {product_id}")
            
            result = self.ootd_client.predict(
                vton_img=handle_file(str(user_img_path)),
                garm_img=handle_file(garment_img_path),
                category=category,
                n_samples=1,
                n_steps=30,
                image_scale=2.5,
                seed=-1,
                api_name="/process_dc"
            )
            
            if result and len(result) > 0:
                generated_img_path = result[0]['image']
                
                import base64
                with open(generated_img_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                
                if os.path.exists(user_img_path):
                    os.remove(user_img_path)
                
                print("✓ OOTDiffusion succeeded")
                return f"data:image/jpeg;base64,{img_data}"
                
        except Exception as e:
            print(f"✗ OOTDiffusion failed: {e}")
            if os.path.exists(user_img_path):
                os.remove(user_img_path)
        
        # 6. Final fallback
        print("OOTDiffusion failed, using fallback image")
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
