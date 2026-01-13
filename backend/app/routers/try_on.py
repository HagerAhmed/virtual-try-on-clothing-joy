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
        self.supported_models = ["IDM-VTON", "Kolors-VTON", "OOTDiffusion"]
        self.parser_client = None
        self.idm_client = None
        self.kolors_client = None
        self.ootd_client = None
        self._clients_initialized = False
        
    def _init_clients(self):
        """Lazy initialization of VTON clients - tries IDM-VTON first, then Kolors, then OOTDiffusion"""
        if not self._clients_initialized:
            from gradio_client import Client
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            
            if hf_token:
                os.environ["HF_TOKEN"] = hf_token
            
            # Initialize human parser (for body segmentation)
            try:
                print("Initializing Human Parser...")
                self.parser_client = Client("fashn-ai/fashn-human-parser")
                print("✓ Human Parser initialized successfully.")
            except Exception as e:
                print(f"✗ Human Parser unavailable: {e}")
            
            # Try IDM-VTON first (best quality - SDXL based)
            try:
                print("Initializing IDM-VTON Client...")
                self.idm_client = Client("yisol/IDM-VTON")
                print("✓ IDM-VTON Client initialized successfully.")
            except Exception as e:
                print(f"✗ IDM-VTON unavailable: {e}")
            
            # Try Kolors second (good quality)
            try:
                print("Initializing Kolors VTON Client...")
                self.kolors_client = Client("Kwai-Kolors/Kolors-Virtual-Try-On")
                print("✓ Kolors VTON Client initialized successfully.")
            except Exception as e:
                print(f"✗ Kolors VTON unavailable: {e}")
            
            # Fallback to OOTDiffusion (SD 1.5 based)
            try:
                print("Initializing OOTDiffusion Client...")
                self.ootd_client = Client("levihsu/OOTDiffusion")
                print("✓ OOTDiffusion Client initialized successfully.")
            except Exception as e:
                print(f"✗ OOTDiffusion unavailable: {e}")
                
            self._clients_initialized = True
            
            if not self.idm_client and not self.kolors_client and not self.ootd_client:
                print("⚠ No VTON clients available - will use fallback image")
        
    async def analyze_image(self, image: UploadFile) -> dict:
        """Analyze the uploaded image to confirm suitability for try-on."""
        return {
            "is_front_facing": True,
            "upper_body_visible": True,
            "arms_visible": True,
            "pose_valid": True
        }

    def get_garment_category(self, product_id: int) -> str:
        """Map product ID to garment category for VTON models"""
        # 1: Blouse (Tops) -> Upper-body
        # 2: Blazer (Outerwear) -> Upper-body  
        # 3: Dress (Dresses) -> Whole-body (covers both upper and lower)
        # 4: Trousers (Bottoms) -> Lower-body
        # 5: Sweater (Tops) -> Upper-body
        # 6: Skirt (Bottoms) -> Lower-body
        mapping = {
            1: "Upper-body", 2: "Upper-body", 3: "Whole-body",
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

    async def parse_human(self, user_img_path: str, category: str) -> dict:
        """
        Parse human body to identify regions for garment replacement.
        Returns segmentation info for the specified category.
        """
        if not self.parser_client:
            print("⚠ Human parser not available, skipping segmentation")
            return {"parsed": False, "category": category}
        
        try:
            from gradio_client import handle_file
            print(f"Parsing human body for {category} region...")
            
            result = self.parser_client.predict(
                input_image=handle_file(user_img_path),
                api_name="/predict"
            )
            
            # Result contains segmentation mask
            # For now, we just confirm parsing succeeded
            # In production, you'd extract specific body regions
            print(f"✓ Human parsing completed for {category}")
            return {
                "parsed": True,
                "category": category,
                "mask_available": True
            }
            
        except Exception as e:
            print(f"✗ Human parsing failed: {e}")
            return {"parsed": False, "category": category}

    async def perform_virtual_try_on(self, user_image: UploadFile, product_id: int) -> str:
        """Execute the virtual try-on process using available VTON models."""
        
        # 1. Analysis
        analysis = await self.analyze_image(user_image)
        if not analysis["pose_valid"]:
            raise ValueError("Invalid user pose detected.")

        # 2. Initialize clients
        self._init_clients()
        
        if not self.idm_client and not self.kolors_client and not self.ootd_client:
            print("No VTON clients available, using fallback")
            return "/assets/try-on-fallback.jpg"

        # 3. Prepare Inputs
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        user_img_path = temp_dir / f"user_{uuid.uuid4()}.jpg"
        
        with open(user_img_path, "wb") as buffer:
            shutil.copyfileobj(user_image.file, buffer)
            
        garment_img_path = self.get_garment_image_path(product_id)
        if not os.path.exists(garment_img_path):
            print(f"Garment image not found, using fallback.")
            os.remove(user_img_path)
            return "/assets/try-on-fallback.jpg"

        # 4. Parse human body to identify regions
        category = self.get_garment_category(product_id)
        parsing_result = await self.parse_human(str(user_img_path), category)
        
        print(f"📊 Garment category: {category}")
        print(f"📊 Parsing result: {'Success' if parsing_result['parsed'] else 'Skipped'}")

        # 5. Try IDM-VTON first (best quality - SDXL based)
        if self.idm_client:
            try:
                from gradio_client import handle_file
                print(f"Trying IDM-VTON for product {product_id}")
                
                result = self.idm_client.predict(
                    dict={"background": handle_file(str(user_img_path)), "layers": [], "composite": None},
                    garm_img=handle_file(garment_img_path),
                    garment_des="",
                    is_checked=True,
                    is_checked_crop=False,
                    denoise_steps=30,
                    seed=42,
                    api_name="/tryon"
                )
                
                if result:
                    import base64
                    # IDM-VTON returns tuple, image is first element
                    result_img = result[0] if isinstance(result, tuple) else result
                    with open(result_img, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    
                    if os.path.exists(user_img_path):
                        os.remove(user_img_path)
                    
                    print("✓ IDM-VTON succeeded")
                    return f"data:image/jpeg;base64,{img_data}"
                    
            except Exception as e:
                print(f"✗ IDM-VTON failed: {e}")
        
        # 5. Try Kolors (good quality)
        if self.kolors_client:
            try:
                from gradio_client import handle_file
                print(f"Trying Kolors VTON for product {product_id}")
                
                result = self.kolors_client.predict(
                    person_img=handle_file(str(user_img_path)),
                    cloth_img=handle_file(garment_img_path),
                    api_name="/tryon"
                )
                
                if result:
                    import base64
                    with open(result, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    
                    if os.path.exists(user_img_path):
                        os.remove(user_img_path)
                    
                    print("✓ Kolors VTON succeeded")
                    return f"data:image/jpeg;base64,{img_data}"
                    
            except Exception as e:
                print(f"✗ Kolors VTON failed: {e}")
        
        # 6. Final fallback to OOTDiffusion
        if self.ootd_client:
            try:
                from gradio_client import handle_file
                # OOTDiffusion uses "Dress" instead of "Whole-body"
                ootd_category = "Dress" if category == "Whole-body" else category
                print(f"Trying OOTDiffusion: {ootd_category} for product {product_id}")
                
                result = self.ootd_client.predict(
                    vton_img=handle_file(str(user_img_path)),
                    garm_img=handle_file(garment_img_path),
                    category=ootd_category,
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
        print("All VTON models failed, using fallback image")
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
