import json
import os
from models.usuario import Senior, Tutor

ARQUIVO_USUARIOS = "data/usuarios.json"


class UsuarioRepository:
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
        self.usuarios = []
        self.usuario_atual = None
        self.carregar_usuarios()

    def carregar_usuarios(self):
        """Carrega os usuários do arquivo JSON."""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(ARQUIVO_USUARIOS):
            self.criar_usuarios_padrao()
            return

        try:
            with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            
            self.usuarios = []
            
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
                    # Carrega os IDs das atividades inscritas
                    usuario._ids_atividades_inscritas = item.get("atividades_inscritas", [])
                else:
                    usuario = Tutor(
                        id=item["id"],
                        nome=item["nome"],
                        email=item["email"],
                        telefone=item["telefone"],
                        senha=item["senha"],
                        especialidade=item["especialidade"]
                    )
                    usuario._ids_atividades_criadas = item.get("atividades_criadas", [])
                
                self.usuarios.append(usuario)
            
            if self.usuarios:
                self.usuario_atual = self.usuarios[0]
                
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            self.criar_usuarios_padrao()

    def criar_usuarios_padrao(self):
        """Cria usuários padrão se o arquivo não existir."""
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
        
        self.usuarios[0]._ids_atividades_inscritas = []
        self.usuarios[1]._ids_atividades_criadas = []
        
        self.usuario_atual = self.usuarios[0]
        self.salvar_usuarios()

    def salvar_usuarios(self):
        """Salva todos os usuários no arquivo JSON."""
        try:
            dados = []
            
            for usuario in self.usuarios:
                item = {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "email": usuario.email,
                    "telefone": usuario.telefone,
                    "senha": usuario.senha
                }
                
                if isinstance(usuario, Senior):
                    item["tipo"] = "senior"
                    item["contato_emergencia"] = usuario.contato_emergencia
                    
                    # 🔥 SALVA OS IDs DAS ATIVIDADES INSCRITAS
                    item["atividades_inscritas"] = [
                        atividade.id for atividade in usuario.atividades_inscritas
                    ]
                    
                    # Atualiza o cache de IDs
                    usuario._ids_atividades_inscritas = item["atividades_inscritas"]
                    
                    # 🔥 DEBUG - Mostra o que está sendo salvo
                    print(f"💾 Salvando {usuario.nome}: atividades_inscritas = {item['atividades_inscritas']}")
                    
                else:  # Tutor
                    item["tipo"] = "tutor"
                    item["especialidade"] = usuario.especialidade
                    item["atividades_criadas"] = [
                        atividade.id for atividade in usuario.atividades_criadas
                    ]
                    usuario._ids_atividades_criadas = item["atividades_criadas"]
                
                dados.append(item)
            
            # 🔥 DEBUG - Mostra o JSON que será salvo
            print(f"💾 Salvando arquivo com {len(dados)} usuários")
            
            with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
                
            print(f"✅ Arquivo {ARQUIVO_USUARIOS} salvo com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao salvar usuários: {e}")

    def get_usuario_atual(self):
        return self.usuario_atual

    def set_usuario_atual(self, usuario):
        self.usuario_atual = usuario

    def get_all(self):
        return self.usuarios

    def buscar_por_id(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id == id_usuario:
                return usuario
        return None

    def atualizar_usuario(self, usuario):
        """Atualiza um usuário e salva no arquivo."""
        for indice, existente in enumerate(self.usuarios):
            if existente.id == usuario.id:
                self.usuarios[indice] = usuario
                if self.usuario_atual is not None and self.usuario_atual.id == usuario.id:
                    self.usuario_atual = usuario
                
                # 🔥 FORÇA O SALVAMENTO IMEDIATO
                self.salvar_usuarios()
                print(f"✅ Usuário {usuario.nome} atualizado e salvo!")
                return True
        return False