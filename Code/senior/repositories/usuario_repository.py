# repositories/usuario_repository.py - CORRIGIDO
import json
import os
from models.usuario import Senior, Tutor
from services.atividade_service import buscar_por_id

ARQUIVO_USUARIOS = "data/usuarios.json"

class UsuarioRepository:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsuarioRepository, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.usuarios = []
        self.usuario_atual = None
        self.carregar_usuarios()
    
    def carregar_usuarios(self):
        """Carrega os usuarios do arquivo JSON"""
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(ARQUIVO_USUARIOS):
            with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for item in dados:
                    if item["tipo"] == "senior":
                        usuario = Senior(
                            id=item["id"],
                            nome=item["nome"],
                            email=item["email"],
                            telefone=item["telefone"],
                            senha=item["senha"],
                            contato_emergencia=item["contato_emergencia"]
                        )
                        # <-- RECUPERA AS ATIVIDADES INSCRITAS
                        usuario.atividades_inscritas = []
                        for ativ_id in item.get("atividades_inscritas", []):
                            atividade = buscar_por_id(ativ_id)
                            if atividade:
                                usuario.atividades_inscritas.append(atividade)
                    else:
                        usuario = Tutor(
                            id=item["id"],
                            nome=item["nome"],
                            email=item["email"],
                            telefone=item["telefone"],
                            senha=item["senha"],
                            especialidade=item["especialidade"]
                        )
                        usuario.atividades_criadas = []
                        for ativ_id in item.get("atividades_criadas", []):
                            atividade = buscar_por_id(ativ_id)
                            if atividade:
                                usuario.atividades_criadas.append(atividade)
                    
                    self.usuarios.append(usuario)
            
            if self.usuarios:
                self.usuario_atual = self.usuarios[0]
        else:
            self.criar_usuarios_padrao()
    
    def criar_usuarios_padrao(self):
        """Cria usuarios padrao e salva no arquivo"""
        self.usuarios = [
            Senior(
                id=1,
                nome="Antonio Silva",
                email="antonio@email.com",
                telefone="(11) 99999-9999",
                senha="123",
                contato_emergencia="Maria - (11) 98888-8888"
            ),
            Tutor(
                id=2,
                nome="Carlos Souza",
                email="carlos@email.com",
                telefone="(11) 98888-7777",
                senha="321",
                especialidade="Educacao Fisica"
            )
        ]
        self.usuario_atual = self.usuarios[0]
        self.salvar_usuarios()
    
    def salvar_usuarios(self):
        """Salva os usuarios no arquivo JSON"""
        dados = []
        for usuario in self.usuarios:
            item = {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "telefone": usuario.telefone,
                "senha": usuario.senha,
            }
            
            if isinstance(usuario, Senior):
                item["tipo"] = "senior"
                item["contato_emergencia"] = usuario.contato_emergencia
                item["atividades_inscritas"] = [a.id for a in usuario.atividades_inscritas]
            else:
                item["tipo"] = "tutor"
                item["especialidade"] = usuario.especialidade
                item["atividades_criadas"] = [a.id for a in usuario.atividades_criadas]
            
            dados.append(item)
        
        with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def get_usuario_atual(self):
        return self.usuario_atual
    
    def set_usuario_atual(self, usuario):
        self.usuario_atual = usuario
        self.salvar_usuarios()
    
    def get_all(self):
        return self.usuarios
    
    def atualizar_usuario(self, usuario):
        """Atualiza um usuario existente"""
        for i, u in enumerate(self.usuarios):
            if u.id == usuario.id:
                self.usuarios[i] = usuario
                if self.usuario_atual and self.usuario_atual.id == usuario.id:
                    self.usuario_atual = usuario
                self.salvar_usuarios()
                return True
        return False