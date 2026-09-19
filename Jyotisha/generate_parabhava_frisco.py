import os
import sys
from datetime import datetime
from math import ceil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from indic_transliteration import sanscript
from pytz import timezone as tz

import jyotisha
import jyotisha.custom_transliteration
from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem, names, Graha, time
from jyotisha.panchaanga.temporal.time import Date, Timezone
from jyotisha.panchaanga.temporal.festival import rules
from jyotisha.panchaanga.writer.tex.day_details import (
    get_raahu_yama_gulika_strings,
    get_karaNa_data_str,
    get_yoga_data_str,
    get_raashi_data_str,
    get_nakshatra_data_str,
    get_tithi_data_str,
    get_lagna_data_str,
    get_abhijit_muhurta_string,
    get_varjyam_strings,
    get_amrita_kalam_strings,
)
from jyotisha.panchaanga.writer.tex.daily_tex_writer import (
    stream_sun_moon_rise_data,
    stream_daylength_based_periods,
    print_festivals_to_stream,
)
from convert_panchanga import convert_to_english, convert_to_telugu, setup_output_dir
from tex2pdf import compile_tex_with_xelatex


def emit_parabhava_panchanga(panchaanga, output_stream, time_format="hh:mm:a", scripts=None):
    if scripts is None:
        scripts = [sanscript.DEVANAGARI]
    languages = ["sa"]
    compute_lagnams = panchaanga.computation_system.festival_options.set_lagnas

    template_path = os.path.join(BASE_DIR, 'jyotisha', 'panchaanga', 'writer', 'tex', 'templates', 'daily_cal_template.tex')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_lines = f.readlines()
    for line in template_lines:
        print(line.rstrip('\r\n'), file=output_stream)

    samvatsara_name_dev = names.NAMES['SAMVATSARA_NAMES']['sa'][scripts[0]][40]

    print(r'\mbox{}', file=output_stream)
    print(r'\renewcommand{\yearname}{2026--2027}', file=output_stream)
    print(r'\begin{center}', file=output_stream)
    print(r'{\sffamily \fontsize{60}{60}\selectfont  2026--2027\\[0.5cm]}', file=output_stream)
    print(r'\mbox{\fontsize{42}{42}\selectfont %s-नाम-संवत्सरः}\\[0.4cm]' % samvatsara_name_dev, file=output_stream)
    print(r'\mbox{\fontsize{22}{22}\selectfont (चैत्र-शुक्ल-प्रतिपद् [युगादि] तः फाल्गुन-कृष्ण-अమాवास्या-पर्यन्तम्)}\\[0.3cm]', file=output_stream)
    print(r'\mbox{\fontsize{24}{24}\selectfont श्री शालिवाहन शक १९४८ \quad कलियुगाब्द ५१२७–५१२८}\\[0.5cm]', file=output_stream)
    print(r'\hrule\vspace{0.3cm}', file=output_stream)
    print(r'{\sffamily \fontsize{46}{46}\selectfont  \uppercase{%s, TEXAS}\\[0.2cm]}' % panchaanga.city.name, file=output_stream)
    print(r'{\sffamily \fontsize{22}{22}\selectfont  {%s}\\[0.2cm]}' % jyotisha.custom_transliteration.print_lat_lon(panchaanga.city.latitude, panchaanga.city.longitude), file=output_stream)
    print(r'{\sffamily \fontsize{18}{18}\selectfont  Timezone: %s}\\[0.3cm]' % panchaanga.city.timezone, file=output_stream)
    print(r'\hrule', file=output_stream)
    print(r'\end{center}', file=output_stream)
    print(r'\clearpage\pagestyle{fancy}', file=output_stream)

    daily_panchaangas = panchaanga.daily_panchaangas_sorted()
    for d, daily_panchaanga in enumerate(daily_panchaangas):
        if d == 0:
            previous_day_panchaanga = None
        else:
            previous_day_panchaanga = daily_panchaangas[d - 1]

        if daily_panchaanga.date < panchaanga.start_date or daily_panchaanga.date > panchaanga.end_date:
            continue

        y, m, dt = daily_panchaanga.date.year, daily_panchaanga.date.month, daily_panchaanga.date.day

        tithi_data_str = get_tithi_data_str(daily_panchaanga, scripts, time_format, previous_day_panchaanga, include_early_end_angas=True)
        nakshatra_data_str = get_nakshatra_data_str(daily_panchaanga, scripts, time_format, previous_day_panchaanga, include_early_end_angas=True)
        yoga_data_str = get_yoga_data_str(daily_panchaanga, scripts, time_format, previous_day_panchaanga, include_early_end_angas=True)
        karana_data_str = get_karaNa_data_str(daily_panchaanga, scripts, time_format, previous_day_panchaanga, include_early_end_angas=True)
        rashi_data_str = get_raashi_data_str(daily_panchaanga, scripts, time_format)
        lagna_data_str = get_lagna_data_str(daily_panchaanga, scripts, time_format) if compute_lagnams else ''

        gulika, rahu, yama, raatri_gulika, raatri_yama, durmuhurta1, durmuhurta2 = get_raahu_yama_gulika_strings(daily_panchaanga, time_format)

        yname = samvatsara_name_dev
        sar_data = '{%s}{%s}{%s}' % (
            yname,
            names.NAMES['AYANA_NAMES']['sa'][scripts[0]][daily_panchaanga.solar_sidereal_date_sunset.month % 12 + 1],
            names.NAMES['RTU_NAMES']['sa'][scripts[0]][daily_panchaanga.solar_sidereal_date_sunset.month]
        )

        if daily_panchaanga.solar_sidereal_date_sunset.month_transition is None:
            month_end_str = ''
        else:
            _m = daily_panchaangas[d - 1].solar_sidereal_date_sunset.month
            if d + 1 < len(daily_panchaangas) and daily_panchaanga.solar_sidereal_date_sunset.month_transition >= daily_panchaangas[d + 1].jd_sunrise:
                month_end_str = r'\mbox{%s{\tiny\RIGHTarrow}{%s}}' % (
                    names.NAMES['RASHI_NAMES']['sa'][scripts[0]][_m],
                    time.Hour(24 * (daily_panchaanga.solar_sidereal_date_sunset.month_transition - daily_panchaangas[d + 1].julian_day_start)).to_string(format=time_format)
                )
            else:
                month_end_str = r'\mbox{%s{\tiny\RIGHTarrow}{%s}}' % (
                    names.NAMES['RASHI_NAMES']['sa'][scripts[0]][_m],
                    time.Hour(24 * (daily_panchaanga.solar_sidereal_date_sunset.month_transition - daily_panchaanga.julian_day_start)).to_string(format=time_format)
                )

        month_data = r'\sunmonth{%s}{%d}{%s}' % (
            names.NAMES['RASHI_NAMES']['sa'][scripts[0]][daily_panchaanga.solar_sidereal_date_sunset.month],
            daily_panchaanga.solar_sidereal_date_sunset.day,
            month_end_str
        )

        print(r'\caldata{%s}{%s}{%s{%s}{%s}{%s}%s}' % (
            names.month_map[m].upper(), dt, month_data,
            names.get_chandra_masa(daily_panchaanga.lunar_date.month.index, scripts[0]),
            names.NAMES['RTU_NAMES']['sa'][scripts[0]][int(ceil(daily_panchaanga.lunar_date.month.index))],
            names.NAMES['VARA_NAMES']['sa'][scripts[0]][daily_panchaanga.date.get_weekday()],
            sar_data
        ), file=output_stream)

        stream_sun_moon_rise_data(daily_panchaanga, output_stream, time_format)
        stream_daylength_based_periods(daily_panchaanga, output_stream, time_format)

        print(r'{\tnykdata{%s}%%' % tithi_data_str, file=output_stream)
        print(r'{%s}{%s}%%' % (nakshatra_data_str, rashi_data_str), file=output_stream)
        print(r'{%s}%%' % yoga_data_str, file=output_stream)
        print(r'{%s}{%s}' % (karana_data_str, lagna_data_str), file=output_stream)
        print(r'}', file=output_stream)

        print_festivals_to_stream(daily_panchaanga, output_stream, panchaanga, languages, scripts)

        print(r'{%s} ' % names.weekday_short_map[daily_panchaanga.date.get_weekday()], file=output_stream)

        durmuhurta_str = durmuhurta1
        if durmuhurta2 is not None:
            durmuhurta_str += ', ' + durmuhurta2
        print(r'\cfoot{\rygdata{%s}{%s}{%s}{%s}{%s}{%s}{%s}}' % (
            rahu, yama, gulika, durmuhurta_str,
            get_abhijit_muhurta_string(daily_panchaanga, time_format),
            get_varjyam_strings(panchaanga, d, time_format),
            get_amrita_kalam_strings(panchaanga, d, time_format)
        ), file=output_stream)

    print(r'\end{document}', file=output_stream)


def main():
    print("=" * 70)
    print("Generating Frisco TX Panchangam for Parābhava Samvatsaram")
    print("Period: 2026-03-19 (Ugadi) to 2027-04-06 (Phalguna Amavasya)")
    print("=" * 70)

    city = City("Frisco", "33:09:19.3428", "-96:49:7.4388", "America/Chicago")
    comp_system = ComputationSystem.read_from_file(
        os.path.join(BASE_DIR, 'computation_systems', 'vishvAsa_bhAskara.toml')
    )

    print("\n[Step 1] Loading precomputed data for 2026 and 2027...")
    p2026 = annual.get_panchaanga_for_civil_year(city=city, year=2026, computation_system=comp_system, allow_precomputed=True)
    p2027 = annual.get_panchaanga_for_civil_year(city=city, year=2027, computation_system=comp_system, allow_precomputed=True)

    combined_dict = {k: v for k, v in p2026.date_str_to_panchaanga.items() if k >= '2026-03-18'}
    combined_dict.update({k: v for k, v in p2027.date_str_to_panchaanga.items() if k <= '2027-04-07'})

    p2026.date_str_to_panchaanga = combined_dict
    p2026.start_date = Date(2026, 3, 19)
    p2026.end_date = Date(2027, 4, 6)

    days_in_panchanga = [dp for dp in p2026.daily_panchaangas_sorted() if p2026.start_date <= dp.date <= p2026.end_date]
    print(f"Total days in Parabhava Samvatsaram: {len(days_in_panchanga)}")
    print(f"First day: {days_in_panchanga[0].date.get_date_str()} (Chaitra Shukla Pratipada / Ugadi)")
    print(f"Last day:  {days_in_panchanga[-1].date.get_date_str()} (Phalguna Krishna Amavasya)")

    deva_dir = os.path.join(BASE_DIR, 'Tex_outputs', 'Frisco')
    telugu_dir = os.path.join(BASE_DIR, 'Tex_outputs_telugu', 'Frisco')
    english_dir = os.path.join(BASE_DIR, 'Tex_outputs_english', 'Frisco')

    print("\n[Step 2] Generating Devanagari TeX...")
    setup_output_dir(deva_dir)
    deva_tex_name = 'Panchanga_Parabhava_Frisco.tex'
    deva_tex_path = os.path.join(deva_dir, deva_tex_name)
    with open(deva_tex_path, 'w', encoding='utf-8') as f:
        emit_parabhava_panchanga(p2026, output_stream=f, scripts=[sanscript.DEVANAGARI])
    print(f"  -> Generated: {deva_tex_path}")

    print("\n[Step 3] Converting to Telugu...")
    setup_output_dir(telugu_dir)
    telugu_tex_name = 'Panchanga_Parabhava_Frisco_Telugu.tex'
    convert_to_telugu(deva_tex_path, telugu_dir, telugu_tex_name)
    print(f"  -> Generated: {os.path.join(telugu_dir, telugu_tex_name)}")

    print("\n[Step 4] Converting to English (IAST)...")
    setup_output_dir(english_dir)
    eng_tex_name = 'Panchanga_Parabhava_Frisco_English.tex'
    convert_to_english(deva_tex_path, english_dir, eng_tex_name)
    print(f"  -> Generated: {os.path.join(english_dir, eng_tex_name)}")

    print("\n[Step 5] Compiling Telugu PDF with XeLaTeX...")
    tel_ok = compile_tex_with_xelatex(telugu_tex_name, telugu_dir)
    print(f"Telugu PDF Compilation: {'SUCCESS' if tel_ok else 'FAILED'}")

    print("\n[Step 6] Compiling English PDF with XeLaTeX...")
    eng_ok = compile_tex_with_xelatex(eng_tex_name, english_dir)
    print(f"English PDF Compilation: {'SUCCESS' if eng_ok else 'FAILED'}")

    print("\n[Step 7] Compiling Devanagari PDF with XeLaTeX...")
    dev_ok = compile_tex_with_xelatex(deva_tex_name, deva_dir)
    print(f"Devanagari PDF Compilation: {'SUCCESS' if dev_ok else 'FAILED'}")

    print("\n" + "=" * 70)
    print("COMPILATION SUMMARY:")
    print(f"Telugu PDF:     {os.path.join(telugu_dir, 'Panchanga_Parabhava_Frisco_Telugu.pdf')}")
    print(f"English PDF:    {os.path.join(english_dir, 'Panchanga_Parabhava_Frisco_English.pdf')}")
    print(f"Devanagari PDF: {os.path.join(deva_dir, 'Panchanga_Parabhava_Frisco.pdf')}")
    print("=" * 70)


if __name__ == '__main__':
    main()