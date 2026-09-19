"""Quick script to regenerate just Frisco 2026 English PDF using precomputed data."""
import os, sys

BASE_DIR = r'd:\Panchangam\Jyotisha'
sys.path.insert(0, BASE_DIR)

from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
from indic_transliteration import sanscript
from convert_panchanga import convert_to_english, setup_output_dir

computation_system = ComputationSystem.read_from_file(
    filename=os.path.join(BASE_DIR, 'computation_systems', 'vishvAsa_bhAskara.toml'))

city = City("Frisco", "33:09:19.3428", "-96:49:7.4388", "America/Chicago")
year = 2026

# Step 1: Generate Devanagari - allow precomputed to skip scipy-dependent calculations
print("Step 1: Computing Panchanga for Frisco 2026 (allowing precomputed)...")
panchaanga = annual.get_panchaanga_for_civil_year(
    city=city, year=year, computation_system=computation_system, allow_precomputed=True)

deva_dir = os.path.join(BASE_DIR, 'Tex_outputs', 'Frisco')
setup_output_dir(deva_dir)
deva_path = os.path.join(deva_dir, 'Panchanga_2026.tex')
emit(panchaanga, output_stream=open(deva_path, 'w', encoding='utf-8'),
     languages=["sa"], scripts=[sanscript.DEVANAGARI])
print(f"  -> Written: {deva_path}")

# Step 2: Convert to English  
print("Step 2: Converting to English (IAST)...")
eng_dir = os.path.join(BASE_DIR, 'Tex_outputs_english', 'Frisco')
convert_to_english(deva_path, eng_dir, 'Panchanga_2026_English.tex')
print("Done!")
