from playwright.sync_api import sync_playwright  # Biblioteca que automatiza navegadores
import random  # Seleciona produtos de forma aleatória
import time  # Pausa o código por alguns segundos

# Função para lidar com pop-ups (caixas de diálogo) que aparecem ao adicionar um produto ao carrinho.
def handle_dialog(dialog): 
    dialog.accept()  # Aceita automaticamente o pop-up de confirmação.


def run_demo_blaze_bot():
     # Inicializa o Playwright e abre o navegador Chromium.
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False) # headless=False faz com que o navegador abra visivelmente.
        pagina_web = navegador.new_page()
        pagina_web.goto("https://www.demoblaze.com/")  # Acessa o site DemoBlaze.
        time.sleep(5) # Espera 5 segundos para garantir que a página carregue completamente.
        
     # Seleciona todos os elementos que têm a classe 'hrefch', que corresponde aos produtos listados na página inicial.   
        produtos_aleatorios = pagina_web.locator(".hrefch").all()
        
         # Verifica se há pelo menos dois produtos disponíveis para o teste.
        if len(produtos_aleatorios) < 2:
            print("Não há produtos suficientes para realizar o teste.")
            navegador.close()
            return
        
        # Seleciona aleatoriamente 2 produtos da lista de produtos disponíveis.
        selecionando_produtos = random.sample(produtos_aleatorios, 2)
        carrinho_produtos = []
      
      # Itera sobre os produtos selecionados aleatoriamente.  
        for produto in selecionando_produtos:
            nome_produto = produto.inner_text()  # Obtém o nome (texto) do produto.
            print(f"Selecionando produto: {nome_produto}") # Exibe o nome do produto no console.
            
            produto.click()  # Clica no produto para abrir a página de detalhes.
            time.sleep(5)
            
            pagina_web.click("text=Add to cart") # Clica no botão "Add to cart" para adicionar o produto ao carrinho.
            time.sleep(5)
            
            # Configura o Playwright para lidar com o pop-up de confirmação que aparece ao adicionar o produto.
            pagina_web.on("dialog", handle_dialog) # Usa a função handle_dialog para aceitar automaticamente o pop-up.
            
            print(f"Produto adicionado ao carrinho: {nome_produto}")  # Confirma que o produto foi adicionado ao carrinho.
            carrinho_produtos.append(nome_produto) # Adiciona o nome do produto à lista de produtos do carrinho.
            
            pagina_web.click("text=Home") # Volta para a página inicial para selecionar o próximo produto.
            time.sleep(5)
            
         # Após adicionar todos os produtos, navega para o carrinho para verificar os itens.
        pagina_web.click("text=Cart")
        time.sleep(10)
        
       # Captura os nomes dos produtos que estão no carrinho, buscando o texto na segunda coluna da tabela.
        itens_carrinho = pagina_web.locator("#tbodyid tr td:nth-child(2)").all_text_contents()
        
        # Valida se todos os produtos adicionados estão no carrinho.
        for produto in carrinho_produtos:
            assert produto in itens_carrinho, f"Erro: {produto} não encontrado no carrinho!"
            # Exibe erro se o produto não estiver no carrinho.
        
        print("Todos os produtos foram adicionados ao carrinho com sucesso!")
        navegador.close() # Fecha o navegador ao final da execução.

if __name__ == "__main__":
    run_demo_blaze_bot()
