import asyncio
from telethon import TelegramClient, events

# TELEGRAM
api_id = '29770543'
api_hash = 'a2e648bef90d6a8572ef5b29858071cd'
phone_number = '5585992388426'
group_username = 'previasdalay'

# INICIAR TELEGRAM
client = TelegramClient('session_name', api_id, api_hash)
user_states = {}

# Perguntas e respostas para convencer a pessoa a comprar o plano VIP
perguntas_respostas = [
    ("Você está pronto para acessar conteúdo exclusivo e excitante? 😉", "Sim, estou pronto! 😈"),
    ("O que você acha de ter acesso a mais de 250 vídeos e fotos de tirar o fôlego? 🔥", "Adoraria ver isso!"),
    ("Imagina só, você assistindo aos conteúdos mais quentes, sem limites! Não é tentador? 😏", "Nossa, sim!"),
    ("Agora, imagine a sensação de ter acesso VIP a tudo isso, sem restrições. Quer garantir já o seu acesso? 💸", "Quero sim! Como faço para assinar?"),
    ("Está pronto para se juntar ao nosso grupo VIP e aproveitar todos os benefícios? 😈", "Sim, me conta mais! 😏")
]

# Função para avançar para a próxima etapa
async def avancar_etapa(user_id):
    if user_id in user_states:
        etapa = user_states[user_id]
        
        if etapa < len(perguntas_respostas):
            pergunta, resposta = perguntas_respostas[etapa]
            
            # Aguarda 5 segundos antes de responder (simulando uma conversa mais natural)
            await asyncio.sleep(5)
            
            # Envia a pergunta ao usuário
            await client.send_message(user_id, pergunta)
            
            # Avança para a próxima pergunta
            user_states[user_id] += 1

        else:
            # Depois da última pergunta, envia uma mensagem final para encorajar a compra
            await client.send_message(user_id, "Você já pode garantir seu acesso VIP agora! 💸 Clique no link para se inscrever e aproveite tudo que temos a oferecer! 😏")
            del user_states[user_id]  # Remove o usuário após a conclusão
    else:
        print(f"Usuário {user_id} não encontrado nas etapas.")

# Função para verificar se o usuário ficou sem resposta por mais de 5 minutos
async def verificar_inatividade(user_id):
    await asyncio.sleep(120)  # Espera 5 minutos (300 segundos)
    
    if user_id in user_states:
        # Envia uma mensagem lembrando o usuário
        await client.send_message(user_id, "Sumiu justo agora que ia te mostrar uma prévia deliciosa? 😏\nTô aqui te esperando pra te mostrar tudo que o VIP tem... Só dizer “quero”.")
    
# BOT PRINCIPAL
async def main():
    await client.start(phone_number)
    group = await client.get_entity(group_username)

    @client.on(events.ChatAction(chats=group))
    async def welcome(event):
        if event.user_joined or event.user_added:
            user = await event.get_user()
            name = f"@{user.username}" if user.username else f"{user.first_name}"

            async def conversar_com_usuario():
                try:
                    await asyncio.sleep(15)  # Espera 15s antes da 1ª mensagem
                    await client.send_message(user.id, f"Oi, seja bem-vindo meu grupo!")
                    await asyncio.sleep(10)  # Espera 10s antes da pergunta
                    await client.send_message(user.id, "Quer saber mais sobre o meu conteúdo VIP +18? Me pergunta qualquer coisa 😏")
                    user_states[user.id] = 0  # Guarda estado pra IA responder
                    asyncio.create_task(verificar_inatividade(user.id))  # Verifica se o usuário ficou inativo por mais de 5 minutos
                except Exception as e:
                    print(f"❌ Erro ao iniciar conversa com {name}: {e}")

            asyncio.create_task(conversar_com_usuario())

    @client.on(events.NewMessage)
    async def ao_receber_mensagem(event):
        user_id = event.sender_id
        if user_id in user_states:
            await asyncio.sleep(5)  # Espera 5 segundos antes de responder (simula um tempo real)
            await avancar_etapa(user_id)

    print(f"Aguardando mensagens e novos membros em {group_username}...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
