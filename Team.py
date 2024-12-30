import os
import gdown
import tabulate
from fpdf import FPDF
import re

L_CEL = 45
H_CEL_INT = 10
H_CEL = 15
H_CEL_PL = 5


class Team:
    def __init__(self, team_name, resp_name, tel, mail, pay_rec_link):
        self.team_name = team_name
        self.resp_name = resp_name
        self.tel = tel
        self.mail = mail
        self.pay_rec_link = pay_rec_link
        self.players = list()

    def add_player(self, player):
        self.players.append(player)

    def to_string(self):
        print(f"TEAM: {self.team_name}\n"
              f"RESPONSABILE: {self.resp_name}\n"
              f"NUMERO DI TELEFONO: {self.tel}\n"
              f"E-MAIL: {self.mail}\n"
              f"LINK RICEVUTA PAGAMENTO: {self.pay_rec_link}\n"
              f"GIOCATORI")
        list_dict = []

        for p in self.players:
            list_dict.append(p.to_dict())

        print(tabulate.tabulate(list_dict, headers="keys", tablefmt='rst'))
        print("\n\n")

    def estrai_id_google_drive(self, url):
        # Utilizza un'espressione regolare per estrarre l'ID del file dal link di Google Drive
        match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
        else:
            return None


    def create_team_folder(self, tournament):
        os.mkdir(f"{tournament}/{self.team_name}")
        os.mkdir(f"{tournament}/{self.team_name}/CI")
        os.mkdir(f"{tournament}/{self.team_name}/AUTH")
        os.mkdir(f"{tournament}/{self.team_name}/CM")
        pdf = FPDF("L", "mm", "A4")
        pdf.add_page()
        pdf.set_font("Times", size=10)

        pdf.set_line_width(0.2)
        pdf.cell(0, H_CEL_INT, txt=f"TEAM: {self.team_name}", ln=1)
        pdf.cell(0, H_CEL_INT, txt=f"RESPONSABILE: {self.resp_name}", ln=1)
        pdf.cell(0, H_CEL_INT, txt=f"NUMERO DI TELEFONO: {self.tel}", ln=1)
        pdf.cell(0, H_CEL_INT, txt=f"E-MAIL: {self.mail}", ln=1)
        if len(self.pay_rec_link) > 0:
            pdf.cell(0, H_CEL_INT, txt="RICEVUTA PAGAMENTO", ln=1, link=self.pay_rec_link)
            output_path = f'{tournament}/{self.team_name}/RicevutaPagamento_{self.team_name}.pdf'
            gdown.download(self.pay_rec_link, output_path, quiet=False, fuzzy=True)
        pdf.cell(0, H_CEL_INT, txt=f"GIOCATORI:", ln=1)

        pdf.set_line_width(0.3)
        pdf.cell(L_CEL, H_CEL_PL, txt="NOME", border='B')
        pdf.cell(L_CEL, H_CEL_PL, txt="COGNOME", border='B')
        pdf.cell(L_CEL, H_CEL_PL, txt="DATA DI NASCITA", border='B')
        pdf.cell(L_CEL, H_CEL_PL, txt="LUOGO DI NASCITA", border='B')
        pdf.cell(L_CEL, H_CEL_PL, txt="CARTA IDENTITA'", border='B')
        pdf.cell(L_CEL, H_CEL_PL, txt="CATEGORIA\n", border='B')
        pdf.cell(0, H_CEL_PL, txt="", ln=1)

        pdf.set_line_width(0.1)
        for p in self.players:
            pdf.cell(L_CEL, H_CEL_PL, txt=f"{p.name}", border='B')
            pdf.cell(L_CEL, H_CEL_PL, txt=f"{p.surname}", border='B')
            pdf.cell(L_CEL, H_CEL_PL, txt=f"{p.date}", border='B')
            pdf.cell(L_CEL, H_CEL_PL, txt=f"{p.place}", border='B')
            pdf.cell(L_CEL, H_CEL_PL, txt=f"{p.ci}", border='B')
            pdf.cell(L_CEL, H_CEL_PL, txt=f"{p.cat}", border='B')
            pdf.cell(0, H_CEL_PL, txt="", ln=1)

        pdf.set_font("Times", 'B', size=13)
        pdf.cell(0, H_CEL_PL, txt=f" ", ln=1)

        # cose da accettare
        pdf.cell(0, H_CEL_PL,
                 txt=f"L'organizzazione declina ogni responsabilità per eventuali danni a cose o persone di qualsiasi natura accaduti durante le partite",
                 ln=1)
        pdf.cell(0, H_CEL_PL,
                 txt=f"o causati sia dall'uso delle attrezzature della società, sia dall'imperizia o negligenza dei partecipanti.",
                 ln=1)
        pdf.cell(0, H_CEL_PL,
                 txt=f"Declina inoltre ogni responsabilità per eventuali danni a persone o cose causati da eventi naturali e/o atti vandalici.",
                 ln=1)
        pdf.cell(0, H_CEL_PL,
                 txt=f"I partecipanti dovranno inoltre rispondere personalmente dei danni causati dal proprio comportamento.",
                 ln=1)

        pdf.cell(0, H_CEL_PL / 3, txt=f" ", ln=1)

        pdf.cell(0, H_CEL_PL,
                 txt=f"Dichiaro che tutti i giocatori in distinta sono in possesso di regolare visita medica sportiva valida (sia non agonistica che agonistica).",
                 ln=1)

        pdf.cell(0, H_CEL_PL, txt=f" ", ln=1)

        pdf.cell(0, H_CEL_PL, txt=f"Firma del Responsabile per accettazione di cui sopra:", ln=1)

        pdf.set_font("Times", size=10)
        pdf.cell(L_CEL, H_CEL_PL * 2, txt=f" ")
        pdf.cell(L_CEL, H_CEL_PL * 2, txt=f" ", border='B')
        pdf.cell(L_CEL, H_CEL_PL * 2, txt=f" ", border='B')

        # save link ci
        pdf.add_page()
        pdf.cell(0, H_CEL_INT, txt=f"CARTE D'IDENTITA'", ln=1)
        for p in self.players:
            if len(p.ci_links) > 0:
                x = p.ci_links.split(";")
                print("lista link google drive ", x)
                for count, el in enumerate(x):
                    print("link google drive ", el)
                    pdf.cell(L_CEL, H_CEL_PL, txt=f"CI_{p.name}_{p.surname}_{count}", ln=1, link=el, border='B')
                    output_path = f'{tournament}/{self.team_name}/CI/CI_{p.name}_{p.surname}_{count}.jpg'

                    # Estrarre l'ID del file dal link di Google Drive
                    file_id = self.estrai_id_google_drive(el)
                    if file_id:
                        download_url = f'https://drive.google.com/uc?id={file_id}'
                        print("download google drive ", download_url)
                        #try:
                            #gdown.download(download_url, output_path, quiet=False, fuzzy=True)
                        #except Exception as e:
                        #    print(f"Errore nel download di {el}: {e}")
                    else:
                        print(f"Link di Google Drive non valido: {el}")

        pdf.cell(0, H_CEL_PL, txt="", ln=1)
        pdf.cell(0, H_CEL_PL, txt="", ln=1)

        pdf.cell(0, H_CEL_INT, txt=f"AUTORIZZAZIONI MINORI e CERTIFICATI MEDICI", ln=1)
        for p in self.players:
            if len(p.auth_link) > 0:
                pdf.cell(L_CEL + L_CEL, H_CEL_PL, txt=f"AUTH_{p.name}_{p.surname}", link=p.auth_link, border='B')
                output_path = f'{tournament}/{self.team_name}/AUTH/AUTH_{p.name}_{p.surname}.pdf'
                #gdown.download(p.auth_link, output_path, quiet=False, fuzzy=True)
            else:
                pdf.cell(L_CEL + L_CEL, H_CEL_PL, txt=f"", border='B')

            pdf.cell(10, H_CEL_PL, txt="")

            if len(p.cert_link) > 0:
                pdf.cell(L_CEL + L_CEL, H_CEL_PL, txt=f"CM_{p.name}_{p.surname}", link=p.cert_link, border='B')
                output_path = f'{tournament}/{self.team_name}/CM/CM_{p.name}_{p.surname}.pdf'
                #gdown.download(p.cert_link, output_path, quiet=False, fuzzy=True)
            else:
                pdf.cell(L_CEL + L_CEL, H_CEL_PL, txt=f"", border='B')

            pdf.cell(0, H_CEL_PL, txt="", ln=1)

        # save the pdf with name .pdf
        pdf.output(f"{tournament}/{self.team_name}/{self.team_name}.pdf")
