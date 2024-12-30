import csv
import os
import shutil

import gdown
import pygsheets as pygsheets
from fpdf import FPDF
from Team import Team
from Player import Player

L_CEL = 45
H_CEL_INT = 10
H_CEL = 15
H_CEL_PL = 5

LINK_CALCETTO = "https://docs.google.com/spreadsheets/d/1sofSc2HIp06Hj8MNdUv573Esi-Nxz6C7M-hRAMfGejc/edit?usp=sharing"

LINL_PALLAVOLO = "https://docs.google.com/spreadsheets/d/1wRe2mJv437FIw7xGAwSiWNCFfd29tSVhNiXwxUa_n2Y/edit?usp=sharing"

def create_resp_pdf(tounament, list_teams, file_name):
    pdf = FPDF("L", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Times", size=30)
    pdf.cell(0, H_CEL_PL, txt=f"Responsabili {tounament}", align='C')
    pdf.cell(0, H_CEL_PL * 3, txt="", ln=1)
    pdf.set_font("Times", size=10)

    pdf.set_line_width(0.3)

    pdf.cell(L_CEL, H_CEL_PL, txt="Squadra", border=1)
    pdf.cell(L_CEL, H_CEL_PL, txt="Referente", border=1)
    pdf.cell(L_CEL*2, H_CEL_PL, txt="Email", border=1)
    pdf.cell(L_CEL, H_CEL_PL, txt="Numero", border=1)
    pdf.cell(L_CEL/2, H_CEL_PL, txt="C.I", border=1)
    pdf.cell(L_CEL/2, H_CEL_PL, txt="Mod.Min.", border=1)
    pdf.cell(0, H_CEL_PL, txt="", ln=1)

    pdf.set_line_width(0.1)

    for t in list_teams:
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.team_name}", border=1)
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.resp_name}", border=1)
        pdf.cell(L_CEL*2, H_CEL_PL, txt=f"{t.mail}", border=1)
        pdf.cell(L_CEL, H_CEL_PL, txt=f"{t.tel}", border=1)
        pdf.cell(L_CEL/2, H_CEL_PL, txt=f" ", border=1)
        pdf.cell(L_CEL/2, H_CEL_PL, txt=f" ", border=1)
        pdf.cell(0, H_CEL_PL, txt="", ln=1)

    pdf.output(f"{tounament}/{file_name}.pdf")


def read_team(file_name):
    list_teams = list()
    file = open(f"{file_name}")
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            teams = Team(row[2], row[3], row[4], row[5], row[6])
            base = 6
            for i in range(10):
                teams.add_player(
                    Player(row[base + 1], row[base + 2], row[base + 3], row[base + 4], row[base + 5], row[base + 6],
                           row[base + 7], row[base + 8], row[base + 9]))
                base += 9
            list_teams.append(teams)
        line_count += 1
    print(f'Processed {line_count - 1} Teams.')
    file.close()
    return list_teams


def create_teams_folders(tournament, list_teams):
    for t in list_teams:
        #t.to_string()
        t.create_team_folder(tournament)

def main():
    torneo = input("Inserire di quale torneo si vogliono scaricare i dati\n"
          "\tPallavolo (p)\n"
          "\tCalcio a 5 (c)\n-> ")
    if torneo == 'p':
        file_name_referenti = 'ReferentiTorneoPallavolo'
        file_name_csv = 'IscrizioniPallavolo2024.csv'
        tournament = 'Pallavolo'
    else:
        if  torneo == 'c':
            file_name_referenti = 'ReferentiTorneoCalcetto'
            file_name_csv = 'IscrizioniCalcetto2024.csv'
            tournament = 'Calcetto'
        else:
            exit("Nessun torneo trovato")
    os.mkdir(tournament)
    list_teams = read_team(file_name_csv)
    create_teams_folders(tournament, list_teams)
    create_resp_pdf(tournament, list_teams, file_name_referenti)



if __name__ == '__main__':
    try:
        shutil.rmtree("la migliore")
        shutil.rmtree("Prova")
        shutil.rmtree("VolleyVinc")
    except:
        print("Niente da cancellare")
    main()