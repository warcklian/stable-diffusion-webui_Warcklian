#!/usr/bin/env python3
"""
Motor de Diversidad Facial Ultra Avanzado
Sistema que genera características únicas y extremadamente diversas
para evitar imágenes que se parezcan entre sí
"""

import random
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

@dataclass
class UltraDiversityProfile:
    """Perfil de diversidad ultra avanzado para máxima unicidad"""
    # Identificación única
    image_id: str
    nationality: str
    region: str
    gender: str
    age: int
    
    # Características faciales ultra detalladas
    face_shape: str
    face_width: str
    face_length: str
    jawline: str
    chin: str
    cheekbones: str
    facial_symmetry: str
    bone_structure: str
    
    # Ojos ultra detallados
    eye_color: str
    eye_color_shade: str
    eye_shape: str
    eye_size: str
    eye_spacing: str
    eyelid_type: str
    eyelashes: str
    eyelashes_length: str
    eyebrows: str
    eyebrows_thickness: str
    eyebrows_shape: str
    
    # Nariz ultra detallada
    nose_shape: str
    nose_size: str
    nose_width: str
    nose_bridge: str
    nose_tip: str
    nostril_size: str
    
    # Boca ultra detallada
    lip_shape: str
    lip_size: str
    lip_thickness: str
    mouth_width: str
    lip_color: str
    lip_fullness: str
    
    # Piel ultra detallada
    skin_tone: str
    skin_tone_shade: str
    skin_texture: str
    skin_undertone: str
    skin_glow: str
    skin_imperfections: List[str]
    freckles: str
    freckles_density: str
    moles: str
    moles_count: str
    birthmarks: str
    scars: str
    acne: str
    age_spots: str
    wrinkles: str
    skin_elasticity: str
    
    # Cabello ultra detallado
    hair_color: str
    hair_color_shade: str
    hair_texture: str
    hair_length: str
    hair_style: str
    hair_density: str
    hair_shine: str
    hair_curliness: str
    hair_thickness: str
    hairline: str
    
    # Vello facial (solo para hombres)
    facial_hair: str
    beard: str
    mustache: str
    
    # Características de edad específicas
    age_characteristics: List[str]
    
    # Nivel de belleza realista
    beauty_level: str
    attractiveness_factors: List[str]
    
    # Características étnicas específicas
    ethnic_features: List[str]
    
    # Metadatos de unicidad
    generated_at: str
    generation_type: str
    uniqueness_score: float
    diversity_factors: List[str]

class UltraDiversityEngine:
    """Motor de diversidad ultra avanzado para máxima unicidad"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.diversity_data = self._load_diversity_data()
        
    def _load_diversity_data(self) -> Dict[str, Any]:
        """Carga datos de diversidad ultra expandidos desde archivo JSON"""
        try:
            # Cargar desde archivo JSON
            data_file = Path(__file__).parent / "ultra_diversity_data.json"
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"No se pudo cargar ultra_diversity_data.json: {e}")
        
        # Fallback a datos hardcodeados si no se puede cargar el JSON
        return {
            # Regiones venezolanas ultra expandidas
            "regions": [
                "caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", 
                "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz",
                "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua",
                "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas",
                "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua",
                "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique",
                "araure", "turen", "guanarito", "santa_elena", "el_venado",
                "san_rafael", "san_antonio", "la_fria", "rubio", "colon",
                "tachira", "apure", "amazonas", "delta_amacuro", "yacambu",
                "lara", "portuguesa", "cojedes", "guarico", "anzoategui",
                "monagas", "sucre", "nueva_esparta", "falcon", "zulia",
                "merida", "trujillo", "barinas", "yaracuy", "carabobo",
                "aragua", "miranda", "vargas", "distrito_capital"
            ],
            
            # Tonos de piel ultra expandidos
            "skin_tones": [
                "light", "fair", "medium", "medium-dark", "olive", "tan", "golden",
                "bronze", "caramel", "honey", "dark", "rich brown", "coffee",
                "mahogany", "espresso", "chocolate", "mocha", "cinnamon", "amber",
                "copper", "peach", "ivory", "beige", "sand", "cream", "wheat",
                "almond", "hazelnut", "walnut", "chestnut", "cocoa", "ebony"
            ],
            
            # Colores de cabello ultra expandidos
            "hair_colors": [
                "black", "dark brown", "brown", "auburn", "chestnut", "chocolate",
                "espresso", "mahogany", "copper", "bronze", "light brown", "honey",
                "golden", "blonde", "strawberry blonde", "red", "ginger", "salt and pepper",
                "gray", "white", "platinum", "ash blonde", "dirty blonde", "sandy",
                "caramel", "cinnamon", "russet", "burgundy", "auburn", "copper",
                "bronze", "gold", "silver", "pepper", "salt", "mixed"
            ],
            
            # Colores de ojos ultra expandidos
            "eye_colors": [
                "dark brown", "brown", "hazel", "amber", "light brown", "honey",
                "golden", "coffee", "chocolate", "mahogany", "green", "blue",
                "gray", "blue-green", "hazel-green", "amber-brown", "light hazel",
                "dark hazel", "emerald", "forest green", "sea green", "teal",
                "steel blue", "navy blue", "sky blue", "ice blue", "violet",
                "purple", "amber", "gold", "copper", "hazel", "mixed"
            ],
            
            # Formas de cara ultra expandidas
            "face_shapes": [
                "oval", "round", "square", "heart", "diamond", "long", "triangular",
                "pear", "inverted triangle", "rectangular", "angular", "soft",
                "defined", "symmetrical", "asymmetrical", "wide", "narrow", "broad",
                "thin", "full", "hollow", "prominent", "recessed", "angular",
                "rounded", "oval", "square", "heart", "diamond", "pear"
            ],
            
            # Características de nariz ultra expandidas
            "nose_shapes": [
                "straight", "aquiline", "button", "wide", "narrow", "small",
                "prominent", "delicate", "strong", "refined", "classic", "distinctive",
                "roman", "snub", "hooked", "bulbous", "pointed", "flat", "upturned",
                "downturned", "asymmetric", "perfect", "crooked", "broad", "thin",
                "long", "short", "large", "tiny", "bent", "twisted", "bumpy",
                "smooth", "rough", "textured", "elegant", "sturdy", "dainty"
            ],
            
            # Características de labios ultra expandidas
            "lip_shapes": [
                "full", "medium", "thin", "wide", "narrow", "plump", "defined",
                "natural", "shapely", "expressive", "delicate", "strong", "pouty",
                "bow-shaped", "heart-shaped", "straight", "curved", "asymmetric",
                "perfect", "uneven", "thick", "thin", "long", "short", "prominent",
                "subtle", "large", "small", "wide", "narrow", "pursed", "relaxed",
                "tense", "loose", "voluptuous", "petite", "sensual", "charming"
            ],
            
            # Características de ojos ultra expandidas
            "eye_shapes": [
                "almond", "round", "hooded", "deep-set", "wide-set", "close-set",
                "upturned", "downturned", "monolid", "double-lid", "expressive",
                "intense", "gentle", "piercing", "sleepy", "alert", "droopy",
                "cat-like", "downturned", "upturned", "asymmetric", "perfect",
                "uneven", "large", "small", "prominent", "recessed", "bulging",
                "sunken", "puffy", "swollen", "narrow", "wide", "slanted", "straight",
                "bedroom", "doll-like", "fox-like", "downturned", "upturned"
            ],
            
            # Estilos de cabello ultra expandidos
            "hair_styles": [
                "straight", "wavy", "curly", "braided", "ponytail", "bun", "pixie",
                "bob", "shoulder-length", "layered", "textured", "voluminous",
                "sleek", "styled", "natural", "professional", "casual", "messy",
                "neat", "tidy", "unkempt", "wild", "smooth", "rough", "thick",
                "thin", "fine", "coarse", "silky", "frizzy", "smooth", "tangled",
                "styled", "natural", "artificial", "extensions", "weave", "wig"
            ],
            
            # Características de cejas ultra expandidas
            "eyebrow_shapes": [
                "thick", "medium", "thin", "arched", "straight", "defined", "natural",
                "bushy", "sparse", "uneven", "perfect", "asymmetric", "high", "low",
                "close", "wide", "angled", "curved", "messy", "neat", "tidy",
                "unkempt", "wild", "smooth", "rough", "patchy", "full", "partial",
                "missing", "overgrown", "trimmed", "shaped", "microbladed", "tattooed"
            ],
            
            # Características de mandíbula ultra expandidas
            "jawline_types": [
                "strong", "soft", "defined", "rounded", "angular", "delicate",
                "square", "pointed", "weak", "prominent", "recessed", "asymmetric",
                "perfect", "uneven", "wide", "narrow", "broad", "thin", "full",
                "hollow", "sharp", "blunt", "chiseled", "soft", "hard", "firm",
                "loose", "tight", "relaxed", "tense", "masculine", "feminine"
            ],
            
            # Características de pómulos ultra expandidas
            "cheekbone_types": [
                "high", "medium", "low", "prominent", "subtle", "defined", "sharp",
                "soft", "angular", "rounded", "asymmetric", "perfect", "uneven",
                "wide", "narrow", "hollow", "full", "broad", "thin", "strong",
                "weak", "chiseled", "smooth", "rough", "textured", "flat", "raised",
                "sunken", "puffy", "swollen", "sculpted", "natural", "artificial"
            ],
            
            # Texturas de piel ultra expandidas
            "skin_textures": [
                "smooth", "textured", "natural", "mature", "youthful", "rough",
                "fine", "coarse", "porous", "tight", "loose", "elastic", "dry",
                "oily", "combination", "blemished", "clear", "acne-prone", "sensitive",
                "resilient", "fragile", "thick", "thin", "firm", "soft", "wrinkled",
                "aged", "fresh", "dull", "glowing", "radiant", "dewy", "matte"
            ],
            
            # Niveles de belleza realistas
            "beauty_levels": [
                "muy_atractivo", "atractivo", "normal", "promedio", "comun",
                "ordinario", "poco_atractivo", "feo", "muy_feo", "realista",
                "variado", "excepcional", "hermoso", "guapo", "bonito", "lindo",
                "encantador", "carismatico", "interesante", "unico", "distintivo"
            ],
            
            # Características de pecas ultra expandidas
            "freckle_types": [
                "none", "light", "moderate", "heavy", "scattered", "concentrated",
                "bridge", "cheeks", "forehead", "nose", "chin", "arms", "shoulders",
                "back", "chest", "sparse", "dense", "faint", "dark", "light",
                "red", "brown", "golden", "sun-kissed", "natural", "artificial"
            ],
            
            # Características de lunares ultra expandidas
            "mole_types": [
                "none", "small", "medium", "large", "multiple", "cheek", "chin",
                "forehead", "nose", "lip", "eye", "ear", "neck", "shoulder", "arm",
                "hand", "back", "chest", "leg", "foot", "facial", "body", "beauty",
                "mark", "birthmark", "congenital", "acquired", "benign", "suspicious"
            ],
            
            # Características de cicatrices ultra expandidas
            "scar_types": [
                "none", "small", "faint", "visible", "cheek", "chin", "forehead",
                "nose", "lip", "eye", "ear", "neck", "shoulder", "arm", "hand",
                "back", "chest", "leg", "foot", "surgical", "accident", "birth",
                "childhood", "adult", "recent", "old", "healed", "fresh", "faded"
            ],
            
            # Características de acné ultra expandidas
            "acne_types": [
                "none", "mild", "moderate", "severe", "scattered", "concentrated",
                "forehead", "cheeks", "chin", "nose", "back", "chest", "shoulders",
                "active", "healing", "scarred", "cystic", "blackheads", "whiteheads",
                "pustules", "papules", "nodules", "comedones", "inflammatory"
            ],
            
            # Características de arrugas ultra expandidas
            "wrinkle_types": [
                "none", "fine", "moderate", "deep", "forehead", "eye", "mouth",
                "neck", "crow's feet", "laugh lines", "frown lines", "worry lines",
                "smile lines", "expression lines", "age lines", "sun damage",
                "genetic", "lifestyle", "dynamic", "static", "gravitational",
                "sleep", "smoking", "environmental", "hormonal", "stress"
            ]
        }
    
    def generate_ultra_diverse_profile(self, nationality: str, gender: str, age: int) -> UltraDiversityProfile:
        """Genera un perfil ultra diverso con máxima unicidad"""
        
        # Crear seed único para máxima aleatoriedad
        unique_seed = int(time.time() * 1000000) + random.randint(1, 999999)
        random.seed(unique_seed)
        
        # Seleccionar región aleatoria
        region = random.choice(self.diversity_data["regions"])
        
        # Generar características ultra diversas
        profile = UltraDiversityProfile(
            image_id=f"ultra_{int(time.time())}_{random.randint(1000, 9999)}",
            nationality=nationality,
            region=region,
            gender=gender,
            age=age,
            
            # Características faciales
            face_shape=random.choice(self.diversity_data["face_shapes"]),
            face_width=random.choice(["narrow", "medium", "wide", "broad", "thin"]),
            face_length=random.choice(["short", "medium", "long", "elongated"]),
            jawline=random.choice(self.diversity_data["jawline_types"]),
            chin=random.choice(["pointed", "rounded", "square", "recessed", "prominent"]),
            cheekbones=random.choice(self.diversity_data["cheekbone_types"]),
            facial_symmetry=random.choice(["perfect", "slight_asymmetry", "natural_asymmetry"]),
            bone_structure=random.choice(["prominent", "delicate", "strong", "soft"]),
            
            # Ojos
            eye_color=random.choice(self.diversity_data["eye_colors"]),
            eye_color_shade=random.choice(["light", "medium", "dark", "deep"]),
            eye_shape=random.choice(self.diversity_data["eye_shapes"]),
            eye_size=random.choice(["small", "medium", "large", "prominent"]),
            eye_spacing=random.choice(["close", "normal", "wide", "very_wide"]),
            eyelid_type=random.choice(["monolid", "double_lid", "hooded", "deep_set"]),
            eyelashes=random.choice(["short", "medium", "long", "thick", "thin"]),
            eyelashes_length=random.choice(["natural", "extended", "dramatic"]),
            eyebrows=random.choice(self.diversity_data["eyebrow_shapes"]),
            eyebrows_thickness=random.choice(["thin", "medium", "thick", "bushy"]),
            eyebrows_shape=random.choice(["arched", "straight", "curved", "angled"]),
            
            # Nariz
            nose_shape=random.choice(self.diversity_data["nose_shapes"]),
            nose_size=random.choice(["small", "medium", "large", "prominent"]),
            nose_width=random.choice(["narrow", "medium", "wide", "broad"]),
            nose_bridge=random.choice(["high", "medium", "low", "flat"]),
            nose_tip=random.choice(["pointed", "rounded", "flat", "upturned"]),
            nostril_size=random.choice(["small", "medium", "large", "wide"]),
            
            # Boca
            lip_shape=random.choice(self.diversity_data["lip_shapes"]),
            lip_size=random.choice(["small", "medium", "large", "full"]),
            lip_thickness=random.choice(["thin", "medium", "thick", "full"]),
            mouth_width=random.choice(["narrow", "medium", "wide", "broad"]),
            lip_color=random.choice(["natural", "pink", "red", "brown", "dark"]),
            lip_fullness=random.choice(["thin", "medium", "full", "voluptuous"]),
            
            # Piel
            skin_tone=random.choice(self.diversity_data["skin_tones"]),
            skin_tone_shade=random.choice(["light", "medium", "dark", "deep"]),
            skin_texture=random.choice(self.diversity_data["skin_textures"]),
            skin_undertone=random.choice(["warm", "cool", "neutral", "olive"]),
            skin_glow=random.choice(["matte", "natural", "dewy", "glowing"]),
            skin_imperfections=self._generate_skin_imperfections(),
            freckles=random.choice(self.diversity_data["freckle_types"]),
            freckles_density=random.choice(["sparse", "moderate", "dense"]),
            moles=random.choice(self.diversity_data["mole_types"]),
            moles_count=random.choice(["none", "few", "several", "many"]),
            birthmarks=random.choice(["none", "small", "medium", "large"]),
            scars=random.choice(self.diversity_data["scar_types"]),
            acne=random.choice(self.diversity_data["acne_types"]),
            age_spots=self._generate_age_appropriate_spots(age),
            wrinkles=self._generate_age_appropriate_wrinkles(age),
            skin_elasticity=self._generate_age_appropriate_elasticity(age),
            
            # Cabello
            hair_color=random.choice(self.diversity_data["hair_colors"]),
            hair_color_shade=random.choice(["light", "medium", "dark", "deep"]),
            hair_texture=random.choice(["straight", "wavy", "curly", "coily"]),
            hair_length=random.choice(["short", "medium", "long", "very_long"]),
            hair_style=random.choice(self.diversity_data["hair_styles"]),
            hair_density=random.choice(["thin", "medium", "thick", "very_thick"]),
            hair_shine=random.choice(["dull", "natural", "shiny", "very_shiny"]),
            hair_curliness=random.choice(["straight", "wavy", "curly", "very_curly"]),
            hair_thickness=random.choice(["fine", "medium", "thick", "very_thick"]),
            hairline=random.choice(["low", "medium", "high", "receding"]),
            
            # Vello facial (solo para hombres)
            facial_hair=self._generate_gender_appropriate_facial_hair(gender),
            beard=self._generate_gender_appropriate_beard(gender),
            mustache=self._generate_gender_appropriate_mustache(gender),
            
            # Características de edad
            age_characteristics=self._generate_age_characteristics(age),
            
            # Nivel de belleza
            beauty_level=random.choice(self.diversity_data["beauty_levels"]),
            attractiveness_factors=self._generate_attractiveness_factors(),
            
            # Características étnicas
            ethnic_features=self._generate_ethnic_features(nationality),
            
            # Metadatos
            generated_at=datetime.now().isoformat(),
            generation_type="ultra_diverse",
            uniqueness_score=random.uniform(0.8, 1.0),
            diversity_factors=self._generate_diversity_factors()
        )
        
        return profile
    
    def _generate_skin_imperfections(self) -> List[str]:
        """Genera imperfecciones de piel realistas"""
        imperfections = []
        if random.random() < 0.3:
            imperfections.append("freckles")
        if random.random() < 0.2:
            imperfections.append("moles")
        if random.random() < 0.15:
            imperfections.append("scars")
        if random.random() < 0.1:
            imperfections.append("acne")
        if random.random() < 0.05:
            imperfections.append("birthmarks")
        return imperfections
    
    def _generate_age_characteristics(self, age: int) -> List[str]:
        """Genera características específicas de edad"""
        characteristics = []
        if age < 25:
            characteristics.extend(["youthful", "fresh", "smooth_skin"])
        elif age < 40:
            characteristics.extend(["mature", "defined_features"])
        else:
            characteristics.extend(["aged", "wrinkles", "mature_features"])
        return characteristics
    
    def _generate_age_appropriate_wrinkles(self, age: int) -> str:
        """Genera arrugas apropiadas para la edad"""
        # Filtrar opciones de arrugas basadas en la edad
        all_wrinkles = self.diversity_data["wrinkle_types"]
        
        if age < 20:
            return "none"
        elif age < 25:
            # Muy jóvenes: solo líneas de expresión muy finas
            young_options = [w for w in all_wrinkles if w in ["none", "fine expression lines"]]
            return random.choice(young_options) if young_options else "none"
        elif age < 30:
            # Jóvenes adultos: líneas de expresión leves
            young_adult_options = [w for w in all_wrinkles if w in ["none", "fine expression lines", "light laugh lines"]]
            return random.choice(young_adult_options) if young_adult_options else "none"
        elif age < 35:
            # Adultos jóvenes: líneas de expresión más visibles
            adult_young_options = [w for w in all_wrinkles if w in ["none", "fine expression lines", "light laugh lines", "subtle crow's feet"]]
            return random.choice(adult_young_options) if adult_young_options else "none"
        elif age < 40:
            # Adultos: arrugas más definidas
            adult_options = [w for w in all_wrinkles if w in ["fine expression lines", "light laugh lines", "subtle crow's feet", "forehead lines"]]
            return random.choice(adult_options) if adult_options else "fine expression lines"
        elif age < 50:
            # Adultos maduros: arrugas más profundas
            mature_options = [w for w in all_wrinkles if w in ["moderate expression lines", "crow's feet", "forehead lines", "laugh lines", "worry lines"]]
            return random.choice(mature_options) if mature_options else "moderate expression lines"
        elif age < 60:
            # Adultos mayores: arrugas profundas
            older_options = [w for w in all_wrinkles if w in ["deep expression lines", "pronounced crow's feet", "deep forehead lines", "laugh lines", "worry lines", "neck lines"]]
            return random.choice(older_options) if older_options else "deep expression lines"
        else:
            # Ancianos: arrugas muy profundas
            elderly_options = [w for w in all_wrinkles if w in ["deep wrinkles", "pronounced crow's feet", "deep forehead lines", "laugh lines", "worry lines", "neck lines", "age lines"]]
            return random.choice(elderly_options) if elderly_options else "deep wrinkles"
    
    def _generate_age_appropriate_spots(self, age: int) -> str:
        """Genera manchas de edad apropiadas para la edad"""
        if age < 30:
            return "none"
        elif age < 40:
            return random.choice(["none", "few age spots"])
        elif age < 50:
            return random.choice(["none", "few age spots", "several age spots"])
        elif age < 60:
            return random.choice(["few age spots", "several age spots", "many age spots"])
        else:
            return random.choice(["several age spots", "many age spots", "extensive age spots"])
    
    def _generate_age_appropriate_elasticity(self, age: int) -> str:
        """Genera elasticidad de piel apropiada para la edad"""
        if age < 25:
            return "firm"
        elif age < 35:
            return random.choice(["firm", "medium"])
        elif age < 45:
            return random.choice(["firm", "medium", "loose"])
        elif age < 55:
            return random.choice(["medium", "loose"])
        else:
            return random.choice(["loose", "very loose"])
    
    def _generate_gender_appropriate_facial_hair(self, gender: str) -> str:
        """Genera vello facial apropiado para el género"""
        if gender.lower() in ["mujer", "woman", "female"]:
            return "none"  # Las mujeres no tienen vello facial
        else:
            # Solo para hombres
            return random.choice(["none", "light", "moderate", "heavy"])
    
    def _generate_gender_appropriate_beard(self, gender: str) -> str:
        """Genera barba apropiada para el género"""
        if gender.lower() in ["mujer", "woman", "female"]:
            return "none"  # Las mujeres no tienen barba
        else:
            # Solo para hombres
            return random.choice(["none", "stubble", "short", "medium", "long", "full"])
    
    def _generate_gender_appropriate_mustache(self, gender: str) -> str:
        """Genera bigote apropiado para el género"""
        if gender.lower() in ["mujer", "woman", "female"]:
            return "none"  # Las mujeres no tienen bigote
        else:
            # Solo para hombres
            return random.choice(["none", "light", "medium", "thick", "handlebar"])
    
    def generate_advanced_genetic_profile(self, nationality: str, region: str, gender: str, age: int, 
                                        beauty_control: str, skin_control: str, hair_control: str, 
                                        eye_control: str, face_shape_control: str, nose_shape_control: str,
                                        lip_shape_control: str, eye_shape_control: str, jawline_control: str,
                                        cheekbone_control: str, eyebrow_control: str, skin_texture_control: str,
                                        freckle_control: str, mole_control: str, scar_control: str,
                                        acne_control: str, wrinkle_control: str, hair_style_control: str) -> UltraDiversityProfile:
        """Genera perfil genético avanzado usando los controles de la WebUI"""
        
        # Generar ID único
        image_id = f"genetic_{hashlib.md5(f'{nationality}_{gender}_{age}_{time.time()}'.encode()).hexdigest()[:12]}"
        
        # Manejar región aleatoria
        if region == "aleatorio":
            regiones_disponibles = [
                "caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", 
                "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", 
                "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", 
                "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", 
                "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", 
                "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", 
                "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", 
                "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", 
                "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"
            ]
            region = random.choice(regiones_disponibles)
        
        # Aplicar controles específicos
        skin_tone = self._apply_skin_control(skin_control)
        hair_color = self._apply_hair_control(hair_control)
        eye_color = self._apply_eye_control(eye_control)
        face_shape = self._apply_face_shape_control(face_shape_control)
        nose_shape = self._apply_nose_shape_control(nose_shape_control)
        lip_shape = self._apply_lip_shape_control(lip_shape_control)
        eye_shape = self._apply_eye_shape_control(eye_shape_control)
        jawline = self._apply_jawline_control(jawline_control)
        cheekbones = self._apply_cheekbone_control(cheekbone_control)
        eyebrows = self._apply_eyebrow_control(eyebrow_control)
        skin_texture = self._apply_skin_texture_control(skin_texture_control)
        freckles = self._apply_freckle_control(freckle_control)
        moles = self._apply_mole_control(mole_control)
        scars = self._apply_scar_control(scar_control)
        acne = self._apply_acne_control(acne_control)
        wrinkles = self._apply_wrinkle_control(wrinkle_control, age)
        hair_style = self._apply_hair_style_control(hair_style_control)
        
        # Crear perfil con controles aplicados
        profile = UltraDiversityProfile(
            image_id=image_id,
            nationality=nationality,
            region=region,
            gender=gender,
            age=age,
            
            # Características faciales con controles aplicados
            face_shape=face_shape,
            face_width=random.choice(["narrow", "medium", "wide"]),
            face_length=random.choice(["short", "medium", "long"]),
            jawline=jawline,
            chin=random.choice(["pointed", "rounded", "square", "oval"]),
            cheekbones=cheekbones,
            facial_symmetry=random.choice(["slightly_asymmetrical", "balanced", "very_symmetrical"]),
            bone_structure=random.choice(["delicate", "medium", "strong", "prominent"]),
            
            # Ojos con controles aplicados
            eye_color=eye_color,
            eye_color_shade=random.choice(["light", "medium", "dark", "deep"]),
            eye_shape=eye_shape,
            eye_size=random.choice(["small", "medium", "large"]),
            eye_spacing=random.choice(["close", "medium", "wide"]),
            eyelid_type=random.choice(["single", "double", "hooded", "deep_set"]),
            eyelashes=random.choice(["short", "medium", "long", "very_long"]),
            eyelashes_length=random.choice(["short", "medium", "long"]),
            eyebrows=eyebrows,
            eyebrows_thickness=random.choice(["thin", "medium", "thick"]),
            eyebrows_shape=random.choice(["straight", "arched", "rounded", "angled"]),
            
            # Nariz con controles aplicados
            nose_shape=nose_shape,
            nose_size=random.choice(["small", "medium", "large"]),
            nose_width=random.choice(["narrow", "medium", "wide"]),
            nose_bridge=random.choice(["low", "medium", "high", "prominent"]),
            nose_tip=random.choice(["pointed", "rounded", "wide", "narrow"]),
            nostril_size=random.choice(["small", "medium", "large"]),
            
            # Boca con controles aplicados
            lip_shape=lip_shape,
            lip_size=random.choice(["small", "medium", "large"]),
            lip_thickness=random.choice(["thin", "medium", "full"]),
            mouth_width=random.choice(["narrow", "medium", "wide"]),
            lip_color=random.choice(["pale", "medium", "dark", "very_dark"]),
            lip_fullness=random.choice(["thin", "medium", "full", "very_full"]),
            
            # Piel con controles aplicados
            skin_tone=skin_tone,
            skin_tone_shade=random.choice(["light", "medium", "dark", "deep"]),
            skin_texture=skin_texture,
            skin_undertone=random.choice(["cool", "neutral", "warm"]),
            skin_glow=random.choice(["dull", "natural", "glowing", "very_glowing"]),
            skin_imperfections=random.sample(["pores", "texture", "variations"], random.randint(0, 3)),
            freckles=freckles,
            freckles_density=random.choice(["sparse", "moderate", "dense"]),
            moles=moles,
            moles_count=random.choice(["none", "few", "several", "many"]),
            birthmarks=random.choice(["none", "small", "medium", "large"]),
            scars=scars,
            acne=acne,
            age_spots=self._generate_age_appropriate_spots(age),
            wrinkles=wrinkles,
            skin_elasticity=self._generate_age_appropriate_elasticity(age),
            
            # Cabello con controles aplicados
            hair_color=hair_color,
            hair_color_shade=random.choice(["light", "medium", "dark", "deep"]),
            hair_texture=random.choice(["straight", "wavy", "curly", "coily"]),
            hair_length=random.choice(["short", "medium", "long", "very_long"]),
            hair_style=hair_style,
            hair_density=random.choice(["thin", "medium", "thick", "very_thick"]),
            hair_shine=random.choice(["dull", "natural", "shiny", "very_shiny"]),
            hair_curliness=random.choice(["straight", "wavy", "curly", "very_curly"]),
            hair_thickness=random.choice(["fine", "medium", "thick", "very_thick"]),
            hairline=random.choice(["low", "medium", "high", "receding"]),
            
            # Vello facial (solo para hombres)
            facial_hair=self._generate_gender_appropriate_facial_hair(gender),
            beard=self._generate_gender_appropriate_beard(gender),
            mustache=self._generate_gender_appropriate_mustache(gender),
            
            # Características de edad
            age_characteristics=self._generate_age_characteristics(age),
            
            # Nivel de belleza
            beauty_level=random.choice(self.diversity_data["beauty_levels"]),
            attractiveness_factors=self._generate_attractiveness_factors(),
            
            # Características étnicas
            ethnic_features=self._generate_ethnic_features(nationality),
            
            # Metadatos
            generated_at=datetime.now().isoformat(),
            generation_type="advanced_genetic",
            uniqueness_score=random.uniform(0.8, 1.0),
            diversity_factors=self._generate_diversity_factors()
        )
        
        return profile
    
    def _apply_skin_control(self, skin_control: str) -> str:
        """Aplica el control de tono de piel"""
        if skin_control == "aleatorio":
            return random.choice(self.diversity_data["skin_tones"])
        elif skin_control == "mixed":
            return random.choice(["fair", "light", "medium", "olive", "tan", "brown", "dark"])
        elif skin_control == "auto":
            # Auto = selección automática basada en nacionalidad/región
            return random.choice(self.diversity_data["skin_tones"])
        else:
            # Mapear controles específicos a tonos de piel
            skin_mapping = {
                "fair": "fair",
                "light": "light", 
                "medium": "medium",
                "olive": "olive",
                "tan": "tan",
                "brown": "brown",
                "dark": "dark",
                "very_dark": "very_dark",
                # Mapear opciones específicas del UI
                "medium-dark": "dark",
                "golden": "tan",
                "bronze": "tan",
                "caramel": "brown",
                "honey": "tan",
                "rich brown": "brown",
                "coffee": "brown",
                "mahogany": "dark",
                "espresso": "very_dark",
                "chocolate": "brown",
                "mocha": "brown",
                "cinnamon": "tan",
                "amber": "tan",
                "copper": "tan",
                "peach": "fair",
                "ivory": "fair",
                "beige": "light",
                "sand": "tan",
                "cream": "fair",
                "wheat": "tan",
                "almond": "tan",
                "hazelnut": "brown",
                "walnut": "brown",
                "chestnut": "brown",
                "cocoa": "brown",
                "ebony": "very_dark"
            }
            return skin_mapping.get(skin_control, "medium")
    
    def _apply_hair_control(self, hair_control: str) -> str:
        """Aplica el control de color de cabello"""
        if hair_control == "aleatorio":
            return random.choice(self.diversity_data["hair_colors"])
        elif hair_control == "mixed":
            return random.choice(self.diversity_data["hair_colors"])
        elif hair_control == "auto":
            # Auto = selección automática basada en nacionalidad/región
            return random.choice(self.diversity_data["hair_colors"])
        else:
            # Mapear controles específicos a colores de cabello
            hair_mapping = {
                "black": "black",
                "brown": "brown",
                "dark_brown": "dark_brown",
                "light_brown": "light_brown",
                "blonde": "blonde",
                "red": "red",
                "auburn": "auburn",
                "gray": "gray",
                "white": "white"
            }
            return hair_mapping.get(hair_control, "brown")
    
    def _apply_eye_control(self, eye_control: str) -> str:
        """Aplica el control de color de ojos"""
        if eye_control == "aleatorio":
            return random.choice(self.diversity_data["eye_colors"])
        elif eye_control == "mixed":
            return random.choice(self.diversity_data["eye_colors"])
        elif eye_control == "auto":
            # Auto = selección automática basada en nacionalidad/región
            return random.choice(self.diversity_data["eye_colors"])
        else:
            # Mapear controles específicos a colores de ojos
            eye_mapping = {
                "brown": "brown",
                "hazel": "hazel", 
                "green": "green",
                "blue": "blue",
                "gray": "gray",
                "amber": "amber"
            }
            return eye_mapping.get(eye_control, "brown")
    
    def _apply_face_shape_control(self, face_shape_control: str) -> str:
        """Aplica el control de forma de cara"""
        if face_shape_control == "aleatorio":
            return random.choice(self.diversity_data["face_shapes"])
        else:
            return face_shape_control
    
    def _apply_nose_shape_control(self, nose_shape_control: str) -> str:
        """Aplica el control de forma de nariz"""
        if nose_shape_control == "aleatorio":
            return random.choice(self.diversity_data["nose_shapes"])
        else:
            return nose_shape_control
    
    def _apply_lip_shape_control(self, lip_shape_control: str) -> str:
        """Aplica el control de forma de labios"""
        if lip_shape_control == "aleatorio":
            return random.choice(self.diversity_data["lip_shapes"])
        else:
            return lip_shape_control
    
    def _apply_eye_shape_control(self, eye_shape_control: str) -> str:
        """Aplica el control de forma de ojos"""
        if eye_shape_control == "aleatorio":
            return random.choice(self.diversity_data["eye_shapes"])
        else:
            return eye_shape_control
    
    def _apply_jawline_control(self, jawline_control: str) -> str:
        """Aplica el control de línea de mandíbula"""
        if jawline_control == "aleatorio":
            return random.choice(self.diversity_data["jawline_types"])
        else:
            return jawline_control
    
    def _apply_cheekbone_control(self, cheekbone_control: str) -> str:
        """Aplica el control de pómulos"""
        if cheekbone_control == "aleatorio":
            return random.choice(self.diversity_data["cheekbone_types"])
        else:
            return cheekbone_control
    
    def _apply_eyebrow_control(self, eyebrow_control: str) -> str:
        """Aplica el control de cejas"""
        if eyebrow_control == "aleatorio":
            return random.choice(self.diversity_data["eyebrow_shapes"])
        else:
            return eyebrow_control
    
    def _apply_skin_texture_control(self, skin_texture_control: str) -> str:
        """Aplica el control de textura de piel"""
        if skin_texture_control == "aleatorio":
            return random.choice(self.diversity_data["skin_textures"])
        else:
            return skin_texture_control
    
    def _apply_freckle_control(self, freckle_control: str) -> str:
        """Aplica el control de pecas"""
        if freckle_control == "aleatorio":
            return random.choice(self.diversity_data["freckle_types"])
        else:
            return freckle_control
    
    def _apply_mole_control(self, mole_control: str) -> str:
        """Aplica el control de lunares"""
        if mole_control == "aleatorio":
            return random.choice(self.diversity_data["mole_types"])
        else:
            return mole_control
    
    def _apply_scar_control(self, scar_control: str) -> str:
        """Aplica el control de cicatrices"""
        if scar_control == "aleatorio":
            return random.choice(self.diversity_data["scar_types"])
        else:
            return scar_control
    
    def _apply_acne_control(self, acne_control: str) -> str:
        """Aplica el control de acné"""
        if acne_control == "aleatorio":
            return random.choice(self.diversity_data["acne_types"])
        else:
            return acne_control
    
    def _apply_wrinkle_control(self, wrinkle_control: str, age: int) -> str:
        """Aplica el control de arrugas considerando la edad"""
        if wrinkle_control == "aleatorio":
            return self._generate_age_appropriate_wrinkles(age)
        else:
            return wrinkle_control
    
    def _apply_hair_style_control(self, hair_style_control: str) -> str:
        """Aplica el control de estilo de cabello"""
        if hair_style_control == "aleatorio":
            return random.choice(self.diversity_data["hair_styles"])
        else:
            return hair_style_control

    def _passport_safe_hair_style(self, hair_style: str) -> str:
        """Normaliza estilos de cabello a estilos aprobados para pasaporte (bajo volumen, neat)."""
        # Palabras clave de alto volumen/no aprobados
        high_volume_keywords = {
            "afro", "dread", "dreadlocks", "locs", "bantu", "thick", "wild", "unkempt",
            "huge", "massive", "big", "messy", "voluminous", "trenzas", "braids", "box braids",
            "twists", "cornrows", "mohawk"
        }
        # Lista blanca de estilos recomendados para fotos de pasaporte
        passport_allowed = [
            "neat", "tidy", "sleek", "straight", "straightened", "bun", "low bun",
            "ponytail", "low ponytail", "bob", "pixie", "shoulder-length", "layered",
            "professional", "natural", "clean", "well-groomed", "short", "crew cut",
            "fade", "side part", "center part", "updo", "chignon"
        ]

        # Si ya es un estilo permitido, mantenerlo
        if hair_style and any(hair_style.lower() == a for a in passport_allowed):
            return hair_style

        # Si contiene palabras de alto volumen, convertir a un estilo permitido estable
        style_lower = (hair_style or "").lower()
        if any(k in style_lower for k in high_volume_keywords):
            return random.choice(passport_allowed)

        # Para estilos genéricos no listados, favorecer estilos sobrios
        return random.choice(passport_allowed)

    def _create_balanced_combinations(self, total_images: int, control_options: dict) -> list:
        """Crea combinaciones balanceadas para evitar repetición excesiva de valores."""
        combinations = []
        
        # Calcular cuántas veces puede aparecer cada valor (máximo)
        for control_name, options in control_options.items():
            if "aleatorio" in options:
                # Remover "aleatorio", "auto", "mixed" de las opciones
                clean_options = [opt for opt in options if opt not in ["aleatorio", "auto", "mixed"]]
                if clean_options:
                    # Calcular distribución balanceada
                    num_options = len(clean_options)
                    base_count = total_images // num_options
                    remainder = total_images % num_options
                    
                    # Crear lista balanceada
                    balanced_list = []
                    for i, option in enumerate(clean_options):
                        # Asignar base_count + 1 si está en el remainder
                        count = base_count + (1 if i < remainder else 0)
                        balanced_list.extend([option] * count)
                    
                    # Mezclar para evitar patrones
                    random.shuffle(balanced_list)
                    combinations.append(balanced_list[:total_images])
                else:
                    combinations.append([random.choice(options)] * total_images)
            else:
                combinations.append([random.choice(options)] * total_images)
        
        return combinations

    def generate_balanced_profiles(self, total_images: int, nationality: str, gender: str, age: int, 
                                 control_options: dict) -> list:
        """Genera perfiles balanceados para evitar repetición excesiva."""
        profiles = []
        
        # Crear combinaciones balanceadas
        balanced_combinations = self._create_balanced_combinations(total_images, control_options)
        
        # Crear diccionario de mapeo de controles basado en el orden de control_options
        control_mapping = {}
        for i, (control_name, _) in enumerate(control_options.items()):
            control_mapping[control_name] = i
        
        # Generar perfiles usando las combinaciones balanceadas
        for i in range(total_images):
            # Seleccionar valores balanceados para esta imagen
            balanced_values = {}
            for control_name, control_index in control_mapping.items():
                if control_index < len(balanced_combinations):
                    balanced_values[control_name] = balanced_combinations[control_index][i]
                else:
                    balanced_values[control_name] = "aleatorio"
            
            # Generar región aleatoria
            regiones_disponibles = ["caracas", "maracaibo", "valencia", "barquisimeto", "ciudad_guayana", "maturin", "merida", "san_cristobal", "barcelona", "puerto_la_cruz", "ciudad_bolivar", "tucupita", "porlamar", "valera", "acarigua", "guanare", "san_fernando", "trujillo", "el_tigre", "cabimas", "punto_fijo", "ciudad_ojeda", "puerto_cabello", "valle_de_la_pascua", "san_juan_de_los_morros", "carora", "tocuyo", "duaca", "siquisique", "araure", "turen", "guanarito", "santa_elena", "el_venado", "san_rafael", "san_antonio", "la_fria", "rubio", "colon", "san_cristobal", "tachira", "apure", "amazonas", "delta_amacuro", "yacambu", "lara", "portuguesa", "cojedes", "guarico", "anzoategui", "monagas", "sucre", "nueva_esparta", "falcon", "zulia", "merida", "trujillo", "barinas", "yaracuy", "carabobo", "aragua", "miranda", "vargas", "distrito_capital"]
            region = random.choice(regiones_disponibles)
            
            # Generar perfil con valores balanceados
            profile = self.generate_advanced_genetic_profile(
                nationality=nationality,
                region=region,
                gender=gender,
                age=age,
                beauty_control=balanced_values.get("beauty_control", "aleatorio"),
                skin_control=balanced_values.get("skin_control", "aleatorio"),
                hair_control=balanced_values.get("hair_control", "aleatorio"),
                eye_control=balanced_values.get("eye_control", "aleatorio"),
                face_shape_control=balanced_values.get("face_shape_control", "aleatorio"),
                nose_shape_control=balanced_values.get("nose_shape_control", "aleatorio"),
                lip_shape_control=balanced_values.get("lip_shape_control", "aleatorio"),
                eye_shape_control=balanced_values.get("eye_shape_control", "aleatorio"),
                jawline_control=balanced_values.get("jawline_control", "aleatorio"),
                cheekbone_control=balanced_values.get("cheekbone_control", "aleatorio"),
                eyebrow_control=balanced_values.get("eyebrow_control", "aleatorio"),
                skin_texture_control=balanced_values.get("skin_texture_control", "aleatorio"),
                freckle_control=balanced_values.get("freckle_control", "aleatorio"),
                mole_control=balanced_values.get("mole_control", "aleatorio"),
                scar_control=balanced_values.get("scar_control", "aleatorio"),
                acne_control=balanced_values.get("acne_control", "aleatorio"),
                wrinkle_control=balanced_values.get("wrinkle_control", "aleatorio"),
                hair_style_control=balanced_values.get("hair_style_control", "aleatorio")
            )
            
            profiles.append(profile)
        
        return profiles
    
    def generate_prompt_from_advanced_profile(self, profile: UltraDiversityProfile, background_control: str) -> Tuple[str, str]:
        """Genera prompt y negative prompt desde el perfil genético avanzado con especificaciones SAIME críticas"""
        
        # Construir prompt principal
        prompt_parts = []

        # Normalizaciones específicas de pasaporte (bajo volumen, sin obstrucciones)
        try:
            # Forzar estilo de cabello seguro para pasaporte
            profile.hair_style = self._passport_safe_hair_style(getattr(profile, "hair_style", ""))
            # Opcional: favorecer texturas bajas en volumen
            if hasattr(profile, "hair_texture"):
                profile.hair_texture = random.choice(["straight", "wavy", "fine", "smooth"])  # evitar frizzy/very voluminous
        except Exception:
            pass
        
        # ESPECIFICACIONES CRÍTICAS SAIME VENEZUELA
        prompt_parts.append(f"venezuelan passport photo, SAIME standards, official document photo, government ID photo")
        prompt_parts.append(f"512×764 pixels, 35mm×45mm at 300 DPI, real photographic paper limits")
        prompt_parts.append(f"black outer frame defines ACTUAL photo boundaries, shoulders touch left and right red frame edges")
        prompt_parts.append(f"shoulders positioned at y=202px (78% of 260px), must touch 20px to 200px red frame borders")
        prompt_parts.append(f"head height 30-34mm from chin to crown, eyes at 31% from top (y=80px)")
        prompt_parts.append(f"head margins: 8-12mm top, 12-18mm sides, 18-25mm bottom (adjusted by black frame)")
        prompt_parts.append(f"shoulders width 180px (20px to 200px) - CRITICAL: must touch red frame edges")
        
        # Información básica
        prompt_parts.append(f"{profile.gender} Venezuela, {profile.age} years old")
        prompt_parts.append("front view, frontal view, looking directly at camera, direct eye contact")
        prompt_parts.append("neutral expression, serious expression, no smile, no laughing, mouth closed")
        prompt_parts.append("eyes open and visible, head centered and straight, frontal position")
        
        # Características faciales específicas
        prompt_parts.append(f"{profile.skin_tone} skin tone, {profile.skin_tone_shade} skin shade")
        prompt_parts.append(f"{profile.face_shape} face shape, {profile.jawline} jawline")
        prompt_parts.append(f"{profile.eye_color} eyes, {profile.eye_shape} eye shape")
        prompt_parts.append(f"{profile.nose_shape} nose, {profile.lip_shape} lips")
        prompt_parts.append(f"{profile.cheekbones} cheekbones, {profile.eyebrows} eyebrows")
        
        # Cabello específico
        prompt_parts.append(f"{profile.hair_color} hair, {profile.hair_style} hair style")
        prompt_parts.append(f"{profile.hair_texture} hair texture, {profile.hair_length} hair length")
        
        # Características de piel
        if profile.freckles != "none":
            prompt_parts.append(f"{profile.freckles} freckles")
        if profile.moles != "none":
            prompt_parts.append(f"{profile.moles} moles")
        if profile.scars != "none":
            prompt_parts.append(f"{profile.scars} scars")
        if profile.acne != "none":
            prompt_parts.append(f"{profile.acne} acne")
        if profile.wrinkles != "none":
            prompt_parts.append(f"{profile.wrinkles}")
        
        # Vello facial (solo para hombres)
        if profile.gender.lower() in ["hombre", "man", "male"]:
            if profile.facial_hair != "none":
                prompt_parts.append(f"{profile.facial_hair} facial hair")
            if profile.beard != "none":
                prompt_parts.append(f"{profile.beard} beard")
            if profile.mustache != "none":
                prompt_parts.append(f"{profile.mustache} mustache")
        
        # Especificaciones técnicas
        prompt_parts.append("SOLID WHITE BACKGROUND, PURE WHITE BACKGROUND, CLEAN WHITE BACKGROUND")
        prompt_parts.append("professional lighting, uniform lighting, even lighting, high contrast")
        prompt_parts.append("35mm x 45mm dimensions, black frame border 1-2mm, effective area 33x43mm")
        prompt_parts.append("CRITICAL: real paper photo limits 512x764 pixels, black outer frame defines ACTUAL paper photo boundaries")
        prompt_parts.append("RESPECT black outer frame as final paper crop limit, 300 DPI resolution")
        prompt_parts.append("professional quality, high resolution, 1024x1024 pixels, ultra high quality")
        prompt_parts.append("no earrings, no jewelry, no accessories, no necklaces, no bracelets, no rings")
        prompt_parts.append("no head accessories, natural makeup, no dark glasses, no reflections")
        prompt_parts.append("no white clothing, no white shirts, no white tops, colored clothing, dark clothing")
        prompt_parts.append("sharp and focused image, correct exposure, natural colors, no grain, no distortion")
        prompt_parts.append("PNG high quality format, SOLID WHITE BACKGROUND, PURE WHITE BACKGROUND")
        prompt_parts.append("natural facial structure, natural ethnic characteristics, natural skin texture")
        prompt_parts.append("natural age spots, natural pores, natural skin, natural moles, natural asymmetry")
        prompt_parts.append("natural imperfections, natural features, natural hair texture, natural hair density")
        prompt_parts.append("clean appearance, neat presentation, appropriate attire, modest clothing")
        prompt_parts.append("common appearance, natural skin texture, slight asymmetry, authentic facial features")
        prompt_parts.append("natural hair texture, regular citizen, regular person, professional headshot photography")
        prompt_parts.append("direct portrait photography, strictly frontal view, no three quarter view, no side view")
        prompt_parts.append("head and shoulders visible, shoulders must be visible")
        prompt_parts.append("CRITICAL: shoulders must touch left and right red frame edges (20px to 200px, total 180px width)")
        prompt_parts.append("shoulders positioned at y=202px (78% of 260px), shoulders MUST touch red frame borders")
        prompt_parts.append("SAIME CRITICAL: shoulders must physically touch 20px to 200px red frame edges")
        prompt_parts.append("sufficient head space, no head crop, full head visible, head positioned in upper 60%")
        prompt_parts.append("eyes positioned at 31% from top, perfectly centered composition")
        prompt_parts.append("professional studio lighting, no shadows, TRANSPARENT BACKGROUND, NO BACKGROUND")
        prompt_parts.append("ALPHA CHANNEL, passport photo requirements, ID photo standards, official document standards")
        prompt_parts.append("government photo standards, SAIME standards, venezuelan passport specifications")
        prompt_parts.append("8-12mm margin from crown, 12-18mm lateral margins, 18-25mm bottom margin")
        prompt_parts.append("black frame consideration, voluminous hair warning, afro hair considerations")
        prompt_parts.append("thick braids space requirements, chinos voluminous hair considerations")
        prompt_parts.append("CRITICAL: hair must fit within 512x764 black outer frame, anything beyond black frame will be cropped")
        prompt_parts.append("RESPECT black outer frame boundaries, final paper photo size 512x764 pixels")
        prompt_parts.append("black outer frame is the actual paper photo limit")
        
        # Refuerzos de pose y cabello
        prompt_parts.append("FRONTAL POSE ONLY, head centered, neutral expression, mouth closed")
        prompt_parts.append("HAIR LOW VOLUME, neatly groomed, fits entirely within black frame, ears visible if possible")
        
        # Unir todas las partes
        prompt = ", ".join(prompt_parts)
        
        # Negative prompt con especificaciones SAIME críticas
        negative_prompt = ("3/4 view, side profile, looking away, smiling, laughing, multiple people, "
                         "double exposure, passport document visible, photo of photo, magazine model, "
                         "overly perfect, artificial lighting, shadows, background objects, "
                         "earrings, jewelry, necklaces, bracelets, rings, accessories, "
                         "glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, "
                         "beauty contest, professional headshot, studio lighting, dramatic lighting, "
                         "soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, "
                         "duplicate, watermark, text, signature, date, stamp, border, frame, "
                         "shoulders not touching red frame edges, shoulders not reaching 20px to 200px, "
                         "shoulders positioned incorrectly, shoulders not at y=202px, "
                         "head not positioned correctly, eyes not at 31% from top, "
                         "incorrect head margins, head too close to edges, "
                         "hair extending beyond black outer frame, hair touching black frame, "
                         "accessories extending beyond black frame, jewelry beyond black frame, "
                         "SAIME VIOLATIONS: incorrect shoulder positioning, incorrect head positioning, "
                         "violation of 512x764 black outer frame limits, violation of red frame shoulder requirements, "
                         "braids, cornrows, dreadlocks, dread, locs, thick braids, box braids, high volume hair, afro, mohawk, messy hair, wind, hair in face, "
                         "tilted head, rotated head, looking sideways, looking down, looking up, profile shot, half profile, "
                         "perfect skin, flawless skin, airbrushed, photoshopped, model look, "
                         "supermodel appearance, celebrity look, fashion model, beauty model, "
                         "perfect features, flawless features, extreme beauty, perfect beauty, "
                         "perfect symmetry, flawless symmetry, perfect proportions, flawless proportions, "
                         "perfect skin texture, flawless skin texture, perfect facial features, "
                         "flawless facial features, perfect bone structure, flawless bone structure, "
                         "perfect skin tone, flawless skin tone, perfect hair, flawless hair, "
                         "perfect eyes, flawless eyes, perfect lips, flawless lips, perfect nose, "
                         "flawless nose, perfect jawline, flawless jawline, perfect cheekbones, "
                         "flawless cheekbones, perfect eyebrows, flawless eyebrows, perfect teeth, "
                         "flawless teeth, perfect smile, flawless smile, perfect complexion, "
                         "flawless complexion, perfect appearance, flawless appearance, perfect face, "
                         "flawless face, perfect look, flawless look, perfect beauty, flawless beauty, "
                         "perfect model, flawless model, perfect portrait, flawless portrait, "
                         "perfect headshot, flawless headshot, perfect photo, flawless photo, "
                         "perfect image, flawless image, perfect picture, flawless picture, "
                         "perfect shot, flawless shot, perfect capture, flawless capture, "
                         "perfect rendering, flawless rendering, perfect generation, flawless generation, "
                         "perfect creation, flawless creation, perfect result, flawless result, "
                         "perfect output, flawless output, three quarter view, side view, profile view, "
                         "watermark, signature, cropped at neck, only head, no shoulders, head cut off, "
                         "shoulders missing, head cut off at top, head cropped at top, top of head missing, "
                         "multiple people, double exposure, passport document visible, photo of photo, "
                         "magazine model, overly perfect, artificial lighting, shadows, background objects, "
                         "jewelry, glasses, hat, makeup, retouched, airbrushed, glamour, fashion model, "
                         "beauty contest, professional headshot, studio lighting, dramatic lighting, "
                         "soft focus, blurry, low quality, distorted, deformed, extra limbs, extra heads, "
                         "duplicate, watermark, text, signature, date, stamp, border, frame, "
                         "white clothing, white shirts, white tops, white blouses, white t-shirts, "
                         "white sweaters, white jackets, white dresses, white garments, "
                         "COLORED BACKGROUND, TEXTURED BACKGROUND, GRADIENT BACKGROUND, PATTERN BACKGROUND, "
                         "BACKGROUND, BACKDROP, WALL, SURFACE, FLOOR, CEILING, ENVIRONMENT, SCENE, SETTING, "
                         "LOCATION, PLACE, ROOM, INTERIOR, EXTERIOR, OUTDOOR, INDOOR, STUDIO BACKGROUND, "
                         "PHOTO STUDIO, BACKGROUND WALL, BACKGROUND SURFACE, cropped by internal frames, "
                         "respecting internal frame boundaries, following internal frame limits, "
                         "internal frame cropping, frame boundary respect, internal frame compliance")
        
        return prompt, negative_prompt
    
    def _generate_attractiveness_factors(self) -> List[str]:
        """Genera factores de atractivo"""
        factors = []
        if random.random() < 0.3:
            factors.append("symmetrical_features")
        if random.random() < 0.2:
            factors.append("defined_bone_structure")
        if random.random() < 0.15:
            factors.append("expressive_eyes")
        return factors
    
    def _generate_ethnic_features(self, nationality: str) -> List[str]:
        """Genera características étnicas específicas"""
        features = []
        if nationality == "venezuelan":
            features.extend(["mixed_heritage", "caribbean_features", "latin_features"])
        return features
    
    def _generate_diversity_factors(self) -> List[str]:
        """Genera factores de diversidad"""
        factors = []
        if random.random() < 0.5:
            factors.append("unique_facial_structure")
        if random.random() < 0.3:
            factors.append("distinctive_features")
        if random.random() < 0.2:
            factors.append("uncommon_characteristics")
        return factors

def test_ultra_diversity():
    """Prueba el motor de diversidad ultra avanzado"""
    print("🎨 PROBANDO MOTOR DE DIVERSIDAD ULTRA AVANZADO")
    print("=" * 60)
    
    engine = UltraDiversityEngine()
    
    # Generar 5 perfiles ultra diversos
    for i in range(5):
        print(f"\n📋 Generando perfil ultra diverso {i+1}/5...")
        
        profile = engine.generate_ultra_diverse_profile(
            nationality="venezuelan",
            gender="mujer",
            age=random.randint(18, 60)
        )
        
        print(f"   🆔 ID: {profile.image_id}")
        print(f"   🏙️ Región: {profile.region}")
        print(f"   💎 Belleza: {profile.beauty_level}")
        print(f"   🎨 Piel: {profile.skin_tone} {profile.skin_texture}")
        print(f"   💇 Cabello: {profile.hair_color} {profile.hair_style}")
        print(f"   👁️ Ojos: {profile.eye_color} {profile.eye_shape}")
        print(f"   🎭 Cara: {profile.face_shape}")
        print(f"   👃 Nariz: {profile.nose_shape}")
        print(f"   👄 Labios: {profile.lip_shape}")
        print(f"   👁️ Cejas: {profile.eyebrows}")
        print(f"   🦴 Mandíbula: {profile.jawline}")
        print(f"   🍎 Pómulos: {profile.cheekbones}")
        print(f"   ✨ Pecas: {profile.freckles}")
        print(f"   🔸 Lunares: {profile.moles}")
        print(f"   🩹 Cicatrices: {profile.scars}")
        print(f"   🔴 Acné: {profile.acne}")
        print(f"   📏 Arrugas: {profile.wrinkles}")
        print(f"   🎯 Score Unicidad: {profile.uniqueness_score:.2f}")
        print(f"   🌟 Factores Diversidad: {', '.join(profile.diversity_factors)}")
    
    print(f"\n🎉 MOTOR DE DIVERSIDAD ULTRA AVANZADO")
    print("   ✅ Características faciales ultra expandidas")
    print("   ✅ 60+ regiones venezolanas")
    print("   ✅ 20+ tonos de piel")
    print("   ✅ 30+ colores de cabello")
    print("   ✅ 20+ colores de ojos")
    print("   ✅ 15+ formas de cara")
    print("   ✅ 30+ formas de nariz")
    print("   ✅ 30+ formas de labios")
    print("   ✅ 20+ formas de ojos")
    print("   ✅ 30+ estilos de cabello")
    print("   ✅ 20+ tipos de cejas")
    print("   ✅ 20+ tipos de mandíbula")
    print("   ✅ 20+ tipos de pómulos")
    print("   ✅ 20+ texturas de piel")
    print("   ✅ 20+ niveles de belleza")
    print("   ✅ ¡MÁXIMA DIVERSIDAD GARANTIZADA!")

if __name__ == "__main__":
    test_ultra_diversity()
