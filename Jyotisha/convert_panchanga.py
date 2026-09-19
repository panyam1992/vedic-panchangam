"""
Convert Devanagari Panchanga .tex files to English (IAST) and Telugu versions.
Performs script transliteration without changing any content or context.

Can be used as a library (import convert_panchanga) or run standalone.
"""

import os
import re
import shutil
from indic_transliteration import sanscript

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FONTS_DIR = os.path.join(BASE_DIR, 'jyotisha', 'panchaanga', 'writer', 'tex', 'templates', 'fonts')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'jyotisha', 'panchaanga', 'writer', 'tex', 'templates')

# Devanagari Unicode range pattern (includes digits, marks, signs)
DEVANAGARI_PATTERN = re.compile(r'[\u0900-\u097F\u200B-\u200D]+')


def transliterate_devanagari(text, target_script):
    """Replace all Devanagari character runs with transliterated equivalents."""
    def replace_match(m):
        return sanscript.transliterate(m.group(0), sanscript.DEVANAGARI, target_script)
    return DEVANAGARI_PATTERN.sub(replace_match, text)


def fix_preamble_english(content):
    """Fix font, digit, and layout settings for English/IAST output.
    
    IAST romanized text is ~40% wider than Devanagari, so we also adjust
    font sizes and spacing to ensure each day fits on exactly one page.
    """
    content = content.replace(
        r'\setmainfont{siddhanta.ttf}[Path=templates/fonts/,Script=Devanagari]',
        r'\setmainfont{NotoSansUI-Regular.ttf}[Path=templates/fonts/]'
    )
    # Replace Devanagari digit macro with pass-through (use Arabic numerals)
    content = content.replace(
        r'\newcommand{\devanumber}[1]{%' + '\n' + r'\num=#1\devanumberrecurse}',
        r'\newcommand{\devanumber}[1]{#1}'
    )
    # Also handle \r\n line endings
    content = content.replace(
        r'\newcommand{\devanumber}[1]{%' + '\r\n' + r'\num=#1\devanumberrecurse}',
        r'\newcommand{\devanumber}[1]{#1}'
    )

    # --- Layout fixes for wider IAST text ---
    content = _fix_layout_english(content)
    return content


def _fix_layout_english(content):
    """Apply layout adjustments so IAST text fits one page per day."""

    # 1. \kalas macro: shrink labels from \small to \scriptsize
    content = content.replace(
        r'{\small{\mbox{',
        r'{\scriptsize{\mbox{'
    )

    # 2. \tnykdata: shrink from \large to \normalsize
    content = content.replace(
        r'\newcommand{\tnykdata}[6]{\large',
        r'\newcommand{\tnykdata}[6]{\normalsize'
    )

    # 3. \tnykdata: tighten the tabular column width from 108mm to 100mm
    content = content.replace(
        r'@{}p{108mm}@{}',
        r'@{}p{100mm}@{}'
    )

    # 4. \rygdata: shrink label sizes
    content = content.replace(
        r'\small rāhu',
        r'\footnotesize rāhu'
    )
    content = content.replace(
        r'\scriptsize durmu',
        r'\tiny durmu'
    )

    # 5. \caldata: reduce vertical gaps between sections
    #    After sun/moon/kalas data: 0.5em -> 0.2em
    content = content.replace(
        r'#4\\[0.5em]%Sun rise, kalas etc',
        r'#4\\[0.2em]%Sun rise, kalas etc'
    )
    #    After tnykdata: 1em -> 0.3em
    content = content.replace(
        r'#5\mbox{}\\\[1em]',
        r'#5\mbox{}\\[0.3em]'
    )
    # Handle the exact raw string version
    content = content.replace(
        '#5\\mbox{}\\\\[1em]',
        '#5\\mbox{}\\\\[0.3em]'
    )

    # 6. \caldata: shrink festival text from \normalsize to \footnotesize
    content = content.replace(
        r'{\centering\normalsize\textcolor{RoyalBlue}{#6}}',
        r'{\centering\footnotesize\textcolor{RoyalBlue}{#6}}'
    )

    # 7. \caldata header: reduce date number sizes for compactness
    #    Main date: 96pt -> 72pt
    content = content.replace(
        r'\fontsize{96}{115}\selectfont #2}',
        r'\fontsize{72}{86}\selectfont #2}'
    )
    #    Solar month date: 90pt -> 66pt
    content = content.replace(
        r'\fontsize{90}{24}\selectfont \devanumber',
        r'\fontsize{66}{20}\selectfont \devanumber'
    )
    #    Day of week: 24pt -> 20pt
    content = content.replace(
        r'\fontsize{24}{28}\selectfont\uppercase{#7}}',
        r'\fontsize{20}{24}\selectfont\uppercase{#7}}'
    )

    # 8. Reduce header row spacing
    content = content.replace(
        r'\\[1.6ex]%DD',
        r'\\[0.8ex]%DD'
    )
    content = content.replace(
        r'\\[1.2ex]%Day of the week',
        r'\\[0.6ex]%Day of the week'
    )
    # 9. Replace Devanagari abbreviation marker with period
    #    NotoSansUI does not include the ॰ (U+0970) glyph
    content = content.replace('॰', '.')

    return content


def fix_preamble_telugu(content):
    """Fix font and digit settings for Telugu output."""
    content = content.replace(
        r'\setmainfont{siddhanta.ttf}[Path=templates/fonts/,Script=Devanagari]',
        r'\setmainfont{Nirmala UI}[Script=Telugu]'
    )
    return content


def setup_output_dir(output_dir):
    """Create output directory and copy supporting files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create templates/fonts directory
    fonts_dest = os.path.join(output_dir, 'templates', 'fonts')
    os.makedirs(fonts_dest, exist_ok=True)
    
    # Copy font files
    for font_file in os.listdir(TEMPLATE_FONTS_DIR):
        src = os.path.join(TEMPLATE_FONTS_DIR, font_file)
        dst = os.path.join(fonts_dest, font_file)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    
    # Copy supporting TeX files
    for support_file in ['listofitems.sty', 'listofitems.tex']:
        src = os.path.join(TEMPLATE_DIR, support_file)
        if os.path.exists(src):
            dst = os.path.join(output_dir, support_file)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)


def convert_panchanga(source_tex, target_script, output_dir, output_filename, preamble_fixer):
    """Convert a Devanagari Panchanga .tex to the target script.
    
    Args:
        source_tex: Path to the source .tex file (Devanagari)
        target_script: Target script constant from sanscript (e.g. sanscript.IAST)
        output_dir: Directory to write the output file
        output_filename: Name of the output .tex file
        preamble_fixer: Function to fix preamble for the target script
    
    Returns:
        Path to the output .tex file
    """
    print(f"  Reading source: {source_tex}")
    with open(source_tex, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"  Transliterating to {target_script}...")
    content = transliterate_devanagari(content, target_script)
    
    print(f"  Fixing preamble...")
    content = preamble_fixer(content)
    
    setup_output_dir(output_dir)
    
    output_path = os.path.join(output_dir, output_filename)
    print(f"  Writing output: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Done! Output saved to: {output_path}")
    return output_path


def convert_to_english(source_tex, output_dir, output_filename):
    """Convenience wrapper to convert a Devanagari .tex to English (IAST)."""
    return convert_panchanga(
        source_tex=source_tex,
        target_script=sanscript.IAST,
        output_dir=output_dir,
        output_filename=output_filename,
        preamble_fixer=fix_preamble_english
    )


def convert_to_telugu(source_tex, output_dir, output_filename):
    """Convenience wrapper to convert a Devanagari .tex to Telugu."""
    return convert_panchanga(
        source_tex=source_tex,
        target_script=sanscript.TELUGU,
        output_dir=output_dir,
        output_filename=output_filename,
        preamble_fixer=fix_preamble_telugu
    )


if __name__ == '__main__':
    # Standalone mode: convert the existing single-year Panchanga.tex
    SOURCE_TEX = os.path.join(BASE_DIR, 'Tex_outputs', 'Panchanga.tex')
    
    # Generate English (IAST) version
    print("=" * 60)
    print("Generating English (IAST) version...")
    print("=" * 60)
    english_dir = os.path.join(BASE_DIR, 'Tex_outputs_english')
    convert_to_english(SOURCE_TEX, english_dir, 'Panchanga_English.tex')
    
    # Generate Telugu version
    print()
    print("=" * 60)
    print("Generating Telugu version...")
    print("=" * 60)
    telugu_dir = os.path.join(BASE_DIR, 'Tex_outputs_telugu')
    convert_to_telugu(SOURCE_TEX, telugu_dir, 'Panchanga_Telugu.tex')
    
    print()
    print("=" * 60)
    print("All conversions complete!")
    print(f"English .tex: {os.path.join(english_dir, 'Panchanga_English.tex')}")
    print(f"Telugu .tex:  {os.path.join(telugu_dir, 'Panchanga_Telugu.tex')}")
    print("=" * 60)
