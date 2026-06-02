
from datetime import datetime


def formatar_data_brasileira(data_iso):
    if not data_iso:
        return ""
    try:
        data = datetime.strptime(data_iso, "%Y-%m-%d")
        return data.strftime("%d/%m/%Y")
    except ValueError:
        return data_iso


def formatar_data_iso(data_brasileira):
    if not data_brasileira:
        return ""
    try:
        data = datetime.strptime(data_brasileira, "%d/%m/%Y")
        return data.strftime("%Y-%m-%d")
    except ValueError:
        return data_brasileira


def aplicar_mascara_data(entry_widget):
    def on_key_press(event):
        if event.keysym in ('BackSpace', 'Delete'):
            return
        
        # Obtém o texto atual
        texto = entry_widget.get()
        
        # Limita a 10 caracteres no total (dd/mm/aaaa)
        if len(texto) >= 10:
            return "break"
        
        # Adiciona as barras automaticamente
        if len(texto) == 2 and event.keysym != 'slash':
            entry_widget.insert(2, '/')
        elif len(texto) == 5 and event.keysym != 'slash':
            entry_widget.insert(5, '/')
    
    # Valida cada caractere digitado
    def validate_input(char):
        # Permite apenas números e barra
        if char.isdigit() or char == '/':
            return True
        return False
    
    # Registra a validação
    vcmd = (entry_widget.register(validate_input), '%S')
    entry_widget.config(validate='key', validatecommand=vcmd)
    entry_widget.bind('<KeyRelease>', on_key_press)


def data_hoje_br():
    return datetime.now().strftime("%d/%m/%Y")

