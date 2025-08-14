import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase_test():
    if firebase_admin._apps:
        return True

    try:
        firebase_creds_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
        api_key = os.getenv("FIREBASE_API_KEY")

        if not firebase_creds_base64 or not api_key:
            print("❌ Falta FIREBASE_CREDENTIALS_BASE64 o FIREBASE_API_KEY")
            return False

        # Decodifica las credenciales
        firebase_creds_json = base64.b64decode(firebase_creds_base64).decode('utf-8')
        firebase_creds = json.loads(firebase_creds_json)

        # Inicializa Firebase
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase inicializado correctamente")
        return True

    except Exception as e:
        print(f"❌ Error al inicializar Firebase: {e}")
        return False


def test_create_user():
    from models.users import User
    import asyncio

    async def create_test_user():
        test_user = User(
            name="RailwayTest",
            lastname="User",
            email="railwaytest@example.com",
            password="Test123!"
        )
        try:
            user_record = auth.create_user(
                email=test_user.email,
                password=test_user.password
            )
            print(f"✅ Usuario temporal creado en Firebase: UID={user_record.uid}")
            # Elimina el usuario de prueba
            auth.delete_user(user_record.uid)
            print("✅ Usuario temporal eliminado correctamente")
        except Exception as e:
            print(f"❌ Error al crear usuario de prueba en Firebase: {e}")

    asyncio.run(create_test_user())


if __name__ == "__main__":
    print("== Verificando Firebase en Railway ==")
    if initialize_firebase_test():
        test_create_user()
