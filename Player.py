class Player:
    def __init__(self,  name, surname, date, place, auth_link, cert_link, ci, ci_links, cat):
        self.name = name
        self.surname = surname
        self.date = date
        self.place = place
        self.auth_link = auth_link
        self.cert_link = cert_link
        self.ci = ci
        self.ci_links = ci_links
        self.cat = cat

    def to_string(self):
        # Nome,Cognome,Data di nascita,Luogo di nascita,Autorizzazione dei genitori,
        # Certificato medico,Carta d'identità,Foto della carta d'identità fronte-retro,Tesserato/Categoria
        print(f"\t{self.name}"
              f"\t{self.surname}"
              f"\t{self.date}"
              f"\t{self.place}"
              f"\t{self.auth_link}"
              f"\t{self.cert_link}"
              f"\t{self.ci}"
              f"\t{self.ci_links}"
              f"\t{self.cat}\n")

    def to_dict(self):
        # print("\tNOME\tCOGNOME\tDATA DI NASCITA\tLUOGO DI NASCITA\tAUTH\tCERT\tCARTA IDENTITà\tFOTO\tCATEGORIA\n")
        p = {
            "NOME": self.name,
            "COGNOME": self.surname,
            "DATA DI NASCITA": self.date,
            "LUOGO DI NASCITA": self.place,
            #"AUTH": self.auth_link,
            #"CERT":self.cert_link,
            "CARTA IDENTITA'": self.ci,
            #"FOTO":self.ci_links,
            "CATEGORIA": self.cat,
        }
        return p