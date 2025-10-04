import tkinter as tk
from tkinter import messagebox
import time

# --- Lógica do Solucionador de Sudoku (Inalterada) ---

def eh_valido(tabuleiro, numero, posicao):
    # Checar linha
    for j in range(9):
        if tabuleiro[posicao[0]][j] == numero and posicao[1] != j:
            return False
    # Checar coluna
    for i in range(9):
        if tabuleiro[i][posicao[1]] == numero and posicao[0] != i:
            return False
    # Checar quadrante 3x3
    quadrante_x = posicao[1] // 3
    quadrante_y = posicao[0] // 3
    for i in range(quadrante_y * 3, quadrante_y * 3 + 3):
        for j in range(quadrante_x * 3, quadrante_x * 3 + 3):
            if tabuleiro[i][j] == numero and (i, j) != posicao:
                return False
    return True

def encontrar_vazio(tabuleiro):
    for i in range(9):
        for j in range(9):
            if tabuleiro[i][j] == 0:
                return (i, j)
    return None

# --- Classe da Interface Gráfica (Atualizada) ---

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Sudoku")
        # Aumentamos a largura para acomodar o painel de números
        self.root.geometry("680x550")
        self.root.resizable(False, False)
        
        # Variáveis para rastrear a célula selecionada
        self.selected_cell = None
        self.selected_widget = None

        # Frame principal que conterá o tabuleiro e o painel de números
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20, padx=10)

        # Frame para o tabuleiro
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.LEFT, padx=10)

        # Frame para o painel de números
        self.numpad_frame = tk.Frame(self.main_frame)
        self.numpad_frame.pack(side=tk.LEFT, padx=10)

        # Matriz para armazenar as caixas de entrada (Entry widgets)
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.quadrant_colors = ["#e0e0e0", "#ffffff"] # Cores para os quadrantes
        self.criar_grade()
        self.criar_painel_numeros()

        # Frame para os botões de controle (Resolver/Limpar)
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.solve_button = tk.Button(self.button_frame, text="Resolver", font=("Arial", 14), command=self.resolver_sudoku_gui)
        self.solve_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Limpar", font=("Arial", 14), command=self.limpar_grade)
        self.clear_button.pack(side=tk.LEFT, padx=10)

    def criar_grade(self):
        """Cria a grade 9x9 de caixas de entrada."""
        for i in range(9):
            for j in range(9):
                cor_idx = (i // 3 + j // 3) % 2
                bg_color = self.quadrant_colors[cor_idx]
                
                entry = tk.Entry(
                    self.board_frame, width=2, font=("Arial", 24, "bold"),
                    justify="center", bd=1, relief="solid", bg=bg_color,
                    readonlybackground=bg_color, # Mantém a cor ao desabilitar
                    fg="black"
                )
                entry.grid(row=i, column=j)
                # Associa o evento de clique à função selecionar_celula
                entry.bind("<Button-1>", lambda event, r=i, c=j: self.selecionar_celula(event, r, c))
                self.cells[i][j] = entry
    
    def selecionar_celula(self, event, row, col):
        """Chamada quando uma célula é clicada, armazena e destaca a seleção."""
        # Restaura a cor da célula anteriormente selecionada
        if self.selected_widget:
            r, c = self.selected_cell
            cor_idx = (r // 3 + c // 3) % 2
            self.selected_widget.config(bg=self.quadrant_colors[cor_idx])

        # Armazena e destaca a nova célula
        self.selected_cell = (row, col)
        self.selected_widget = self.cells[row][col]
        self.selected_widget.config(bg="#a0c4ff") # Cor de destaque (azul claro)

    def criar_painel_numeros(self):
        """Cria os botões de 1 a 9 e o de apagar."""
        label = tk.Label(self.numpad_frame, text="Opções", font=("Arial", 16))
        label.pack(pady=10)
        
        numbers_frame = tk.Frame(self.numpad_frame)
        numbers_frame.pack()
        
        for i in range(1, 10):
            # Usamos lambda para passar o valor do número para a função
            btn = tk.Button(numbers_frame, text=str(i), font=("Arial", 14), width=4,
                            command=lambda num=i: self.inserir_numero(num))
            btn.grid(row=(i-1)//3, column=(i-1)%3, padx=2, pady=2)
        
        clear_btn = tk.Button(self.numpad_frame, text="Apagar", font=("Arial", 14),
                              command=self.apagar_numero)
        clear_btn.pack(pady=15)

    def inserir_numero(self, numero):
        """Insere um número na célula atualmente selecionada."""
        if self.selected_widget:
            self.selected_widget.config(state=tk.NORMAL)
            self.selected_widget.delete(0, tk.END)
            self.selected_widget.insert(0, str(numero))
            # Opcional: desabilitar edição direta para forçar o uso do painel
            # self.selected_widget.config(state='readonly')
    
    def apagar_numero(self):
        """Apaga o número da célula atualmente selecionada."""
        if self.selected_widget:
            self.selected_widget.config(state=tk.NORMAL)
            self.selected_widget.delete(0, tk.END)
            # self.selected_widget.config(state='readonly')

    def limpar_grade(self):
        """Limpa todos os valores e a seleção da grade."""
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state=tk.NORMAL, fg="black")
                self.cells[i][j].delete(0, tk.END)
        
        if self.selected_widget:
            r, c = self.selected_cell
            cor_idx = (r // 3 + c // 3) % 2
            self.selected_widget.config(bg=self.quadrant_colors[cor_idx])
            self.selected_widget = None
            self.selected_cell = None

    def obter_tabuleiro_da_grade(self):
        """Lê os valores da grade e os converte para uma matriz de inteiros."""
        tabuleiro = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                valor = self.cells[i][j].get()
                if valor.isdigit():
                    num = int(valor)
                    # Zera o valor para checar a validade contra os outros números fixos
                    self.cells[i][j].delete(0, tk.END)
                    temp_board = self.obter_tabuleiro_temporario()
                    self.cells[i][j].insert(0, valor)

                    if eh_valido(temp_board, num, (i, j)):
                         tabuleiro[i][j] = num
                    else:
                        messagebox.showerror("Erro de Entrada", f"O número {num} na linha {i+1}, coluna {j+1} viola as regras do Sudoku.")
                        return None
        return tabuleiro

    def obter_tabuleiro_temporario(self):
        """Função auxiliar para validação, obtém o estado atual da grade."""
        board = [[0]*9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get()
                if val.isdigit():
                    board[r][c] = int(val)
        return board

    def resolver_sudoku_gui(self):
        """Função chamada pelo botão 'Resolver'."""
        tabuleiro = self.obter_tabuleiro_da_grade()
        if tabuleiro is None: return

        self.solve_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        
        for i in range(9):
            for j in range(9):
                if tabuleiro[i][j] != 0:
                    self.cells[i][j].config(fg="#333333")
                else:
                    self.cells[i][j].config(fg="blue")
        
        if self.resolver_recursivo(tabuleiro):
            messagebox.showinfo("Sucesso", "Sudoku resolvido com sucesso!")
        else:
            messagebox.showerror("Falha", "Não foi encontrada uma solução para este Sudoku.")

        self.solve_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)

    def resolver_recursivo(self, tabuleiro):
        """Resolve usando backtracking e atualiza a GUI em tempo real."""
        encontrar = encontrar_vazio(tabuleiro)
        if not encontrar:
            return True
        else:
            linha, coluna = encontrar

        for i in range(1, 10):
            if eh_valido(tabuleiro, i, (linha, coluna)):
                tabuleiro[linha][coluna] = i
                
                self.cells[linha][coluna].delete(0, tk.END)
                self.cells[linha][coluna].insert(0, str(i))
                self.root.update_idletasks()
                
                if self.resolver_recursivo(tabuleiro):
                    return True

                tabuleiro[linha][coluna] = 0
                self.cells[linha][coluna].delete(0, tk.END)
                self.root.update_idletasks()
        return False

# --- Programa Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()