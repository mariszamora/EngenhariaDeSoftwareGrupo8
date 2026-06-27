# repositories/atividade_repository.py - COM ARQUIVO JSON
import json
import os
from models.atividade import AtividadePresencial, AtividadeRemota

ARQUIVO_ATIVIDADES = "data/atividades.json"

class AtividadeRepository:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AtividadeRepository, cls).__new__(cls)
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
        """Carrega as atividades do arquivo JSON"""
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(ARQUIVO_ATIVIDADES):
            with open(ARQUIVO_ATIVIDADES, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.proximo_id = dados.get("proximo_id", 1)
                
                for item in dados.get("atividades", []):
                    if item["tipo"] == "Remota":
                        atividade = AtividadeRemota(
                            id=item["id"],
                            titulo=item["titulo"],
                            descricao=item["descricao"],
                            data=item["data"],
                            horario=item["horario"],
                            tutor=None,  # Será resolvido depois
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
                    
                    # Recupera os inscritos (IDs serao resolvidos depois)
                    self.atividades.append(atividade)
        else:
            self.criar_atividades_padrao()
    
    def criar_atividades_padrao(self):
        """Cria atividades padrao"""
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
        self.salvar_atividades()
    
    def salvar_atividades(self):
        """Salva as atividades no arquivo JSON"""
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
                "tipo": atividade.tipo(),
                "inscritos": [u.id for u in atividade.inscritos]
            }
            
            if isinstance(atividade, AtividadeRemota):
                item["link"] = atividade.link
            else:
                item["endereco"] = atividade.endereco
            
            dados["atividades"].append(item)
        
        with open(ARQUIVO_ATIVIDADES, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def adicionar(self, atividade):
        atividade.id = self.proximo_id
        self.proximo_id += 1
        self.atividades.append(atividade)
        self.salvar_atividades()
    
    def listar(self):
        return self.atividades
    
    def buscar_por_id(self, id):
        for atividade in self.atividades:
            if atividade.id == id:
                return atividade
        return None
    
    def buscar_por_data(self, data):
        resultado = []
        for atividade in self.atividades:
            if atividade.data == data:
                resultado.append(atividade)
        return resultado
    
    def remover(self, id):
        atividade = self.buscar_por_id(id)
        if atividade is not None:
            self.atividades.remove(atividade)
            self.salvar_atividades()
            return True
        return False