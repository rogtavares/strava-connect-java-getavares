import httpx
import asyncio

# Seu token atual
ACCESS_TOKEN = "f973c9aabd3cf9fae18814782db37ffcdd94ec2d"


async def test_strava_connection():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = "https://www.strava.com/api/v3/athlete"

    print(f"🔄 Testando conexão com Strava usando token: {ACCESS_TOKEN[:10]}...")

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCESSO! Conexão estabelecida.")
        print(f"👋 Olá, {data.get('firstname')} {data.get('lastname')}!")
        print(f"🆔 ID do Atleta: {data.get('id')}")
        print(f"🌍 Cidade: {data.get('city')}, {data.get('state')}")
        return True
    else:
        print(f"\n❌ ERRO: {response.status_code}")
        print(f"Detalhes: {response.text}")
        return False


if __name__ == "__main__":
    asyncio.run(test_strava_connection())
