import json
import os
from models.atividade import AtividadePresencial, AtividadeRemota

ARQUIVO_ATIVIDADES = "data/atividades.json"


class AtividadeRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.atividades = []
        self.proximo_id = 1
        self.carregar_atividades()

    def carregar_atividades(self):
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(ARQUIVO_ATIVIDADES):
            self.criar_atividades_padrao()
            return

        with open(ARQUIVO_ATIVIDADES, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        
        self.proximo_id = dados.get("proximo_id", 1)
        self.atividades = []
        
        for item in dados.get("atividades", []):
            if item["tipo"] == "Remota":
                atividade = AtividadeRemota(
                    id=item["id"],
                    titulo=item["titulo"],
                    descricao=item["descricao"],
                    data=item["data"],
                    horario=item["horario"],
                    tutor=None,
                    local=item["local"],
                    vagas=item["vagas"],
                    link=item.get("link", "")
                )
            else:
                atividade = AtividadePresencial(
                    id=item["id"],
                    titulo=item["titulo"],
                    descricao=item["descricao"],
                    data=item["data"],
                    horario=item["horario"],
                    tutor=None,
                    local=item["local"],
                    vagas=item["vagas"],
                    endereco=item.get("endereco", "")
                )
            
            atividade.inscritos = []
            self.atividades.append(atividade)

    def criar_atividades_padrao(self):
        self.adicionar(
            AtividadeRemota(
                id=0,
                titulo="Roda de Conversa",
                descricao="Conversa entre os participantes.",
                data="01/06",
                horario="13:30",
                tutor=None,
                local="Sala Virtual",
                vagas=30,
                link="https://meet.google.com/"
            )
        )
        self.adicionar(
            AtividadePresencial(
                id=0,
                titulo="Pilates",
                descricao="Pilates para terceira idade.",
                data="04/06",
                horario="13:30",
                tutor=None,
                local="Parque Central",
                vagas=20,
                endereco="Parque Central"
            )
        )
        self.adicionar(
            AtividadeRemota(
                id=0,
                titulo="Yoga",
                descricao="Alongamento e relaxamento.",
                data="08/06",
                horario="08:00",
                tutor=None,
                local="Google Meet",
                vagas=40,
                link="https://meet.google.com/"
            )
        )

    def salvar_atividades(self):
        dados = {
            "proximo_id": self.proximo_id,
            "atividades": []
        }
        
        for atividade in self.atividades:
            item = {
                "id": atividade.id,
                "titulo": atividade.titulo,
                "descricao": atividade.descricao,
                "data": atividade.data,
                "horario": atividade.horario,
                "local": atividade.local,
                "vagas": atividade.vagas,
                "tipo": atividade.tipo()
            }
            
            if isinstance(atividade, AtividadeRemota):
                item["link"] = atividade.link
            else:
                item["endereco"] = atividade.endereco
            
            dados["atividades"].append(item)
        
        with open(ARQUIVO_ATIVIDADES, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    def adicionar(self, atividade):
        atividade.id = self.proximo_id
        self.proximo_id += 1
        atividade.inscritos = []
        self.atividades.append(atividade)
        self.salvar_atividades()

    def listar(self):
        return self.atividades

    def buscar_por_id(self, id_atividade):
        for atividade in self.atividades:
            if atividade.id == id_atividade:
                return atividade
        return None

    def buscar_por_data(self, data):
        resultado = []
        for atividade in self.atividades:
            if atividade.data == data:
                resultado.append(atividade)
        return resultado

    def atualizar(self, atividade):
        for indice, existente in enumerate(self.atividades):
            if existente.id == atividade.id:
                self.atividades[indice] = atividade
                self.salvar_atividades()
                return True
        return False

    def remover(self, id_atividade):
        atividade = self.buscar_por_id(id_atividade)
        if atividade is None:
            return False
        self.atividades.remove(atividade)
        self.salvar_atividades()
        return True